"""
WEEK 27 - PYTHON ADVANCED TOPICS
Topic: Sweep Line - Bentley-Ottmann (intersection counting) and Skyline
File: sweep_line.py

CONCEPT:
    A sweep line is a conceptual vertical line that sweeps left to right
    across the plane, maintaining an ordered structure of "active" objects
    that the line currently intersects. Events trigger insertions, removals,
    or queries. Two showcase problems:
      1. Count overlapping segments (axis-parallel) using start/end events.
      2. Compute the city skyline outline of overlapping rectangles using a
         max-heap of active heights.

KEY POINTS:
    - Process events in sorted order by x (or by primary coordinate).
    - Active set is typically a balanced BST or heap; for axis-aligned
      problems often a counter or heap suffices.
    - Bentley-Ottmann achieves O((n+k) log n) for k segment intersections.

ALGORITHM / APPROACH:
    SKYLINE:
      events: for each building (l, r, h) emit (l, -h, r) for "start" and
              (r, 0, 0) for "end".
      sort events by (x, h)
      heap of (-h, end_x). Process events keeping current max height,
      append (x, h) to result when max changes.
    OVERLAP COUNT (axis-parallel intervals):
      events: (start, +1) (end, -1). Sort by x. Track running count and
      max overlap.

PYTHON-SPECIFIC NOTES:
    - `heapq` provides a binary min-heap; negate keys for max-heap behaviour.
    - `sorted` is stable, perfect for breaking ties on multiple sort keys.

DRY RUN / EXAMPLE:
    Buildings = [(2,9,10),(3,7,15),(5,12,12),(15,20,10),(19,24,8)]
    Skyline   = [(2,10),(3,15),(7,12),(12,0),(15,10),(20,8),(24,0)]

COMPLEXITY:
    Time:  O(n log n).
    Space: O(n).
"""

from __future__ import annotations

import heapq
from typing import List, Tuple


def skyline(buildings: List[Tuple[int, int, int]]) -> List[Tuple[int, int]]:
    """LeetCode 218: classic skyline problem via sweep + max-heap."""
    events: List[Tuple[int, int, int]] = []
    for l, r, h in buildings:
        events.append((l, -h, r))    # start
        events.append((r, 0, 0))     # end
    events.sort()

    result: List[Tuple[int, int]] = []
    heap: List[Tuple[int, int]] = [(0, float("inf"))]  # (-height, end_x)
    for x, neg_h, r in events:
        if neg_h:
            heapq.heappush(heap, (neg_h, r))
        # discard heap top while it is "expired" (end_x <= x)
        while heap[0][1] <= x:
            heapq.heappop(heap)
        cur_h = -heap[0][0]
        if not result or result[-1][1] != cur_h:
            result.append((x, cur_h))
    return result


def max_overlap(intervals: List[Tuple[int, int]]) -> int:
    """Maximum number of intervals overlapping at any single point."""
    events: List[Tuple[int, int]] = []
    for s, e in intervals:
        events.append((s, +1))
        events.append((e, -1))
    events.sort(key=lambda x: (x[0], -x[1]))  # close after opens at same x
    cur = best = 0
    for _, delta in events:
        cur += delta
        best = max(best, cur)
    return best


def _demo() -> None:
    print("Skyline:",
          skyline([(2, 9, 10), (3, 7, 15), (5, 12, 12), (15, 20, 10), (19, 24, 8)]))
    print("Max overlap:",
          max_overlap([(1, 5), (2, 6), (3, 4), (7, 8)]))


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Java's geometry.java does not include sweep-line algorithms. We add
#     two canonical examples (skyline and max overlap) here.
#   * heapq + tuple negation is Python's idiom for a max-heap.
#   * Sorting by composite tuple is a clean way to encode tie-breakers.
