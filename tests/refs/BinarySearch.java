/*
 * Reference Java implementation for tests/cases/binary_search.json.
 * Iterative binary search; returns matched index or -1.
 */
public class BinarySearch {
    public static long binarySearch(long[] arr, long target) {
        int low = 0, high = arr.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == target) return mid;
            else if (arr[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }
}
