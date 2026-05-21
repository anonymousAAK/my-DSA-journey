/*
 * Reference Java implementation for tests/cases/quick_sort.json.
 * Lomuto quicksort with a seeded RNG for deterministic pivot choice.
 */
import java.util.Random;

public class QuickSort {
    private static final Random RNG = new Random(42);

    private static int partition(long[] a, int low, int high) {
        long pivot = a[high];
        int i = low - 1;
        for (int j = low; j < high; ++j) {
            if (a[j] <= pivot) {
                i++;
                long t = a[i]; a[i] = a[j]; a[j] = t;
            }
        }
        long t = a[i + 1]; a[i + 1] = a[high]; a[high] = t;
        return i + 1;
    }

    private static void qs(long[] a, int low, int high) {
        if (low >= high) return;
        int pivotIdx = low + RNG.nextInt(high - low + 1);
        long t = a[pivotIdx]; a[pivotIdx] = a[high]; a[high] = t;
        int p = partition(a, low, high);
        qs(a, low, p - 1);
        qs(a, p + 1, high);
    }

    public static long[] quickSort(long[] arr) {
        long[] a = arr.clone();
        if (a.length > 0) qs(a, 0, a.length - 1);
        return a;
    }
}
