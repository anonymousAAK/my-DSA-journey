"""
WEEK 27 - PYTHON ADVANCED TOPICS
Topic: Line Segment Intersection
File: line_intersection.py

CONCEPT:
    Two segments AB and CD intersect (or touch) iff:
      1. The endpoints C, D lie on opposite sides of line AB (or one is on
         AB), AND
      2. The endpoints A, B lie on opposite sides of line CD (or one is on
         CD), AND
      3. (degenerate case) if all four are collinear, the projections of
         the segments onto x and y both overlap.

    Cross-product orientation test:
        ccw(p,q,r) = sign((q-p) x (r-p))
    encodes the three branches above with O(1) arithmetic.

KEY POINTS:
    - O(1) per query.
    - Returns the intersection point when it is unique (proper crossing).
    - Pure cross-product math; no division needed for the boolean test.
    - For computing the actual intersection point, parametrise one segment.

ALGORITHM / APPROACH:
    o1 = ccw(A, B, C); o2 = ccw(A, B, D)
    o3 = ccw(C, D, A); o4 = ccw(C, D, B)
    if signs(o1)!=signs(o2) and signs(o3)!=signs(o4): return True
    handle collinear sub-cases via on-segment tests
    intersection point: solve t along AB using cross ratios

PYTHON-SPECIFIC NOTES:
    - We return both a boolean and (when proper) the intersection point as
      a tuple of floats. The boolean is exact (integer math), the point
      conversion uses floating point for division.

DRY RUN / EXAMPLE:
    Segments (0,0)-(4,4) and (0,4)-(4,0): cross at (2,2). The orientation
    test gives o1>0,o2<0,o3>0,o4<0 -> proper intersection.

COMPLEXITY:
    Time:  O(1) per query.
    Space: O(1).
"""

from __future__ import annotations

from typing import Optional, Tuple

Point = Tuple[float, float]


def _ccw(p: Point, q: Point, r: Point) -> float:
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def _on_segment(p: Point, q: Point, r: Point) -> bool:
    """True if r lies on segment pq, assuming the three are collinear."""
    return (min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and
            min(p[1], q[1]) <= r[1] <= max(p[1], q[1]))


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    o1, o2, o3, o4 = _ccw(a, b, c), _ccw(a, b, d), _ccw(c, d, a), _ccw(c, d, b)
    if (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0):
        return True
    # Collinear / endpoint-on-segment cases
    if o1 == 0 and _on_segment(a, b, c): return True
    if o2 == 0 and _on_segment(a, b, d): return True
    if o3 == 0 and _on_segment(c, d, a): return True
    if o4 == 0 and _on_segment(c, d, b): return True
    return False


def line_intersection(a: Point, b: Point, c: Point, d: Point) -> Optional[Point]:
    """Return the intersection point of two infinite lines through AB and CD.

    Returns None if the lines are parallel.
    """
    denom = (a[0] - b[0]) * (c[1] - d[1]) - (a[1] - b[1]) * (c[0] - d[0])
    if denom == 0:
        return None
    t = ((a[0] - c[0]) * (c[1] - d[1]) - (a[1] - c[1]) * (c[0] - d[0])) / denom
    x = a[0] + t * (b[0] - a[0])
    y = a[1] + t * (b[1] - a[1])
    return (x, y)


def _demo() -> None:
    a, b = (0, 0), (4, 4)
    c, d = (0, 4), (4, 0)
    print(f"Segments {a}-{b} and {c}-{d} intersect: {segments_intersect(a, b, c, d)}")
    print(f"Intersection point: {line_intersection(a, b, c, d)}")

    # Parallel test
    e, f = (0, 0), (5, 0)
    g, h = (0, 1), (5, 1)
    print(f"Parallel segments intersect: {segments_intersect(e, f, g, h)}")
    print(f"Lines through them: {line_intersection(e, f, g, h)}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Java's geometry.java does not include explicit segment intersection,
#     so this file fills the spec gap.
#   * Python tuples make point arithmetic concise and hashable.
#   * Boolean intersection uses integer math when inputs are integral; only
#     line_intersection needs floating point division.
