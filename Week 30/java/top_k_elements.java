/*
 * WEEK 30 - JAVA ADVANCED TOPICS
 * Topic: Top-K Elements Pattern
 * File: top_k_elements.java
 *
 * CONCEPT:
 *     Many interview problems reduce to "find the K largest / smallest /
 *     most-frequent elements". Three idiomatic solutions:
 *       1. Min-heap of size K (keeps largest): O(n log K), O(K) space.
 *       2. Bucket sort by frequency: O(n) time, O(n) space (when input is
 *          integer / hashable with bounded counts).
 *       3. Quickselect partition: O(n) expected time, O(1) extra space.
 *
 * KEY POINTS:
 *     - Min-heap of size K is the safe default when K << n.
 *     - Bucket sort works for top-K frequent because counts are bounded by n.
 *     - Quickselect (Hoare partition) is the fastest but has O(n^2) worst
 *       case unless you randomise or use median-of-medians.
 *
 * ALGORITHM / APPROACH:
 *     KTH LARGEST (heap):
 *         push x into heap; if size > K: pop. top = K-th largest.
 *     TOP K FREQUENT (heap):
 *         count freq; min-heap on freq with size K.
 *     TOP K FREQUENT (bucket):
 *         count freq; buckets[freq].append(item); collect from highest bucket.
 *     QUICKSELECT:
 *         pivot partition; recurse into the side containing K.
 *
 * DRY RUN / EXAMPLE:
 *     findKthLargest [3,2,1,5,6,4], k=2 -> 5
 *     topKFrequent  [1,1,1,2,2,3], k=2 -> [1, 2]
 *     quickselect    [3,2,1,5,6,4], k=2 -> 5
 *
 * COMPLEXITY:
 *     Heap-based:  O(n log K) time, O(K) space.
 *     Bucket:      O(n) time, O(n) space.
 *     Quickselect: O(n) expected time, O(1) extra space.
 */

// snake_case filename is fine; class TopKElements is package-private.

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Random;

class TopKElements {

    static int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        for (int x : nums) {
            heap.offer(x);
            if (heap.size() > k) heap.poll();
        }
        return heap.peek();
    }

    static int[] topKFrequentHeap(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int x : nums) freq.merge(x, 1, Integer::sum);
        PriorityQueue<Map.Entry<Integer, Integer>> heap =
            new PriorityQueue<>(Comparator.comparingInt(Map.Entry::getValue));
        for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
            heap.offer(e);
            if (heap.size() > k) heap.poll();
        }
        int[] result = new int[k];
        for (int i = 0; i < k; i++) result[i] = heap.poll().getKey();
        return result;
    }

    @SuppressWarnings("unchecked")
    static int[] topKFrequentBucket(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int x : nums) freq.merge(x, 1, Integer::sum);
        List<Integer>[] buckets = new List[nums.length + 1];
        for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
            int f = e.getValue();
            if (buckets[f] == null) buckets[f] = new ArrayList<>();
            buckets[f].add(e.getKey());
        }
        int[] out = new int[k];
        int idx = 0;
        for (int i = buckets.length - 1; i >= 0 && idx < k; i--) {
            if (buckets[i] == null) continue;
            for (int v : buckets[i]) {
                out[idx++] = v;
                if (idx == k) break;
            }
        }
        return out;
    }

    /** Hoare-partition quickselect (expected O(n)). Returns the K-th largest. */
    static int quickselectKthLargest(int[] nums, int k) {
        int[] arr = nums.clone();
        int target = arr.length - k;
        Random rng = new Random(0);
        int lo = 0, hi = arr.length - 1;
        while (lo < hi) {
            int pivot = arr[lo + rng.nextInt(hi - lo + 1)];
            int i = lo, j = hi;
            while (i <= j) {
                while (arr[i] < pivot) i++;
                while (arr[j] > pivot) j--;
                if (i <= j) {
                    int t = arr[i]; arr[i] = arr[j]; arr[j] = t;
                    i++; j--;
                }
            }
            if (i <= target) lo = i;
            else hi = i - 1;
        }
        return arr[target];
    }

    public static void main(String[] args) {
        System.out.println("Kth largest [3,2,1,5,6,4] k=2: "
            + findKthLargest(new int[]{3, 2, 1, 5, 6, 4}, 2));
        int[] heapResult = topKFrequentHeap(new int[]{1, 1, 1, 2, 2, 3}, 2);
        Arrays.sort(heapResult);
        System.out.println("Top 2 frequent (heap):   " + Arrays.toString(heapResult));
        int[] bucketResult = topKFrequentBucket(new int[]{1, 1, 1, 2, 2, 3}, 2);
        Arrays.sort(bucketResult);
        System.out.println("Top 2 frequent (bucket): " + Arrays.toString(bucketResult));
        System.out.println("Quickselect kth=2: "
            + quickselectKthLargest(new int[]{3, 2, 1, 5, 6, 4}, 2));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in top_k_elements.py:
 *   - Java's PriorityQueue is a min-heap by default; we pass an explicit
 *     Comparator for entries with composite keys.
 *   - The bucket array uses raw List[] with @SuppressWarnings; Java's
 *     generics-array limitations force this idiom.
 *   - Quickselect uses a seeded Random for deterministic output across runs.
 *   - The companion interview_patterns.java already covers findKthLargest /
 *     topKFrequent; we add quickselect for parity with the Python split.
 */
