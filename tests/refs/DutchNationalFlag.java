/*
 * Reference Java implementation for tests/cases/dutch_national_flag.json.
 * In-place three-way partition; returns a fresh sorted array.
 */
public class DutchNationalFlag {
    public static long[] dutchFlag(long[] input) {
        long[] a = input.clone();
        int low = 0, mid = 0, high = a.length - 1;
        while (mid <= high) {
            if (a[mid] == 0) {
                long t = a[low]; a[low] = a[mid]; a[mid] = t;
                low++; mid++;
            } else if (a[mid] == 1) {
                mid++;
            } else {
                long t = a[mid]; a[mid] = a[high]; a[high] = t;
                high--;
            }
        }
        return a;
    }
}
