"""Reference: Rabin-Karp all-occurrence search returning sorted positions."""

from __future__ import annotations
from typing import List


def rabinKarpSearch(text: str, pattern: str,
                    base: int = 256, prime: int = 1_000_000_007) -> List[int]:
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []

    h = pow(base, m - 1, prime)
    p_hash = 0
    t_hash = 0
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % prime
        t_hash = (base * t_hash + ord(text[i])) % prime

    results: List[int] = []
    for i in range(n - m + 1):
        if p_hash == t_hash and text[i:i + m] == pattern:
            results.append(i)
        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t_hash < 0:
                t_hash += prime
    return results
