"""
WEEK 25 - PYTHON ADVANCED DSA
Topic: KMP (Knuth-Morris-Pratt) Pattern Matching
File: 1.kmp.py

CONCEPT:
    Given a text T of length n and a pattern P of length m, find every
    index i in T where P occurs. Naive scanning costs O(n*m). KMP achieves
    O(n + m) by precomputing a "failure function" / LPS array on P so that
    after a partial match of length j fails, matching resumes at P[lps[j-1]]
    instead of restarting from P[0].

KEY POINTS:
    - lps[i] = length of the longest PROPER prefix of P[0..i] that is also
      a suffix of P[0..i].
    - The text pointer i never moves backwards -> linear-time guarantee.
    - To collect OVERLAPPING matches, on a full match set j = lps[j-1] and
      keep scanning instead of resetting j to 0.
    - Building lps is essentially KMP applied to the pattern against itself.

ALGORITHM / APPROACH:
    build_lps(P):
        length = 0; i = 1
        while i < m:
            if P[i] == P[length]: length += 1; lps[i] = length; i += 1
            elif length != 0:     length = lps[length - 1]   # fall back
            else:                 lps[i] = 0; i += 1

    search(T, P):
        lps = build_lps(P); i = j = 0
        while i < n:
            if T[i] == P[j]: i += 1; j += 1
            if j == m: report match at i-j; j = lps[j-1]
            elif i < n and T[i] != P[j]: j = lps[j-1] if j else 0; if j == 0: i += 1

PYTHON-SPECIFIC NOTES vs JAVA:
    - Strings are sequences; direct indexing s[i] returns a 1-char str.
    - lps is a regular list[int] initialised with [0] * m.
    - Results returned as list[int].

DRY RUN:
    P = "ABABCABAB" -> lps = [0,0,1,2,0,1,2,3,4]
    T = "ABABDABACDABABCABAB" -> single match at index 10.
    P = "AAA", T = "AAAAAA": lps = [0,1,2]; overlapping matches at [0,1,2,3].

COMPLEXITY:
    Time  : O(n + m)
    Space : O(m)
"""

from __future__ import annotations
from typing import List


def build_lps(pattern: str) -> List[int]:
    """Build the LPS / failure array. O(m)."""
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def search(text: str, pattern: str) -> List[int]:
    """Return all starting indices (including overlapping) of pattern in text."""
    n, m = len(text), len(pattern)
    if m == 0:
        return []
    lps = build_lps(pattern)
    results: List[int] = []
    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            results.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return results


def main() -> None:
    print("=== KMP Pattern Matching (Python) ===")
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    print(f"Text   : {text}")
    print(f"Pattern: {pattern}")
    print(f"LPS    : {build_lps(pattern)}")
    print(f"Matches: {search(text, pattern)}")  # [10]

    print("\n--- Overlapping matches ---")
    t2, p2 = "AAAAAA", "AAA"
    print(f"Text   : {t2}")
    print(f"Pattern: {p2}")
    print(f"Matches: {search(t2, p2)}")          # [0, 1, 2, 3]


if __name__ == "__main__":
    main()


# NOTES (vs Java baseline):
#     - Logic and control flow are identical to the Java version.
#     - Python's negative indexing is NOT used here; we keep semantics close to
#       Java to make line-by-line comparison easy.
#     - For very long patterns, consider str.find / re.finditer for production
#       use — they call into optimised C code (Boyer-Moore family).
