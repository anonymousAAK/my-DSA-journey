"""Reference: Dutch National Flag in-place partition of {0,1,2}.

Wrapped to return the sorted array so the harness can compare values rather
than rely on in-place mutation.
"""

from __future__ import annotations
from typing import List


def dutchFlag(arr: List[int]) -> List[int]:
    a = list(arr)
    low, mid, high = 0, 0, len(a) - 1
    while mid <= high:
        if a[mid] == 0:
            a[low], a[mid] = a[mid], a[low]
            low += 1
            mid += 1
        elif a[mid] == 1:
            mid += 1
        else:
            a[mid], a[high] = a[high], a[mid]
            high -= 1
    return a
