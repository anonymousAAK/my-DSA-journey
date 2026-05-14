/*
 * WEEK 6 - ARRAYS
 * Topic: Return Array Sum
 *
 * PROBLEM:
 * Given an array of length N, find and return the sum of all elements.
 *
 * Input Format:
 * First line: N (size of array)
 * Second line: N space-separated integers
 *
 * Output Format:
 * Sum of all array elements.
 *
 * APPROACH:
 * Iterate through the array, accumulate each element into a running sum.
 *
 * Time Complexity:  O(n) — single pass through the array
 * Space Complexity: O(1) — only one extra variable
 *
 * ALTERNATIVE: Arrays.stream(arr).sum() — Java 8+ one-liner (same O(n))
 */

import java.util.Scanner;
import java.util.Arrays;

public class ReturnArraySum {

    // Iterative approach — O(n) time, O(1) space
    public static int sum(int[] arr) {
        int sum = 0;
        for (int val : arr) {
            sum += val;
        }
        return sum;
    }

    // Recursive approach — O(n) time, O(n) stack space
    public static int sumRecursive(int[] arr, int index) {
        if (index == arr.length) return 0;
        return arr[index] + sumRecursive(arr, index + 1);
    }

    public static void main(String[] args) {
        // Test cases
        int[] test1 = {1, 2, 3, 4, 5};
        System.out.println("Array: " + Arrays.toString(test1));
        System.out.println("Sum (iterative):  " + sum(test1));          // 15
        System.out.println("Sum (recursive):  " + sumRecursive(test1, 0)); // 15

        int[] test2 = {-1, 0, 5, -3, 10};
        System.out.println("\nArray: " + Arrays.toString(test2));
        System.out.println("Sum: " + sum(test2)); // 11

        int[] test3 = {};
        System.out.println("\nEmpty array sum: " + sum(test3)); // 0

        // Interactive
        Scanner s = new Scanner(System.in);
        System.out.print("\nEnter array size: ");
        int n = s.nextInt();
        int[] arr = new int[n];
        System.out.print("Enter " + n + " elements: ");
        for (int i = 0; i < n; i++) arr[i] = s.nextInt();
        System.out.println("Sum = " + sum(arr));
        s.close();
    }
}
