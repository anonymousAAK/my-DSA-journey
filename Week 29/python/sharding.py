"""
WEEK 29 - PYTHON ADVANCED TOPICS
Topic: Sharding Strategies
File: sharding.py

CONCEPT:
    Sharding partitions data across multiple nodes so each holds a subset of
    the key space. Three common strategies:
      1. Range-based:   sort keys, contiguous ranges per shard (good for
                        range scans; risk of hot ranges).
      2. Hash-based:    shard = hash(key) mod N (good distribution; bad
                        rebalancing on N change -> see consistent hashing).
      3. Directory-based / lookup: a metadata service maps key -> shard
                        (max flexibility, extra hop).

    Each strategy trades off write amplification, range-query latency,
    and rebalance cost.

KEY POINTS:
    - Range shards keep keys contiguous: efficient prefix/range scans, but
      hot ranges (e.g. time-sorted writes) bottleneck on one shard.
    - Hash shards spread keys evenly but break locality for range scans.
    - Directory shards give per-key control but require a coordinator
      cluster.

ALGORITHM / APPROACH:
    RANGE:        sort shard boundaries; binary search by key.
    HASH:         shard_idx = hash(key) mod N.
    DIRECTORY:    look up key in a registry (dict in this demo).

PYTHON-SPECIFIC NOTES:
    - bisect.bisect_right is the natural fit for range shard lookup.
    - hashlib gives stable cross-process hash values (Python's built-in
      hash() is salted per process and not portable).

DRY RUN / EXAMPLE:
    range shards (boundaries = ['c','m','t']): 'apple'->0, 'banana'->0,
    'cat'->1, 'mango'->2, 'tiger'->3.
    hash shards (N=4): 'user:42' -> some deterministic value mod 4.
    directory: explicit mapping registered by the user.

COMPLEXITY:
    Range: O(log shards) per lookup.
    Hash : O(L) where L is key length (for hashing).
    Dir  : O(1) per lookup.
"""

from __future__ import annotations

import bisect
import hashlib
from typing import Dict, List


class RangeShardRouter:
    """Each shard handles keys lexicographically in [boundary[i-1], boundary[i])."""

    def __init__(self, boundaries: List[str]) -> None:
        self.boundaries = sorted(boundaries)

    def route(self, key: str) -> int:
        return bisect.bisect_right(self.boundaries, key)


class HashShardRouter:
    def __init__(self, n_shards: int) -> None:
        self.n = n_shards

    def route(self, key: str) -> int:
        digest = hashlib.sha256(key.encode("utf-8")).digest()
        return int.from_bytes(digest[:8], "big") % self.n


class DirectoryShardRouter:
    def __init__(self) -> None:
        self.registry: Dict[str, int] = {}

    def assign(self, key: str, shard: int) -> None:
        self.registry[key] = shard

    def route(self, key: str) -> int:
        return self.registry.get(key, -1)


def _demo() -> None:
    rng = RangeShardRouter(["c", "m", "t"])
    for k in ["apple", "banana", "cat", "mango", "tiger"]:
        print(f"range {k!r:>9} -> shard {rng.route(k)}")

    hashr = HashShardRouter(4)
    for k in ["user:42", "user:43", "order:99", "session:xyz"]:
        print(f"hash  {k!r:>15} -> shard {hashr.route(k)}")

    dr = DirectoryShardRouter()
    dr.assign("hot-customer:Acme", 0)
    dr.assign("hot-customer:Globex", 1)
    print(f"dir   'hot-customer:Acme' -> shard {dr.route('hot-customer:Acme')}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Java's system_design.java does not include sharding; we add it here.
#   * bisect.bisect_right replaces Java's Collections.binarySearch + sign
#     adjustment for the range-shard lookup.
#   * hashlib.sha256 (deterministic across runs) is used instead of
#     Python's hash() which is salted per-process.
