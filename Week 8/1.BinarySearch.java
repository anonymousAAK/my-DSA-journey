/*
 * WEEK 8 - SEARCHING ALGORITHMS
 * Topic: Binary Search (Iterative & Recursive)
 *
 * PREREQUISITE: Array must be SORTED.
 *
 * IDEA: Compare target with the middle element.
 * - If target == mid: found!
 * - If target < mid: search LEFT half
 * - If target > mid: search RIGHT half
 * Each comparison halves the search space → O(log n)
 *
 * PITFALL: Integer overflow in mid calculation.
 * BAD:  mid = (low + high) / 2   → can overflow if low+high > Integer.MAX_VALUE
 * GOOD: mid = low + (high - low) / 2
 *
 * Time: O(log n)
 * Space: O(1) iterative, O(log n) recursive (call stack)
 *
 * VARIATIONS COVERED:
 * 1. Standard binary search (find exact target)
 * 2. Find first occurrence (leftmost)
 * 3. Find last occurrence (rightmost)
 * 4. Search in rotated sorted array
 */

public class BinarySearch {

    // Standard binary search — returns index of target, or -1
    static int binarySearch(int[] arr, int target) {
        int low = 0, high = arr.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2; // safe mid
            if (arr[mid] == target) return mid;
            else if (arr[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }

    // Recursive binary search
    static int binarySearchRec(int[] arr, int target, int low, int high) {
        if (low > high) return -1;
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) return binarySearchRec(arr, target, mid + 1, high);
        else return binarySearchRec(arr, target, low, mid - 1);
    }

    // Find FIRST occurrence of target (leftmost index)
    static int firstOccurrence(int[] arr, int target) {
        int low = 0, high = arr.length - 1, result = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == target) {
                result = mid;
                high = mid - 1; // keep searching LEFT
            } else if (arr[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return result;
    }

    // Find LAST occurrence of target (rightmost index)
    static int lastOccurrence(int[] arr, int target) {
        int low = 0, high = arr.length - 1, result = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == target) {
                result = mid;
                low = mid + 1; // keep searching RIGHT
            } else if (arr[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return result;
    }

    // Count occurrences using first and last
    static int countOccurrences(int[] arr, int target) {
        int first = firstOccurrence(arr, target);
        if (first == -1) return 0;
        return lastOccurrence(arr, target) - first + 1;
    }

    // Search in ROTATED sorted array
    // Example: [4,5,6,7,0,1,2], target=0 → 4
    static int searchRotated(int[] arr, int target) {
        int low = 0, high = arr.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == target) return mid;

            // Check which half is sorted
            if (arr[low] <= arr[mid]) { // left half is sorted
                if (arr[low] <= target && target < arr[mid])
                    high = mid - 1; // target is in sorted left half
                else
                    low = mid + 1;
            } else { // right half is sorted
                if (arr[mid] < target && target <= arr[high])
                    low = mid + 1; // target is in sorted right half
                else
                    high = mid - 1;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] sorted = {-5, -2, 0, 1, 3, 5, 7, 9, 11};

        System.out.println("Array: [-5,-2,0,1,3,5,7,9,11]");
        System.out.println("binarySearch(5) = " + binarySearch(sorted, 5));   // 5
        System.out.println("binarySearch(0) = " + binarySearch(sorted, 0));   // 2
        System.out.println("binarySearch(4) = " + binarySearch(sorted, 4));   // -1
        System.out.println("binarySearchRec(7) = " + binarySearchRec(sorted, 7, 0, sorted.length - 1)); // 6

        int[] withDups = {1, 2, 2, 2, 3, 4, 4, 5};
        System.out.println("\nArray with duplicates: [1,2,2,2,3,4,4,5]");
        System.out.println("firstOccurrence(2) = " + firstOccurrence(withDups, 2));  // 1
        System.out.println("lastOccurrence(2)  = " + lastOccurrence(withDups, 2));   // 3
        System.out.println("countOccurrences(2) = " + countOccurrences(withDups, 2)); // 3
        System.out.println("countOccurrences(4) = " + countOccurrences(withDups, 4)); // 2
        System.out.println("countOccurrences(6) = " + countOccurrences(withDups, 6)); // 0

        int[] rotated = {4, 5, 6, 7, 0, 1, 2};
        System.out.println("\nRotated array: [4,5,6,7,0,1,2]");
        System.out.println("searchRotated(0) = " + searchRotated(rotated, 0)); // 4
        System.out.println("searchRotated(6) = " + searchRotated(rotated, 6)); // 2
        System.out.println("searchRotated(3) = " + searchRotated(rotated, 3)); // -1
    }
}
