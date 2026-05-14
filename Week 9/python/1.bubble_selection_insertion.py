"""
WEEK 9 - PYTHON DSA
Topic: Bubble Sort, Selection Sort, Insertion Sort
File: 1.bubble_selection_insertion.py

CONCEPT:
    Three classic O(n^2) "elementary" sorts. Despite the same worst-case
    time complexity, they differ in:
      - swap count
      - stability
      - best-case behaviour
      - performance on nearly-sorted input

KEY POINTS:
    Bubble sort:
        - Repeatedly swap adjacent out-of-order elements.
        - Best O(n) with early-stop optimisation.
        - Stable.
    Selection sort:
        - Find min of unsorted region; swap to the front.
        - O(n) swaps in total — useful when writes are costly.
        - Not stable in basic form.
    Insertion sort:
        - Build sorted prefix one element at a time.
        - Best O(n) for nearly-sorted input.
        - Stable.
        - Used inside hybrid sorts (TimSort, Introsort) for small N.

ALGORITHM / APPROACH:
    See per-function code; mirrors Java exactly.

PYTHON-SPECIFIC NOTES:
    - In-place swap: a[i], a[j] = a[j], a[i].
    - Lists are reference types — pass-by-reference, mutations visible.
    - The built-in `sorted` / `list.sort` use TimSort (stable, O(n log n)).

DRY RUN:
    arr = [64, 25, 12, 22, 11]
    bubble pass1: 25,12,22,11,64 (largest bubbles to end)
    bubble pass2: 12,22,11,25,64
    bubble pass3: 12,11,22,25,64
    bubble pass4: 11,12,22,25,64 (no swaps -> done)

COMPLEXITY:
    Bubble    : best O(n) avg/worst O(n^2)  stable  O(1) space
    Selection : O(n^2) all cases             not stable, O(1) space
    Insertion : best O(n) avg/worst O(n^2)  stable  O(1) space
"""

from typing import List


def bubble_sort(arr: List[int]) -> None:
    """In-place bubble sort with early-stop optimisation."""
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break


def selection_sort(arr: List[int]) -> None:
    """In-place selection sort."""
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]


def insertion_sort(arr: List[int]) -> None:
    """In-place insertion sort."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def count_inversions(arr: List[int]) -> int:
    """Brute-force inversion count — O(n^2)."""
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


def main() -> None:
    base = [64, 25, 12, 22, 11]

    arr1 = base.copy()
    print("Bubble Sort:")
    print(f"Before: {arr1}")
    bubble_sort(arr1)
    print(f"After:  {arr1}")

    arr2 = base.copy()
    print("\nSelection Sort:")
    print(f"Before: {arr2}")
    selection_sort(arr2)
    print(f"After:  {arr2}")

    arr3 = base.copy()
    print("\nInsertion Sort:")
    print(f"Before: {arr3}")
    insertion_sort(arr3)
    print(f"After:  {arr3}")

    already = [1, 2, 3, 4, 5]
    print("\nAlready sorted — bubble sort:")
    print(f"Before: {already}")
    bubble_sort(already)
    print(f"After:  {already}")

    inv = [5, 3, 1, 4, 2]
    print(f"\nArray: {inv}")
    print(f"Inversions: {count_inversions(inv)}")  # 8


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - Tuple swap (`a[i], a[j] = a[j], a[i]`) replaces three-line temp swaps.
    - list.copy() is the Pythonic shallow clone.
    - list.sort() / sorted() are the production-grade routines; we
      hand-roll here to learn the underlying algorithms.
"""
