"""
WEEK 6 - PYTHON DSA
Topic: Array Reverse and Rotate
File: 3.array_reverse_and_rotate.py

CONCEPT:
    Two foundational in-place transformations on a list:
      1. Reverse a list using two pointers.
      2. Left/right rotate by k using the "reversal algorithm".

KEY POINTS:
    - Two-pointer reversal is O(n) time and O(1) extra space.
    - Reversal-based rotation is also O(n) time and O(1) space —
      far better than the naive O(n*k) shift loop.
    - Always reduce k modulo n; rotations of length n are no-ops.

ALGORITHM / APPROACH:
    Reverse subarray [l..r]:
        while l < r: swap, l++, r--
    Left rotate by k (k = k % n):
        reverse(arr, 0, k-1)
        reverse(arr, k, n-1)
        reverse(arr, 0, n-1)
    Right rotate by k = left rotate by (n - k % n).

PYTHON-SPECIFIC NOTES:
    - The "Pythonic" reverse is `arr.reverse()` or `arr[::-1]`.
    - Slice assignment can rotate in one expression:
        arr[:] = arr[k:] + arr[:k]   (uses O(n) extra space).
    - We still implement the manual algorithm because the topic is
      to learn the *technique*, not just the standard library.

DRY RUN:
    arr = [1,2,3,4,5]
        reverse: l=0,r=4 swap -> [5,2,3,4,1]
                 l=1,r=3 swap -> [5,4,3,2,1]
                 l=2,r=2 stop
    arr = [1,2,3,4,5], left rotate k=2
        rev(0,1): [2,1,3,4,5]
        rev(2,4): [2,1,5,4,3]
        rev(0,4): [3,4,5,1,2]

COMPLEXITY:
    Reverse : O(n) time, O(1) space
    Rotate  : O(n) time, O(1) space
"""

from typing import List


def reverse(arr: List[int], l: int, r: int) -> None:
    """In-place reverse of arr[l..r]."""
    while l < r:
        arr[l], arr[r] = arr[r], arr[l]
        l += 1
        r -= 1


def reverse_array(arr: List[int]) -> None:
    """In-place reverse of the whole array."""
    reverse(arr, 0, len(arr) - 1)


def left_rotate(arr: List[int], k: int) -> None:
    """In-place left rotation by k positions (reversal algorithm)."""
    n = len(arr)
    if n == 0:
        return
    k = k % n
    if k == 0:
        return
    reverse(arr, 0, k - 1)
    reverse(arr, k, n - 1)
    reverse(arr, 0, n - 1)


def right_rotate(arr: List[int], k: int) -> None:
    """Right rotate by k = left rotate by (n - k mod n)."""
    n = len(arr)
    if n == 0:
        return
    left_rotate(arr, n - (k % n))


def main() -> None:
    # --- Reverse ---
    arr1 = [1, 2, 3, 4, 5]
    print(f"Original: {arr1}")
    reverse_array(arr1)
    print(f"Reversed: {arr1}")

    # --- Left Rotate ---
    arr2 = [1, 2, 3, 4, 5]
    print(f"\nOriginal:         {arr2}")
    left_rotate(arr2, 2)
    print(f"Left Rotate by 2: {arr2}")

    # --- Right Rotate ---
    arr3 = [1, 2, 3, 4, 5]
    print(f"\nOriginal:          {arr3}")
    right_rotate(arr3, 2)
    print(f"Right Rotate by 2: {arr3}")

    # --- Edge cases ---
    single = [42]
    left_rotate(single, 5)
    print(f"\nSingle element rotated: {single}")

    empty: List[int] = []
    left_rotate(empty, 3)
    print(f"Empty array: {empty}")

    # Pythonic alternatives
    print("\nPythonic shortcuts:")
    print(f"reversed slice : {[1,2,3,4,5][::-1]}")
    arr = [1, 2, 3, 4, 5]
    k = 2
    print(f"slice rotation : {arr[k:] + arr[:k]}")


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - `a, b = b, a` performs a swap without a temporary variable.
    - Slicing (`arr[k:] + arr[:k]`) is concise but allocates O(n).
    - `list.reverse()` mutates in place; `reversed(list)` returns an iterator.
    - Java needs explicit length checks for empty arrays; Python's range/slice
      handle empty lists naturally.
"""
