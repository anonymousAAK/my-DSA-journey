# Why Your CDN Uses Consistent Hashing (and What Happens Without It)

## The problem

A content delivery network has a fleet of edge servers around the world — let's say 10,000 of them — and a catalog of cacheable objects (images, JS bundles, video chunks): billions of them. When a request comes in for object `cat.jpg`, you need to pick *which* edge server caches it. The same object should land on the same cache every time (so cache hits work). When you add or remove edge servers (which happens constantly — autoscaling, failures, rolling deploys), the mapping can't change for *most* objects, or you'd invalidate the entire cache and the origin servers would melt under the traffic spike.

## Why the obvious approach didn't work

The textbook hash: `shard = hash(key) mod N`. Lovely, fast, even distribution. But N changes.

Go from N=10,000 to N=10,001 (you just added a server). For each key, `hash(key) mod 10000` and `hash(key) mod 10001` give different answers about 9,999/10,000 of the time. That means **99.99% of your cache entries are now on the wrong server.** The next time someone requests `cat.jpg`, the new "owner" doesn't have it, fetches from origin, populates locally. Multiply by *every* object in the system, requested simultaneously — your origin servers see traffic spikes orders of magnitude above normal. CDN providers have had outages from exactly this.

Even worse, removing a server moves *all* of its keys, but `mod N` reshuffling means the load doesn't go cleanly to the dead server's neighbors — it sprays across the entire fleet, often causing secondary hotspots.

## What they actually use

**Consistent hashing**, originally described by Karger et al. (1997) for the Akamai CDN, which is still in production today.

Imagine a circle representing the hash space [0, 2^64). Each edge server is hashed onto one or more points on the circle. Each object is hashed to a point. To find the owning server for an object: hash the object, walk clockwise around the circle until you hit a server's marker — that's the owner.

When you add a server: it grabs an arc of the circle. Only the keys in that arc change owners — about 1/N of the data. Everyone else's mapping is unchanged. Cache stays warm.

To handle uneven arc lengths (some servers get unlucky placements and own huge arcs while others own tiny ones), each physical server is placed at ~100-200 **virtual nodes** scattered around the circle. With enough virtual nodes the load variance is fine even with diverse server capacities.

For very high availability, the algorithm extends naturally to replication: instead of "the next server clockwise," you use "the next K distinct servers clockwise." Now each object has K replicas, and adding/removing servers still only touches 1/N of the data.

## The tradeoff

Consistent hashing trades a *little* bit of look-up complexity (a binary search on the sorted ring instead of a single `mod`) for **massively reduced cache churn during fleet changes**. The lookup cost is negligible — O(log N) on a ring of 10,000 servers × 100 vnodes = 20 comparisons, plenty fast.

The harder tradeoff is **hot spots**. Consistent hashing makes the *mapping* stable, but it doesn't help if one key is intrinsically hot (a viral video chunk). For that you need replication of hot keys onto multiple shards, request coalescing, or a higher cache tier in front. The Phase 6 walkthrough talks about this for URL shorteners; the same trick applies in CDNs.

A subtle additional tradeoff: virtual nodes consume memory in the routing layer. Every router holds the ring; at 10,000 servers × 100 vnodes = 1M ring entries. Each entry is ~16 bytes → 16 MB. Fine in practice, but it bounds how many vnodes you can afford.

## You can implement a toy version of this using Week 13 and Week 27

- Week 13 (hashing) — implement a hash function and observe distribution. Build the naive `hash mod N` version and see, empirically, how many keys move when N changes.
- Week 27 (system design / sharding) — implement consistent hashing in 50 lines: a sorted list of (hash, server_id) entries, binary search to find owner, virtual nodes for balance.
- Compare both: build a simulator with 10,000 keys and 10 servers, add an 11th server, count how many keys change ownership in each scheme. The naive version will move ~9,000; consistent hashing will move ~900.

For a really tangible exercise, run the simulator continuously, randomly add and remove servers, plot cache hit rate over time for both schemes. The naive version's hit rate crashes on every change; consistent hashing barely flinches. That graph is the entire reason the technique exists.
