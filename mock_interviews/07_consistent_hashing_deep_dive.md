# Mock Interview: Consistent Hashing Deep Dive

**Setup**: Staff engineer at a fictional distributed-cache vendor, Hashr. Candidate has 2 years of experience and has used DynamoDB and Cassandra at a surface level.

**Difficulty**: Hard system-design
**Topic**: Weeks 26-30 (consistent hashing, sharding, replication, rebalancing).

---

## Transcript

**Interviewer**: Walk me through consistent hashing. I'd like you to start from "why" — what problem does it solve — then get to implementation, then to the parts most people get wrong.

> 🔍 **What's happening here**: The prompt itself encodes the rubric. The interviewer is asking "why → how → pitfalls" so they can grade each section. Mirror that structure.

**Candidate**: Sure. The problem: I have K cache servers. I want to map keys to servers so that lookups are deterministic and load is even. The naive scheme is `hash(key) % K`. It works until K changes. Adding or removing one server changes (K-1)/K of all keys' assignments — your cache hit rate craters and your backing store gets flooded.

**Candidate**: Consistent hashing reduces that to roughly 1/K of keys moving when one node joins or leaves. The trick: hash both keys *and* node identifiers to the same large ring (say a 32-bit space). A key is assigned to the next node clockwise from its hash. When a node joins, it only takes keys from its successor; when a node leaves, its keys go to its successor. Other nodes are unaffected.

> 🔍 **What's happening here**: The candidate sized the failure mode ((K-1)/K of keys move under modulo) before explaining the fix. Showing the "before" delta lets the interviewer measure how impressive the "after" is.

**Interviewer**: Implementation?

**Candidate**: I keep a sorted structure of `(hash, node)` pairs. Lookup is binary search for the smallest hash ≥ `hash(key)`, wrapping around if none. Insert/remove is one update on the sorted structure. Concretely:

```python
from bisect import insort, bisect_left
import hashlib

def _h(s: str) -> int:
    return int(hashlib.md5(s.encode()).hexdigest()[:8], 16)  # 32-bit

class HashRing:
    def __init__(self, vnodes_per_node: int = 100):
        self.vnodes_per_node = vnodes_per_node
        self.hashes: list[int] = []
        self.owner: dict[int, str] = {}

    def add_node(self, node: str) -> None:
        for i in range(self.vnodes_per_node):
            h = _h(f"{node}#{i}")
            insort(self.hashes, h)
            self.owner[h] = node

    def remove_node(self, node: str) -> None:
        for i in range(self.vnodes_per_node):
            h = _h(f"{node}#{i}")
            idx = bisect_left(self.hashes, h)
            if idx < len(self.hashes) and self.hashes[idx] == h:
                self.hashes.pop(idx)
                del self.owner[h]

    def get_node(self, key: str) -> str | None:
        if not self.hashes:
            return None
        h = _h(key)
        idx = bisect_left(self.hashes, h)
        if idx == len(self.hashes):
            idx = 0  # wrap
        return self.owner[self.hashes[idx]]
```

**Interviewer**: Why `vnodes_per_node = 100`?

**Candidate**: Two reasons.

First, **variance**: with one hash per node, the ring positions are random and node load is highly skewed. By the standard random-interval-on-a-ring argument, one node ends up with a 1/K share *on average* but the variance is O(1/K), so with 10 nodes you can see a 2× imbalance. With V virtual nodes per physical node, the load standard deviation drops by roughly √V. V=100 to V=200 is the standard answer.

Second, **incremental migration**: with V=100 and 10 physical nodes, the ring has 1000 segments. When you add an 11th physical node, you peel ~1/11 of segments from across the other 10 nodes uniformly. With V=1, you'd move all of one neighbor's range at once.

> 🔍 **What's happening here**: The candidate gave the *quantitative* reason for vnodes (√V variance reduction) instead of just saying "it spreads load better". The quantitative form is what a senior interviewer is waiting to hear.

**Interviewer**: What does most people get wrong?

> 🔍 **What's happening here**: This is an invitation to demonstrate war wounds. Even if you've never operated this in production, name the *classic* failure modes that show up in postmortems.

**Candidate**: A handful of common mistakes:

**1. Hash function choice.** Using `hash(string)` in Python or Java's default — it's randomized per process or per JVM, so two clients disagree on where a key goes. You need a *stable* hash like MD5, SHA1, MurmurHash, xxHash. MD5 is fine here; cryptographic strength isn't needed, but stability is.

**2. Forgetting replication.** Consistent hashing tells you the *primary* owner. For replication factor R, the convention is to walk clockwise and take the next R distinct physical nodes — not the next R vnodes, which might all live on the same physical machine. Many implementations get this wrong and lose data when one box dies.

**3. The "hot key" problem.** Consistent hashing balances *keys* across nodes, not *load*. If one key is hit 1000× more than the rest, the node owning it is hot. Solutions: (a) detect and fan out hot keys to multiple replicas with random selection on read, (b) bound load per node via "bounded-load consistent hashing" (Google's variant — overflow keys spill to the next vnode), (c) shard the hot key itself by appending a random prefix on writes and reading all shards.

**4. Range queries.** Consistent hashing scatters adjacent keys. If your access pattern is "give me all users with ID in [1000, 2000]", you're hitting every node. Cassandra and DynamoDB handle this with a partition key (consistent hashing) plus a sort key (range within a partition). Don't reach for consistent hashing if you need range scans.

**5. Rebalancing storms.** When a node leaves, the next node clockwise gets all its keys *immediately*. If that successor is already near capacity, it OOMs and falls over, and now its successor inherits all of *that* — a cascading failure. Mitigation: bounded-load variant, or graceful drain (the leaving node hands off in batches before disappearing).

**6. Configuration drift.** Two clients believe the ring has different members because membership info is gossiped and they haven't converged. Some keys get cached on both nodes temporarily. Resolve by version-tagging the membership view and treating cross-version cache returns with skepticism.

> 🔍 **What's happening here**: The candidate listed six failure modes with concrete mitigations. Notice they didn't just say "replication is tricky" — they specified the trap (next R vnodes vs. next R *physical* nodes). Concreteness is what separates "read the wikipedia article" from "operated this".

**Interviewer**: Bounded-load consistent hashing — explain.

**Candidate**: Standard consistent hashing assigns key k to the first node clockwise from `hash(k)`. Variance means some nodes own more keys than others. Bounded-load adds: if that node is already at `(1 + ε)` times the average load, skip to the next clockwise node, and so on. The proof in the Google paper shows that load on any node is at most `(1 + ε)` × average while still moving only O(1/ε²) keys per node change. It's the trick behind Vimeo's HAProxy load balancer and Discord's session pinning.

**Interviewer**: How do you bootstrap a node?

**Candidate**: New node joins, picks vnode positions on the ring, and starts accepting writes for its newly-acquired key ranges. For each acquired range, it requests a transfer from the previous owner — a streaming snapshot followed by a tail of writes since the snapshot started, then a brief cutover where the previous owner stops serving and forwards. During this window, reads can serve stale data; if strong consistency is required, route reads to the previous owner until cutover.

**Interviewer**: Last challenge. The ring has 10 physical nodes with 100 vnodes each. A node fails. How many keys move, to which nodes, and how long does it take?

**Candidate**: About 1/10 of keys move — specifically the keys owned by the 100 vnodes belonging to the dead node. Each vnode's keys go to the next *physical* node clockwise from that vnode position (skipping vnodes of the dead node itself). Because the 100 vnodes are scattered ~uniformly, the failed node's load is shared across roughly all 9 surviving nodes — each absorbs ~1/9 of 1/10 ≈ 1.1% additional load.

Time to recover depends on data size per node and inter-node bandwidth. With 100 GB per node and 1 GB/s links, the dead node's 100 GB streams to 9 destinations in parallel — bottlenecked by the slowest receiver, ~11 GB each, ~11 seconds for raw bytes plus overhead. With replication factor 3 already in place, reads can serve from the surviving replicas during the rebuild and the system stays available.

> 🔍 **What's happening here**: The candidate did *numerical* sizing on the spot. Even rough numbers (10%, 1%, ~10 seconds) tell the interviewer you carry around order-of-magnitude intuition. This is the highest-leverage habit for distributed-systems interviews.

---

## Annotation legend

Each 🔍 callout teaches a specific *interview meta-skill*.

---

## What was tested
- Clarifying questions: ⚠️ minimal because the prompt structured itself — the candidate matched the prompt's structure instead
- Brute force first: ✅ named modulo hashing's failure mode
- Complexity-driven optimization: ✅ √V variance reduction, 1/K key movement
- Edge cases without prompting: ✅ six pitfalls, all real
- Communication while coding: ✅ commented the wrap-around
- Handling interviewer hints: ✅ "most people get wrong" → enumerated rather than picked one

## Reflection prompts for the learner
- Write down the formula for the variance of node load with V virtual nodes per node and K physical nodes. (Hint: think of each key as a uniform pick on the ring; the load is the sum of V exponential-ish intervals.)
- Implement bounded-load consistent hashing on top of the `HashRing` class. What's the right data structure to track per-node load while keeping `get_node` cheap?
- The candidate said "consistent hashing scatters adjacent keys" — so why does Cassandra still use it? Look up "token-aware partitioner" and "ByteOrderedPartitioner" and explain the deprecation of the latter.
