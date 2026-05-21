# Bug Case Study: A CDN's consistent-hash ring was 40% imbalanced because it had no virtual nodes

**Project**: This is an approximate reconstruction of a class of bug seen across Cassandra, Memcached, Riak, Couchbase, and multiple early CDN designs. The Dynamo paper (Amazon, 2007) called out the problem; Cassandra's vnodes work (2012) was a high-profile fix; the same lesson was relearned by many in-house systems.
**Date**: ~2007–2014 (the most-cited "classic" period; still resurfaces in new systems written from scratch)
**Severity**: performance / availability (some shards 2-3x overloaded, slow tail latency, occasional shard OOM)
**DSA principle**: hashing N points onto a circle does not produce N equal arcs — Week 16 (hashing) and capstone 6 (sharded systems)

## What happened

Consistent hashing places servers and keys onto a conceptual ring (typically `[0, 2^64)`). A key goes to the first server clockwise from its hash. Adding or removing a server only displaces the keys in the arc the new server now covers — a property that's essential for CDNs and distributed caches, because rehashing every key whenever a node joins or leaves would be catastrophic.

The naive implementation puts one point on the ring per server. With N servers, the ring is partitioned into N arcs, and those arcs are *not equal*. The expected variance is significant: when you hash 10 server IDs to 64-bit positions, the gaps between them follow an exponential distribution; the ratio of the largest arc to the smallest is, in expectation, O(log N) and easily 2-4x in practice for small N. So a ring of 10 servers might have one server holding 18% of keys and another holding 4%. Multiply by traffic volume and you get one shard at 80% CPU while another sits at 20% — and the hot shard's tail latency is what users actually feel.

Add a server and the situation can get *worse*: the new server takes one arc, but you've only added ~10% capacity to soak up the imbalance, and which arc you happen to hit is itself a coin flip. In a real CDN around the early 2010s, a node addition to relieve a hot shard ended up *splitting the second-busiest shard* and leaving the busiest unchanged — a result that looked like the consistent-hash literature had lied. It hadn't; the literature assumed virtual nodes.

The fix is **virtual nodes (vnodes)**: place each physical server at many positions on the ring (typically 100-200 per server). The variance of the resulting arc distribution drops as O(1 / √V) where V is the total number of points; with V = 1000+, the largest-arc to smallest-arc ratio is essentially 1.05–1.1. As a bonus, adding a physical server now adds 100-200 small arcs spread around the ring, so the load it takes on is drawn proportionally from every existing server — exactly the "minimal disruption" property consistent hashing is supposed to give you.

## The naive code

```python
class HashRing:
    def __init__(self, nodes):
        self.ring = sorted((hash(n), n) for n in nodes)  # one point per node

    def lookup(self, key):
        h = hash(key)
        i = bisect.bisect_left(self.ring, (h,))
        return self.ring[i % len(self.ring)][1]
```

With 10 nodes this ring has 10 arcs. The largest arc routinely ends up 3-4x the smallest in real distributions.

## The DSA insight

This is a *concentration-of-measure* fact about randomly placed points on a circle. Drop N points uniformly on [0, 1); the expected size of the largest gap is roughly `(ln N) / N`, while the mean gap is `1/N`. The ratio is `ln N`, which is "small" only asymptotically — for N=10, ln 10 ≈ 2.3, matching the 2-3x imbalance observed in practice.

You can *fix the variance two ways*:

1. **More points (vnodes)**. The variance of the maximum gap shrinks as you add more points. With kN points (k = vnodes-per-server), the imbalance ratio drops as O(√(ln(kN)/k)). For k=100, the ratio is well under 1.1.
2. **Deterministic placement (rendezvous / HRW hashing)**. Instead of placing servers on a ring, hash (key, server_id) jointly and pick the server with the maximum joint hash. This gives perfect uniformity in expectation and doesn't require any vnodes — but it makes "which keys move when I add a server?" a more complex question to reason about than the simple arc-displacement story.

Both are valid; consistent-hash-with-vnodes won historically because the arc visualization is intuitive and the operational story ("add a server, ~K/N keys move") is easy to explain to ops teams.

## The fix

```python
class HashRing:
    def __init__(self, nodes, vnodes_per_node=128):
        self.ring = []
        for n in nodes:
            for v in range(vnodes_per_node):
                self.ring.append((hash(f"{n}#{v}"), n))    # 128 points per node
        self.ring.sort()

    def lookup(self, key):
        h = hash(key)
        i = bisect.bisect_left(self.ring, (h,))
        return self.ring[i % len(self.ring)][1]
```

Capstone 6 has the long-form derivation of why 128 vnodes is enough for ~100-node clusters and what happens when you scale up — the formulas are short, the experiment is even shorter.

## What you can learn

- "Hash the server name and put it on a ring" gives you the *correctness* of consistent hashing and very little of the *balance*. Always add virtual nodes (or use rendezvous hashing).
- A natural-looking uniform random construction can have surprisingly large variance — your intuition about "uniform" is wrong for small N. The largest-gap-of-N-points formula is the kind of fact worth memorizing.
- Whenever you scale a system by adding a shard / node / partition, ask "by what factor did the variance of the load go down?" If the answer isn't roughly `1/√k` where k is the number of placements, you're not getting the load smoothing you think you are.
- The same problem shows up in random-partitioner designs for Kafka, Cassandra, ScyllaDB, and any hash-based sharded store. The mitigation (more partitions per node, or rendezvous hashing) is universal.

## Related curriculum
- Week 16 (Hashing — universal hashing and load-balancing properties)
- Capstone 6 (URL shortener / distributed store) — the long-form lab on hash rings
- `tests/cases/consistent_hashing.json` — synthesize a 10-node ring with and without vnodes; measure max-arc / min-arc on 10⁶ random keys
