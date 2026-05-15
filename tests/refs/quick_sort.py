"""Reference: quicksort (Lomuto with randomised pivot) returning a sorted copy."""

from __future__ import annotations
import random
from typing import List

_rng = random.Random(42)


def _partition(arr: List[int], low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def _qs(arr: List[int], low: int, high: int) -> None:
    if low >= high:
        return
    pivot_idx = _rng.randint(low, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    p = _partition(arr, low, high)
    _qs(arr, low, p - 1)
    _qs(arr, p + 1, high)


def quickSort(arr: List[int]) -> List[int]:
    a = list(arr)
    if a:
        _qs(a, 0, len(a) - 1)
    return a
