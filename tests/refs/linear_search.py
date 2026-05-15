"""Reference: linear search returning index of first occurrence or -1."""

from __future__ import annotations
from typing import List


def linearSearch(arr: List[int], target: int) -> int:
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1
