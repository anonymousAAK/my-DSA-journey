"""
WEEK 6 - PYTHON DSA
Topic: Return Array Sum
File: 1.return_array_sum.py

CONCEPT:
    Given a list of N integers, compute the sum of all its elements.
    A foundational warm-up for array iteration patterns.

KEY POINTS:
    - In Python a "list" replaces Java's int[]; it can hold any object.
    - The built-in sum() walks the iterable in C and is typically the
      fastest pure-Python option.
    - The recursive variant is included to demonstrate call-stack
      cost (Python's default recursion limit is 1000).

ALGORITHM / APPROACH:
    Iterative:
        total = 0
        for value in arr:
            total += value
        return total
    Recursive:
        sum(arr, i) = 0                    if i == len(arr)
                    = arr[i] + sum(arr,i+1) otherwise

PYTHON-SPECIFIC NOTES:
    - Use `from typing import List` (Python 3.8) or `list[int]` (3.9+).
    - `sum(arr)` is preferred to a manual loop; it returns 0 for [].
    - For large arrays, prefer the iterative form: Python recursion is
      not tail-call optimised.

DRY RUN:
    arr = [1, 2, 3, 4, 5]
        i=0 total=1
        i=1 total=3
        i=2 total=6
        i=3 total=10
        i=4 total=15  -> return 15
    arr = [-1, 0, 5, -3, 10]
        steps -> -1, -1, 4, 1, 11 -> return 11

COMPLEXITY:
    Iterative : O(n) time, O(1) extra space.
    Recursive : O(n) time, O(n) call-stack space.
"""

from typing import List


def array_sum(arr: List[int]) -> int:
    """Iterative O(n) sum."""
    total = 0
    for value in arr:
        total += value
    return total


def array_sum_recursive(arr: List[int], index: int = 0) -> int:
    """Recursive O(n) sum, O(n) stack."""
    if index == len(arr):
        return 0
    return arr[index] + array_sum_recursive(arr, index + 1)


def array_sum_builtin(arr: List[int]) -> int:
    """Pythonic one-liner using sum()."""
    return sum(arr)


def main() -> None:
    test1: List[int] = [1, 2, 3, 4, 5]
    print(f"Array: {test1}")
    print(f"Sum (iterative): {array_sum(test1)}")            # 15
    print(f"Sum (recursive): {array_sum_recursive(test1)}")  # 15
    print(f"Sum (builtin):   {array_sum_builtin(test1)}")    # 15

    test2: List[int] = [-1, 0, 5, -3, 10]
    print(f"\nArray: {test2}")
    print(f"Sum: {array_sum(test2)}")                        # 11

    test3: List[int] = []
    print(f"\nEmpty array sum: {array_sum(test3)}")          # 0

    # Optional interactive section guarded so the file remains scriptable.
    try:
        raw = input("\nEnter space-separated integers (or blank to skip): ").strip()
        if raw:
            arr = [int(x) for x in raw.split()]
            print(f"Sum = {array_sum(arr)}")
    except EOFError:
        pass


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - No explicit Scanner; input() returns a str and we split/parse manually.
    - List comprehensions replace the index-loop array fill pattern.
    - sum() handles the empty-list case naturally (returns 0); Java needs
      Arrays.stream(arr).sum() for the same effect.
    - Type hints (List[int]) are documentation only — not enforced at runtime.
"""
