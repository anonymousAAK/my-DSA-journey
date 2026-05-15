"""Reference: LRU cache driven by a list of operations.

The fixture input is `[capacity, ops]` where `ops` is a list of operations:
    ["put", k, v]   -> returns None (not included in output)
    ["get", k]      -> returns the looked-up value (or -1) and appends to output

The driver returns the ordered list of get results.
"""

from __future__ import annotations
from collections import OrderedDict
from typing import List, Any


class _LRU:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: "OrderedDict[int, int]" = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


def lruDriver(capacity: int, ops: List[List[Any]]) -> List[int]:
    cache = _LRU(capacity)
    out: List[int] = []
    for op in ops:
        name = op[0]
        if name == "put":
            cache.put(op[1], op[2])
        elif name == "get":
            out.append(cache.get(op[1]))
        else:
            raise ValueError(f"unknown op {name!r}")
    return out
