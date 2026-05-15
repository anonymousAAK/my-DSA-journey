"""Reference: binary-search-on-answer (Koko eating bananas, LC 875)."""

from __future__ import annotations
from typing import List


def _can_finish(piles: List[int], h: int, speed: int) -> bool:
    hours = 0
    for pile in piles:
        hours += (pile + speed - 1) // speed
    return hours <= h


def minEatingSpeed(piles: List[int], h: int) -> int:
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if _can_finish(piles, h, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
