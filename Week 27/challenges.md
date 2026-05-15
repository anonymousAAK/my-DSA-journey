# Week 27 — Hard Mode Challenges (Boss Level)

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Convex Hull via Andrew's Monotone Chain

**Spec**:
Read `n` 2D integer points. Compute the convex hull and print its vertices in counter-clockwise order starting from the lowest-leftmost point. Required: Andrew's monotone chain in O(n log n). Use integer cross product (no floating-point comparisons) to determine turn direction. Handle collinear points: do not include intermediate collinear hull-edge points (i.e., strict convex hull).

**Constraints**:
- `1 <= n <= 10^6`, coordinates in `[-10^9, 10^9]`
- Time: O(n log n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| 4 corners of a square `(0,0)(0,1)(1,0)(1,1)` | `(0,0)(1,0)(1,1)(0,1)` |
| collinear `(0,0)(1,1)(2,2)(3,3)` | `(0,0)(3,3)` (degenerate, 2 points; or document a convention) |
| single point | itself |
| triangle | three vertices |

**Stretch**: Convex hull including collinear edge points; also dynamic convex hull (point insertions in amortized polylog).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Closest Pair of Points (Divide and Conquer)

**Spec**:
Read `n` 2D points. Print the distance between the closest pair and one such pair. Required: divide-and-conquer in O(n log n) — sort by x, recurse on halves, then check the strip of points within `δ` of the dividing line, sorted by y, with the "look at at most 7 next points" optimization. Brute O(n^2) and KD-tree solutions are forbidden.

**Constraints**:
- `2 <= n <= 10^6`
- Time: O(n log n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `(0,0)(1,1)(5,5)(10,10)` | distance `sqrt(2)`, pair `(0,0)(1,1)` |
| `(0,0)(3,4)(6,8)` | distance `5`, pair `(0,0)(3,4)` |
| two coincident points | distance `0` |

**Stretch**: Closest pair in higher dimensions (KD-tree expected O(n log n) for low dimensions).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Line Segment Intersection (Bentley–Ottmann Sweep)

**Spec**:
Read `n` 2D line segments. Print the number of distinct intersection points among them. Required: Bentley–Ottmann sweep in O((n + k) log n) where `k` = number of intersections. The O(n^2) all-pairs approach is forbidden for `n > 1000`.

**Constraints**:
- `1 <= n <= 10^5`, coordinates integer in `[-10^4, 10^4]`
- Time: O((n + k) log n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| two crossing segments `(0,0)-(2,2), (0,2)-(2,0)` | `1` |
| three concurrent (all pass through origin) | depends on counting rules — pick one |
| parallel segments | `0` |
| `n=4` forming an X and a separate X | `2` |

**Stretch**: Output the intersection coordinates exactly (rational arithmetic, avoiding floating-point).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Point in Polygon (Ray Casting + Winding Number)

**Spec**:
Read a simple polygon (vertices in order) and `q` query points. For each, print `IN`, `OUT`, or `ON_BOUNDARY`. Implement two methods and cross-check:
1. Ray casting (count edges crossed by a horizontal ray from the point).
2. Winding number (sum signed angles).

Handle degenerate cases (point on edge, ray hits a vertex) carefully.

**Constraints**:
- `3 <= n <= 10^5`, `q <= 10^5`, coords up to `10^9`
- Time: O((n + q) * log n) via preprocessing; O(n) per query naive
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| unit square `(0,0)(1,0)(1,1)(0,1)`, query `(0.5, 0.5)` | `IN` |
| same square, query `(0, 0.5)` | `ON_BOUNDARY` |
| same square, query `(2, 2)` | `OUT` |
| non-convex L-shape with query in the concavity | `OUT` |

**Stretch**: For a convex polygon, point-in-polygon in O(log n) per query via two binary searches over fans from one vertex.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: Polygon Area (Shoelace) + Centroid + Triangulation

**Spec**:
Read a simple polygon. Print: (a) its area via the shoelace formula, (b) its centroid (geometric center, weighted by area not by vertex count), (c) a fan triangulation from vertex 0 (a list of triangles by index). Use the signed area to determine orientation.

**Constraints**:
- `3 <= n <= 10^5`, coords integer up to `10^4`
- Time: O(n) for area/centroid; O(n) for triangulation
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| unit square `(0,0)(1,0)(1,1)(0,1)` | area `1.0`, centroid `(0.5, 0.5)`, triangles `(0,1,2)(0,2,3)` |
| right triangle `(0,0)(4,0)(0,3)` | area `6.0`, centroid `(4/3, 1)`, one triangle |
| L-shape (non-convex) | fan triangulation only works for convex polygons; use ear-clipping instead for stretch |

**Stretch**: Ear-clipping triangulation for non-convex (but still simple) polygons in O(n^2).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
