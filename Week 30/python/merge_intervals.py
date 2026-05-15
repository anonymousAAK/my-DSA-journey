"""
WEEK 30 - PYTHON ADVANCED TOPICS
Topic: Merge Intervals Pattern
File: merge_intervals.py

CONCEPT:
    A family of problems where each input is an interval [start, end]:
    merge overlapping intervals, insert a new interval, count meeting
    rooms, check whether a person can attend all meetings, etc. The
    canonical step is sort by start and then a single pass.

KEY POINTS:
    - Sort by start (then by end as tie-breaker if needed).
    - For merging: keep a running "last" interval; if new.start <= last.end
      then extend last.end; else push new interval.
    - For insertion (when input is already sorted): do three passes
      (before / overlap / after) to avoid re-sorting.
    - For meeting rooms: separate sorted starts/ends, two-pointer scan; or
      min-heap of end times.

ALGORITHM / APPROACH:
    MERGE:
        sort by start
        result = [first]
        for each iv: if overlaps with result[-1]: extend; else: push
    INSERT:
        push intervals ending before newIv.start
        merge while overlapping; push merged
        push remaining
    MEETING ROOMS II:
        sorted starts / ends two-pointer; rooms_in_use peak

PYTHON-SPECIFIC NOTES:
    - Tuples (start, end) compare lexicographically by default — no
      custom comparator needed.

DRY RUN / EXAMPLE:
    merge [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]
    insert [[1,3],[6,9]] with [2,5] -> [[1,5],[6,9]]
    meeting rooms [[0,30],[5,10],[15,20]] -> 2

COMPLEXITY:
    Merge:        O(n log n) (sort) + O(n) scan.
    Insert:       O(n).
    Rooms count:  O(n log n).
"""

from __future__ import annotations

import heapq
from typing import List


def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda iv: iv[0])
    out: List[List[int]] = [intervals[0][:]]
    for s, e in intervals[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def insert_interval(intervals: List[List[int]], new_iv: List[int]) -> List[List[int]]:
    out: List[List[int]] = []
    n = len(intervals)
    i = 0
    while i < n and intervals[i][1] < new_iv[0]:
        out.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= new_iv[1]:
        new_iv = [min(new_iv[0], intervals[i][0]), max(new_iv[1], intervals[i][1])]
        i += 1
    out.append(new_iv)
    while i < n:
        out.append(intervals[i])
        i += 1
    return out


def min_meeting_rooms(intervals: List[List[int]]) -> int:
    """LC 253 — minimum number of rooms needed."""
    if not intervals:
        return 0
    starts = sorted(s for s, _ in intervals)
    ends   = sorted(e for _, e in intervals)
    rooms = busiest = 0
    j = 0
    for s in starts:
        if s < ends[j]:
            rooms += 1
            busiest = max(busiest, rooms)
        else:
            j += 1
    return busiest


def can_attend_all_meetings(intervals: List[List[int]]) -> bool:
    """LC 252 — can a single person attend every meeting?"""
    for a, b in zip(sorted(intervals), sorted(intervals)[1:]):
        if a[1] > b[0]:
            return False
    return True


def _demo() -> None:
    print(f"Merge {[[1,3],[2,6],[8,10],[15,18]]}: "
          f"{merge_intervals([[1,3],[2,6],[8,10],[15,18]])}")
    print(f"Insert [2,5] into [[1,3],[6,9]]: "
          f"{insert_interval([[1,3],[6,9]], [2,5])}")
    print(f"Min meeting rooms [[0,30],[5,10],[15,20]]: "
          f"{min_meeting_rooms([[0,30],[5,10],[15,20]])}")
    print(f"Can attend [[0,30],[5,10],[15,20]]: "
          f"{can_attend_all_meetings([[0,30],[5,10],[15,20]])}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Lists vs int[][]; same algorithms.
#   * Tuple/list sort uses Python's natural lexicographic order without a
#     custom comparator.
