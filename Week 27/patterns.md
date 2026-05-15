# Week 27 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which geometry pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given n ≤ 10^5 points in the plane, compute the convex hull (smallest convex polygon containing them).
Pattern: ______
Why: ______

### 2. Given n ≤ 10^5 points, find the two closest points.
Pattern: ______
Why: ______

### 3. Given n ≤ 10^5 axis-aligned line segments, count the number of intersection pairs.
Pattern: ______
Why: ______

### 4. Given n ≤ 10^5 axis-aligned rectangles, compute the total area of their union.
Pattern: ______
Why: ______

### 5. Given a simple polygon (n ≤ 10^5 vertices in order), compute its area.
Pattern: ______
Why: ______

### 6. Given a polygon and a query point, decide whether the point is inside the polygon.
Pattern: ______
Why: ______

### 7. Distractor: Given n ≤ 10^5 points, find the pair with maximum Euclidean distance. (Closest-pair algorithm?)
Pattern: ______
Why: ______

### 8. Given a set of segments, decide if any two of them intersect.
Pattern: ______
Why: ______

### 9. Given n ≤ 10^5 collinear points and m ≤ 10^5 query intervals on the line, count the number of points in each interval.
Pattern: ______
Why: ______

### 10. Given 3 points, decide whether they make a left turn, right turn, or are collinear.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Andrew's monotone chain (or Graham scan). **Why**: sort by x; build lower then upper hull using cross-product turn tests.
2. **Pattern**: Divide-and-conquer closest pair. **Why**: O(n log n) via split + strip merge.
3. **Pattern**: Sweep line with active set (BIT/BBST). **Why**: events at segment endpoints; count overlaps along the sweep.
4. **Pattern**: Sweep line + segment tree over coordinate-compressed y. **Why**: classic "Klee's measure" — vertical sweep accumulating covered length.
5. **Pattern**: Shoelace formula. **Why**: ½|Σ (x_i · y_{i+1} − x_{i+1} · y_i)|.
6. **Pattern**: Ray casting (count intersections with horizontal ray). **Why**: odd ⇒ inside.
7. **Pattern**: Convex hull diameter + rotating calipers. **Why**: max-distance pair lies on the hull — O(n log n).
8. **Pattern**: Bentley–Ottmann sweep line. **Why**: any-intersection detection in O((n+k) log n).
9. **Pattern**: Sort + binary search (or Fenwick if interleaved updates). **Why**: 1-D points in interval = `upper_bound − lower_bound`.
10. **Pattern**: Cross-product sign of `(p2-p1) × (p3-p1)`. **Why**: > 0 left, < 0 right, = 0 collinear — geometric primitive.

</details>
