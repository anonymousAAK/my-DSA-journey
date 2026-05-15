# Phase 6: Systems — URL Shortener at 10⁹ URLs, No Hot Shard

## The Word Problem

> We're shipping a URL shortener for the marketing team. They expect to generate up to a billion short links over the next 2 years. Reads will be hugely lopsided — most short links get a handful of clicks, but a few campaigns will get hundreds of millions in a day. We have a fleet of 32 web servers and we want to scale to 100+. We need short, URL-safe codes (think `goo.gl/Xy3kP`). One critical thing: we *cannot* have a hot shard. Last quarter our other service had one viral link that took down the database. Design something that won't do that.

## Step 1: Restate the problem precisely

We're designing two things:

1. A **mapping**: short_code ↔ long_url. Write-once, read-many.
2. A **system**: that distributes both writes (code generation) and reads (lookup + redirect) across many machines without hot spots.

Functional requirements:
- `shorten(long_url) → short_code` (e.g., `Xy3kP`).
- `resolve(short_code) → long_url` (then HTTP 301).
- Codes should be short, URL-safe, ideally ~6-8 chars.
- 10⁹ codes over 2 years → about 16 reads/sec average for codes, with peaks of hundreds of thousands/sec for viral links.

Non-functional:
- No single shard should serve >2x the average load even during virality.
- Adding/removing servers should not require remapping most of the data.

## Step 2: Identify constraints

- 10⁹ codes: each at ~50 bytes (short + long URL) → 50 GB. Doesn't fit in one box's RAM cheaply; will need disk + cache.
- 6-character code in base62 (a-z, A-Z, 0-9) = 62⁶ ≈ 56 billion combinations. Plenty of headroom.
- Read traffic: viral links can be 100k req/sec for one code. Most codes: ~zero.
- Latency: a redirect should feel instant. <30ms p99.
- Edge cases:
  - Duplicate `shorten()` of the same long URL — return same code, or fresh? (Pick one; common choice: same.)
  - Malicious long URLs (spam, malware).
  - Code collisions when generating randomly.
  - A shard goes down mid-write.
  - Hot code: one short code receiving 100k+ req/sec.
  - Adding a 33rd server should not cause 31/32 of cache misses to suddenly happen.

## Step 3: Brute force first

Naive design:
- One Postgres table `(short_code PRIMARY KEY, long_url, created_at)`.
- `shorten`: insert with a random base62 code; retry on collision.
- `resolve`: SELECT.
- Sharding: `shard = hash(short_code) mod N`. Round-robin among the 32 servers.

Why this fails:
- **Hot shard on viral links.** A single hot code lives on one shard. That shard gets 100k req/sec; its 31 peers get ~zero. The shard dies.
- **Adding a new server**: changes N from 32 to 33. `hash mod 32 ≠ hash mod 33` for almost every code → essentially every cache entry is invalidated, every disk lookup is now on the wrong shard. The system thrashes for hours.
- **Random codes**: collision rate is fine at 10⁹ in 56B space (~2%), but every retry is a DB round-trip.

So we have two problems: code generation strategy, and hash strategy for sharding.

## Step 4: Identify wasted work

Two distinct kinds of wasted work, plus a third subtle one:

1. **`hash mod N` re-maps everything when N changes.** This is the canonical motivation for **consistent hashing** (Phase B real-world #3). With consistent hashing, adding a node only remaps ~1/N of the keys.

2. **Random code generation with collision retries** wastes a DB roundtrip every collision. We should generate codes that are guaranteed unique by construction.

3. **Hot shards still hot under consistent hashing.** Consistent hashing fixes *re-sharding* pain but doesn't solve hot keys. A viral code is still on one shard. We need a **caching layer** between clients and shards.

## Step 5: Optimize

The composed solution has three parts:

### Part A: Code generation via base62 of a global counter

Assign each new URL a monotonically increasing integer ID (from a centralized counter service, or several counter services giving disjoint ranges — e.g., server K hands out IDs ≡ K mod 32, pre-allocated in batches of 10,000 so we don't hit the counter on every write). Encode the integer in base62 to get the short code.

- ID 1 → `"1"`, ID 100 → `"1c"`, ID 10⁹ → 6 characters.
- No collisions, ever — by construction.
- Counter pre-allocation amortizes the round-trip: each web server pre-grabs a range of 10k IDs and only hits the counter service every 10k inserts.

Trade-off: codes are sequentially guessable, which lets scrapers enumerate. Mitigate by **scrambling** the integer (e.g., XOR with a secret, or apply a permutation like Feistel) before base62 encoding. Now codes look random but are still bijective with the counter.

### Part B: Consistent hashing for storage

Hash each short_code onto a ring (e.g., murmurhash on the 6-char string → 64-bit number, mapped onto a [0, 2^64) circle). Each shard owns a contiguous arc of the ring. To find a code's shard: hash it, walk clockwise to the next shard's marker.

To avoid imbalance from arc-length variance, give each physical shard ~100 **virtual nodes** sprinkled around the ring. Now arc ownership is roughly uniform even with 32 shards.

Adding a 33rd shard: place its virtual nodes; ~1/33 of keys re-map to it from various neighbors. The other 32/33 stay put. **Cache stays warm.**

### Part C: Edge cache for hot codes

In front of the shards, run a layer of caches (think Varnish, Cloudflare's edge, or just an in-process LRU like Phase 3 but distributed). Cache `resolve(short_code)` results with a long TTL (URLs don't change). A viral code now hits the cache 99.99% of the time; the underlying shard sees the same ~1 req/sec it would have seen otherwise.

If even the cache layer has a hot spot (one cache node serving the viral code): use **request coalescing** ("only one DB roundtrip in flight per key") and **probabilistic spreading** — replicate the hot key onto K random cache nodes and have clients hash to a random one of them. Twitter's "fanout" architecture (Phase B real-world #5) uses similar ideas.

### Putting it together

Write path: web server → next ID from pre-allocated batch → scramble → base62 → consistent-hash to shard → write `(code, long_url)`.

Read path: client GET /code → edge cache lookup → cache hit returns long_url → 301 redirect. On cache miss, consistent-hash to shard, read, populate cache.

## Step 6: Implementation gotchas

- **Counter service is a single point of failure**: must be replicated. Use ZooKeeper/etcd, or partition the counter space so each web server has its own pre-allocated namespace with no coordination.
- **Pre-allocated IDs are lost on web-server crash** (the next batch starts higher). That's fine — we have 56B codes and only need 10⁹. Wasting some is free.
- **Scrambling**: don't roll your own crypto. A 32-bit Feistel network or an HMAC-based permutation is fine. Just make sure the scramble is a *bijection* on the integer space.
- **Consistent hashing virtual nodes**: too few → imbalance; too many → wasted memory and slow ring lookup. 100-200 per physical shard is the sweet spot.
- **Ring updates** when adding/removing shards: must be atomic across all routing layers, or you'll route writes to the old shard and reads to the new one. Use a single source of truth (a config service) that publishes ring versions.
- **TTL on the cache**: long URLs don't change, but they CAN be deleted (DMCA, spam takedowns). Have an invalidation channel; on delete, blast a tombstone to all caches.
- **Spam and abuse**: rate-limit `shorten()` per IP/user; scan long URLs against safe-browsing lists (which themselves use Bloom filters — Phase B real-world #10).

## Step 7: Verification

- Unit: `base62_encode(decode(x)) == x` for random x. `scramble(unscramble(x)) == x`.
- Sharding distribution: hash 10⁶ codes, count how many land on each shard, verify max-shard/min-shard ratio < 2x.
- Add a shard: simulate adding the 33rd shard, count how many of the 10⁶ keys change ownership — should be ~1/33 = 3%.
- Hot-key simulation: replay a workload where 1 code is 50% of traffic. Measure shard-level QPS — without cache should be horrific; with cache should be flat.
- Failover: kill a shard, verify clients are routed to its successor and writes don't lose data (assuming replication).

## Step 8: Reflection

What made this hard: this is a *system design* problem in algorithmic clothing. The algorithms (base62, consistent hashing, LRU cache) are individually simple — each is a week of curriculum. The skill is **combining them** to satisfy a real, multi-constraint requirement. No single data structure solves it; the *composition* solves it.

Patterns assembled:
- **Numbering as identification** — assigning sequential IDs and encoding them is the canonical alternative to hashing for ID generation.
- **Consistent hashing** (Week 27) — the right tool when shard membership is dynamic.
- **Distributed caching** with TTL (Phase 3 pattern, distributed) — handles read skew.
- **Pre-allocation / batching** — turns "one round-trip per op" into "one round-trip per 10k ops."

Curriculum tie-in:
- Week 13 (hashing) — the foundation. Consistent hashing is "hashing, but on a ring."
- Week 26-27 (system design fundamentals, sharding).
- Phase 3's LRU cache, distributed.
- Phase 4's appreciation for "the same problem, but distributed" — the algorithms don't change, the constraints do.

Where else this pattern lives: every CDN (Phase B real-world #3), every distributed key-value store (Cassandra, DynamoDB, Riak), the GitHub URL routing layer, image hosting at scale. Once you've designed one of these, you've designed all of them — the fundamentals are the same; the details are flavor.
