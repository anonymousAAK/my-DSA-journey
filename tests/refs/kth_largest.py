"""Reference: kth largest element via a min-heap of size k."""

from __future__ import annotations
import heapq
from typing import List


def kthLargest(arr: List[int], k: int) -> int:
    h: List[int] = []
    for x in arr:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return h[0]
