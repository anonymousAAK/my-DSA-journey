/*
 * WEEK 6 - ARRAYS
 * Topic: Linear Search
 *
 * PROBLEM:
 * Given an array of size N and an integer X, find the index of the first
 * occurrence of X. Return -1 if X is not found.
 *
 * ALGORITHM:
 * Sequentially check each element until a match is found or the array ends.
 * This is the simplest search algorithm — no prerequisites on array order.
 *
 * Time Complexity:
 *   Best:    O(1)   — target is the first element
 *   Average: O(n/2) = O(n)
 *   Worst:   O(n)   — target is last element or not present
 *
 * Space Complexity: O(1)
 *
 * COMPARISON WITH BINARY SEARCH:
 * Linear search works on ANY array (sorted or unsorted).
 * Binary search requires a SORTED array but runs in O(log n).
 * For small arrays (n < 30), linear search can be faster due to cache effects.
 *
 * See Week 8 for Binary Search.
 */

import java.util.Arrays;
import java.util.Scanner;

public class LinearSearch {

    // Return index of first occurrence of target, or -1 if not found
    public static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }

    // Return index of LAST occurrence
    public static int linearSearchLast(int[] arr, int target) {
        int lastIdx = -1;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) lastIdx = i;
        }
        return lastIdx;
    }

    // Count all occurrences
    public static int countOccurrences(int[] arr, int target) {
        int count = 0;
        for (int val : arr) {
            if (val == target) count++;
        }
        return count;
    }

    // Find minimum and maximum element in one pass — O(n)
    public static int[] findMinMax(int[] arr) {
        if (arr.length == 0) throw new IllegalArgumentException("Empty array");
        int min = arr[0], max = arr[0];
        for (int val : arr) {
            if (val < min) min = val;
            if (val > max) max = val;
        }
        return new int[]{min, max};
    }

    public static void main(String[] args) {
        int[] arr = {4, 2, 7, 1, 9, 3, 7, 5};
        System.out.println("Array: " + Arrays.toString(arr));

        // Search
        System.out.println("linearSearch(7) = " + linearSearch(arr, 7));    // 2
        System.out.println("linearSearch(6) = " + linearSearch(arr, 6));    // -1

        // Last occurrence
        System.out.println("linearSearchLast(7) = " + linearSearchLast(arr, 7)); // 6

        // Count
        System.out.println("countOccurrences(7) = " + countOccurrences(arr, 7)); // 2
        System.out.println("countOccurrences(6) = " + countOccurrences(arr, 6)); // 0

        // Min/Max
        int[] minMax = findMinMax(arr);
        System.out.println("Min = " + minMax[0] + ", Max = " + minMax[1]); // 1, 9

        // Interactive
        Scanner s = new Scanner(System.in);
        System.out.print("\nEnter element to search for: ");
        int target = s.nextInt();
        int idx = linearSearch(arr, target);
        System.out.println(idx == -1 ? "Not found" : "Found at index " + idx);
        s.close();
    }
}
