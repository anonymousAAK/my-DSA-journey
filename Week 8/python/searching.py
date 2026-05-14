"""
Week 8 — Searching
====================
Topics covered:
  - Binary search: iterative + recursive
  - First and last occurrence in a sorted array
  - Count occurrences of a target in a sorted array
  - Search in a rotated sorted array
  - Binary search on answer:
      • Integer square root
      • Koko eating bananas
      • Ship packages within D days

Each function includes time/space complexity analysis in its docstring.
"""

from __future__ import annotations

import math
from typing import List, Optional


# ---------------------------------------------------------------------------
# Binary Search — Iterative & Recursive
# ---------------------------------------------------------------------------

def binary_search_iterative(arr: List[int], target: int) -> int:
    """Return the index of *target* in sorted *arr*, or -1 if not found.

    Time:  O(log n)
    Space: O(1)
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def binary_search_recursive(
    arr: List[int], target: int, lo: int = 0, hi: int | None = None
) -> int:
    """Return the index of *target* in sorted *arr*, or -1 if not found.

    Time:  O(log n)
    Space: O(log n) — recursion depth
    """
    if hi is None:
        hi = len(arr) - 1
    if lo > hi:
        return -1
    mid = lo + (hi - lo) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, hi)
    else:
        return binary_search_recursive(arr, target, lo, mid - 1)


# ---------------------------------------------------------------------------
# First / Last Occurrence
# ---------------------------------------------------------------------------

def first_occurrence(arr: List[int], target: int) -> int:
    """Return the index of the first occurrence of *target*, or -1.

    Time:  O(log n)
    Space: O(1)
    """
    lo, hi = 0, len(arr) - 1
    result = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            result = mid
            hi = mid - 1  # keep searching left
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result


def last_occurrence(arr: List[int], target: int) -> int:
    """Return the index of the last occurrence of *target*, or -1.

    Time:  O(log n)
    Space: O(1)
    """
    lo, hi = 0, len(arr) - 1
    result = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            result = mid
            lo = mid + 1  # keep searching right
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result


# ---------------------------------------------------------------------------
# Count Occurrences
# ---------------------------------------------------------------------------

def count_occurrences(arr: List[int], target: int) -> int:
    """Count how many times *target* appears in a sorted array.

    Uses first_occurrence and last_occurrence for an O(log n) solution.

    Time:  O(log n)
    Space: O(1)
    """
    first = first_occurrence(arr, target)
    if first == -1:
        return 0
    last = last_occurrence(arr, target)
    return last - first + 1


# ---------------------------------------------------------------------------
# Search in Rotated Sorted Array
# ---------------------------------------------------------------------------

def search_rotated(arr: List[int], target: int) -> int:
    """Find *target* in a rotated sorted array (no duplicates).

    At each step, one half is guaranteed to be sorted.  Determine which
    half the target lies in and discard the other.

    Time:  O(log n)
    Space: O(1)
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid

        # Left half is sorted
        if arr[lo] <= arr[mid]:
            if arr[lo] <= target < arr[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        # Right half is sorted
        else:
            if arr[mid] < target <= arr[hi]:
                lo = mid + 1
            else:
                hi = mid - 1

    return -1


# ---------------------------------------------------------------------------
# Binary Search on Answer
# ---------------------------------------------------------------------------

def integer_sqrt(n: int) -> int:
    """Return floor(sqrt(n)) using binary search.

    Time:  O(log n)
    Space: O(1)
    """
    if n < 0:
        raise ValueError("Square root not defined for negative numbers")
    if n < 2:
        return n
    lo, hi = 1, n // 2
    result = 0
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if mid * mid == n:
            return mid
        elif mid * mid < n:
            result = mid  # mid might be the answer
            lo = mid + 1
        else:
            hi = mid - 1
    return result


def koko_bananas(piles: List[int], h: int) -> int:
    """Koko loves bananas.  She has *h* hours to eat all *piles*.
    Return the minimum eating speed *k* (bananas/hour).

    Binary search on the answer space [1, max(piles)].  For a given speed,
    compute total hours needed: sum(ceil(p / k) for p in piles).

    Time:  O(n * log(max_pile))
    Space: O(1)
    """

    def hours_needed(speed: int) -> int:
        return sum(math.ceil(p / speed) for p in piles)

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if hours_needed(mid) <= h:
            hi = mid  # try slower
        else:
            lo = mid + 1  # need faster
    return lo


def ship_packages(weights: List[int], days: int) -> int:
    """Return the minimum ship capacity to ship all *weights* within *days*.

    Binary search on the answer space [max(weights), sum(weights)].

    Time:  O(n * log(sum - max))
    Space: O(1)
    """

    def days_needed(capacity: int) -> int:
        d, current_load = 1, 0
        for w in weights:
            if current_load + w > capacity:
                d += 1
                current_load = 0
            current_load += w
        return d

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if days_needed(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ---- Binary Search ----
    sorted_arr = [1, 3, 5, 7, 9, 11, 13]
    for fn in (binary_search_iterative, binary_search_recursive):
        assert fn(sorted_arr, 7) == 3
        assert fn(sorted_arr, 1) == 0
        assert fn(sorted_arr, 13) == 6
        assert fn(sorted_arr, 4) == -1
        assert fn([], 1) == -1
    print("[PASS] Binary search — iterative & recursive")

    # ---- First / Last Occurrence ----
    rep = [1, 2, 2, 2, 3, 4, 5]
    assert first_occurrence(rep, 2) == 1
    assert last_occurrence(rep, 2) == 3
    assert first_occurrence(rep, 6) == -1
    print("[PASS] First / last occurrence")

    # ---- Count Occurrences ----
    assert count_occurrences(rep, 2) == 3
    assert count_occurrences(rep, 1) == 1
    assert count_occurrences(rep, 6) == 0
    print("[PASS] Count occurrences")

    # ---- Search in Rotated Sorted Array ----
    rotated = [4, 5, 6, 7, 0, 1, 2]
    assert search_rotated(rotated, 0) == 4
    assert search_rotated(rotated, 4) == 0
    assert search_rotated(rotated, 3) == -1
    assert search_rotated([1], 1) == 0
    print("[PASS] Search in rotated sorted array")

    # ---- Integer Sqrt ----
    assert integer_sqrt(0) == 0
    assert integer_sqrt(1) == 1
    assert integer_sqrt(8) == 2
    assert integer_sqrt(16) == 4
    assert integer_sqrt(26) == 5
    print("[PASS] Integer sqrt (binary search on answer)")

    # ---- Koko Bananas ----
    assert koko_bananas([3, 6, 7, 11], 8) == 4
    assert koko_bananas([30, 11, 23, 4, 20], 5) == 30
    assert koko_bananas([30, 11, 23, 4, 20], 6) == 23
    print("[PASS] Koko eating bananas")

    # ---- Ship Packages ----
    assert ship_packages([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
    assert ship_packages([3, 2, 2, 4, 1, 4], 3) == 6
    print("[PASS] Ship packages within D days")

    print("\nAll Week 8 tests passed!")
