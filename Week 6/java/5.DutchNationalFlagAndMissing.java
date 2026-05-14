/*
 * WEEK 6 - ARRAYS
 * Topic: Dutch National Flag + Missing/Duplicate Numbers
 *
 * ==========================================
 * PART A: DUTCH NATIONAL FLAG (3-WAY PARTITION)
 * ==========================================
 * Problem: Sort an array containing only 0s, 1s, and 2s in-place.
 * Example: [2,0,2,1,1,0] → [0,0,1,1,2,2]
 *
 * Algorithm (Dijkstra's 3-way partition):
 * Maintain three pointers: low, mid, high
 * - arr[0..low-1]  = 0s
 * - arr[low..mid-1] = 1s
 * - arr[mid..high]  = unsorted
 * - arr[high+1..n-1] = 2s
 *
 * Time: O(n), Space: O(1)  — single pass, in-place!
 *
 * ==========================================
 * PART B: FIND MISSING NUMBER
 * ==========================================
 * Given array [0..n] with one number missing, find it.
 * Approach 1: Expected sum = n*(n+1)/2, subtract actual sum. O(n) time, O(1) space.
 * Approach 2: XOR of [0..n] XOR all elements. (Handles overflow better.)
 *
 * ==========================================
 * PART C: FIND DUPLICATE NUMBER
 * ==========================================
 * Given array of n+1 integers where each is in [1..n], one number repeats.
 * Approach: Floyd's Cycle Detection (linked-list in disguise). O(n) time, O(1) space.
 */

import java.util.Arrays;

public class DutchNationalFlagAndMissing {

    // Part A: Dutch National Flag
    static void dutchFlag(int[] arr) {
        int low = 0, mid = 0, high = arr.length - 1;
        while (mid <= high) {
            if (arr[mid] == 0) {
                // swap arr[low] and arr[mid], advance both
                int t = arr[low]; arr[low] = arr[mid]; arr[mid] = t;
                low++; mid++;
            } else if (arr[mid] == 1) {
                mid++; // 1 is in correct region
            } else { // arr[mid] == 2
                // swap arr[mid] and arr[high], shrink high (don't advance mid)
                int t = arr[mid]; arr[mid] = arr[high]; arr[high] = t;
                high--;
            }
        }
    }

    // Part B: Missing number using sum formula
    static int missingNumberSum(int[] arr) {
        int n = arr.length; // array has n elements, numbers should be 0..n
        int expected = n * (n + 1) / 2;
        int actual = 0;
        for (int x : arr) actual += x;
        return expected - actual;
    }

    // Part B: Missing number using XOR
    static int missingNumberXOR(int[] arr) {
        int n = arr.length;
        int xor = 0;
        for (int i = 0; i <= n; i++) xor ^= i;
        for (int x : arr) xor ^= x;
        return xor; // all pairs cancel; only missing number remains
    }

    // Part C: Find duplicate — Floyd's Cycle Detection
    // Treat array as a linked list: arr[i] is the "next" pointer from node i
    // Duplicate creates a cycle; find the cycle entry = duplicate number
    // Time: O(n), Space: O(1)
    static int findDuplicate(int[] arr) {
        // Phase 1: find intersection point inside cycle
        int slow = arr[0], fast = arr[0];
        do {
            slow = arr[slow];
            fast = arr[arr[fast]];
        } while (slow != fast);

        // Phase 2: find cycle entrance (= duplicate)
        slow = arr[0];
        while (slow != fast) {
            slow = arr[slow];
            fast = arr[fast];
        }
        return slow;
    }

    public static void main(String[] args) {
        // --- Dutch National Flag ---
        int[] colors = {2, 0, 2, 1, 1, 0};
        System.out.println("Before: " + Arrays.toString(colors));
        dutchFlag(colors);
        System.out.println("After:  " + Arrays.toString(colors));

        int[] colors2 = {2, 2, 2, 0, 0, 1};
        dutchFlag(colors2);
        System.out.println("Sorted: " + Arrays.toString(colors2));

        // --- Missing Number ---
        int[] arr1 = {3, 0, 1}; // missing 2
        System.out.println("\narr = " + Arrays.toString(arr1));
        System.out.println("Missing (sum):  " + missingNumberSum(arr1));
        System.out.println("Missing (XOR):  " + missingNumberXOR(arr1));

        int[] arr2 = {9, 6, 4, 2, 3, 5, 7, 0, 1}; // missing 8
        System.out.println("\narr = " + Arrays.toString(arr2));
        System.out.println("Missing (sum):  " + missingNumberSum(arr2));
        System.out.println("Missing (XOR):  " + missingNumberXOR(arr2));

        // --- Find Duplicate ---
        int[] dup = {1, 3, 4, 2, 2}; // duplicate: 2
        System.out.println("\narr = " + Arrays.toString(dup));
        System.out.println("Duplicate: " + findDuplicate(dup));

        int[] dup2 = {3, 1, 3, 4, 2}; // duplicate: 3
        System.out.println("arr = " + Arrays.toString(dup2));
        System.out.println("Duplicate: " + findDuplicate(dup2));
    }
}
