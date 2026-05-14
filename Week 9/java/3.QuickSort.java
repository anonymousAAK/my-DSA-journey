/*
 * WEEK 9 - SORTING ALGORITHMS
 * Topic: Quick Sort
 *
 * ALGORITHM:
 * 1. Choose a PIVOT element.
 * 2. PARTITION: rearrange so all elements < pivot are left of it,
 *    all elements > pivot are right of it. Pivot is now in its final position.
 * 3. Recursively sort left and right partitions.
 *
 * PARTITION SCHEMES:
 * - Lomuto: Simpler, uses last element as pivot. O(n) with O(1) space.
 * - Hoare:  Original, more efficient (3x fewer swaps). Uses two pointers.
 *
 * Time:  O(n log n) average
 *        O(n²) worst — when pivot is always min or max (sorted/reverse sorted)
 * Space: O(log n) average (call stack), O(n) worst
 * Stable: NO (in basic form)
 *
 * RANDOMIZED QUICKSORT:
 * Randomly swap a random element with the last before partitioning.
 * Expected time: O(n log n) regardless of input distribution.
 *
 * WHY QUICK SORT IN PRACTICE?
 * - Better cache performance than merge sort (in-place)
 * - ~2x faster than merge sort in practice despite same big-O
 * - Java uses Dual-Pivot Quicksort (Yaroslavskiy) for primitive arrays
 */

import java.util.Arrays;
import java.util.Random;

public class QuickSort {

    static Random rand = new Random(42);

    // Lomuto partition scheme — pivot = last element
    static int lomutoPartition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1; // boundary of "less than pivot" region
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                int temp = arr[i]; arr[i] = arr[j]; arr[j] = temp;
            }
        }
        // Place pivot in correct position
        int temp = arr[i + 1]; arr[i + 1] = arr[high]; arr[high] = temp;
        return i + 1; // pivot's final index
    }

    static void quickSortLomuto(int[] arr, int low, int high) {
        if (low >= high) return;
        int pivotIdx = lomutoPartition(arr, low, high);
        quickSortLomuto(arr, low, pivotIdx - 1);
        quickSortLomuto(arr, pivotIdx + 1, high);
    }

    // Hoare partition scheme — pivot = first element
    static int hoarePartition(int[] arr, int low, int high) {
        int pivot = arr[low];
        int i = low - 1, j = high + 1;
        while (true) {
            do { i++; } while (arr[i] < pivot);
            do { j--; } while (arr[j] > pivot);
            if (i >= j) return j;
            int temp = arr[i]; arr[i] = arr[j]; arr[j] = temp;
        }
    }

    static void quickSortHoare(int[] arr, int low, int high) {
        if (low >= high) return;
        int p = hoarePartition(arr, low, high);
        quickSortHoare(arr, low, p);
        quickSortHoare(arr, p + 1, high);
    }

    // Randomized Quicksort — avoids O(n²) worst case with high probability
    static void quickSortRandom(int[] arr, int low, int high) {
        if (low >= high) return;
        // Randomly select pivot and swap to last position
        int pivotIdx = low + rand.nextInt(high - low + 1);
        int temp = arr[pivotIdx]; arr[pivotIdx] = arr[high]; arr[high] = temp;
        int p = lomutoPartition(arr, low, high);
        quickSortRandom(arr, low, p - 1);
        quickSortRandom(arr, p + 1, high);
    }

    public static void main(String[] args) {
        int[] base = {10, 7, 8, 9, 1, 5};

        int[] arr1 = base.clone();
        System.out.println("Lomuto QuickSort:");
        System.out.println("Before: " + Arrays.toString(arr1));
        quickSortLomuto(arr1, 0, arr1.length - 1);
        System.out.println("After:  " + Arrays.toString(arr1));

        int[] arr2 = base.clone();
        System.out.println("\nHoare QuickSort:");
        System.out.println("Before: " + Arrays.toString(arr2));
        quickSortHoare(arr2, 0, arr2.length - 1);
        System.out.println("After:  " + Arrays.toString(arr2));

        int[] arr3 = base.clone();
        System.out.println("\nRandomized QuickSort:");
        quickSortRandom(arr3, 0, arr3.length - 1);
        System.out.println("After:  " + Arrays.toString(arr3));

        // Worst case for unrandomized: already sorted
        int[] worstCase = {1, 2, 3, 4, 5, 6, 7, 8};
        System.out.println("\nAlready sorted input (Randomized):");
        quickSortRandom(worstCase, 0, worstCase.length - 1);
        System.out.println("After: " + Arrays.toString(worstCase));

        // QuickSelect: find kth smallest element in O(n) average
        int[] arr4 = {3, 2, 1, 5, 6, 4};
        System.out.println("\nQuickSelect — kth smallest:");
        for (int k = 1; k <= arr4.length; k++) {
            int[] copy = arr4.clone();
            System.out.println("k=" + k + ": " + quickSelect(copy, 0, copy.length - 1, k));
        }
    }

    // QuickSelect: find kth smallest (1-indexed) in O(n) average
    static int quickSelect(int[] arr, int low, int high, int k) {
        if (low == high) return arr[low];
        int pivotIdx = low + rand.nextInt(high - low + 1);
        int temp = arr[pivotIdx]; arr[pivotIdx] = arr[high]; arr[high] = temp;
        int p = lomutoPartition(arr, low, high);
        int rank = p - low + 1; // rank of pivot in this subarray (1-indexed)
        if (rank == k) return arr[p];
        else if (k < rank) return quickSelect(arr, low, p - 1, k);
        else return quickSelect(arr, p + 1, high, k - rank);
    }
}
