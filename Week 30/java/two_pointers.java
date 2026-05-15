/*
 * WEEK 30 - JAVA ADVANCED TOPICS
 * Topic: Two Pointers Pattern
 * File: two_pointers.java
 *
 * CONCEPT:
 *     The two-pointer pattern uses two indices that move through an array
 *     (often a sorted one) under monotonic rules. Each index advances at
 *     most n times, giving O(n) or O(n log n) algorithms for problems
 *     naively O(n^2) or worse.
 *
 * KEY POINTS:
 *     - On a sorted array, the sum a[l] + a[r] is monotonic in (l, r), so
 *       we move pointers based on the comparison with target.
 *     - For partitioning (Dutch flag, etc.), use l and r as low / high
 *       cursors.
 *     - For container / area problems the wider window dominates so always
 *       shrink the smaller side.
 *
 * ALGORITHM / APPROACH:
 *     TWO SUM SORTED:    l=0, r=n-1; while l<r: shift based on sum vs target.
 *     3SUM:              sort + iterate i; two-pointer inside for sum 0.
 *     CONTAINER MAX:     l=0, r=n-1; best = (r-l)*min(h[l],h[r]); shrink
 *                        the lower side.
 *     REMOVE DUPLICATES: write index w; iterate r; copy when a[r] != a[w-1].
 *
 * DRY RUN / EXAMPLE:
 *     twoSumSorted [2,7,11,15], target 9 -> indices (1,2) 1-indexed.
 *     3Sum [-1,0,1,2,-1,-4] -> [[-1,-1,2],[-1,0,1]].
 *     Max area [1,8,6,2,5,4,8,3,7] -> 49.
 *
 * COMPLEXITY:
 *     Two-sum sorted:  O(n)
 *     3Sum:            O(n^2)
 *     Container max:   O(n)
 */

// snake_case filename is fine; class TwoPointers is package-private.

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class TwoPointers {

    /** LC 167 - returns 1-indexed pair or {-1,-1} if no solution. */
    static int[] twoSumSorted(int[] nums, int target) {
        int l = 0, r = nums.length - 1;
        while (l < r) {
            int s = nums[l] + nums[r];
            if (s == target) return new int[]{l + 1, r + 1};
            if (s < target) l++;
            else r--;
        }
        return new int[]{-1, -1};
    }

    /** LC 15 - all unique triples summing to 0. */
    static List<List<Integer>> threeSum(int[] nums) {
        int[] sorted = nums.clone();
        Arrays.sort(sorted);
        List<List<Integer>> result = new ArrayList<>();
        int n = sorted.length;
        for (int i = 0; i < n - 2; i++) {
            if (i > 0 && sorted[i] == sorted[i - 1]) continue;
            int l = i + 1, r = n - 1;
            while (l < r) {
                int s = sorted[i] + sorted[l] + sorted[r];
                if (s == 0) {
                    result.add(Arrays.asList(sorted[i], sorted[l], sorted[r]));
                    while (l < r && sorted[l] == sorted[l + 1]) l++;
                    while (l < r && sorted[r] == sorted[r - 1]) r--;
                    l++; r--;
                } else if (s < 0) l++;
                else r--;
            }
        }
        return result;
    }

    /** LC 11 - container with most water. */
    static int maxArea(int[] height) {
        int l = 0, r = height.length - 1, best = 0;
        while (l < r) {
            best = Math.max(best, (r - l) * Math.min(height[l], height[r]));
            if (height[l] < height[r]) l++;
            else r--;
        }
        return best;
    }

    /** LC 26 - in-place dedupe sorted array; returns new length. */
    static int removeDuplicatesSorted(int[] nums) {
        if (nums.length == 0) return 0;
        int w = 1;
        for (int r = 1; r < nums.length; r++) {
            if (nums[r] != nums[w - 1]) nums[w++] = nums[r];
        }
        return w;
    }

    public static void main(String[] args) {
        System.out.println("Two Sum II [2,7,11,15] t=9: "
            + Arrays.toString(twoSumSorted(new int[]{2, 7, 11, 15}, 9)));
        System.out.println("3Sum [-1,0,1,2,-1,-4]: "
            + threeSum(new int[]{-1, 0, 1, 2, -1, -4}));
        System.out.println("Max Area [1,8,6,2,5,4,8,3,7]: "
            + maxArea(new int[]{1, 8, 6, 2, 5, 4, 8, 3, 7}));

        int[] arr = {0, 0, 1, 1, 1, 2, 2, 3, 3, 4};
        int newLen = removeDuplicatesSorted(arr);
        StringBuilder prefix = new StringBuilder("[");
        for (int i = 0; i < newLen; i++) {
            if (i > 0) prefix.append(", ");
            prefix.append(arr[i]);
        }
        prefix.append("]");
        System.out.println("Remove duplicates: newLen=" + newLen + ", prefix=" + prefix);
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in two_pointers.py:
 *   - Java returns int[] tuples / List<List<Integer>> instead of Python
 *     lists.
 *   - Arrays.sort mutates in place; we clone() the input to remain pure.
 *   - removeDuplicatesSorted IS purely in-place to mirror the LeetCode
 *     contract.
 */
