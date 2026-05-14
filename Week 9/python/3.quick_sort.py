"""
WEEK 9 - PYTHON DSA
Topic: Quick Sort
File: 3.quick_sort.py

CONCEPT:
    Pick a PIVOT, partition the array so smaller values precede the pivot
    and larger values follow it; recursively sort the two halves.

KEY POINTS:
    - Two common partition schemes:
        Lomuto (simpler) — pivot at last index
        Hoare  (original) — two-pointer; fewer swaps
    - Average O(n log n); worst O(n^2) on sorted input without randomisation.
    - In place: O(log n) stack on average, O(n) worst.
    - Quickselect: find kth smallest in O(n) average using the same partition.

ALGORITHM / APPROACH:
    Lomuto partition:
        pivot = arr[high]
        i = low - 1
        for j in [low..high):
            if arr[j] <= pivot:
                i += 1
                swap(arr[i], arr[j])
        swap(arr[i+1], arr[high])   # pivot in place
        return i + 1
    Recurse on [low..i] and [i+2..high].

PYTHON-SPECIFIC NOTES:
    - Use random.randint for pivot selection.
    - Recursion limit is 1000; reach via sys.setrecursionlimit if needed.

DRY RUN:
    arr = [10, 7, 8, 9, 1, 5], Lomuto with pivot=5
        j=0 10>5
        j=1 7>5
        j=2 8>5
        j=3 9>5
        j=4 1<=5: i=0 swap(10,1) -> [1,7,8,9,10,5]
        end: swap arr[1] and arr[5] -> [1,5,8,9,10,7]
        pivot index = 1
        Recurse on [1..0] (empty) and [2..5]

COMPLEXITY:
    Average:  O(n log n) time, O(log n) stack
    Worst:    O(n^2) time (mitigated by randomisation)
    Stable:   NO
"""

import random
from typing import List


_rng = random.Random(42)


def lomuto_partition(arr: List[int], low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_lomuto(arr: List[int], low: int = 0, high: int | None = None) -> None:
    if high is None:
        high = len(arr) - 1
    if low >= high:
        return
    p = lomuto_partition(arr, low, high)
    quick_sort_lomuto(arr, low, p - 1)
    quick_sort_lomuto(arr, p + 1, high)


def hoare_partition(arr: List[int], low: int, high: int) -> int:
    pivot = arr[low]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while arr[j] > pivot:
            j -= 1
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]


def quick_sort_hoare(arr: List[int], low: int = 0, high: int | None = None) -> None:
    if high is None:
        high = len(arr) - 1
    if low >= high:
        return
    p = hoare_partition(arr, low, high)
    quick_sort_hoare(arr, low, p)
    quick_sort_hoare(arr, p + 1, high)


def quick_sort_random(arr: List[int], low: int = 0, high: int | None = None) -> None:
    if high is None:
        high = len(arr) - 1
    if low >= high:
        return
    pivot_idx = _rng.randint(low, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    p = lomuto_partition(arr, low, high)
    quick_sort_random(arr, low, p - 1)
    quick_sort_random(arr, p + 1, high)


def quick_select(arr: List[int], low: int, high: int, k: int) -> int:
    """k is 1-indexed."""
    if low == high:
        return arr[low]
    pivot_idx = _rng.randint(low, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    p = lomuto_partition(arr, low, high)
    rank = p - low + 1
    if rank == k:
        return arr[p]
    if k < rank:
        return quick_select(arr, low, p - 1, k)
    return quick_select(arr, p + 1, high, k - rank)


def main() -> None:
    base = [10, 7, 8, 9, 1, 5]

    arr1 = base.copy()
    print("Lomuto QuickSort:")
    print(f"Before: {arr1}")
    quick_sort_lomuto(arr1)
    print(f"After:  {arr1}")

    arr2 = base.copy()
    print("\nHoare QuickSort:")
    print(f"Before: {arr2}")
    quick_sort_hoare(arr2)
    print(f"After:  {arr2}")

    arr3 = base.copy()
    print("\nRandomized QuickSort:")
    quick_sort_random(arr3)
    print(f"After:  {arr3}")

    worst = [1, 2, 3, 4, 5, 6, 7, 8]
    quick_sort_random(worst)
    print(f"\nAlready sorted -> randomised: {worst}")

    arr4 = [3, 2, 1, 5, 6, 4]
    print("\nQuickSelect — kth smallest:")
    for k in range(1, len(arr4) + 1):
        copy = arr4.copy()
        print(f"k={k}: {quick_select(copy, 0, len(copy) - 1, k)}")


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - random.Random(seed) gives a reproducible RNG.
    - Recursive quicksort can exceed Python's default recursion limit on
      large adversarial inputs — randomisation keeps depth O(log n) w.h.p.
    - Tuple swaps simplify the in-place partition code substantially.
"""
