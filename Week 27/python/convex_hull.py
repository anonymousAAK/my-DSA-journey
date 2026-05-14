"""
WEEK 27 - PYTHON ADVANCED TOPICS
Topic: Convex Hull (Andrew's Monotone Chain)
File: convex_hull.py

CONCEPT:
    The convex hull of a finite set of points is the smallest convex polygon
    containing every point. Andrew's Monotone Chain sorts points lex (x then
    y) and builds the lower and upper hulls in two linear passes using a
    cross-product orientation test.

KEY POINTS:
    - Cross product:   (a-o) x (b-o) > 0 means counter-clockwise (left turn).
    - Pop from the hull while the new triple makes a right turn or is
      collinear (`<= 0`) to keep a strictly counter-clockwise hull.
    - Lower hull: left-to-right; upper hull: right-to-left; concatenate
      and drop the duplicated endpoints.
    - Foundational for many computational-geometry problems (diameter,
      width, smallest enclosing rectangle).

ALGORITHM / APPROACH:
    sort points lexicographically
    build lower hull: for each p, pop while last triple is non-CCW; append
    build upper hull: same, iterating in reverse
    return lower[:-1] + upper[:-1]

PYTHON-SPECIFIC NOTES:
    - Tuples (x, y) are hashable & sortable: use them directly.
    - List operations append/pop are O(1) amortised — perfect for a stack.
    - For numerical robustness use only integer arithmetic when inputs are
      integers (no floats, no overflow with Python's bigints).

DRY RUN / EXAMPLE:
    Points: [(0,0),(1,1),(2,2),(3,1),(0,3),(2,4)]
    Sorted: [(0,0),(0,3),(1,1),(2,2),(2,4),(3,1)]
    Lower hull -> [(0,0),(3,1)]  (the (1,1)/(2,2) collinear pts are popped)
    Upper hull -> [(3,1),(2,4),(0,3),(0,0)]
    Hull       -> [(0,0),(3,1),(2,4),(0,3)]

COMPLEXITY:
    Time:  O(n log n) — dominated by the sort.
    Space: O(n) for the hull.
"""

from __future__ import annotations

from typing import List, Tuple

Point = Tuple[float, float]


def cross(o: Point, a: Point, b: Point) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points: List[Point]) -> List[Point]:
    pts = sorted(set(points))
    if len(pts) < 2:
        return pts
    lower: List[Point] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: List[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _demo() -> None:
    pts = [(0, 0), (1, 1), (2, 2), (3, 1), (0, 3), (2, 4)]
    print("Convex hull:", convex_hull(pts))


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Python uses tuples for points; sorting is lexicographic by default.
#   * `sorted(set(points))` deduplicates which matters when input may have
#     repeated points; Java's `geometry.java` assumes distinct points.
#   * Pure-int / arbitrary-precision arithmetic eliminates overflow worries.
