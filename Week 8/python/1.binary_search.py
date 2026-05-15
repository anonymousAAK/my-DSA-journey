"""
WEEK 8 - PYTHON DSA
Topic: Binary Search (Iterative & Recursive)
File: 1.binary_search.py

CONCEPT:
    Binary search finds a value in a SORTED list in O(log n) by halving
    the search interval at each step.

KEY POINTS:
    - Prerequisite: array MUST be sorted.
    - Compute mid as low + (high - low) // 2 to avoid overflow (Python
      integers don't overflow, but the habit transfers to other langs).
    - Variants:
        * first occurrence (leftmost match)
        * last  occurrence (rightmost match)
        * count via first..last
        * search in a rotated sorted array

ALGORITHM / APPROACH:
    Standard:
        low, high = 0, n - 1
        while low <= high:
            mid = low + (high - low) // 2
            if arr[mid] == target: return mid
            elif arr[mid] < target: low = mid + 1
            else:                   high = mid - 1
        return -1

PYTHON-SPECIFIC NOTES:
    - bisect.bisect_left / bisect_right give a standard-library variant.
    - For the rotated case, identify which side is sorted and check the
      target lies in the sorted side's range.

DRY RUN:
    arr = [-5,-2,0,1,3,5,7,9,11], target = 5
        low=0 high=8 mid=4 arr[4]=3<5  -> low=5
        low=5 high=8 mid=6 arr[6]=7>5  -> high=5
        low=5 high=5 mid=5 arr[5]=5 -> return 5

    Rotated [4,5,6,7,0,1,2], target=0
        low=0 high=6 mid=3 arr[3]=7
            left half [4..7] sorted, target 0 not in [4..7), low=4
        low=4 high=6 mid=5 arr[5]=1
            arr[low]=0<=arr[mid]=1, target 0 in [0..1)? 0<=0<1 yes -> high=4
        low=4 high=4 mid=4 arr[4]=0 -> return 4

COMPLEXITY:
    Time:  O(log n)
    Space: O(1) iterative, O(log n) recursive
"""

from typing import List


def binary_search(arr: List[int], target: int) -> int:
    """Iterative O(log n)."""
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


def binary_search_rec(arr: List[int], target: int, low: int, high: int) -> int:
    if low > high:
        return -1
    mid = low + (high - low) // 2
    if arr[mid] == target:
        return mid
    if arr[mid] < target:
        return binary_search_rec(arr, target, mid + 1, high)
    return binary_search_rec(arr, target, low, mid - 1)


def first_occurrence(arr: List[int], target: int) -> int:
    """Leftmost index of target."""
    low, high = 0, len(arr) - 1
    result = -1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            result = mid
            high = mid - 1   # keep searching LEFT
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return result


def last_occurrence(arr: List[int], target: int) -> int:
    """Rightmost index of target."""
    low, high = 0, len(arr) - 1
    result = -1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            result = mid
            low = mid + 1    # keep searching RIGHT
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return result


def count_occurrences(arr: List[int], target: int) -> int:
    first = first_occurrence(arr, target)
    if first == -1:
        return 0
    return last_occurrence(arr, target) - first + 1


def search_rotated(arr: List[int], target: int) -> int:
    """Search in a rotated sorted array."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid
        if arr[low] <= arr[mid]:  # left half sorted
            if arr[low] <= target < arr[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:                     # right half sorted
            if arr[mid] < target <= arr[high]:
                low = mid + 1
            else:
                high = mid - 1
    return -1


def main() -> None:
    sorted_arr = [-5, -2, 0, 1, 3, 5, 7, 9, 11]
    print("Array: [-5,-2,0,1,3,5,7,9,11]")
    print(f"binary_search(5) = {binary_search(sorted_arr, 5)}")           # 5
    print(f"binary_search(0) = {binary_search(sorted_arr, 0)}")           # 2
    print(f"binary_search(4) = {binary_search(sorted_arr, 4)}")           # -1
    print(f"binary_search_rec(7) = {binary_search_rec(sorted_arr, 7, 0, len(sorted_arr) - 1)}")  # 6

    with_dups = [1, 2, 2, 2, 3, 4, 4, 5]
    print("\nArray with duplicates: [1,2,2,2,3,4,4,5]")
    print(f"first_occurrence(2) = {first_occurrence(with_dups, 2)}")      # 1
    print(f"last_occurrence(2)  = {last_occurrence(with_dups, 2)}")       # 3
    print(f"count_occurrences(2) = {count_occurrences(with_dups, 2)}")    # 3
    print(f"count_occurrences(4) = {count_occurrences(with_dups, 4)}")    # 2
    print(f"count_occurrences(6) = {count_occurrences(with_dups, 6)}")    # 0

    rotated = [4, 5, 6, 7, 0, 1, 2]
    print("\nRotated array: [4,5,6,7,0,1,2]")
    print(f"search_rotated(0) = {search_rotated(rotated, 0)}")            # 4
    print(f"search_rotated(6) = {search_rotated(rotated, 6)}")            # 2
    print(f"search_rotated(3) = {search_rotated(rotated, 3)}")            # -1


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - bisect.bisect_left(arr, t) returns the leftmost insertion index
      and is the idiomatic way to do binary search in production Python.
    - Python ints have arbitrary precision, so the (low+high)//2 mid
      cannot overflow; we still use the safer form for habit/teaching.
    - The chained comparison `arr[low] <= target < arr[mid]` reads naturally.
"""
