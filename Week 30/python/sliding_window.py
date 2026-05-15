"""
WEEK 30 - PYTHON ADVANCED TOPICS
Topic: Sliding Window Pattern
File: sliding_window.py

CONCEPT:
    The sliding-window pattern processes contiguous subarrays / substrings
    by maintaining a window [left, right] that grows on the right and
    shrinks on the left as needed. Each element enters / leaves the window
    at most once, giving O(n) algorithms for problems otherwise O(n^2) or
    worse.

KEY POINTS:
    - Fixed-size window: slide by one each step, drop the outgoing left.
    - Variable-size window: grow right; shrink left while invariant violated.
    - Common state: counter / hash map / sum / max-deque.
    - Canonical problems: longest substring without repeats (LC 3), minimum
      window substring (LC 76), longest substring with at most k distinct
      characters (LC 340), maximum sliding window (LC 239).

ALGORITHM / APPROACH (variable size):
    left = 0
    for right in range(n):
        update window state with arr[right]
        while window invariant violated:
            remove arr[left] from state
            left += 1
        record best window so far

PYTHON-SPECIFIC NOTES:
    - `collections.Counter` and `collections.deque` are the natural state
      stores.
    - For maximum-in-window, use a monotonic-decreasing deque of indices.

DRY RUN / EXAMPLE:
    s = "abcabcbb" (LC 3): walk right; on first repeat reset left = idx+1;
    best length = 3 ("abc").
    Min window "ADOBECODEBANC" for "ABC" -> "BANC".

COMPLEXITY:
    Time:  O(n) for most variants.
    Space: O(charset) or O(window size).
"""

from __future__ import annotations

from collections import Counter, deque
from typing import List


def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}
    left = best = 0
    for right, c in enumerate(s):
        if c in last and last[c] >= left:
            left = last[c] + 1
        last[c] = right
        best = max(best, right - left + 1)
    return best


def min_window(s: str, t: str) -> str:
    if not t or len(s) < len(t):
        return ""
    need = Counter(t)
    required = len(need)
    formed = 0
    window: Counter[str] = Counter()
    left = best_left = 0
    best_len = float("inf")
    for right, c in enumerate(s):
        window[c] += 1
        if c in need and window[c] == need[c]:
            formed += 1
        while formed == required:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_left = left
            lc = s[left]
            window[lc] -= 1
            if lc in need and window[lc] < need[lc]:
                formed -= 1
            left += 1
    return "" if best_len == float("inf") else s[best_left:best_left + int(best_len)]


def longest_k_distinct(s: str, k: int) -> int:
    """Longest substring with at most k distinct characters (LC 340)."""
    if k == 0 or not s:
        return 0
    counts: Counter[str] = Counter()
    left = best = 0
    for right, c in enumerate(s):
        counts[c] += 1
        while len(counts) > k:
            counts[s[left]] -= 1
            if counts[s[left]] == 0:
                del counts[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best


def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """LC 239 - maximum in each window of size k via monotonic deque."""
    dq: deque[int] = deque()
    out: List[int] = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] == i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


def _demo() -> None:
    print(f"Longest unique 'abcabcbb': {length_of_longest_substring('abcabcbb')}")
    print(f"Min window 'ADOBECODEBANC','ABC': {min_window('ADOBECODEBANC', 'ABC')!r}")
    print(f"Longest 2-distinct 'eceba': {longest_k_distinct('eceba', 2)}")
    print(f"Max sliding window [1,3,-1,-3,5,3,6,7] k=3: "
          f"{max_sliding_window([1,3,-1,-3,5,3,6,7], 3)}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * collections.Counter replaces HashMap<Character, Integer>.
#   * deque is the idiomatic monotonic-deque for max-sliding-window.
#   * f-strings instead of String.format.
