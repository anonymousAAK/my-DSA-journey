"""
WEEK 29 - PYTHON ADVANCED TOPICS
Topic: Consistent Hashing with Virtual Nodes
File: consistent_hashing.py

CONCEPT:
    Plain hash-mod-N sharding breaks horribly when you add/remove a node:
    most keys remap. Consistent hashing arranges hash space as a circle
    (0..2^64-1), places each node at multiple points (virtual nodes / VNs),
    and assigns a key to the *next* virtual node clockwise. Adding a node
    only displaces a 1/N fraction of keys.

KEY POINTS:
    - Used by: DynamoDB, Cassandra, memcached clients, Akka, Riak, CDNs.
    - Virtual nodes per physical node ensure balanced load and smooth
      rebalancing.
    - Lookup is O(log(N*V)) via ordered map / sorted list + binary search.
    - Removal is symmetric: only neighbours of the removed node take its
      keys.

ALGORITHM / APPROACH:
    add_node(name):    for i in range(vnodes): ring[hash(f"{name}#VN{i}")] = name
    remove_node(name): delete all VN entries belonging to it
    get_node(key):     find smallest ring entry >= hash(key); wrap if none

PYTHON-SPECIFIC NOTES:
    - We use `sortedcontainers` style logic with bisect on a sorted list
      of hash values, plus a parallel dict from hash -> node. We avoid the
      third-party `sortedcontainers` to keep stdlib-only.
    - `hashlib.sha256` for stable hash values.

DRY RUN / EXAMPLE:
    ring = empty; add A, B, C with V=150 VNs each -> 450 ring entries.
    get_node("user:1001"): hash to integer, binary-search next ring entry,
    return its node. Adding D moves ~25% of keys to D's neighbourhood.

COMPLEXITY:
    Time:  add/remove O(V log(NV)); get O(log(NV)).
    Space: O(NV).
"""

from __future__ import annotations

import bisect
import hashlib
from typing import Dict, List, Optional


class ConsistentHashRing:
    def __init__(self, vnodes_per_node: int = 150) -> None:
        self.v = vnodes_per_node
        self.sorted_hashes: List[int] = []
        self.hash_to_node: Dict[int, str] = {}

    @staticmethod
    def _hash(key: str) -> int:
        return int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest()[:8], "big")

    def add_node(self, name: str) -> None:
        for i in range(self.v):
            h = self._hash(f"{name}#VN{i}")
            self.hash_to_node[h] = name
            bisect.insort(self.sorted_hashes, h)

    def remove_node(self, name: str) -> None:
        for i in range(self.v):
            h = self._hash(f"{name}#VN{i}")
            if self.hash_to_node.pop(h, None) is not None:
                idx = bisect.bisect_left(self.sorted_hashes, h)
                if idx < len(self.sorted_hashes) and self.sorted_hashes[idx] == h:
                    self.sorted_hashes.pop(idx)

    def get_node(self, key: str) -> Optional[str]:
        if not self.sorted_hashes:
            return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.sorted_hashes, h)
        if idx == len(self.sorted_hashes):
            idx = 0
        return self.hash_to_node[self.sorted_hashes[idx]]


def _demo() -> None:
    ring = ConsistentHashRing(vnodes_per_node=150)
    for n in ["server-A", "server-B", "server-C"]:
        ring.add_node(n)
    for k in ["user:1001", "session:xyz", "order:42"]:
        print(f"  {k} -> {ring.get_node(k)}")

    print("\nAfter removing server-B:")
    ring.remove_node("server-B")
    for k in ["user:1001", "session:xyz", "order:42"]:
        print(f"  {k} -> {ring.get_node(k)}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Java uses TreeMap<Long, String> with `ceilingEntry`. Python's stdlib
#     does not ship a sorted dict, so we maintain a sorted list of hashes
#     plus a parallel dict — bisect for ceilingEntry behaviour.
#   * `hashlib.sha256` provides cross-process stability (built-in hash()
#     is salted per process).
