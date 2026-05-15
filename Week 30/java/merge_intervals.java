/*
 * WEEK 30 - JAVA ADVANCED TOPICS
 * Topic: Merge Intervals Pattern
 * File: merge_intervals.java
 *
 * CONCEPT:
 *     A family of problems where each input is an interval [start, end]:
 *     merge overlapping intervals, insert a new interval, count meeting
 *     rooms, check whether a person can attend all meetings, etc. The
 *     canonical step is sort by start, then a single pass.
 *
 * KEY POINTS:
 *     - Sort by start (then by end as tie-breaker if needed).
 *     - Merging: maintain a running "last" interval; if new.start <= last.end
 *       extend last.end; else push new interval.
 *     - Insertion (already-sorted input): three passes (before / overlap /
 *       after) to avoid a re-sort.
 *     - Meeting rooms: sorted starts / ends two-pointer, or min-heap of end
 *       times.
 *
 * ALGORITHM / APPROACH:
 *     MERGE:
 *         sort by start
 *         result = [first]
 *         for each iv: if overlaps result[-1]: extend; else push
 *     INSERT:
 *         push intervals ending before newIv.start
 *         merge while overlapping; push merged
 *         push remaining
 *     MEETING ROOMS II:
 *         sorted starts/ends two-pointer; rooms_in_use peak
 *
 * DRY RUN / EXAMPLE:
 *     merge [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]
 *     insert [[1,3],[6,9]] with [2,5] -> [[1,5],[6,9]]
 *     meeting rooms [[0,30],[5,10],[15,20]] -> 2
 *
 * COMPLEXITY:
 *     Merge:        O(n log n) (sort) + O(n) scan.
 *     Insert:       O(n).
 *     Rooms count:  O(n log n).
 */

// snake_case filename is fine; class MergeIntervals is package-private.

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class MergeIntervals {

    static int[][] mergeIntervals(int[][] intervals) {
        if (intervals.length == 0) return new int[0][];
        int[][] sorted = intervals.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> merged = new ArrayList<>();
        merged.add(sorted[0].clone());
        for (int i = 1; i < sorted.length; i++) {
            int[] last = merged.get(merged.size() - 1);
            if (sorted[i][0] <= last[1]) last[1] = Math.max(last[1], sorted[i][1]);
            else merged.add(sorted[i].clone());
        }
        return merged.toArray(new int[0][]);
    }

    static int[][] insertInterval(int[][] intervals, int[] newIv) {
        List<int[]> out = new ArrayList<>();
        int n = intervals.length, i = 0;
        int[] iv = newIv.clone();
        while (i < n && intervals[i][1] < iv[0]) out.add(intervals[i++]);
        while (i < n && intervals[i][0] <= iv[1]) {
            iv[0] = Math.min(iv[0], intervals[i][0]);
            iv[1] = Math.max(iv[1], intervals[i][1]);
            i++;
        }
        out.add(iv);
        while (i < n) out.add(intervals[i++]);
        return out.toArray(new int[0][]);
    }

    /** LC 253 - minimum number of rooms needed. */
    static int minMeetingRooms(int[][] intervals) {
        if (intervals.length == 0) return 0;
        int n = intervals.length;
        int[] starts = new int[n], ends = new int[n];
        for (int i = 0; i < n; i++) { starts[i] = intervals[i][0]; ends[i] = intervals[i][1]; }
        Arrays.sort(starts);
        Arrays.sort(ends);
        int rooms = 0, best = 0, j = 0;
        for (int s : starts) {
            if (s < ends[j]) { rooms++; best = Math.max(best, rooms); }
            else j++;
        }
        return best;
    }

    /** LC 252 - can a single person attend every meeting? */
    static boolean canAttendAll(int[][] intervals) {
        if (intervals.length < 2) return true;
        int[][] sorted = intervals.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        for (int i = 1; i < sorted.length; i++) {
            if (sorted[i - 1][1] > sorted[i][0]) return false;
        }
        return true;
    }

    private static String fmt(int[][] arr) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < arr.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(Arrays.toString(arr[i]));
        }
        return sb.append("]").toString();
    }

    public static void main(String[] args) {
        System.out.println("Merge [[1,3],[2,6],[8,10],[15,18]]: "
            + fmt(mergeIntervals(new int[][]{{1, 3}, {2, 6}, {8, 10}, {15, 18}})));
        System.out.println("Insert [2,5] into [[1,3],[6,9]]: "
            + fmt(insertInterval(new int[][]{{1, 3}, {6, 9}}, new int[]{2, 5})));
        System.out.println("Min meeting rooms [[0,30],[5,10],[15,20]]: "
            + minMeetingRooms(new int[][]{{0, 30}, {5, 10}, {15, 20}}));
        System.out.println("Can attend [[0,30],[5,10],[15,20]]: "
            + canAttendAll(new int[][]{{0, 30}, {5, 10}, {15, 20}}));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in merge_intervals.py:
 *   - Python lists support natural lexicographic sort; Java needs explicit
 *     Comparator on a[0].
 *   - We clone() sub-arrays before mutating to keep the API non-destructive
 *     on caller-owned data.
 *   - The companion interview_patterns.java covers mergeIntervals and
 *     insertInterval; we add minMeetingRooms and canAttendAll for parity
 *     with the Python / C++ / Rust splits.
 */
