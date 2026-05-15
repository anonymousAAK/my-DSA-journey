"""Reference: length of the longest substring without repeating characters (LC 3)."""

from __future__ import annotations


def longestUniqueSubstring(s: str) -> int:
    last: dict[str, int] = {}
    left = best = 0
    for right, c in enumerate(s):
        if c in last and last[c] >= left:
            left = last[c] + 1
        last[c] = right
        best = max(best, right - left + 1)
    return best
