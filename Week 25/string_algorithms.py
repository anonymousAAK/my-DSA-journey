"""
Week 25: String Algorithms
===========================
This module covers fundamental string matching and pattern search algorithms.

Topics covered:
    1. KMP (Knuth-Morris-Pratt) Pattern Matching
    2. Rabin-Karp String Matching (rolling hash)
    3. Z-Algorithm for Pattern Matching

Each algorithm includes:
    - Problem statement
    - Step-by-step approach explanation
    - Time / space complexity analysis
    - Example usage via main driver
"""

from __future__ import annotations

from typing import List


# ---------------------------------------------------------------------------
# 1. KMP (Knuth-Morris-Pratt) Pattern Matching
# ---------------------------------------------------------------------------
# Problem:
#   Given a text T of length n and a pattern P of length m, find all
#   occurrences of P in T.
#
# Approach:
#   1. Build a "failure function" (also called the LPS — Longest Proper
#      Prefix which is also a Suffix — array) for the pattern.
#      lps[i] = length of the longest proper prefix of P[0..i] that is
#      also a suffix of P[0..i].
#   2. Scan the text with two pointers (i for text, j for pattern).
#      On a mismatch after j matches, we don't restart from scratch;
#      instead we set j = lps[j-1] and continue, skipping characters
#      we already know must match.
#
# Complexity:
#   Time  : O(n + m)  — linear in the combined length
#   Space : O(m)      — for the LPS array


def kmp_build_lps(pattern: str) -> List[int]:
    """
    Build the Longest Proper Prefix-Suffix (LPS) array for *pattern*.

    lps[i] is the length of the longest proper prefix of pattern[0..i]
    that is also a suffix of that substring.

    Time : O(m)
    Space: O(m)
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # length of the previous longest prefix-suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # Fall back — do NOT increment i
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Return a list of starting indices where *pattern* occurs in *text*
    using the Knuth-Morris-Pratt algorithm.

    Time : O(n + m)
    Space: O(m)
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return []

    lps = kmp_build_lps(pattern)
    results: List[int] = []

    i = 0  # index into text
    j = 0  # index into pattern

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:
            # Full match found at index i - j
            results.append(i - j)
            j = lps[j - 1]  # look for next overlapping match
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return results


# ---------------------------------------------------------------------------
# 2. Rabin-Karp String Matching
# ---------------------------------------------------------------------------
# Problem:
#   Same as above — find all occurrences of pattern P in text T — but
#   using a rolling hash to achieve expected linear time.
#
# Approach:
#   1. Compute the hash of the pattern and the hash of the first window
#      (length m) of the text.
#   2. Slide the window one character at a time.  At each step update the
#      hash in O(1) by removing the contribution of the outgoing character
#      and adding the incoming one.
#   3. When hashes match, verify character by character to rule out
#      spurious hits (hash collisions).
#
# Hash function used:
#   H(s) = (s[0]*d^(m-1) + s[1]*d^(m-2) + ... + s[m-1]) mod q
#   where d = 256 (alphabet size) and q is a large prime.
#
# Complexity:
#   Time  : O(n + m) expected, O(n*m) worst-case (many hash collisions)
#   Space : O(1) extra (besides the output list)


def rabin_karp_search(
    text: str,
    pattern: str,
    base: int = 256,
    prime: int = 101,
) -> List[int]:
    """
    Return a list of starting indices where *pattern* occurs in *text*
    using the Rabin-Karp rolling-hash algorithm.

    Parameters
    ----------
    base  : alphabet size (default 256 for extended ASCII)
    prime : a prime used for the modular hash to reduce collisions

    Time : O(n + m) expected
    Space: O(1) extra
    """
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []

    results: List[int] = []

    # h = base^(m-1) mod prime — used to remove the leading digit
    h = pow(base, m - 1, prime)

    # Compute initial hashes for pattern and first window of text
    p_hash = 0
    t_hash = 0
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % prime
        t_hash = (base * t_hash + ord(text[i])) % prime

    # Slide the window over the text
    for i in range(n - m + 1):
        # If hashes match, verify character by character
        if p_hash == t_hash:
            if text[i : i + m] == pattern:
                results.append(i)

        # Compute hash for the next window (if there is one)
        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            # Ensure non-negative
            if t_hash < 0:
                t_hash += prime

    return results


# ---------------------------------------------------------------------------
# 3. Z-Algorithm for Pattern Matching
# ---------------------------------------------------------------------------
# Problem:
#   Given a string S, compute the Z-array where Z[i] is the length of the
#   longest substring starting at index i that is also a prefix of S.
#   This can be used for pattern matching by constructing the string
#   P + '$' + T and checking where Z[i] == len(P).
#
# Approach:
#   Maintain a "Z-box" [l, r) — the interval of the rightmost substring
#   that matches a prefix.  For each new position i:
#     - If i < r, we can reuse previously computed information:
#       Z[i] = min(r - i, Z[i - l]).
#     - Then try to extend character by character.
#     - Update [l, r) if we extended past r.
#
# Complexity:
#   Time  : O(n)  — each character is compared at most twice
#   Space : O(n)  — for the Z-array


def z_function(s: str) -> List[int]:
    """
    Compute and return the Z-array for string *s*.

    Z[0] is defined as 0 (or len(s) by some conventions; here 0).
    Z[i] = length of the longest substring starting at s[i] that matches
    a prefix of s.

    Time : O(n)
    Space: O(n)
    """
    n = len(s)
    if n == 0:
        return []

    z = [0] * n
    l, r = 0, 0  # Z-box boundaries [l, r)

    for i in range(1, n):
        if i < r:
            # We are inside the current Z-box; reuse known info
            z[i] = min(r - i, z[i - l])

        # Try to extend the match
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1

        # Update the Z-box if we went past r
        if i + z[i] > r:
            l, r = i, i + z[i]

    return z


def z_search(text: str, pattern: str) -> List[int]:
    """
    Find all occurrences of *pattern* in *text* using the Z-algorithm.

    We build the concatenated string  pattern + '$' + text  and look for
    positions where Z[i] == len(pattern).

    Time : O(n + m)
    Space: O(n + m)
    """
    if not pattern:
        return []

    concat = pattern + "$" + text
    z = z_function(concat)
    m = len(pattern)

    results: List[int] = []
    for i in range(m + 1, len(concat)):
        if z[i] == m:
            results.append(i - m - 1)  # map back to text index

    return results


# ---------------------------------------------------------------------------
# Driver / demo
# ---------------------------------------------------------------------------

def main() -> None:
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"

    print("=" * 60)
    print("Week 25 — String Algorithms  (Python)")
    print("=" * 60)
    print(f"\nText   : {text}")
    print(f"Pattern: {pattern}\n")

    # KMP
    kmp_result = kmp_search(text, pattern)
    print(f"[KMP]        Matches at indices : {kmp_result}")

    # Rabin-Karp
    rk_result = rabin_karp_search(text, pattern)
    print(f"[Rabin-Karp] Matches at indices : {rk_result}")

    # Z-algorithm
    z_result = z_search(text, pattern)
    print(f"[Z-algo]     Matches at indices : {z_result}")

    # Additional example with overlapping matches
    print("\n--- Overlapping-match example ---")
    text2 = "AAAAAA"
    pattern2 = "AAA"
    print(f"Text   : {text2}")
    print(f"Pattern: {pattern2}")
    print(f"[KMP]        Matches at indices : {kmp_search(text2, pattern2)}")
    print(f"[Rabin-Karp] Matches at indices : {rabin_karp_search(text2, pattern2)}")
    print(f"[Z-algo]     Matches at indices : {z_search(text2, pattern2)}")

    # Z-array demo
    print("\n--- Z-array demo ---")
    demo = "aabxaab"
    print(f"String  : {demo}")
    print(f"Z-array : {z_function(demo)}")


if __name__ == "__main__":
    main()
