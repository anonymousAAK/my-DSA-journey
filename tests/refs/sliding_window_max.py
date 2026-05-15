"""Reference: maximum value in each sliding window of size k (LC 239)."""

from __future__ import annotations
from collections import deque
from typing import Deque, List


def slidingWindowMax(arr: List[int], k: int) -> List[int]:
    n = len(arr)
    if n == 0 or k == 0:
        return []
    result: List[int] = []
    dq: Deque[int] = deque()
    for i in range(n):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and arr[dq[-1]] < arr[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(arr[dq[0]])
    return result
