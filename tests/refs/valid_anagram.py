"""Reference: anagram check via character frequency comparison."""

from __future__ import annotations
from collections import Counter


def isAnagram(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    return Counter(a) == Counter(b)
