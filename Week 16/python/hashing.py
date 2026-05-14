"""
Week 16: Hash Tables
=====================
Hash tables provide O(1) average-case lookup, insert, and delete by mapping
keys to array indices via a hash function.

Python's built-in dict and set are hash-table implementations (open addressing
with probing).  collections.Counter and collections.defaultdict are thin
wrappers that simplify common patterns.

Topics covered:
    1. two_sum (hash map approach)
    2. frequency_count
    3. group_anagrams
    4. subarray_with_zero_sum (prefix sum + set)
    5. subarray_sum_equals_k (prefix count map)
    6. longest_consecutive_sequence
    7. count_distinct_in_window (sliding window)
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# 1. Two Sum — hash map approach
# ---------------------------------------------------------------------------
def two_sum(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Return indices (i, j) such that nums[i] + nums[j] == target.
    Returns None if no solution exists.

    Strategy: for each element, check if (target - element) has already been
    seen.  Store seen values in a dict mapping value -> index.

    Time:  O(n) — single pass
    Space: O(n) — hash map of at most n entries
    """
    seen: Dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None


# ---------------------------------------------------------------------------
# 2. Frequency Count
# ---------------------------------------------------------------------------
def frequency_count(arr: List[int]) -> Dict[int, int]:
    """
    Return a dict mapping each element to its frequency.

    Time:  O(n)
    Space: O(n)
    """
    freq: Dict[int, int] = {}
    for val in arr:
        freq[val] = freq.get(val, 0) + 1
    return freq


def frequency_count_counter(arr: List[int]) -> Dict[int, int]:
    """Same as above but using collections.Counter (Pythonic shortcut)."""
    return dict(Counter(arr))


# ---------------------------------------------------------------------------
# 3. Group Anagrams
# ---------------------------------------------------------------------------
def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Group strings that are anagrams of each other.

    Key idea: two strings are anagrams iff they have the same sorted
    character tuple.  Use that tuple as a dict key.

    Time:  O(n * k log k)  where n = len(strs), k = max string length
           (sorting each string costs O(k log k))
    Space: O(n * k)
    """
    groups: Dict[tuple, List[str]] = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())


def group_anagrams_counting(strs: List[str]) -> List[List[str]]:
    """
    Alternate approach using character counts instead of sorting.

    Time:  O(n * k)  — avoids sorting each string
    Space: O(n * k)
    """
    groups: Dict[tuple, List[str]] = defaultdict(list)
    for s in strs:
        # 26-element tuple of character frequencies
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())


# ---------------------------------------------------------------------------
# 4. Subarray with Zero Sum (prefix sum + set)
# ---------------------------------------------------------------------------
def subarray_with_zero_sum(arr: List[int]) -> bool:
    """
    Determine whether *arr* contains a contiguous subarray that sums to 0.

    Key insight: if prefix_sum[i] == prefix_sum[j] for i < j, then
    arr[i+1..j] sums to 0.  Also, if any prefix_sum is 0, arr[0..i] sums to 0.

    Time:  O(n)
    Space: O(n)
    """
    seen = set()
    seen.add(0)  # handles case where prefix sum itself is 0
    prefix = 0
    for val in arr:
        prefix += val
        if prefix in seen:
            return True
        seen.add(prefix)
    return False


def find_zero_sum_subarray(arr: List[int]) -> Optional[Tuple[int, int]]:
    """
    Return (start, end) indices of a zero-sum subarray, or None.

    Time:  O(n)
    Space: O(n)
    """
    seen: Dict[int, int] = {0: -1}  # prefix_sum -> index
    prefix = 0
    for i, val in enumerate(arr):
        prefix += val
        if prefix in seen:
            return (seen[prefix] + 1, i)
        seen[prefix] = i
    return None


# ---------------------------------------------------------------------------
# 5. Subarray Sum Equals k (prefix count map)
# ---------------------------------------------------------------------------
def subarray_sum_equals_k(nums: List[int], k: int) -> int:
    """
    Count the number of contiguous subarrays whose sum equals *k*.

    For each index j we need the count of earlier indices i where
    prefix[j] - prefix[i] == k, i.e. prefix[i] == prefix[j] - k.
    We maintain a running count of each prefix sum seen so far.

    Time:  O(n)
    Space: O(n)
    """
    count = 0
    prefix = 0
    # Maps prefix_sum -> number of times this sum has occurred.
    prefix_counts: Dict[int, int] = defaultdict(int)
    prefix_counts[0] = 1  # empty prefix

    for num in nums:
        prefix += num
        # How many earlier prefixes equal (prefix - k)?
        count += prefix_counts[prefix - k]
        prefix_counts[prefix] += 1

    return count


# ---------------------------------------------------------------------------
# 6. Longest Consecutive Sequence
# ---------------------------------------------------------------------------
def longest_consecutive_sequence(nums: List[int]) -> int:
    """
    Find the length of the longest sequence of consecutive integers in *nums*.
    e.g. [100, 4, 200, 1, 3, 2] -> 4  (the sequence 1,2,3,4)

    Strategy:
        1. Put all numbers in a set for O(1) lookup.
        2. For each number that is the *start* of a sequence (i.e. num-1 not
           in the set), count how far the sequence extends.

    Time:  O(n) — each number is visited at most twice (once as a start,
                  once during extension).
    Space: O(n)
    """
    num_set = set(nums)
    best = 0

    for num in num_set:
        # Only start counting from the beginning of a sequence.
        if num - 1 not in num_set:
            current = num
            length = 1
            while current + 1 in num_set:
                current += 1
                length += 1
            best = max(best, length)

    return best


# ---------------------------------------------------------------------------
# 7. Count Distinct Elements in Every Window of Size k
# ---------------------------------------------------------------------------
def count_distinct_in_window(arr: List[int], k: int) -> List[int]:
    """
    For each window of size *k* in *arr*, return the count of distinct elements.

    Strategy: maintain a frequency map for the current window.
    - Slide the window by adding the new element and removing the oldest.
    - Track distinct count by checking when a frequency goes to 0 or from 0.

    Time:  O(n)
    Space: O(k) for the frequency map
    """
    if k <= 0 or k > len(arr):
        return []

    result: List[int] = []
    freq: Dict[int, int] = defaultdict(int)
    distinct = 0

    for i in range(len(arr)):
        # Add new element entering the window
        if freq[arr[i]] == 0:
            distinct += 1
        freq[arr[i]] += 1

        # Remove element leaving the window (once we've passed the first k elements)
        if i >= k:
            leaving = arr[i - k]
            freq[leaving] -= 1
            if freq[leaving] == 0:
                distinct -= 1

        # Record result once we have a full window
        if i >= k - 1:
            result.append(distinct)

    return result


# ===========================================================================
# Test Cases
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Week 16 — Hash Tables")
    print("=" * 60)

    # --- Two Sum -----------------------------------------------------------
    print("\n--- Two Sum ---")
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([3, 2, 4], 6) == (1, 2)
    assert two_sum([3, 3], 6) == (0, 1)
    assert two_sum([1, 2, 3], 10) is None
    print("two_sum([2,7,11,15], 9) =", two_sum([2, 7, 11, 15], 9))
    print("All two_sum tests passed.")

    # --- Frequency Count ---------------------------------------------------
    print("\n--- Frequency Count ---")
    assert frequency_count([1, 2, 2, 3, 3, 3]) == {1: 1, 2: 2, 3: 3}
    print("frequency_count([1,2,2,3,3,3]) =", frequency_count([1, 2, 2, 3, 3, 3]))

    # --- Group Anagrams ----------------------------------------------------
    print("\n--- Group Anagrams ---")
    groups = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    # Sort each group and the outer list for deterministic comparison.
    groups_sorted = sorted(sorted(g) for g in groups)
    expected = sorted([["ate", "eat", "tea"], ["bat"], ["nat", "tan"]])
    assert groups_sorted == expected, f"Got {groups_sorted}"
    print(f"group_anagrams result: {groups}")

    # --- Subarray with Zero Sum --------------------------------------------
    print("\n--- Subarray with Zero Sum ---")
    assert subarray_with_zero_sum([4, 2, -3, 1, 6]) is True   # [2,-3,1] sums to 0
    assert subarray_with_zero_sum([4, 2, 0, 1, 6]) is True    # [0] sums to 0
    assert subarray_with_zero_sum([1, 2, 3]) is False
    print("subarray_with_zero_sum([4,2,-3,1,6]) =", subarray_with_zero_sum([4, 2, -3, 1, 6]))

    indices = find_zero_sum_subarray([4, 2, -3, 1, 6])
    print(f"Zero-sum subarray indices in [4,2,-3,1,6]: {indices}")

    # --- Subarray Sum Equals k ---------------------------------------------
    print("\n--- Subarray Sum Equals k ---")
    assert subarray_sum_equals_k([1, 1, 1], 2) == 2
    assert subarray_sum_equals_k([1, 2, 3], 3) == 2  # [1,2] and [3]
    assert subarray_sum_equals_k([1], 0) == 0
    print("subarray_sum_equals_k([1,1,1], 2) =", subarray_sum_equals_k([1, 1, 1], 2))

    # --- Longest Consecutive Sequence --------------------------------------
    print("\n--- Longest Consecutive Sequence ---")
    assert longest_consecutive_sequence([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive_sequence([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive_sequence([]) == 0
    print("longest_consecutive_sequence([100,4,200,1,3,2]) =",
          longest_consecutive_sequence([100, 4, 200, 1, 3, 2]))

    # --- Count Distinct in Window ------------------------------------------
    print("\n--- Count Distinct in Sliding Window ---")
    assert count_distinct_in_window([1, 2, 1, 3, 4, 2, 3], 4) == [3, 4, 4, 3]
    assert count_distinct_in_window([1, 2, 4, 4], 2) == [2, 2, 1]
    print("count_distinct_in_window([1,2,1,3,4,2,3], k=4) =",
          count_distinct_in_window([1, 2, 1, 3, 4, 2, 3], 4))

    print("\nAll tests passed!")
