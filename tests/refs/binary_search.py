"""Reference: classical iterative binary search on a sorted array.

Returns the index of `target` (any matching index — the leftmost in the
fixture cases) or -1 if not found.
"""

from __future__ import annotations
from typing import List


def binarySearch(arr: List[int], target: int) -> int:
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
