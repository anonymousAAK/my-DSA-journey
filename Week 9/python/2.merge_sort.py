"""
WEEK 9 - PYTHON DSA
Topic: Merge Sort (Divide and Conquer)
File: 2.merge_sort.py

CONCEPT:
    Recursively split the list in half, sort each half, then merge two
    sorted halves into one in O(n).

KEY POINTS:
    - Stable sort (use `<=` while merging to keep equal-key order).
    - Worst-case O(n log n) — same as best/average.
    - O(n) auxiliary memory for the merge buffer.
    - Foundation of TimSort (Python's built-in sort).

ALGORITHM / APPROACH:
    merge_sort(arr, left, right):
        if left >= right: return
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)

    merge: two pointers over L and R, write back into arr.

PYTHON-SPECIFIC NOTES:
    - Slicing `arr[left:mid+1]` creates a copy; we accept the cost for clarity.
    - The bonus "count inversions" routine uses the merging step's
      `len(L) - i` increment.

DRY RUN:
    arr = [38, 27, 43, 3, 9, 82, 10]
    halves at 38|27|43, 3|9|82|10 etc.
    after sort -> [3, 9, 10, 27, 38, 43, 82]

    Count inversions of [2,4,1,3,5]:
        recursion finds 3 inversions: (2,1),(4,1),(4,3).

COMPLEXITY:
    Time:  O(n log n) all cases
    Space: O(n) aux
    Stable: YES
"""

from typing import List


def _merge(arr: List[int], left: int, mid: int, right: int) -> None:
    L = arr[left:mid + 1]
    R = arr[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]; i += 1
        else:
            arr[k] = R[j]; j += 1
        k += 1
    while i < len(L):
        arr[k] = L[i]; i += 1; k += 1
    while j < len(R):
        arr[k] = R[j]; j += 1; k += 1


def merge_sort(arr: List[int], left: int = 0, right: int | None = None) -> None:
    if right is None:
        right = len(arr) - 1
    if left >= right:
        return
    mid = left + (right - left) // 2
    merge_sort(arr, left, mid)
    merge_sort(arr, mid + 1, right)
    _merge(arr, left, mid, right)


# --- BONUS: count inversions during merge ---
def _merge_count(arr: List[int], left: int, mid: int, right: int) -> int:
    L = arr[left:mid + 1]
    R = arr[mid + 1:right + 1]
    i = j = 0
    k = left
    inv = 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]; i += 1
        else:
            # All remaining L are greater than R[j]
            inv += len(L) - i
            arr[k] = R[j]; j += 1
        k += 1
    while i < len(L):
        arr[k] = L[i]; i += 1; k += 1
    while j < len(R):
        arr[k] = R[j]; j += 1; k += 1
    return inv


def _merge_sort_count(arr: List[int], left: int, right: int) -> int:
    if left >= right:
        return 0
    mid = left + (right - left) // 2
    inv = _merge_sort_count(arr, left, mid)
    inv += _merge_sort_count(arr, mid + 1, right)
    inv += _merge_count(arr, left, mid, right)
    return inv


def count_inversions(arr: List[int]) -> int:
    """O(n log n) inversion count using merge sort."""
    copy = arr.copy()
    return _merge_sort_count(copy, 0, len(copy) - 1)


def main() -> None:
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"Before: {arr}")
    merge_sort(arr)
    print(f"After:  {arr}")

    single = [5]
    merge_sort(single)
    print(f"\nSingle: {single}")

    already = [1, 2, 3, 4, 5]
    merge_sort(already)
    print(f"Already sorted: {already}")

    reverse = [5, 4, 3, 2, 1]
    merge_sort(reverse)
    print(f"Reverse sorted: {reverse}")

    print("\n=== Count Inversions ===")
    for t in [[2, 4, 1, 3, 5], [5, 3, 1, 4, 2], [1, 2, 3]]:
        print(f"{t} -> inversions: {count_inversions(t)}")


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - List slicing replaces Arrays.copyOfRange.
    - We pass the inversion count as a return value rather than using
      a class-level static field (no static state needed).
    - Python's built-in `sorted` is also stable and runs in O(n log n).
"""
