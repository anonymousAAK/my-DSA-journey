"""
WEEK 16 - PYTHON DSA
Topic: Hashing Fundamentals + Classic HashMap Problems
File: 1.HashingAndHashMap.py

CONCEPT:
    Hashing maps a key to an array index using a hash function so that insert,
    lookup, and delete are all O(1) average. The mapping is one-way and aims
    for uniform distribution to keep collisions rare.

KEY POINTS:
    - Hash function must be deterministic, fast, and uniform.
    - Collisions are inevitable (pigeonhole principle); resolve by:
        * Chaining: each bucket is a linked list / dynamic array.
        * Open addressing: probe for next free slot (linear / quadratic / double).
    - Load factor alpha = n/m. When alpha > threshold (~0.66 for CPython dict),
      the table is resized and all keys are rehashed.
    - Python's built-in `dict` and `set` are highly optimized open-addressing
      hash tables backed by perturbation probing — average O(1), worst O(n).
    - `collections.Counter` is a `dict` subclass for frequency tables.
    - `collections.defaultdict(list)` gives "compute-if-absent" semantics.

ALGORITHM / APPROACH:
    For each problem, the recipe is:
        1. Pick a key that captures the invariant you care about.
           (e.g., complement value, sorted-letters tuple, prefix sum.)
        2. Look the key up in O(1); if present, derive the answer.
        3. Otherwise insert the key with whatever payload you'll need later.

PYTHON-SPECIFIC NOTES:
    - Use type hints from `typing` (`List`, `Dict`, etc.) or PEP 585 generics
      (`list[int]`).
    - Prefer `dict.get(key, default)` to `if key in d` + `d[key]` (one lookup).
    - `collections.Counter(iterable)` replaces Java's `merge(x, 1, sum)` loop.
    - `defaultdict(list)` replaces `computeIfAbsent(k, _ -> new ArrayList())`.
    - For anagram grouping, `tuple(sorted(s))` is a hashable key (strings work
      too: `''.join(sorted(s))`).
    - `set` membership test is O(1) average — exactly like Java HashSet.

DRY RUN:
    Example A — twoSum([2,7,11,15], target=9)
        i=0 nums[0]=2  complement=7  seen={}              -> add 2:0    seen={2:0}
        i=1 nums[1]=7  complement=2  seen={2:0} hit!      -> return [0,1]

    Example B — longestConsecutive([100,4,200,1,3,2])
        s = {100,4,200,1,3,2}
        Start at x=1 (since 0 not in s):  1->2->3->4   length=4
        Start at x=100 (since 99 not in s): length=1
        Start at x=200 (since 199 not in s): length=1
        Other elements (2,3,4) skipped because their predecessor IS in set.
        longest = 4

COMPLEXITY:
    twoSum                 O(n) time, O(n) space
    frequency              O(n) time, O(n) space
    groupAnagrams          O(n * k log k) time, O(n*k) space (k = max str len)
    hasZeroSumSubarray     O(n) time, O(n) space
    subarraySum            O(n) time, O(n) space
    longestConsecutive     O(n) time, O(n) space
"""

from __future__ import annotations
from collections import Counter, defaultdict
from typing import Dict, List, Tuple


# PROBLEM 1: Two Sum
def two_sum(nums: List[int], target: int) -> List[int]:
    """Return indices of the two numbers that sum to `target`, or [-1, -1]."""
    seen: Dict[int, int] = {}  # value -> index
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return [-1, -1]


# PROBLEM 2: Frequency Count
def frequency(arr: List[int]) -> Dict[int, int]:
    """Return a dict mapping each element to its number of occurrences."""
    return dict(Counter(arr))


# PROBLEM 3: Group Anagrams
def group_anagrams(strs: List[str]) -> List[List[str]]:
    """Group strings that are anagrams of each other."""
    groups: Dict[Tuple[str, ...], List[str]] = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # hashable canonical form
        groups[key].append(s)
    return list(groups.values())


# PROBLEM 4: Subarray With Zero Sum
def has_zero_sum_subarray(arr: List[int]) -> bool:
    """True if any contiguous subarray sums to zero."""
    prefix_sums = {0}  # empty prefix = sum 0
    running = 0
    for x in arr:
        running += x
        if running in prefix_sums:
            return True
        prefix_sums.add(running)
    return False


def subarray_sum(nums: List[int], k: int) -> int:
    """Count contiguous subarrays whose sum equals k."""
    counts: Dict[int, int] = defaultdict(int)
    counts[0] = 1
    running = 0
    total = 0
    for x in nums:
        running += x
        total += counts[running - k]
        counts[running] += 1
    return total


# PROBLEM 5: Longest Consecutive Sequence
def longest_consecutive(nums: List[int]) -> int:
    """Length of the longest run of consecutive integers in `nums`."""
    s = set(nums)
    best = 0
    for x in s:
        if (x - 1) not in s:           # only start from sequence beginnings
            length = 1
            while (x + length) in s:
                length += 1
            if length > best:
                best = length
    return best


def main() -> None:
    print("=== Two Sum ===")
    print(two_sum([2, 7, 11, 15], 9))   # [0, 1]
    print(two_sum([3, 2, 4], 6))        # [1, 2]

    print("\n=== Frequency Count ===")
    print(frequency([1, 3, 2, 3, 1, 1, 4]))  # {1: 3, 3: 2, 2: 1, 4: 1}

    print("\n=== Group Anagrams ===")
    for g in group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]):
        print(g)

    print("\n=== Subarray With Zero Sum ===")
    print(has_zero_sum_subarray([4, 2, -3, 1, 6]))   # True
    print(has_zero_sum_subarray([4, 2, 0, 1, 6]))    # True (0 alone)
    print(has_zero_sum_subarray([-3, 2, 3, 1, 6]))   # False

    print("\n=== Subarray Sum == k ===")
    print(subarray_sum([1, 1, 1], 2))                # 2
    print(subarray_sum([1, 2, 3], 3))                # 2

    print("\n=== Longest Consecutive Sequence ===")
    print(longest_consecutive([100, 4, 200, 1, 3, 2]))               # 4
    print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))       # 9


if __name__ == "__main__":
    main()


"""
NOTES (Python vs Java):
    - Java needs a ceremony of `new HashMap<>()` and `merge(key, 1, Integer::sum)`;
      Python uses `Counter` or `defaultdict(int)` directly.
    - Java arrays are not iterable with index by default; Python's `enumerate`
      gives us `(i, value)` pairs cleanly.
    - Java `String.toCharArray() + Arrays.sort + new String` is two lines and
      a temporary array; Python's `''.join(sorted(s))` (or `tuple(sorted(s))`
      if you need a hashable key) is a one-liner.
    - Java `HashSet` uses `.contains`; Python uses the `in` operator on `set`.
    - Python's dict/set raise `KeyError`/`KeyError` on missing keys, so
      `.get(k, default)` and `defaultdict` are idiomatic.
    - Counter has handy methods Java HashMap lacks: `.most_common(k)`,
      arithmetic (`Counter(a) + Counter(b)`), and intersection (`a & b`).
"""
