/*
 * Reference Java implementation for tests/cases/merge_sort.json.
 * Classic top-down merge sort returning a sorted copy.
 */
public class MergeSort {
    private static void merge(long[] a, int left, int mid, int right) {
        long[] L = new long[mid - left + 1];
        long[] R = new long[right - mid];
        System.arraycopy(a, left, L, 0, L.length);
        System.arraycopy(a, mid + 1, R, 0, R.length);
        int i = 0, j = 0, k = left;
        while (i < L.length && j < R.length) {
            if (L[i] <= R[j]) a[k++] = L[i++];
            else a[k++] = R[j++];
        }
        while (i < L.length) a[k++] = L[i++];
        while (j < R.length) a[k++] = R[j++];
    }

    private static void msort(long[] a, int left, int right) {
        if (left >= right) return;
        int mid = left + (right - left) / 2;
        msort(a, left, mid);
        msort(a, mid + 1, right);
        merge(a, left, mid, right);
    }

    public static long[] mergeSort(long[] arr) {
        long[] a = arr.clone();
        if (a.length > 0) msort(a, 0, a.length - 1);
        return a;
    }
}
