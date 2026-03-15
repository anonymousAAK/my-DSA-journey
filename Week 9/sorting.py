"""
Week 9 — Sorting
==================
Topics covered:
  - Bubble sort (with early termination)
  - Selection sort
  - Insertion sort
  - Merge sort (with inversion count)
  - Quicksort (Lomuto partition + randomized pivot)
  - Quickselect (k-th smallest element)
  - Counting sort

Each function includes time/space complexity analysis in its docstring.
All sort functions sort **in-place** unless noted otherwise, and return the
list for convenience.
"""

from __future__ import annotations

import random
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Bubble Sort (with early termination)
# ---------------------------------------------------------------------------

def bubble_sort(arr: List[int]) -> List[int]:
    """Sort *arr* in-place using bubble sort.

    Optimisation: if no swaps occur during a full pass, the array is already
    sorted and we can terminate early.

    Time:  O(n^2) worst/average, O(n) best (already sorted)
    Space: O(1)
    Stable: Yes
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break  # early termination
    return arr


# ---------------------------------------------------------------------------
# Selection Sort
# ---------------------------------------------------------------------------

def selection_sort(arr: List[int]) -> List[int]:
    """Sort *arr* in-place using selection sort.

    Find the minimum element in the unsorted portion and swap it into place.

    Time:  O(n^2)
    Space: O(1)
    Stable: No (default implementation)
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# ---------------------------------------------------------------------------
# Insertion Sort
# ---------------------------------------------------------------------------

def insertion_sort(arr: List[int]) -> List[int]:
    """Sort *arr* in-place using insertion sort.

    Build up a sorted prefix one element at a time by shifting elements.

    Time:  O(n^2) worst/average, O(n) best (already sorted)
    Space: O(1)
    Stable: Yes
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# ---------------------------------------------------------------------------
# Merge Sort (with inversion count)
# ---------------------------------------------------------------------------

def merge_sort(arr: List[int]) -> List[int]:
    """Sort *arr* in-place using merge sort (top-down, recursive).

    Time:  O(n log n) — always
    Space: O(n) — temporary arrays during merge
    Stable: Yes
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    merge_sort(left)
    merge_sort(right)

    # Merge back into arr
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
    return arr


def merge_sort_count_inversions(arr: List[int]) -> Tuple[List[int], int]:
    """Sort *arr* and return (sorted_array, inversion_count).

    An inversion is a pair (i, j) where i < j but arr[i] > arr[j].
    Counting inversions during merge sort is a classic divide-and-conquer
    application.

    Time:  O(n log n)
    Space: O(n)
    """
    if len(arr) <= 1:
        return arr[:], 0

    mid = len(arr) // 2
    left, left_inv = merge_sort_count_inversions(arr[:mid])
    right, right_inv = merge_sort_count_inversions(arr[mid:])

    merged: list[int] = []
    inversions = left_inv + right_inv
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            # All remaining elements in left are > right[j] → inversions
            merged.append(right[j])
            inversions += len(left) - i
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inversions


# ---------------------------------------------------------------------------
# Quicksort (Lomuto partition + randomized)
# ---------------------------------------------------------------------------

def _lomuto_partition(arr: List[int], lo: int, hi: int) -> int:
    """Lomuto partition scheme: pick arr[hi] as pivot.

    Returns the final index of the pivot after partitioning.
    Elements <= pivot are moved to the left, elements > pivot to the right.
    """
    pivot = arr[hi]
    i = lo - 1  # boundary of the "small" region
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


def quicksort(arr: List[int], lo: int = 0, hi: int | None = None) -> List[int]:
    """Sort *arr* in-place using quicksort with Lomuto partition.

    Time:  O(n log n) average, O(n^2) worst
    Space: O(log n) average stack depth
    Stable: No
    """
    if hi is None:
        hi = len(arr) - 1
    if lo < hi:
        pivot_idx = _lomuto_partition(arr, lo, hi)
        quicksort(arr, lo, pivot_idx - 1)
        quicksort(arr, pivot_idx + 1, hi)
    return arr


def quicksort_randomized(
    arr: List[int], lo: int = 0, hi: int | None = None
) -> List[int]:
    """Randomized quicksort — swap a random element to the pivot position
    before partitioning to avoid worst-case on already-sorted input.

    Time:  O(n log n) expected
    Space: O(log n) expected stack depth
    Stable: No
    """
    if hi is None:
        hi = len(arr) - 1
    if lo < hi:
        # Randomize pivot
        rand_idx = random.randint(lo, hi)
        arr[rand_idx], arr[hi] = arr[hi], arr[rand_idx]
        pivot_idx = _lomuto_partition(arr, lo, hi)
        quicksort_randomized(arr, lo, pivot_idx - 1)
        quicksort_randomized(arr, pivot_idx + 1, hi)
    return arr


# ---------------------------------------------------------------------------
# Quickselect — k-th Smallest Element
# ---------------------------------------------------------------------------

def quickselect(arr: List[int], k: int) -> int:
    """Return the k-th smallest element (1-indexed) using quickselect.

    Modifies *arr* in-place (partial sorting).

    Time:  O(n) average, O(n^2) worst
    Space: O(1) iterative tail
    """
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} is out of range for array of length {len(arr)}")

    target = k - 1  # convert to 0-indexed
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        # Randomize pivot for expected O(n) performance
        rand_idx = random.randint(lo, hi)
        arr[rand_idx], arr[hi] = arr[hi], arr[rand_idx]
        pivot_idx = _lomuto_partition(arr, lo, hi)

        if pivot_idx == target:
            return arr[pivot_idx]
        elif pivot_idx < target:
            lo = pivot_idx + 1
        else:
            hi = pivot_idx - 1

    return arr[lo]  # lo == hi == target


# ---------------------------------------------------------------------------
# Counting Sort
# ---------------------------------------------------------------------------

def counting_sort(arr: List[int]) -> List[int]:
    """Sort *arr* of non-negative integers using counting sort.

    Time:  O(n + k)  where k = max(arr)
    Space: O(n + k)
    Stable: Yes
    """
    if not arr:
        return arr

    max_val = max(arr)
    count = [0] * (max_val + 1)

    # Count occurrences
    for val in arr:
        count[val] += 1

    # Compute prefix sums (cumulative counts)
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Build the output array (iterate backwards for stability)
    output = [0] * len(arr)
    for val in reversed(arr):
        count[val] -= 1
        output[count[val]] = val

    # Copy back
    arr[:] = output
    return arr


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import copy

    test_cases = [
        [5, 3, 8, 4, 2],
        [1],
        [],
        [3, 3, 3],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [64, 34, 25, 12, 22, 11, 90],
    ]

    # ---- O(n^2) sorts ----
    for sort_fn in (bubble_sort, selection_sort, insertion_sort):
        for tc in test_cases:
            data = tc[:]
            sort_fn(data)
            assert data == sorted(tc), f"{sort_fn.__name__} failed on {tc}"
    print("[PASS] Bubble, Selection, Insertion sort")

    # ---- Merge sort ----
    for tc in test_cases:
        data = tc[:]
        merge_sort(data)
        assert data == sorted(tc), f"merge_sort failed on {tc}"
    print("[PASS] Merge sort")

    # ---- Merge sort with inversion count ----
    result, inv = merge_sort_count_inversions([2, 4, 1, 3, 5])
    assert result == [1, 2, 3, 4, 5]
    assert inv == 3  # (2,1), (4,1), (4,3)
    _, inv2 = merge_sort_count_inversions([5, 4, 3, 2, 1])
    assert inv2 == 10  # fully reversed — n*(n-1)/2
    print("[PASS] Merge sort with inversion count")

    # ---- Quicksort ----
    for sort_fn in (quicksort, quicksort_randomized):
        for tc in test_cases:
            data = tc[:]
            sort_fn(data)
            assert data == sorted(tc), f"{sort_fn.__name__} failed on {tc}"
    print("[PASS] Quicksort — Lomuto & randomized")

    # ---- Quickselect ----
    data = [7, 10, 4, 3, 20, 15]
    assert quickselect(data[:], 1) == 3
    assert quickselect(data[:], 3) == 7
    assert quickselect(data[:], 6) == 20
    print("[PASS] Quickselect (k-th smallest)")

    # ---- Counting sort ----
    for tc in test_cases:
        if tc and min(tc) >= 0:  # counting sort needs non-negative
            data = tc[:]
            counting_sort(data)
            assert data == sorted(tc), f"counting_sort failed on {tc}"
    print("[PASS] Counting sort")

    print("\nAll Week 9 tests passed!")
