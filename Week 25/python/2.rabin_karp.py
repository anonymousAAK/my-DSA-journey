"""
WEEK 25 - PYTHON ADVANCED DSA
Topic: Rabin-Karp String Matching (rolling hash)
File: 2.rabin_karp.py

CONCEPT:
    Compare every length-m window of T to P via a numeric fingerprint
    instead of a character-by-character comparison. With a hash that can
    be updated incrementally in O(1) as the window slides, expected
    runtime is O(n + m). On hash hits we verify literally to guard against
    collisions.

KEY POINTS:
    - Polynomial rolling hash modulo a prime:
          H(s) = (s[0]*B^(m-1) + s[1]*B^(m-2) + ... + s[m-1]) mod Q
      with B = alphabet base and Q a prime.
    - Update: t_hash = (B * (t_hash - T[i]*h) + T[i+m]) mod Q,
      where h = B^(m-1) mod Q (precomputed once).
    - Always verify on hash match — collisions exist.
    - Worst case O(n*m) for pathological inputs; expected O(n+m).

ALGORITHM / APPROACH:
    1. h = pow(B, m-1, Q)
    2. Compute p_hash for P and t_hash for T[0..m-1]
    3. For i in 0..n-m:
           if p_hash == t_hash and T[i:i+m] == P: report i
           t_hash = (B * (t_hash - ord(T[i])*h) + ord(T[i+m])) % Q

PYTHON-SPECIFIC NOTES vs JAVA:
    - ord(c) gives the integer code point.
    - Use pow(base, m-1, prime) for fast modular exponent.
    - Python ints are arbitrary precision so we don't need explicit `long`.

DRY RUN:
    P = "AAA", T = "AAAAAA", B = 256, Q = 101 (small for demo).
    h = pow(256, 2, 101). p_hash and the first window hash coincide;
    sliding by one keeps the fingerprint identical (same character codes),
    so matches are reported at [0, 1, 2, 3].

COMPLEXITY:
    Time  : O(n + m) expected, O(n*m) worst-case.
    Space : O(1) extra besides the output list.
"""

from __future__ import annotations
from typing import List


def search(text: str, pattern: str, base: int = 256, prime: int = 1_000_000_007) -> List[int]:
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []

    h = pow(base, m - 1, prime)
    p_hash = 0
    t_hash = 0
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % prime
        t_hash = (base * t_hash + ord(text[i]))    % prime

    results: List[int] = []
    for i in range(n - m + 1):
        if p_hash == t_hash and text[i : i + m] == pattern:
            results.append(i)
        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t_hash < 0:
                t_hash += prime
    return results


def main() -> None:
    print("=== Rabin-Karp Pattern Matching (Python) ===")
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    print(f"Text   : {text}")
    print(f"Pattern: {pattern}")
    print(f"Matches: {search(text, pattern)}")    # [10]

    print("\n--- Overlapping matches ---")
    t2, p2 = "AAAAAA", "AAA"
    print(f"Text   : {t2}")
    print(f"Pattern: {p2}")
    print(f"Matches: {search(t2, p2)}")           # [0, 1, 2, 3]


if __name__ == "__main__":
    main()


# NOTES (vs Java baseline):
#     - Python's arbitrary-precision int removes Java's `long` cast concerns.
#     - ord() replaces Java's implicit char->int promotion.
#     - For very long patterns consider double-hashing (two (B,Q) pairs) to
#       reduce collision probability further.
