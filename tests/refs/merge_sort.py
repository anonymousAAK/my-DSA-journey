"""Reference: merge sort returning a new sorted list."""

from __future__ import annotations
from typing import List


def _merge(arr: List[int], left: int, mid: int, right: int) -> None:
    L = arr[left:mid + 1]
    R = arr[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1
    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1


def _msort(arr: List[int], left: int, right: int) -> None:
    if left >= right:
        return
    mid = left + (right - left) // 2
    _msort(arr, left, mid)
    _msort(arr, mid + 1, right)
    _merge(arr, left, mid, right)


def mergeSort(arr: List[int]) -> List[int]:
    a = list(arr)
    if a:
        _msort(a, 0, len(a) - 1)
    return a
