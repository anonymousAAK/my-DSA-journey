/*
 * Reference Java implementation for tests/cases/kth_largest.json.
 * Min-heap of size k retains the k largest; the root is the answer.
 */
import java.util.PriorityQueue;

public class KthLargest {
    public static long kthLargest(long[] arr, long k) {
        PriorityQueue<Long> heap = new PriorityQueue<>();
        for (long x : arr) {
            heap.offer(x);
            if (heap.size() > k) heap.poll();
        }
        return heap.peek();
    }
}
