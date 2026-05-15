"""
WEEK 6 - PYTHON DSA
Topic: Linear Search
File: 2.linear_search.py

CONCEPT:
    Sequentially scan an array for a target value. Works on any
    array — sorted or not. The simplest possible search algorithm.

KEY POINTS:
    - Returns the index of the first occurrence, or -1 if absent.
    - Variants: last occurrence, count, min/max in one pass.
    - For small N (< 30) it can outperform binary search due to
      cache locality and the lack of branching cost.

ALGORITHM / APPROACH:
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

PYTHON-SPECIFIC NOTES:
    - `enumerate(arr)` gives (index, value) pairs idiomatically.
    - `arr.index(target)` raises ValueError if missing — a try/except
      wrap is needed if you want -1 semantics.
    - min() / max() do the min/max pass for you in O(n).

DRY RUN:
    arr = [4,2,7,1,9,3,7,5], target = 7
        i=0 4!=7
        i=1 2!=7
        i=2 7==7 -> return 2
    arr = [4,2,7,1,9,3,7,5], target = 6
        scan all, return -1

COMPLEXITY:
    Best  : O(1)  target at index 0
    Avg   : O(n)
    Worst : O(n)
    Space : O(1)
"""

from typing import List, Tuple


def linear_search(arr: List[int], target: int) -> int:
    """Index of first occurrence, or -1."""
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1


def linear_search_last(arr: List[int], target: int) -> int:
    """Index of last occurrence, or -1."""
    last_idx = -1
    for i, value in enumerate(arr):
        if value == target:
            last_idx = i
    return last_idx


def count_occurrences(arr: List[int], target: int) -> int:
    """Total times target appears."""
    return sum(1 for value in arr if value == target)


def find_min_max(arr: List[int]) -> Tuple[int, int]:
    """Single-pass min/max — raises ValueError on empty list."""
    if not arr:
        raise ValueError("Empty array")
    mn = mx = arr[0]
    for value in arr:
        if value < mn:
            mn = value
        if value > mx:
            mx = value
    return mn, mx


def main() -> None:
    arr = [4, 2, 7, 1, 9, 3, 7, 5]
    print(f"Array: {arr}")

    print(f"linear_search(7) = {linear_search(arr, 7)}")            # 2
    print(f"linear_search(6) = {linear_search(arr, 6)}")            # -1
    print(f"linear_search_last(7) = {linear_search_last(arr, 7)}")  # 6

    print(f"count_occurrences(7) = {count_occurrences(arr, 7)}")    # 2
    print(f"count_occurrences(6) = {count_occurrences(arr, 6)}")    # 0

    mn, mx = find_min_max(arr)
    print(f"Min = {mn}, Max = {mx}")                                # 1, 9

    try:
        raw = input("\nEnter element to search (blank to skip): ").strip()
        if raw:
            target = int(raw)
            idx = linear_search(arr, target)
            print("Not found" if idx == -1 else f"Found at index {idx}")
    except EOFError:
        pass


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - `enumerate` removes the need to manage an index variable manually.
    - Generator expressions (`sum(1 for ...)`) are concise but allocate;
      a manual counter is equally fine.
    - find_min_max returns a tuple, not a 2-element array — destructuring
      is built into the language.
"""
