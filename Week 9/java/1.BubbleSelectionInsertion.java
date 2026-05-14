/*
 * WEEK 9 - SORTING ALGORITHMS
 * Topic: Bubble Sort, Selection Sort, Insertion Sort
 *
 * These are the O(n²) "elementary" sorting algorithms.
 * Understand them deeply — they reveal key sorting ideas.
 *
 * ===================================================
 * BUBBLE SORT
 * ===================================================
 * Repeatedly swap adjacent elements if they are out of order.
 * "Largest element bubbles to the end each pass."
 * Optimization: stop early if no swap occurred (array already sorted).
 * Best:    O(n)   — when array is already sorted (with early-stop)
 * Average: O(n²)
 * Worst:   O(n²)  — reverse sorted
 * Space:   O(1)   stable
 *
 * ===================================================
 * SELECTION SORT
 * ===================================================
 * Find minimum of unsorted portion, swap to front.
 * NEVER more than O(n) swaps — good when write operations are expensive.
 * Best/Average/Worst: O(n²)
 * Space: O(1)   NOT stable (in basic form)
 *
 * ===================================================
 * INSERTION SORT
 * ===================================================
 * Build sorted portion one element at a time.
 * Pick next element, insert it into correct position in sorted portion.
 * Best:    O(n)   — when nearly sorted
 * Average: O(n²)
 * Worst:   O(n²)  — reverse sorted
 * Space:   O(1)   stable
 * NOTE: Insertion sort is used in practice for small arrays (n < 16) and
 *       as a component in TimSort (Java's Arrays.sort for objects).
 */

import java.util.Arrays;

public class BubbleSelectionInsertion {

    // --- BUBBLE SORT ---
    static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j]; arr[j] = arr[j + 1]; arr[j + 1] = temp;
                    swapped = true;
                }
            }
            if (!swapped) break; // already sorted — early termination
        }
    }

    // --- SELECTION SORT ---
    static void selectionSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            int minIdx = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIdx]) minIdx = j;
            }
            if (minIdx != i) {
                int temp = arr[i]; arr[i] = arr[minIdx]; arr[minIdx] = temp;
            }
        }
    }

    // --- INSERTION SORT ---
    static void insertionSort(int[] arr) {
        int n = arr.length;
        for (int i = 1; i < n; i++) {
            int key = arr[i]; // element to insert
            int j = i - 1;
            // Shift elements greater than key one position right
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key; // insert key at correct position
        }
    }

    // Helper: count inversions (pairs where arr[i] > arr[j] with i < j)
    // Inversions ≈ how "unsorted" an array is; insertion sort takes O(inversions) swaps
    static long countInversions(int[] arr) {
        long count = 0;
        for (int i = 0; i < arr.length; i++)
            for (int j = i + 1; j < arr.length; j++)
                if (arr[i] > arr[j]) count++;
        return count;
    }

    public static void main(String[] args) {
        int[] base = {64, 25, 12, 22, 11};

        int[] arr1 = base.clone();
        System.out.println("Bubble Sort:");
        System.out.println("Before: " + Arrays.toString(arr1));
        bubbleSort(arr1);
        System.out.println("After:  " + Arrays.toString(arr1));

        int[] arr2 = base.clone();
        System.out.println("\nSelection Sort:");
        System.out.println("Before: " + Arrays.toString(arr2));
        selectionSort(arr2);
        System.out.println("After:  " + Arrays.toString(arr2));

        int[] arr3 = base.clone();
        System.out.println("\nInsertion Sort:");
        System.out.println("Before: " + Arrays.toString(arr3));
        insertionSort(arr3);
        System.out.println("After:  " + Arrays.toString(arr3));

        // Already sorted — bubble sort exits immediately
        int[] sorted = {1, 2, 3, 4, 5};
        System.out.println("\nAlready sorted — bubble sort:");
        System.out.println("Before: " + Arrays.toString(sorted));
        bubbleSort(sorted);
        System.out.println("After:  " + Arrays.toString(sorted));

        // Inversions
        int[] inv = {5, 3, 1, 4, 2};
        System.out.println("\nArray: " + Arrays.toString(inv));
        System.out.println("Inversions: " + countInversions(inv)); // 8
    }
}
