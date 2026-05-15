/*
 * WEEK 27 - JAVA ADVANCED TOPICS
 * Topic: Line / Segment Intersection
 * File: line_intersection.java
 *
 * CONCEPT:
 *     Two segments AB and CD intersect (or touch) iff:
 *       1. The endpoints C, D lie on opposite sides of line AB (or one is on
 *          AB), AND
 *       2. The endpoints A, B lie on opposite sides of line CD (or one is on
 *          CD), AND
 *       3. (degenerate) if all four are collinear, x- and y-projections of
 *          the two segments overlap.
 *
 *     The cross-product orientation test
 *         ccw(p, q, r) = sign((q-p) x (r-p))
 *     encodes the three branches above with O(1) arithmetic.
 *
 * KEY POINTS:
 *     - O(1) per query.
 *     - Returns the intersection point for the underlying infinite lines
 *       using the cross-ratio formula.
 *     - Pure cross-product math; division only needed for the actual point.
 *
 * ALGORITHM / APPROACH:
 *     o1 = ccw(A, B, C); o2 = ccw(A, B, D)
 *     o3 = ccw(C, D, A); o4 = ccw(C, D, B)
 *     if signs(o1) != signs(o2) and signs(o3) != signs(o4): proper intersect
 *     handle collinear sub-cases via on-segment tests
 *     line intersection point: solve t along AB with cross ratios
 *
 * DRY RUN / EXAMPLE:
 *     Segments (0,0)-(4,4) and (0,4)-(4,0): cross at (2,2).
 *     o1>0, o2<0, o3>0, o4<0 -> proper intersection.
 *     Parallel segments (0,0)-(5,0) and (0,1)-(5,1): no intersection.
 *
 * COMPLEXITY:
 *     Time:  O(1) per query.
 *     Space: O(1).
 */

// snake_case filename is fine; class LineIntersection is package-private.

class LineIntersection {

    static long ccw(long[] p, long[] q, long[] r) {
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]);
    }

    /** True if r lies on segment pq, assuming the three are collinear. */
    static boolean onSegment(long[] p, long[] q, long[] r) {
        return Math.min(p[0], q[0]) <= r[0] && r[0] <= Math.max(p[0], q[0]) &&
               Math.min(p[1], q[1]) <= r[1] && r[1] <= Math.max(p[1], q[1]);
    }

    static boolean segmentsIntersect(long[] a, long[] b, long[] c, long[] d) {
        long o1 = ccw(a, b, c), o2 = ccw(a, b, d);
        long o3 = ccw(c, d, a), o4 = ccw(c, d, b);
        if ((o1 > 0) != (o2 > 0) && (o3 > 0) != (o4 > 0)) return true;
        if (o1 == 0 && onSegment(a, b, c)) return true;
        if (o2 == 0 && onSegment(a, b, d)) return true;
        if (o3 == 0 && onSegment(c, d, a)) return true;
        if (o4 == 0 && onSegment(c, d, b)) return true;
        return false;
    }

    /** Intersection point of the infinite lines AB and CD; null if parallel. */
    static double[] lineIntersection(long[] a, long[] b, long[] c, long[] d) {
        double denom = (double)(a[0] - b[0]) * (c[1] - d[1])
                     - (double)(a[1] - b[1]) * (c[0] - d[0]);
        if (denom == 0.0) return null;
        double t = ((double)(a[0] - c[0]) * (c[1] - d[1])
                  - (double)(a[1] - c[1]) * (c[0] - d[0])) / denom;
        double x = a[0] + t * (b[0] - a[0]);
        double y = a[1] + t * (b[1] - a[1]);
        return new double[]{x, y};
    }

    public static void main(String[] args) {
        long[] a = {0, 0}, b = {4, 4};
        long[] c = {0, 4}, d = {4, 0};
        System.out.println("(0,0)-(4,4) and (0,4)-(4,0) intersect: " + segmentsIntersect(a, b, c, d));
        double[] p = lineIntersection(a, b, c, d);
        System.out.printf("Intersection point: (%.4f, %.4f)%n", p[0], p[1]);

        long[] e = {0, 0}, f = {5, 0};
        long[] g = {0, 1}, h = {5, 1};
        System.out.println("Parallel segments intersect: " + segmentsIntersect(e, f, g, h));
        System.out.println("Parallel lines intersection: " + (lineIntersection(e, f, g, h) == null ? "null" : "non-null"));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in line_intersection.py:
 *   - Java promotes coordinates to `long` to avoid 32-bit overflow on the
 *     cross product when coordinates are large.
 *   - Returns a `double[2]` instead of a Python tuple; null sentinel
 *     replaces Python's Optional[Point].
 *   - geometry.java does not include segment intersection; this file fills
 *     the gap mirroring the Python split.
 */
