/*
 * WEEK 27 - JAVA ADVANCED TOPICS
 * Topic: Convex Hull (Andrew's Monotone Chain)
 * File: convex_hull.java
 *
 * CONCEPT:
 *     The convex hull of a finite set of points is the smallest convex
 *     polygon containing every point. Andrew's Monotone Chain sorts the
 *     points lexicographically (x then y) and builds the lower and upper
 *     hulls in two linear passes using a cross-product orientation test.
 *
 * KEY POINTS:
 *     - Cross product:  (a-o) x (b-o) > 0  means counter-clockwise turn.
 *     - Pop from the hull while the latest triple makes a right turn or is
 *       collinear (<= 0) to keep a strictly CCW hull.
 *     - Lower hull: left-to-right. Upper hull: right-to-left. Concatenate
 *       and drop the duplicated endpoints.
 *     - Foundational for diameter, width, smallest enclosing rectangle, etc.
 *
 * ALGORITHM / APPROACH:
 *     sort points lexicographically
 *     build lower: for each p, pop while last triple is non-CCW; append
 *     build upper: same, iterating in reverse
 *     return lower[:-1] + upper[:-1]
 *
 * DRY RUN / EXAMPLE:
 *     Points (0,0),(1,1),(2,2),(3,1),(0,3),(2,4):
 *     sorted: (0,0),(0,3),(1,1),(2,2),(2,4),(3,1)
 *     lower hull -> (0,0),(3,1)
 *     upper hull -> (3,1),(2,4),(0,3),(0,0)
 *     hull       -> (0,0),(3,1),(2,4),(0,3)
 *
 * COMPLEXITY:
 *     Time:  O(n log n) -- dominated by the sort.
 *     Space: O(n).
 */

// snake_case filename is fine; class ConvexHull is package-private.

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class ConvexHull {

    /** 2D cross product of (a-o) and (b-o); long arithmetic avoids overflow. */
    static long cross(long[] o, long[] a, long[] b) {
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
    }

    /** Returns the counter-clockwise hull vertices, no duplicated endpoint. */
    static List<long[]> convexHull(long[][] points) {
        int n = points.length;
        long[][] pts = points.clone();
        Arrays.sort(pts, (a, b) -> a[0] != b[0] ? Long.compare(a[0], b[0])
                                                : Long.compare(a[1], b[1]));
        // Deduplicate
        List<long[]> uniq = new ArrayList<>();
        for (long[] p : pts) {
            if (uniq.isEmpty() || uniq.get(uniq.size() - 1)[0] != p[0]
                               || uniq.get(uniq.size() - 1)[1] != p[1]) uniq.add(p);
        }
        if (uniq.size() < 2) return new ArrayList<>(uniq);

        List<long[]> lower = new ArrayList<>();
        for (long[] p : uniq) {
            while (lower.size() >= 2 &&
                   cross(lower.get(lower.size() - 2), lower.get(lower.size() - 1), p) <= 0)
                lower.remove(lower.size() - 1);
            lower.add(p);
        }
        List<long[]> upper = new ArrayList<>();
        for (int i = uniq.size() - 1; i >= 0; i--) {
            long[] p = uniq.get(i);
            while (upper.size() >= 2 &&
                   cross(upper.get(upper.size() - 2), upper.get(upper.size() - 1), p) <= 0)
                upper.remove(upper.size() - 1);
            upper.add(p);
        }
        List<long[]> hull = new ArrayList<>();
        for (int i = 0; i < lower.size() - 1; i++) hull.add(lower.get(i));
        for (int i = 0; i < upper.size() - 1; i++) hull.add(upper.get(i));
        if (n == 1) hull.add(uniq.get(0));
        return hull;
    }

    public static void main(String[] args) {
        long[][] pts = {{0, 0}, {1, 1}, {2, 2}, {3, 1}, {0, 3}, {2, 4}};
        List<long[]> hull = convexHull(pts);
        System.out.print("Convex hull:");
        for (long[] p : hull) System.out.print(" (" + p[0] + "," + p[1] + ")");
        System.out.println();
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in convex_hull.py:
 *   - Java uses long[] points to avoid overflow in the cross product; Python
 *     uses arbitrary-precision ints automatically.
 *   - Manual deduplication step replaces Python's `sorted(set(points))`.
 *   - The geometry.java overview file uses int[] with cast-to-long inside
 *     cross; we promote to long[] here for safety on large coordinates.
 */
