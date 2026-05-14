"""
Week 6 — Arrays
=================
Topics covered:
  - Reverse array in-place (two pointers)
  - Rotate array by k positions (reversal algorithm)
  - Prefix sum array + range sum query
  - Kadane's algorithm (max subarray sum with start/end indices)
  - Dutch National Flag — sort 0s, 1s, 2s in one pass
  - Find missing number (sum approach + XOR approach)
  - Find duplicate (Floyd's cycle detection on index mapping)

Each function includes time/space complexity analysis in its docstring.
"""

from __future__ import annotations

from typing import List, Tuple


# ---------------------------------------------------------------------------
# Reverse Array In-Place
# ---------------------------------------------------------------------------

def reverse_array(arr: List[int]) -> List[int]:
    """Reverse *arr* in-place using two converging pointers.

    Time:  O(n)
    Space: O(1)
    """
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr


# ---------------------------------------------------------------------------
# Rotate Array
# ---------------------------------------------------------------------------

def rotate_array(arr: List[int], k: int) -> List[int]:
    """Rotate *arr* to the right by *k* positions using the reversal algorithm.

    Example: [1,2,3,4,5], k=2  →  [4,5,1,2,3]

    Algorithm:
      1. Reverse the whole array.
      2. Reverse the first k elements.
      3. Reverse the remaining n-k elements.

    Time:  O(n)
    Space: O(1)
    """
    n = len(arr)
    if n == 0:
        return arr
    k %= n  # handle k > n

    def _reverse(lo: int, hi: int) -> None:
        while lo < hi:
            arr[lo], arr[hi] = arr[hi], arr[lo]
            lo += 1
            hi -= 1

    _reverse(0, n - 1)
    _reverse(0, k - 1)
    _reverse(k, n - 1)
    return arr


# ---------------------------------------------------------------------------
# Prefix Sum & Range Sum Query
# ---------------------------------------------------------------------------

def build_prefix_sum(arr: List[int]) -> List[int]:
    """Build a prefix-sum array where prefix[i] = sum(arr[0..i-1]).

    prefix[0] = 0  (empty prefix)
    prefix[i] = prefix[i-1] + arr[i-1]

    Time:  O(n)
    Space: O(n)
    """
    prefix = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix


def range_sum(prefix: List[int], left: int, right: int) -> int:
    """Return sum(arr[left..right]) inclusive using a precomputed prefix array.

    Time:  O(1) per query  (after O(n) preprocessing)
    Space: O(1)
    """
    return prefix[right + 1] - prefix[left]


# ---------------------------------------------------------------------------
# Kadane's Algorithm — Maximum Subarray Sum with Indices
# ---------------------------------------------------------------------------

def kadane(arr: List[int]) -> Tuple[int, int, int]:
    """Return (max_sum, start_index, end_index) of the maximum subarray.

    Kadane's algorithm maintains a running sum and resets it whenever
    starting fresh yields a higher value.

    Time:  O(n)
    Space: O(1)
    """
    if not arr:
        return (0, -1, -1)

    max_sum = current_sum = arr[0]
    start = end = temp_start = 0

    for i in range(1, len(arr)):
        if current_sum + arr[i] < arr[i]:
            # Better to start a new subarray at i
            current_sum = arr[i]
            temp_start = i
        else:
            current_sum += arr[i]

        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i

    return (max_sum, start, end)


# ---------------------------------------------------------------------------
# Dutch National Flag — Sort 0s, 1s, 2s
# ---------------------------------------------------------------------------

def dutch_national_flag(arr: List[int]) -> List[int]:
    """Sort an array containing only 0, 1, 2 in a single pass (3-way partition).

    Three pointers:
      - low  : boundary for 0s (everything before low is 0)
      - mid  : current element under inspection
      - high : boundary for 2s (everything after high is 2)

    Time:  O(n)
    Space: O(1)
    """
    low = mid = 0
    high = len(arr) - 1

    while mid <= high:
        if arr[mid] == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else:  # arr[mid] == 2
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
            # Don't advance mid — the swapped element needs inspection

    return arr


# ---------------------------------------------------------------------------
# Find Missing Number
# ---------------------------------------------------------------------------

def missing_number_sum(nums: List[int]) -> int:
    """Find the missing number in [0..n] using the sum formula.

    Given an array of n distinct numbers from the range [0, n],
    exactly one number is missing.

    Time:  O(n)
    Space: O(1)
    """
    n = len(nums)
    expected = n * (n + 1) // 2
    return expected - sum(nums)


def missing_number_xor(nums: List[int]) -> int:
    """Find the missing number in [0..n] using XOR.

    XOR of a number with itself is 0, so XOR all indices and values:
    the unpaired one is the missing number.

    Time:  O(n)
    Space: O(1)
    """
    xor = len(nums)  # start with n (the last index value)
    for i, v in enumerate(nums):
        xor ^= i ^ v
    return xor


# ---------------------------------------------------------------------------
# Find Duplicate — Floyd's Cycle Detection
# ---------------------------------------------------------------------------

def find_duplicate(nums: List[int]) -> int:
    """Find the one duplicate in an array of n+1 integers in range [1, n].

    Uses Floyd's tortoise-and-hare cycle detection treating the array as
    an implicit linked list where nums[i] is the 'next' pointer.

    Time:  O(n)
    Space: O(1)
    """
    # Phase 1: detect cycle (find meeting point)
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: find the entrance to the cycle (the duplicate value)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ---- Reverse ----
    assert reverse_array([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]
    assert reverse_array([]) == []
    assert reverse_array([42]) == [42]
    print("[PASS] Reverse array in-place")

    # ---- Rotate ----
    assert rotate_array([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
    assert rotate_array([1, 2, 3], 0) == [1, 2, 3]
    assert rotate_array([1, 2, 3], 3) == [1, 2, 3]
    print("[PASS] Rotate array (reversal algorithm)")

    # ---- Prefix Sum ----
    a = [2, 4, 6, 8, 10]
    ps = build_prefix_sum(a)
    assert range_sum(ps, 0, 4) == 30
    assert range_sum(ps, 1, 3) == 18  # 4 + 6 + 8
    assert range_sum(ps, 2, 2) == 6
    print("[PASS] Prefix sum + range sum query")

    # ---- Kadane ----
    max_s, s, e = kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    assert max_s == 6  # subarray [4, -1, 2, 1]
    assert (s, e) == (3, 6)
    assert kadane([5])[0] == 5
    assert kadane([-1, -2, -3])[0] == -1
    print("[PASS] Kadane's algorithm (max subarray with indices)")

    # ---- Dutch National Flag ----
    assert dutch_national_flag([2, 0, 1, 2, 0, 1, 0]) == [0, 0, 0, 1, 1, 2, 2]
    assert dutch_national_flag([0]) == [0]
    assert dutch_national_flag([2, 1, 0]) == [0, 1, 2]
    print("[PASS] Dutch National Flag")

    # ---- Missing Number ----
    for fn in (missing_number_sum, missing_number_xor):
        assert fn([3, 0, 1]) == 2
        assert fn([0, 1]) == 2
        assert fn([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
    print("[PASS] Missing number (sum & XOR)")

    # ---- Find Duplicate ----
    assert find_duplicate([1, 3, 4, 2, 2]) == 2
    assert find_duplicate([3, 1, 3, 4, 2]) == 3
    print("[PASS] Find duplicate (Floyd's cycle detection)")

    print("\nAll Week 6 tests passed!")
