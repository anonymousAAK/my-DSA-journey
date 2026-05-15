/*
 * WEEK 27 - JAVA ADVANCED TOPICS
 * Topic: Closest Pair of Points (Divide & Conquer)
 * File: closest_pair.java
 *
 * CONCEPT:
 *     Given n points in the plane, find the minimum Euclidean distance
 *     between any two. Brute force is O(n^2). The classic divide-and-
 *     conquer algorithm sorts on x, recurses on each half, then examines
 *     a "strip" of width 2d around the dividing line.
 *
 * KEY POINTS:
 *     - Recursion base case (<= 3 points): brute-force pairwise.
 *     - Combine step: sort the strip by y; each point only needs to compare
 *       to the next few neighbours whose y-difference is < d (max 7).
 *     - O(n log n) total, O(n) auxiliary space.
 *
 * ALGORITHM / APPROACH:
 *     sort points by x
 *     def solve(l, r):
 *         if r - l <= 3: brute-force
 *         mid -> recurse left/right; d = min of the two
 *         build strip of points within d of the mid line; sort by y
 *         scan adjacent pairs while dy < d, update d
 *         return d
 *     closest = solve(0, n-1)
 *
 * DRY RUN / EXAMPLE:
 *     pts = (2,3),(12,30),(40,50),(5,1),(12,10),(3,4)
 *     sorted by x: (2,3),(3,4),(5,1),(12,10),(12,30),(40,50)
 *     left half closest: dist((2,3),(3,4)) = sqrt(2) ~= 1.4142
 *     right half closest: bigger.
 *     Final: 1.4142.
 *
 * COMPLEXITY:
 *     Time:  O(n log n) (with pre-sorted strip by y) -- worst-case
 *            O(n log^2 n) if we sort the strip every recurrence.
 *     Space: O(n).
 */

// snake_case filename is fine; class ClosestPair is package-private.

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class ClosestPair {

    static double dist(double[] a, double[] b) {
        return Math.hypot(a[0] - b[0], a[1] - b[1]);
    }

    static double solve(double[][] pts, int lo, int hi) {
        if (hi - lo < 3) {
            double best = Double.POSITIVE_INFINITY;
            for (int i = lo; i <= hi; i++)
                for (int j = i + 1; j <= hi; j++)
                    best = Math.min(best, dist(pts[i], pts[j]));
            return best;
        }
        int mid = (lo + hi) / 2;
        double midX = pts[mid][0];
        double d = Math.min(solve(pts, lo, mid), solve(pts, mid + 1, hi));

        List<double[]> strip = new ArrayList<>();
        for (int i = lo; i <= hi; i++)
            if (Math.abs(pts[i][0] - midX) < d) strip.add(pts[i]);
        strip.sort((a, b) -> Double.compare(a[1], b[1]));
        for (int i = 0; i < strip.size(); i++) {
            for (int j = i + 1; j < strip.size() && strip.get(j)[1] - strip.get(i)[1] < d; j++)
                d = Math.min(d, dist(strip.get(i), strip.get(j)));
        }
        return d;
    }

    static double closestPair(double[][] points) {
        if (points.length < 2) return Double.POSITIVE_INFINITY;
        double[][] pts = points.clone();
        Arrays.sort(pts, (a, b) -> Double.compare(a[0], b[0]));
        return solve(pts, 0, pts.length - 1);
    }

    /** O(n^2) brute-force reference. */
    static double closestPairBruteForce(double[][] points) {
        double best = Double.POSITIVE_INFINITY;
        int n = points.length;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                best = Math.min(best, dist(points[i], points[j]));
        return best;
    }

    public static void main(String[] args) {
        double[][] pts = {{2, 3}, {12, 30}, {40, 50}, {5, 1}, {12, 10}, {3, 4}};
        System.out.printf("Closest pair (D&C):         %.4f%n", closestPair(pts));
        System.out.printf("Closest pair (brute force): %.4f%n", closestPairBruteForce(pts));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in closest_pair.py:
 *   - Java uses double[] for points (Python tuples). Math.hypot is the
 *     numerically-stable Euclidean distance just like math.hypot.
 *   - The strip is a List<double[]>; Java's `sort` accepts a Comparator on
 *     double values via Double.compare.
 *   - Double.POSITIVE_INFINITY replaces math.inf / Double.MAX_VALUE.
 */
