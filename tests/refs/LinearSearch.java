/*
 * Reference Java implementation for tests/cases/linear_search.json.
 * Returns the index of the first occurrence of target, or -1.
 */
public class LinearSearch {
    public static long linearSearch(long[] arr, long target) {
        for (int i = 0; i < arr.length; ++i) {
            if (arr[i] == target) return i;
        }
        return -1;
    }
}
