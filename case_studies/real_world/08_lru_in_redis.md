# LRU vs LFU vs ARC in Redis

## The problem

Redis is an in-memory data store, often used as a cache in front of slower databases. A user configures Redis with a max memory cap. When that cap is hit and a new write arrives, Redis must **evict** something. The choice of *what* to evict is shockingly impactful: a wrong policy can collapse cache hit rate from 90% to 40% and double your database load. The eviction policy is also one of the most well-studied algorithmic problems in computer systems — it's essentially the page replacement problem, which was the subject of OS research literature for decades.

## Why the obvious approach didn't work

The textbook answer is **least-recently-used** (LRU): evict the item that hasn't been accessed in the longest time. This works great when access patterns have **temporal locality** — recently accessed items are likely to be accessed again soon. Most cache workloads have this property.

But:

1. **A scan of cold data evicts your hot working set.** If a one-time analytical query reads 10 GB of data through your cache, LRU happily evicts every actually-hot item to make room for the scan, then evicts the scan items right after — leaving your cache empty of useful data. LRU has no concept of *frequency*, only *recency*.

2. **True LRU is expensive at scale.** Strict LRU needs O(1) lookup + O(1) recency update, requiring the hash-table-plus-doubly-linked-list pattern. The pointer updates and memory overhead are non-trivial at Redis's scale (millions of keys). For each access, you're doing 4-6 cache-line dirty writes.

3. **Some items are sticky-popular**: visited often but with bursty patterns where they aren't visited for a while. LRU evicts these during quiet periods even though they'll be wanted soon.

## What they actually use

Redis supports several policies; each has a regime where it shines:

1. **Approximate LRU (`allkeys-lru`)**: Redis doesn't track true LRU. Instead, on each eviction, it samples N random keys (default N=5; configurable up to 10) and evicts the oldest of the sampled set. As N grows, this approaches true LRU. With N=10 it's empirically within a few percent of strict LRU but enormously cheaper — no doubly-linked list maintenance per access, just a per-key "last access time" field and random sampling at eviction time.

2. **Approximate LFU (`allkeys-lfu`)**: Same sampling approach, but each key has a *logarithmic counter* of access frequency. Counter increments are probabilistic (with diminishing probability at higher counters) and decay over time. This avoids the classic LFU pitfall of "items that were popular years ago dominate the cache forever." LFU is the right choice when the working set has a heavy-tailed access distribution (a small number of items get most of the traffic, regardless of recency).

3. **TTL-only (`volatile-ttl`)**: evict the key closest to its expiry. Useful when you've sized TTLs deliberately and want them respected.

4. **Random (`allkeys-random`)**: yes, this is a real option. Surprisingly competitive in some workloads. It's the trivial baseline.

A more sophisticated policy that **Redis doesn't ship** but other systems do is **ARC (Adaptive Replacement Cache)**, used in ZFS and pre-2016 PostgreSQL versions. ARC maintains two LRU lists — one for recently-accessed-once items, one for recently-accessed-twice — plus *ghost* lists tracking recently-evicted items from each. Cache hits on ghost lists tell ARC whether to bias toward recency or frequency, and it adjusts its split adaptively. ARC handles the "scan poisoning" problem from above naturally — scan items live in the "once" list and don't displace the "twice" working set.

Redis's design philosophy is that approximate LRU/LFU is simpler, easier to reason about, and within a few percentage points of ARC in practice for most workloads. They left ARC on the table for that reason.

## The tradeoff

LRU vs LFU vs ARC is fundamentally **how much state you maintain per key** and **how cleverly you use it**.

- LRU: maintain order. Best when access pattern is recent-is-good.
- LFU: maintain count. Best when access pattern is popular-is-good.
- ARC: maintain order *and* count and adapt. Best for mixed workloads. Cost: more memory and more code.

The other axis: **strict vs approximate**. Strict LRU is great in theory; the bookkeeping is expensive. Approximate LRU via sampling pays a tiny accuracy cost for massive simplicity. Approximate algorithms are an under-appreciated theme in real-world caching.

A subtle tradeoff: **LFU's "frequency" needs decay** or items popular years ago dominate forever. Redis uses logarithmic counters with periodic decay; ARC's "ghost lists" implicitly decay; pure-LFU implementations often have a "frequency-aging" parameter. Decay parameters are themselves tuning knobs that hurt simplicity but help quality.

## You can implement a toy version of this using Phase 3 case study

- The Phase 3 walkthrough builds an LRU cache with TTL using a hash map + doubly-linked list + heap. That's the "strict LRU" baseline.
- Replace strict LRU with approximate LRU: instead of moving nodes on every access, store `last_access_time` and on eviction sample 5 random keys. Compare hit rates on synthetic workloads — you'll see they're nearly identical.
- Implement approximate LFU: per-key counter that increments with diminishing probability `1 / (counter + 1)`, decay all counters every N seconds. Compare hit rate to LRU on a Zipfian-distributed workload (`numpy.random.zipf`). LFU should win.

A weekend project: build a workload simulator. Generate three traces — Zipfian (a few hot items dominate), temporal-locality (sliding hot set), scan-heavy (one big sequential scan + a hot set). Run each trace through LRU, LFU, random, ARC. Plot hit rate. You'll *see* the regimes where each shines — and that mixed traces have no single winner. That graph is the entire reason eviction policies are a configurable.

The deep lesson: a cache is not a data structure; it's a **policy applied to a data structure**. The Week 12/13 LRU pattern is the substrate. Real systems differentiate by *how* they decide what to keep — and that decision is workload-dependent.
