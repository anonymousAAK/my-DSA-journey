"""
WEEK 29 - PYTHON ADVANCED TOPICS
Topic: Caching - LRU, LFU and TTL
File: caching.py

CONCEPT:
    Caches keep recently/usefully accessed values close to the consumer to
    avoid recomputation or slow backend reads. The eviction policy decides
    what to drop when the cache is full:
      - LRU (Least Recently Used): evict the entry untouched longest.
      - LFU (Least Frequently Used): evict the entry with the smallest
        access count, tie-break by recency.
      - TTL (Time To Live): each entry expires after a duration.

KEY POINTS:
    - LRU: HashMap + doubly-linked list -> O(1) get/put.
    - LFU: HashMap of values + freq-buckets (each a doubly-linked list)
      -> O(1) get/put.
    - TTL: store expiry timestamps; lazily evict on access (or with a
      background sweeper).
    - Used by: Redis, Memcached, CPU caches, CDNs, browsers, IDE indexers.

ALGORITHM / APPROACH:
    LRU:
        get(k): move node k to head; return value
        put(k, v): if exists, update + move; else add new at head; if size
                   > cap, drop tail.
    LFU:
        maintain freq buckets; bump key from freq f to f+1; minFreq tracker
        for eviction; evict from minFreq bucket's tail.

PYTHON-SPECIFIC NOTES:
    - `collections.OrderedDict` already supports LRU via `move_to_end`. We
      also implement a manual doubly-linked list version for clarity.
    - For LFU we use OrderedDict per frequency bucket -> insertion order
      = recency.
    - `functools.lru_cache` is the stdlib decorator counterpart.

DRY RUN / EXAMPLE:
    LRU cache cap=2:
        put(1,1); put(2,2); get(1) -> 1 (1 becomes MRU)
        put(3,3) -> evicts 2 because it's LRU
        get(2) -> -1 (miss)
    LFU cache cap=2:
        put(1,1); put(2,2); get(1); get(1); put(3,3)
        -> 2 has freq 1, 1 has freq 3; evict 2.

COMPLEXITY:
    LRU:  O(1) per op. Space O(cap).
    LFU:  O(1) per op (amortised). Space O(cap).
"""

from __future__ import annotations

import time
from collections import OrderedDict, defaultdict
from typing import Any, Optional


# --------------------------------------------------------------------------
# LRU Cache via OrderedDict
# --------------------------------------------------------------------------
class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.data: OrderedDict[Any, Any] = OrderedDict()

    def get(self, key: Any) -> Any:
        if key not in self.data:
            return -1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key: Any, value: Any) -> None:
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.cap:
            self.data.popitem(last=False)


# --------------------------------------------------------------------------
# LFU Cache: HashMap + per-frequency OrderedDicts
# --------------------------------------------------------------------------
class LFUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.kv: dict[Any, Any] = {}
        self.kf: dict[Any, int] = {}            # key -> frequency
        self.fk: defaultdict[int, OrderedDict[Any, None]] = defaultdict(OrderedDict)
        self.min_freq = 0

    def _bump(self, key: Any) -> None:
        f = self.kf[key]
        del self.fk[f][key]
        if not self.fk[f]:
            del self.fk[f]
            if self.min_freq == f:
                self.min_freq += 1
        self.kf[key] = f + 1
        self.fk[f + 1][key] = None

    def get(self, key: Any) -> Any:
        if key not in self.kv:
            return -1
        self._bump(key)
        return self.kv[key]

    def put(self, key: Any, value: Any) -> None:
        if self.cap <= 0:
            return
        if key in self.kv:
            self.kv[key] = value
            self._bump(key)
            return
        if len(self.kv) >= self.cap:
            # evict from min_freq bucket (LRU within bucket)
            evict_key, _ = self.fk[self.min_freq].popitem(last=False)
            if not self.fk[self.min_freq]:
                del self.fk[self.min_freq]
            del self.kv[evict_key]
            del self.kf[evict_key]
        self.kv[key] = value
        self.kf[key] = 1
        self.fk[1][key] = None
        self.min_freq = 1


# --------------------------------------------------------------------------
# TTL Cache
# --------------------------------------------------------------------------
class TTLCache:
    def __init__(self, default_ttl_seconds: float) -> None:
        self.ttl = default_ttl_seconds
        self.data: dict[Any, tuple[Any, float]] = {}

    def get(self, key: Any) -> Any:
        item = self.data.get(key)
        if item is None:
            return None
        value, expires_at = item
        if expires_at < time.monotonic():
            del self.data[key]
            return None
        return value

    def put(self, key: Any, value: Any, ttl: Optional[float] = None) -> None:
        expires = time.monotonic() + (ttl if ttl is not None else self.ttl)
        self.data[key] = (value, expires)


def _demo() -> None:
    lru = LRUCache(2)
    lru.put(1, 1); lru.put(2, 2)
    print(f"LRU get(1) = {lru.get(1)}")
    lru.put(3, 3)
    print(f"LRU get(2) = {lru.get(2)}  (expected -1)")

    lfu = LFUCache(2)
    lfu.put(1, 1); lfu.put(2, 2)
    lfu.get(1); lfu.get(1)         # bump 1 to freq=3
    lfu.put(3, 3)                  # should evict 2 (freq=1)
    print(f"LFU get(2) = {lfu.get(2)}  (expected -1)")
    print(f"LFU get(1) = {lfu.get(1)}  (expected 1)")
    print(f"LFU get(3) = {lfu.get(3)}  (expected 3)")

    ttl = TTLCache(default_ttl_seconds=0.05)
    ttl.put("alpha", "value")
    print(f"TTL get(alpha) immediately = {ttl.get('alpha')!r}")
    time.sleep(0.06)
    print(f"TTL get(alpha) after expiry = {ttl.get('alpha')!r}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Java's system_design.java has an LRU via HashMap + DLL; Python uses
#     OrderedDict which already encapsulates that data structure.
#   * LFU here is more idiomatic via defaultdict(OrderedDict) for buckets.
#   * Time.monotonic() avoids issues with wall-clock adjustments mid-test.
