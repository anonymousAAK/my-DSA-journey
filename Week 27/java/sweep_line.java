/*
 * WEEK 27 - JAVA ADVANCED TOPICS
 * Topic: Sweep Line -- Skyline & Maximum Interval Overlap
 * File: sweep_line.java
 *
 * CONCEPT:
 *     A sweep line is a conceptual vertical line that moves left to right
 *     across the plane, maintaining an ordered structure of "active"
 *     objects the line currently intersects. Events trigger insertions,
 *     removals, or queries. We illustrate two canonical problems:
 *       1. Skyline outline of overlapping rectangles (LC 218) using a
 *          max-heap of active heights.
 *       2. Maximum interval overlap (axis-parallel intervals) using
 *          +1 / -1 events.
 *
 * KEY POINTS:
 *     - Process events in sorted x order; tie-break carefully (close after
 *       open at the same x to avoid spurious gaps).
 *     - Active set is typically a balanced BST / heap; for axis-aligned
 *       problems often a counter or heap suffices.
 *     - Bentley-Ottmann achieves O((n+k) log n) for k segment intersections.
 *
 * ALGORITHM / APPROACH:
 *     SKYLINE:
 *       events: for each building (l, r, h) emit (l, -h, r) ["start"] and
 *               (r, 0, 0) ["end"]
 *       sort events
 *       max-heap of (-h, endX). On each event, push start; pop while top
 *       expired; record (x, curHeight) when curHeight changes.
 *     OVERLAP COUNT:
 *       events: (start, +1), (end, -1). Sort by (x, -delta) so opens
 *       process before closes at the same x. Running counter -> max.
 *
 * DRY RUN / EXAMPLE:
 *     Buildings = [(2,9,10),(3,7,15),(5,12,12),(15,20,10),(19,24,8)]
 *     Skyline   = [(2,10),(3,15),(7,12),(12,0),(15,10),(20,8),(24,0)]
 *     Intervals = [(1,5),(2,6),(3,4),(7,8)] -> max overlap = 3.
 *
 * COMPLEXITY:
 *     Time:  O(n log n).
 *     Space: O(n).
 */

// snake_case filename is fine; class SweepLine is package-private.

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

class SweepLine {

    /** LC 218 skyline. Returns list of {x, height} change points. */
    static List<int[]> skyline(int[][] buildings) {
        // Events: (x, heightDelta, endX). For starts heightDelta = -h, for
        // ends heightDelta = 0. Sorting (x asc, heightDelta asc) makes
        // starts precede ends at the same x and taller starts precede
        // shorter ones, matching the LeetCode reference behaviour.
        List<int[]> events = new ArrayList<>();
        for (int[] b : buildings) {
            events.add(new int[]{b[0], -b[2], b[1]});
            events.add(new int[]{b[1], 0, 0});
        }
        events.sort((a, c) -> a[0] != c[0] ? Integer.compare(a[0], c[0])
                                           : Integer.compare(a[1], c[1]));

        // Max-heap on height; second element is endX so we can lazy-expire.
        PriorityQueue<int[]> heap = new PriorityQueue<>(
            (a, c) -> Integer.compare(c[0], a[0]));
        heap.offer(new int[]{0, Integer.MAX_VALUE});

        List<int[]> result = new ArrayList<>();
        for (int[] ev : events) {
            int x = ev[0], delta = ev[1], r = ev[2];
            if (delta != 0) heap.offer(new int[]{-delta, r});
            while (heap.peek()[1] <= x) heap.poll();
            int curH = heap.peek()[0];
            if (result.isEmpty() || result.get(result.size() - 1)[1] != curH) {
                result.add(new int[]{x, curH});
            }
        }
        return result;
    }

    /** Maximum number of intervals overlapping at any single point. */
    static int maxOverlap(int[][] intervals) {
        int[][] events = new int[intervals.length * 2][2];
        int idx = 0;
        for (int[] iv : intervals) {
            events[idx++] = new int[]{iv[0], +1};
            events[idx++] = new int[]{iv[1], -1};
        }
        // Sort by x asc; at ties, opens (+1) come before closes (-1) so that
        // an interval that ends and another that starts at the same x both
        // count as overlapping. Reverse the secondary direction to model
        // half-open intervals instead.
        Arrays.sort(events, Comparator.<int[]>comparingInt(e -> e[0])
                                       .thenComparingInt(e -> -e[1]));
        int cur = 0, best = 0;
        for (int[] e : events) {
            cur += e[1];
            best = Math.max(best, cur);
        }
        return best;
    }

    public static void main(String[] args) {
        int[][] buildings = {{2, 9, 10}, {3, 7, 15}, {5, 12, 12},
                             {15, 20, 10}, {19, 24, 8}};
        System.out.print("Skyline:");
        for (int[] p : skyline(buildings))
            System.out.print(" (" + p[0] + "," + p[1] + ")");
        System.out.println();

        int[][] intervals = {{1, 5}, {2, 6}, {3, 4}, {7, 8}};
        System.out.println("Max overlap: " + maxOverlap(intervals));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in sweep_line.py:
 *   - Java needs an explicit PriorityQueue with a Comparator since
 *     heapq's negate-for-max trick isn't natural in Java.
 *   - We seed the heap with a sentinel (0, MAX_VALUE) so heap.peek() is
 *     always defined -- mirrors the Python (0, inf) seed.
 *   - Skyline result is List<int[]>; consumers can flatten to a 2D array.
 *   - geometry.java does not include sweep-line algorithms; this file
 *     adds them to mirror the Python split.
 */
