"""
WEEK 27 - PYTHON ADVANCED TOPICS
Topic: Closest Pair of Points (Divide & Conquer)
File: closest_pair.py

CONCEPT:
    Given n points in the plane, find the minimum Euclidean distance between
    any two. Brute force is O(n^2). The classic divide-and-conquer algorithm
    achieves O(n log n) by sorting on x, recursing on each half, then
    examining a "strip" of width 2d around the dividing line.

KEY POINTS:
    - Recursion base case: <= 3 points -> brute force.
    - Combine step: sort the strip by y; for each point only inspect the
      next few neighbours whose y-difference is < d (max 7 candidates).
    - O(n log n) total, O(n) auxiliary space.

ALGORITHM / APPROACH:
    sort points by x
    def solve(l, r):
        if r - l <= 3: brute-force
        mid -> recurse left and right; d = min of the two
        build strip of points within d of mid line; sort by y
        scan adjacent pairs in strip while dy < d
        return d
    closest = solve(0, n-1)

PYTHON-SPECIFIC NOTES:
    - We use math.hypot for Euclidean distance — numerically stable.
    - Sorting uses key=lambda; tuples compare lexicographically.

DRY RUN / EXAMPLE:
    pts = [(2,3),(12,30),(40,50),(5,1),(12,10),(3,4)]
    Sorted by x: [(2,3),(3,4),(5,1),(12,10),(12,30),(40,50)]
    Recurse left (4 pts) -> closest = dist((2,3),(3,4)) = sqrt(2) ~ 1.414
    Recurse right (3 pts) -> brute force ~ distance(12,10..12,30)=20 etc
    Strip combine -> still 1.414... Final answer: ~1.4142.

COMPLEXITY:
    Time:  O(n log n) — actually T(n)=2T(n/2)+O(n log n) without
           pre-sorting strip; with pre-sort by y we get true O(n log n).
    Space: O(n) for recursion + strip.
"""

from __future__ import annotations

import math
from typing import List, Tuple

Point = Tuple[float, float]


def _dist(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _solve(pts: List[Point], lo: int, hi: int) -> float:
    if hi - lo < 3:
        best = math.inf
        for i in range(lo, hi + 1):
            for j in range(i + 1, hi + 1):
                best = min(best, _dist(pts[i], pts[j]))
        return best
    mid = (lo + hi) // 2
    mid_x = pts[mid][0]
    d = min(_solve(pts, lo, mid), _solve(pts, mid + 1, hi))
    strip = [p for p in pts[lo:hi + 1] if abs(p[0] - mid_x) < d]
    strip.sort(key=lambda p: p[1])
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and strip[j][1] - strip[i][1] < d:
            d = min(d, _dist(strip[i], strip[j]))
            j += 1
    return d


def closest_pair(points: List[Point]) -> float:
    if len(points) < 2:
        return math.inf
    pts = sorted(points, key=lambda p: p[0])
    return _solve(pts, 0, len(pts) - 1)


def closest_pair_bruteforce(points: List[Point]) -> float:
    """O(n^2) reference implementation, useful for testing."""
    best = math.inf
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            best = min(best, _dist(points[i], points[j]))
    return best


def _demo() -> None:
    pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print(f"Closest pair (D&C):       {closest_pair(pts):.4f}")
    print(f"Closest pair (brute force): {closest_pair_bruteforce(pts):.4f}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Python uses math.hypot for numerically stable Euclidean distance.
#   * The strip is built with a list comprehension and sorted in-place.
#   * `math.inf` substitutes for Double.MAX_VALUE.
