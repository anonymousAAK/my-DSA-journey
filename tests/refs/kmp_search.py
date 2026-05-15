"""Reference: KMP all-occurrences string search."""

from __future__ import annotations
from typing import List


def _build_lps(pattern: str) -> List[int]:
    m = len(pattern)
    lps = [0] * m
    if m == 0:
        return lps
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmpSearch(text: str, pattern: str) -> List[int]:
    positions: List[int] = []
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return positions
    lps = _build_lps(pattern)
    i = j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return positions
