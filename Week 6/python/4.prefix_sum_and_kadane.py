"""
WEEK 6 - PYTHON DSA
Topic: Prefix Sum & Kadane's Algorithm
File: 4.prefix_sum_and_kadane.py

CONCEPT:
    PART A — Prefix Sum:
        Build P[i] = arr[0] + arr[1] + ... + arr[i] once in O(n);
        thereafter answer any range-sum query [l, r] in O(1) as
            P[r] - (P[l-1] if l > 0 else 0)

    PART B — Kadane's Algorithm:
        Find the contiguous subarray with the maximum sum.
        DP recurrence at index i:
            current = max(arr[i], current + arr[i])
            best    = max(best, current)
        Linear time, constant space.

KEY POINTS:
    - Prefix sum trades O(n) preprocessing for O(1) queries.
    - Kadane's handles all-negative arrays correctly because it
      starts with arr[0] rather than 0.
    - Extended Kadane returns the start/end indices.

ALGORITHM / APPROACH:
    Build prefix:
        P[0] = arr[0];  P[i] = P[i-1] + arr[i]
    Range sum:
        l == 0 -> P[r]
        else   -> P[r] - P[l-1]
    Kadane:
        best = current = arr[0]
        for i in 1..n-1:
            current = max(arr[i], current + arr[i])
            best    = max(best, current)
        return best

PYTHON-SPECIFIC NOTES:
    - itertools.accumulate(arr) gives the prefix array lazily; we
      keep an explicit loop to mirror the Java code 1:1.
    - max() of generator works but a manual loop is faster here.

DRY RUN:
    Prefix:
        arr = [3,-1,2,4,-3,7]
        P   = [3, 2,4,8, 5,12]
        rangeSum(1,4) = 5 - 3 = 2

    Kadane on [-2,1,-3,4,-1,2,1,-5,4]:
        i=0  cur=-2 best=-2
        i=1  cur=max(1,-2+1)=1 best=1
        i=2  cur=max(-3,1-3)=-2 best=1
        i=3  cur=max(4,-2+4)=4 best=4
        i=4  cur=max(-1,4-1)=3 best=4
        i=5  cur=max(2,3+2)=5 best=5
        i=6  cur=max(1,5+1)=6 best=6
        i=7  cur=max(-5,6-5)=1 best=6
        i=8  cur=max(4,1+4)=5 best=6
        -> 6 (subarray [4,-1,2,1])

COMPLEXITY:
    Prefix build : O(n) time, O(n) space
    Range sum    : O(1) per query
    Kadane       : O(n) time, O(1) space
"""

from typing import List, Tuple


def build_prefix(arr: List[int]) -> List[int]:
    """Inclusive prefix sums; prefix[i] = arr[0]+...+arr[i]."""
    n = len(arr)
    prefix = [0] * n
    if n == 0:
        return prefix
    prefix[0] = arr[0]
    for i in range(1, n):
        prefix[i] = prefix[i - 1] + arr[i]
    return prefix


def range_sum(prefix: List[int], l: int, r: int) -> int:
    """Sum of arr[l..r] using the prefix array, O(1)."""
    if l == 0:
        return prefix[r]
    return prefix[r] - prefix[l - 1]


def max_subarray_sum(arr: List[int]) -> int:
    """Kadane's algorithm — maximum contiguous subarray sum."""
    best = current = arr[0]
    for i in range(1, len(arr)):
        current = max(arr[i], current + arr[i])
        best = max(best, current)
    return best


def max_subarray_with_indices(arr: List[int]) -> Tuple[int, int, int]:
    """Returns (max_sum, start, end) — both inclusive."""
    best = current = arr[0]
    start = end = 0
    temp_start = 0
    for i in range(1, len(arr)):
        if arr[i] > current + arr[i]:
            current = arr[i]
            temp_start = i
        else:
            current += arr[i]
        if current > best:
            best = current
            start = temp_start
            end = i
    return best, start, end


def main() -> None:
    # --- Prefix Sum Demo ---
    arr = [3, -1, 2, 4, -3, 7]
    prefix = build_prefix(arr)
    print(f"Array:  {arr}")
    print(f"Prefix: {prefix}")
    print(f"Sum of arr[1..4] = {range_sum(prefix, 1, 4)}")  # 2
    print(f"Sum of arr[0..5] = {range_sum(prefix, 0, 5)}")  # 12
    print(f"Sum of arr[2..2] = {range_sum(prefix, 2, 2)}")  # 2

    # --- Kadane ---
    test1 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"\nArray: {test1}")
    print(f"Max subarray sum: {max_subarray_sum(test1)}")  # 6

    best, s, e = max_subarray_with_indices(test1)
    print(f"Max sum: {best} | Subarray: arr[{s}..{e}] = {test1[s:e+1]}")

    all_neg = [-5, -1, -8, -3]
    print(f"\nAll-negative: {all_neg}")
    print(f"Max sum: {max_subarray_sum(all_neg)}")          # -1

    single = [42]
    print(f"\nSingle element {single}: max sum = {max_subarray_sum(single)}")


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - `itertools.accumulate(arr)` is the standard-library prefix sum.
    - Tuple returns + unpacking replace the Java int[]{sum,start,end} idiom.
    - Slicing (`test1[s:e+1]`) is more readable than Arrays.copyOfRange.
    - max() in Python takes any number of arguments or an iterable.
"""
