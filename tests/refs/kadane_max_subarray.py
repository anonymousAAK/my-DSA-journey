"""Reference: maximum contiguous subarray sum (Kadane's algorithm).

Extracted from Week 6/python/4.prefix_sum_and_kadane.py — pure function with
a defined empty-array result of 0 (the Week 6 file crashes on empty; the
fixture defines 0 as the contract).
"""

from __future__ import annotations
from typing import List


def maxSubarraySum(arr: List[int]) -> int:
    if not arr:
        return 0
    best = current = arr[0]
    for i in range(1, len(arr)):
        current = max(arr[i], current + arr[i])
        best = max(best, current)
    return best
