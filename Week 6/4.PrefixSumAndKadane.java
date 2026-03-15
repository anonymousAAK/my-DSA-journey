/*
 * WEEK 6 - ARRAYS
 * Topic: Prefix Sum & Kadane's Algorithm (Maximum Subarray Sum)
 *
 * ==========================================
 * PART A: PREFIX SUM
 * ==========================================
 * A prefix sum array P where P[i] = arr[0] + arr[1] + ... + arr[i].
 *
 * USE CASE: Answer range-sum queries in O(1) after O(n) preprocessing.
 * Sum of arr[l..r] = P[r] - P[l-1]   (with P[-1] = 0)
 *
 * Time:  O(n) build, O(1) per query
 * Space: O(n)
 *
 * ==========================================
 * PART B: KADANE'S ALGORITHM
 * ==========================================
 * Find the contiguous subarray with the maximum sum.
 * Example: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
 *          → subarray [4, -1, 2, 1] has sum 6
 *
 * ALGORITHM:
 * Maintain 'currentSum' = best sum ending at current index.
 * At each position: currentSum = max(arr[i], currentSum + arr[i])
 * (Either start fresh at arr[i], or extend the previous subarray.)
 * maxSum = max(maxSum, currentSum) at each step.
 *
 * Time:  O(n)
 * Space: O(1)
 *
 * This is a classic DYNAMIC PROGRAMMING problem solved in linear time!
 */

import java.util.Arrays;

public class PrefixSumAndKadane {

    // Build prefix sum array
    static int[] buildPrefix(int[] arr) {
        int n = arr.length;
        int[] prefix = new int[n];
        prefix[0] = arr[0];
        for (int i = 1; i < n; i++) {
            prefix[i] = prefix[i - 1] + arr[i];
        }
        return prefix;
    }

    // Range sum query [l, r] using prefix array — O(1)
    static int rangeSum(int[] prefix, int l, int r) {
        if (l == 0) return prefix[r];
        return prefix[r] - prefix[l - 1];
    }

    // Kadane's Algorithm — returns max subarray sum
    static int maxSubarraySum(int[] arr) {
        int maxSum = arr[0];
        int currentSum = arr[0];
        for (int i = 1; i < arr.length; i++) {
            currentSum = Math.max(arr[i], currentSum + arr[i]);
            maxSum = Math.max(maxSum, currentSum);
        }
        return maxSum;
    }

    // Extended Kadane's: also return start and end indices of the subarray
    static int[] maxSubarrayWithIndices(int[] arr) {
        int maxSum = arr[0], currentSum = arr[0];
        int start = 0, end = 0, tempStart = 0;
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > currentSum + arr[i]) {
                currentSum = arr[i];
                tempStart = i;
            } else {
                currentSum += arr[i];
            }
            if (currentSum > maxSum) {
                maxSum = currentSum;
                start = tempStart;
                end = i;
            }
        }
        return new int[]{maxSum, start, end};
    }

    public static void main(String[] args) {
        // --- Prefix Sum Demo ---
        int[] arr = {3, -1, 2, 4, -3, 7};
        int[] prefix = buildPrefix(arr);
        System.out.println("Array:  " + Arrays.toString(arr));
        System.out.println("Prefix: " + Arrays.toString(prefix));
        System.out.println("Sum of arr[1..4] = " + rangeSum(prefix, 1, 4)); // -1+2+4-3 = 2
        System.out.println("Sum of arr[0..5] = " + rangeSum(prefix, 0, 5)); // 12
        System.out.println("Sum of arr[2..2] = " + rangeSum(prefix, 2, 2)); // 2

        // --- Kadane's Algorithm Demo ---
        int[] test1 = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        System.out.println("\nArray: " + Arrays.toString(test1));
        System.out.println("Max subarray sum: " + maxSubarraySum(test1)); // 6

        int[] result = maxSubarrayWithIndices(test1);
        System.out.println("Max sum: " + result[0] + " | Subarray: arr[" + result[1] + ".." + result[2] + "]");
        System.out.println("Subarray: " + Arrays.toString(Arrays.copyOfRange(test1, result[1], result[2] + 1)));

        // All-negative array
        int[] allNeg = {-5, -1, -8, -3};
        System.out.println("\nAll-negative: " + Arrays.toString(allNeg));
        System.out.println("Max sum: " + maxSubarraySum(allNeg)); // -1

        // Single element
        int[] single = {42};
        System.out.println("\nSingle element {42}: max sum = " + maxSubarraySum(single));
    }
}
