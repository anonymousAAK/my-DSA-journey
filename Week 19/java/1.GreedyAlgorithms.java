/*
 * WEEK 19 - GREEDY ALGORITHMS
 * Topic: Greedy Paradigm + Classic Problems
 *
 * GREEDY STRATEGY:
 * At each step, make the locally optimal choice.
 * Hope that local optimum leads to global optimum.
 *
 * WHEN DOES GREEDY WORK?
 * The problem must have:
 * 1. GREEDY CHOICE PROPERTY: A global optimum can be reached by making locally optimal choices.
 * 2. OPTIMAL SUBSTRUCTURE: Optimal solution contains optimal solutions to subproblems.
 *
 * PROVING CORRECTNESS:
 * - Exchange argument: Show swapping greedy choice with any other choice doesn't improve the solution.
 * - Induction on greedy choices.
 *
 * PROBLEMS COVERED:
 * 1. Activity Selection (maximum non-overlapping intervals)
 * 2. Fractional Knapsack
 * 3. Minimum Number of Coins (canonical coin systems)
 * 4. Job Sequencing with Deadlines
 * 5. Merge Intervals
 *
 * IMPORTANT: Greedy DOESN'T always work! (e.g., 0/1 Knapsack needs DP)
 */

import java.util.*;

public class GreedyAlgorithms {

    // PROBLEM 1: Activity Selection
    // Given activities with start/end times, select maximum non-overlapping activities.
    // GREEDY: Always pick the activity that ENDS earliest.
    // Time: O(n log n) for sorting
    static int activitySelection(int[] start, int[] end) {
        int n = start.length;
        // Sort by end time
        Integer[] idx = new Integer[n];
        for (int i = 0; i < n; i++) idx[i] = i;
        Arrays.sort(idx, (a, b) -> end[a] - end[b]);

        int count = 1;
        int lastEnd = end[idx[0]];
        for (int i = 1; i < n; i++) {
            if (start[idx[i]] >= lastEnd) {
                count++;
                lastEnd = end[idx[i]];
            }
        }
        return count;
    }

    // PROBLEM 2: Fractional Knapsack
    // Can take fractions of items. Greedy: take by highest value/weight ratio.
    // Time: O(n log n)
    static double fractionalKnapsack(int[] weights, int[] values, int W) {
        int n = weights.length;
        Integer[] idx = new Integer[n];
        for (int i = 0; i < n; i++) idx[i] = i;
        // Sort by value/weight ratio (descending)
        Arrays.sort(idx, (a, b) -> Double.compare((double)values[b]/weights[b], (double)values[a]/weights[a]));

        double totalValue = 0;
        int remaining = W;
        for (int i : idx) {
            if (remaining <= 0) break;
            int take = Math.min(weights[i], remaining);
            totalValue += take * (double)values[i] / weights[i];
            remaining -= take;
        }
        return totalValue;
    }

    // PROBLEM 3: Minimum coins (standard greedy — works for canonical systems like USD)
    // NOTE: Greedy FAILS for non-canonical coin systems (e.g., {1,3,4} for target=6: greedy gives 4+1+1=3, DP gives 3+3=2)
    static Map<Integer, Integer> minCoinsGreedy(int[] coins, int target) {
        Arrays.sort(coins);
        Map<Integer, Integer> result = new LinkedHashMap<>();
        for (int i = coins.length - 1; i >= 0 && target > 0; i--) {
            if (coins[i] <= target) {
                int count = target / coins[i];
                result.put(coins[i], count);
                target -= coins[i] * count;
            }
        }
        return result;
    }

    // PROBLEM 4: Merge Intervals
    // Given list of intervals, merge all overlapping ones.
    // Time: O(n log n)
    static int[][] mergeIntervals(int[][] intervals) {
        if (intervals.length <= 1) return intervals;
        Arrays.sort(intervals, (a, b) -> a[0] - b[0]); // sort by start
        List<int[]> merged = new ArrayList<>();
        int[] current = intervals[0];
        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] <= current[1]) { // overlapping
                current[1] = Math.max(current[1], intervals[i][1]);
            } else {
                merged.add(current);
                current = intervals[i];
            }
        }
        merged.add(current);
        return merged.toArray(new int[0][]);
    }

    // PROBLEM 5: Minimum number of meeting rooms needed
    // Greedy + sorting + min-heap
    // Time: O(n log n)
    static int minMeetingRooms(int[][] intervals) {
        if (intervals.length == 0) return 0;
        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
        PriorityQueue<Integer> ends = new PriorityQueue<>(); // min-heap of end times
        ends.offer(intervals[0][1]);
        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] >= ends.peek()) ends.poll(); // room becomes free
            ends.offer(intervals[i][1]);
        }
        return ends.size();
    }

    public static void main(String[] args) {
        // Activity Selection
        System.out.println("=== Activity Selection ===");
        int[] start = {1, 3, 0, 5, 8, 5};
        int[] end   = {2, 4, 6, 7, 9, 9};
        System.out.println("Max activities: " + activitySelection(start, end)); // 4

        // Fractional Knapsack
        System.out.println("\n=== Fractional Knapsack ===");
        System.out.printf("Max value: %.2f%n",
            fractionalKnapsack(new int[]{10,20,30}, new int[]{60,100,120}, 50)); // 240.0

        // Min Coins
        System.out.println("\n=== Min Coins (US denominations) ===");
        int[] usd = {1, 5, 10, 25, 50, 100};
        System.out.println("Change for 87 cents: " + minCoinsGreedy(usd, 87));
        System.out.println("Change for 30 cents: " + minCoinsGreedy(usd, 30));

        // Merge Intervals
        System.out.println("\n=== Merge Intervals ===");
        int[][] intervals = {{1,3},{2,6},{8,10},{15,18}};
        int[][] merged = mergeIntervals(intervals);
        System.out.print("Merged: ");
        for (int[] iv : merged) System.out.print(Arrays.toString(iv) + " ");
        System.out.println();
        // Expected: [1,6] [8,10] [15,18]

        // Meeting Rooms
        System.out.println("\n=== Min Meeting Rooms ===");
        int[][] meetings = {{0,30},{5,10},{15,20}};
        System.out.println("Min rooms needed: " + minMeetingRooms(meetings)); // 2
        int[][] meetings2 = {{7,10},{2,4}};
        System.out.println("Min rooms needed: " + minMeetingRooms(meetings2)); // 1
    }
}
