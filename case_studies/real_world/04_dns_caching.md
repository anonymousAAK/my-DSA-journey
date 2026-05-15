# Caching Strategies in DNS Resolvers

## The problem

Every time you type a URL, your machine needs to translate the domain name (`github.com`) into an IP address. The authoritative source of that mapping is a DNS server somewhere in the world — possibly multiple hops away. If every page load required a fresh DNS lookup, the internet would feel like the 1990s again. Resolvers cache aggressively. But DNS records are sometimes wrong, sometimes change, and operators *need* changes to propagate within bounded time — so the cache can't be eternal.

The hard part: balancing "fast lookups" (long cache lifetime) against "fresh data" (short cache lifetime), at internet scale, against adversaries who would love to poison your cache.

## Why the obvious approach didn't work

The obvious approach: a giant in-memory hash map of domain → IP, never evicting. This is essentially what your `/etc/hosts` file is, statically. It "works" in that lookups are O(1). It fails for three reasons:

1. **Records change.** A site moves to a new IP; if your cache never expires, your users hit the old IP forever.
2. **Memory.** A recursive resolver serving a big ISP might see millions of distinct domains a day. Hold them all forever and the cache exceeds available memory.
3. **Security.** If an attacker can inject a poisoned record into your cache and it lives forever, that's permanent compromise.

DNS solved this in the 1980s with two interlocking mechanisms: **TTL** on every record, and **LRU-style eviction** when caches fill.

## What they actually use

Every DNS record carries a **Time-To-Live** (TTL) value, set by the authoritative server. The cache stores `(name, type, value, expires_at)` quadruples, and `expires_at = received_at + ttl`. On lookup, if `expires_at <= now`, the entry is stale — drop it and refetch.

When the cache hits its memory bound, evict on **LRU** order. Modern resolvers (like Unbound, BIND with its `cache-max-ttl`, dnsmasq) use a hash table for O(1) lookup combined with a doubly-linked list for O(1) recency updates — the exact LRU pattern we built in Phase 3.

Additional refinements you see in production resolvers:

- **Negative caching (RFC 2308)**: if a lookup returns NXDOMAIN ("no such domain"), cache that *negative* result too, with its own (usually shorter) TTL. Otherwise a typo'd domain causes a fresh upstream query every time someone hits it.
- **Prefetch on near-expiry**: if a popular record is about to expire (say, in the last 10% of its TTL), proactively refresh it *before* it's needed, so users never see a cache-miss latency spike. Cloudflare's `1.1.1.1` famously does this.
- **TTL clamping**: even if the authoritative server says TTL = 7 days, the resolver may cap it to, say, 1 hour, to protect against stale data and aid in faster propagation of changes. Conversely, very short TTLs (≤ 5 sec) are sometimes floored to a minimum to protect upstream servers from being hammered.
- **Cache-line stratification**: separate the cache into hot (small, hash-table only, sub-µs) and cold (larger, on disk for big resolvers) tiers.
- **DNS over HTTPS / TLS** adds connection caching as a layer on top — the cache strategy is the same, but lookups themselves are encrypted, so connection reuse matters.

## The tradeoff

The fundamental tradeoff is **freshness vs. load**. Long TTLs → fewer upstream queries, faster average lookup, but slower propagation of legitimate changes. Short TTLs → opposite. The authoritative operator picks per record (e.g., `www.example.com` IN A might have TTL=300s; `mx.example.com` MX might have TTL=86400s).

Resolvers can also choose to **violate the TTL** in emergencies — e.g., if the authoritative server is unreachable, serve stale records past expiry rather than fail. This is the `serve-stale` behavior in modern Unbound/BIND and reflects a pragmatic decision: a slightly old answer is usually better than no answer.

The security tradeoff: caches are an attack surface (cache poisoning, Kaminsky 2008). DNSSEC, query randomization (source port, transaction ID, query name 0x20 mixed case) all help, but each has cost. Resolvers pay it because the cache is too valuable to abandon.

## You can implement a toy version of this using Week 12-13 + Phase 3 case study

- Week 12 (linked lists) — the doubly-linked list backbone for LRU.
- Week 13 (hash tables) — the hash map for O(1) lookup.
- Phase 3 walkthrough — the *combination* of map + list + heap-by-TTL is exactly the DNS resolver cache pattern.

A weekend project: build a tiny DNS proxy in 200 lines of Python. Listen on UDP port 5353, on a query, check your LRU+TTL cache, on miss forward to `8.8.8.8`, cache the result with its TTL, return to the client. You'll quickly observe the speedup on repeated queries — and you'll quickly hit the design questions real resolvers grapple with: what about negative answers? What if upstream times out? Do I evict by LRU or just let entries die at TTL?

These are not "advanced" data structure problems. They're the same hash map + linked list + heap you learn in Phases 2-3, composed at network scale. The whole internet relies on this pattern working correctly.
