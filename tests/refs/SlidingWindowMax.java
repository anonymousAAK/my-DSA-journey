/*
 * Reference Java implementation for tests/cases/sliding_window_max.json.
 * Monotonic deque to compute max in every sliding window of size k.
 */
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

public class SlidingWindowMax {
    public static List<Long> slidingWindowMax(long[] arr, long k) {
        List<Long> result = new ArrayList<>();
        int n = arr.length, K = (int) k;
        if (n == 0 || K == 0) return result;
        Deque<Integer> dq = new ArrayDeque<>();
        for (int i = 0; i < n; ++i) {
            while (!dq.isEmpty() && dq.peekFirst() < i - K + 1) dq.pollFirst();
            while (!dq.isEmpty() && arr[dq.peekLast()] < arr[i]) dq.pollLast();
            dq.offerLast(i);
            if (i >= K - 1) result.add(arr[dq.peekFirst()]);
        }
        return result;
    }
}
