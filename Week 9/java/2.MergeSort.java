/*
 * WEEK 9 - SORTING ALGORITHMS
 * Topic: Merge Sort (Divide and Conquer)
 *
 * ALGORITHM:
 * 1. DIVIDE: Split array in half recursively until size 1 (already sorted).
 * 2. CONQUER: Merge two sorted halves into one sorted array.
 *
 * MERGING: Use two pointers — one for each half. Pick the smaller element.
 *
 * Time:  O(n log n) — always (best, average, worst)
 * Space: O(n) — temporary array for merging
 * Stable: YES — equal elements maintain their relative order.
 *
 * APPLICATIONS:
 * 1. External sorting (data too large to fit in memory)
 * 2. Counting inversions (as seen below)
 * 3. Foundation of TimSort (Java's built-in sort for objects)
 *
 * RECURRENCE: T(n) = 2T(n/2) + O(n)  → O(n log n) by Master Theorem
 *
 * BONUS: Count Inversions using merge sort
 * An inversion is a pair (i, j) where i < j but arr[i] > arr[j].
 * While merging, whenever we pick from RIGHT half before LEFT half,
 * we have (mid - left + 1) inversions.
 */

import java.util.Arrays;

public class MergeSort {

    // Merge two sorted halves arr[left..mid] and arr[mid+1..right]
    static void merge(int[] arr, int left, int mid, int right) {
        int n1 = mid - left + 1;
        int n2 = right - mid;

        int[] L = Arrays.copyOfRange(arr, left, mid + 1);
        int[] R = Arrays.copyOfRange(arr, mid + 1, right + 1);

        int i = 0, j = 0, k = left;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) arr[k++] = L[i++]; // <= keeps it stable
            else arr[k++] = R[j++];
        }
        while (i < n1) arr[k++] = L[i++];
        while (j < n2) arr[k++] = R[j++];
    }

    static void mergeSort(int[] arr, int left, int right) {
        if (left >= right) return; // base case: 0 or 1 element
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }

    // Convenience wrapper
    static void mergeSort(int[] arr) {
        mergeSort(arr, 0, arr.length - 1);
    }

    // --- COUNT INVERSIONS (bonus application) ---
    static long invCount;

    static void mergeCount(int[] arr, int left, int mid, int right) {
        int[] L = Arrays.copyOfRange(arr, left, mid + 1);
        int[] R = Arrays.copyOfRange(arr, mid + 1, right + 1);
        int i = 0, j = 0, k = left;
        while (i < L.length && j < R.length) {
            if (L[i] <= R[j]) {
                arr[k++] = L[i++];
            } else {
                // L[i..L.length-1] are all greater than R[j] (left is sorted)
                invCount += (L.length - i);
                arr[k++] = R[j++];
            }
        }
        while (i < L.length) arr[k++] = L[i++];
        while (j < R.length) arr[k++] = R[j++];
    }

    static void mergeSortCount(int[] arr, int left, int right) {
        if (left >= right) return;
        int mid = left + (right - left) / 2;
        mergeSortCount(arr, left, mid);
        mergeSortCount(arr, mid + 1, right);
        mergeCount(arr, left, mid, right);
    }

    static long countInversions(int[] arr) {
        int[] copy = arr.clone();
        invCount = 0;
        mergeSortCount(copy, 0, copy.length - 1);
        return invCount;
    }

    public static void main(String[] args) {
        // Basic sort
        int[] arr = {38, 27, 43, 3, 9, 82, 10};
        System.out.println("Before: " + Arrays.toString(arr));
        mergeSort(arr);
        System.out.println("After:  " + Arrays.toString(arr));

        // Single element and already sorted
        int[] single = {5};
        mergeSort(single);
        System.out.println("\nSingle: " + Arrays.toString(single));

        int[] already = {1, 2, 3, 4, 5};
        mergeSort(already);
        System.out.println("Already sorted: " + Arrays.toString(already));

        // Reverse sorted (worst case for naive sorts, same for merge sort)
        int[] reverse = {5, 4, 3, 2, 1};
        mergeSort(reverse);
        System.out.println("Reverse sorted: " + Arrays.toString(reverse));

        // Count inversions
        System.out.println("\n=== Count Inversions ===");
        int[][] tests = {{2, 4, 1, 3, 5}, {5, 3, 1, 4, 2}, {1, 2, 3}};
        for (int[] t : tests) {
            System.out.println(Arrays.toString(t) + " → inversions: " + countInversions(t));
        }
        // {2,4,1,3,5}: (2,1),(4,1),(4,3) = 3 inversions
        // {5,3,1,4,2}: 8 inversions
        // {1,2,3}: 0 inversions
    }
}
