"""
WEEK 25 - PYTHON ADVANCED DSA
Topic: Z-Algorithm for Pattern Matching
File: 3.z_algorithm.py

CONCEPT:
    For a string S of length n the Z-array satisfies:
        Z[0] = 0 (by convention)
        Z[i] = length of the longest substring starting at S[i] that is
               also a prefix of S.
    With Z computed in linear time, pattern matching reduces to building
    C = P + '$' + T (where '$' is a sentinel not in the alphabet) and
    reporting positions where Z[i] == |P|.

KEY POINTS:
    - Maintain the "Z-box" [l, r) = the right-most prefix match seen so far.
    - If i < r, we can BORROW: Z[i] = min(r - i, Z[i - l]) before extending.
    - Each character of S is involved in at most two comparisons -> O(n).
    - The sentinel '$' ensures Z[i] never exceeds |P| in the matching region.

ALGORITHM / APPROACH:
    z[0] = 0; l = r = 0
    for i in 1..n:
        if i < r: z[i] = min(r-i, z[i-l])
        while i+z[i] < n and s[z[i]] == s[i+z[i]]: z[i] += 1
        if i+z[i] > r: l = i; r = i+z[i]

    search(T, P): build C = P + '$' + T, compute Z(C),
                  return [i - |P| - 1 for i where Z[i] == |P|].

PYTHON-SPECIFIC NOTES vs JAVA:
    - Same control flow; Python's min() is a built-in.
    - String concatenation is cheap for short inputs; for huge inputs use
      io.StringIO or '$'.join(...) idioms.

DRY RUN:
    S = "aabxaab" -> Z = [0,1,0,0,3,1,0].
    Pattern "ABABCABAB" in "ABABDABACDABABCABAB":
        C = "ABABCABAB$ABABDABACDABABCABAB"; Z[20] = 9 -> match at i = 10.

COMPLEXITY:
    Time  : O(n + m)
    Space : O(n + m)
"""

from __future__ import annotations
from typing import List


def z_function(s: str) -> List[int]:
    n = len(s)
    if n == 0:
        return []
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def search(text: str, pattern: str) -> List[int]:
    if not pattern:
        return []
    concat = pattern + "$" + text
    z = z_function(concat)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(concat)) if z[i] == m]


def main() -> None:
    print("=== Z-Algorithm (Python) ===")
    demo = "aabxaab"
    print(f"String : {demo}")
    print(f"Z-array: {z_function(demo)}")          # [0, 1, 0, 0, 3, 1, 0]

    text, pattern = "ABABDABACDABABCABAB", "ABABCABAB"
    print(f"\nText   : {text}")
    print(f"Pattern: {pattern}")
    print(f"Matches: {search(text, pattern)}")     # [10]

    print("\n--- Overlapping matches ---")
    t2, p2 = "AAAAAA", "AAA"
    print(f"Text   : {t2}")
    print(f"Pattern: {p2}")
    print(f"Matches: {search(t2, p2)}")            # [0, 1, 2, 3]


if __name__ == "__main__":
    main()


# NOTES (vs Java baseline):
#     - Logic and indices match the Java implementation 1:1.
#     - Python tuple-assignment (l, r = i, i + z[i]) replaces two lines.
#     - The sentinel '$' assumes it does not appear in the alphabet of
#       (text + pattern). For binary data choose a byte outside the domain.
