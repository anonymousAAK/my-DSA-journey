"""
WEEK 30 - PYTHON ADVANCED TOPICS
Topic: Two Pointers Pattern
File: two_pointers.py

CONCEPT:
    The two-pointer pattern uses two indices that move through an array
    (often a sorted one) under monotonic rules. Each index advances at
    most n times, giving O(n) or O(n log n) algorithms for problems
    naively O(n^2) or worse.

KEY POINTS:
    - On a sorted array, the sum a[l] + a[r] is monotonic in (l, r), so
      we move pointers based on comparison with target.
    - For partitioning (Dutch flag, etc.), use l and r as low/high cursors.
    - For container / area problems the wider window dominates so always
      shrink the smaller side.

ALGORITHM / APPROACH:
    TWO SUM SORTED:    l=0,r=n-1; while l<r: shift based on s vs target.
    3SUM:              sort + iterate i; two-pointer inside for sum 0.
    CONTAINER MAX:     l=0,r=n-1; best = (r-l)*min(h[l],h[r]); shrink lower.
    REMOVE DUPLICATES: write index w; iterate r; copy when arr[r] != arr[w-1].

PYTHON-SPECIFIC NOTES:
    - Use list slicing for readability when extracting triples.
    - sorted() is stable; tuple list output for 3Sum is canonical.

DRY RUN / EXAMPLE:
    twoSumII [2,7,11,15], target 9 -> indices (1,2).
    3Sum [-1,0,1,2,-1,-4] -> [[-1,-1,2],[-1,0,1]].
    Max area [1,8,6,2,5,4,8,3,7] -> 49.

COMPLEXITY:
    Two-sum sorted:  O(n)
    3Sum:            O(n^2)
    Container max:   O(n)
"""

from __future__ import annotations

from typing import List, Tuple


def two_sum_sorted(nums: List[int], target: int) -> Tuple[int, int]:
    """LC 167 — returns 1-indexed pair or (-1,-1) if no solution."""
    l, r = 0, len(nums) - 1
    while l < r:
        s = nums[l] + nums[r]
        if s == target:
            return (l + 1, r + 1)
        if s < target:
            l += 1
        else:
            r -= 1
    return (-1, -1)


def three_sum(nums: List[int]) -> List[List[int]]:
    """LC 15 — all unique triples summing to 0."""
    nums = sorted(nums)
    result: List[List[int]] = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s == 0:
                result.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l + 1]:
                    l += 1
                while l < r and nums[r] == nums[r - 1]:
                    r -= 1
                l += 1
                r -= 1
            elif s < 0:
                l += 1
            else:
                r -= 1
    return result


def max_area(height: List[int]) -> int:
    """LC 11 — container with most water."""
    l, r, best = 0, len(height) - 1, 0
    while l < r:
        best = max(best, (r - l) * min(height[l], height[r]))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return best


def remove_duplicates_sorted(nums: List[int]) -> int:
    """LC 26 — in-place remove duplicates from sorted array; return new length."""
    if not nums:
        return 0
    w = 1
    for r in range(1, len(nums)):
        if nums[r] != nums[w - 1]:
            nums[w] = nums[r]
            w += 1
    return w


def _demo() -> None:
    print(f"Two Sum II [2,7,11,15] t=9: {two_sum_sorted([2,7,11,15], 9)}")
    print(f"3Sum [-1,0,1,2,-1,-4]: {three_sum([-1,0,1,2,-1,-4])}")
    print(f"Max Area [1,8,6,2,5,4,8,3,7]: {max_area([1,8,6,2,5,4,8,3,7])}")
    arr = [0,0,1,1,1,2,2,3,3,4]
    new_len = remove_duplicates_sorted(arr)
    print(f"Remove duplicates: new_len={new_len}, prefix={arr[:new_len]}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Python returns tuples / lists naturally for multi-value answers.
#   * `sorted(nums)` is non-destructive; Java's Arrays.sort mutates in place.
