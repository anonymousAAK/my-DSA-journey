/*
 * WEEK 6 - ARRAYS
 * Topic: Reverse and Rotate an Array
 *
 * PROBLEM 1: Reverse an array in-place.
 * Input:  [1, 2, 3, 4, 5]
 * Output: [5, 4, 3, 2, 1]
 *
 * APPROACH: Two-pointer technique — swap arr[left] and arr[right], move inward.
 * Time: O(n)  Space: O(1)
 *
 * PROBLEM 2: Left-rotate an array by k positions.
 * Input:  [1, 2, 3, 4, 5], k=2
 * Output: [3, 4, 5, 1, 2]
 *
 * APPROACH (Reversal algorithm — O(n) time, O(1) space):
 * Step 1: Reverse first k elements:   [2,1, 3,4,5]
 * Step 2: Reverse remaining n-k:      [2,1, 5,4,3]
 * Step 3: Reverse entire array:       [3,4,5, 1,2]
 *
 * This is more efficient than the naive O(n*k) shift approach.
 */

import java.util.Arrays;

public class ArrayReverseAndRotate {

    // Reverse a subarray from index l to r (inclusive)
    static void reverse(int[] arr, int l, int r) {
        while (l < r) {
            int temp = arr[l];
            arr[l] = arr[r];
            arr[r] = temp;
            l++;
            r--;
        }
    }

    // Reverse entire array
    static void reverseArray(int[] arr) {
        reverse(arr, 0, arr.length - 1);
    }

    // Left rotate by k positions using reversal algorithm
    // Time: O(n), Space: O(1)
    static void leftRotate(int[] arr, int k) {
        int n = arr.length;
        k = k % n; // handle k >= n
        if (k == 0) return;
        reverse(arr, 0, k - 1);
        reverse(arr, k, n - 1);
        reverse(arr, 0, n - 1);
    }

    // Right rotate by k positions = left rotate by (n - k)
    static void rightRotate(int[] arr, int k) {
        int n = arr.length;
        leftRotate(arr, n - (k % n));
    }

    public static void main(String[] args) {
        // --- Reverse ---
        int[] arr1 = {1, 2, 3, 4, 5};
        System.out.println("Original: " + Arrays.toString(arr1));
        reverseArray(arr1);
        System.out.println("Reversed: " + Arrays.toString(arr1));

        // --- Left Rotate ---
        int[] arr2 = {1, 2, 3, 4, 5};
        System.out.println("\nOriginal:         " + Arrays.toString(arr2));
        leftRotate(arr2, 2);
        System.out.println("Left Rotate by 2: " + Arrays.toString(arr2));

        // --- Right Rotate ---
        int[] arr3 = {1, 2, 3, 4, 5};
        System.out.println("\nOriginal:          " + Arrays.toString(arr3));
        rightRotate(arr3, 2);
        System.out.println("Right Rotate by 2: " + Arrays.toString(arr3));

        // --- Edge cases ---
        int[] single = {42};
        leftRotate(single, 5);
        System.out.println("\nSingle element rotated: " + Arrays.toString(single));

        int[] empty = {};
        System.out.println("Empty array: " + Arrays.toString(empty));
    }
}
