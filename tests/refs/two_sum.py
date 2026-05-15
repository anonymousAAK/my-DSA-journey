"""Reference: two-sum returning the pair of indices summing to `target`.

The returned indices are in ascending order; returns [-1, -1] when no pair
exists.
"""

from __future__ import annotations
from typing import Dict, List


def twoSum(nums: List[int], target: int) -> List[int]:
    seen: Dict[int, int] = {}
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return [-1, -1]
