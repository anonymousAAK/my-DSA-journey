/*
 * WEEK 15 - HEAPS & PRIORITY QUEUES
 * Topic: Heap, Heap Sort, Priority Queue Applications
 *
 * HEAP: A complete binary tree stored as an array where:
 * - MAX-HEAP: every parent >= children (root = max element)
 * - MIN-HEAP: every parent <= children (root = min element)
 *
 * ARRAY REPRESENTATION (1-indexed for clarity):
 * - Parent of node i: i / 2
 * - Left child of i: 2 * i
 * - Right child of i: 2 * i + 1
 *
 * OPERATIONS:
 * - insert:    Add at end, sift UP     O(log n)
 * - extractMax/Min: Replace root with last, sift DOWN  O(log n)
 * - buildHeap: Convert array to heap   O(n) — better than n inserts!
 *              (Start from last non-leaf, sift down each)
 * - peekMax:   O(1) — root element
 *
 * HEAP SORT:
 * 1. buildHeap O(n)
 * 2. Extract max n times, place at end O(n log n)
 * Overall: O(n log n), in-place, O(1) space
 * NOT stable.
 *
 * CLASSIC PROBLEMS:
 * - Kth largest element: O(n log k) using min-heap of size k
 * - Merge K sorted arrays: O(n log k) using min-heap
 * - Median from stream: O(log n) per insert using two heaps
 */

import java.util.*;

public class HeapAndPriorityQueue {

    // --- MAX-HEAP from scratch (0-indexed array) ---
    static class MaxHeap {
        int[] data;
        int size;

        MaxHeap(int capacity) { data = new int[capacity]; size = 0; }

        int parent(int i) { return (i - 1) / 2; }
        int left(int i) { return 2 * i + 1; }
        int right(int i) { return 2 * i + 2; }

        void swap(int i, int j) { int t = data[i]; data[i] = data[j]; data[j] = t; }

        // Sift up: fix heap property from node i upward
        void siftUp(int i) {
            while (i > 0 && data[parent(i)] < data[i]) {
                swap(i, parent(i));
                i = parent(i);
            }
        }

        // Sift down: fix heap property from node i downward
        void siftDown(int i) {
            int largest = i;
            int l = left(i), r = right(i);
            if (l < size && data[l] > data[largest]) largest = l;
            if (r < size && data[r] > data[largest]) largest = r;
            if (largest != i) { swap(i, largest); siftDown(largest); }
        }

        void insert(int x) { data[size++] = x; siftUp(size - 1); }
        int extractMax() {
            int max = data[0];
            data[0] = data[--size];
            siftDown(0);
            return max;
        }
        int peekMax() { return data[0]; }
        boolean isEmpty() { return size == 0; }
    }

    // Heap Sort using max-heap (in-place)
    static void heapSort(int[] arr) {
        int n = arr.length;
        // Build max-heap: start from last non-leaf, sift down
        for (int i = n / 2 - 1; i >= 0; i--) siftDownInPlace(arr, n, i);
        // Extract max one by one: place at end
        for (int i = n - 1; i > 0; i--) {
            int t = arr[0]; arr[0] = arr[i]; arr[i] = t; // swap max to end
            siftDownInPlace(arr, i, 0); // restore heap for reduced size
        }
    }
    static void siftDownInPlace(int[] arr, int n, int i) {
        int largest = i, l = 2*i+1, r = 2*i+2;
        if (l < n && arr[l] > arr[largest]) largest = l;
        if (r < n && arr[r] > arr[largest]) largest = r;
        if (largest != i) {
            int t = arr[i]; arr[i] = arr[largest]; arr[largest] = t;
            siftDownInPlace(arr, n, largest);
        }
    }

    // Kth Largest Element — min-heap of size k
    // Time: O(n log k), Space: O(k)
    static int kthLargest(int[] arr, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(); // default = min-heap
        for (int x : arr) {
            minHeap.offer(x);
            if (minHeap.size() > k) minHeap.poll(); // remove smallest
        }
        return minHeap.peek(); // kth largest
    }

    // Median from a Data Stream — two heaps
    // maxHeap (left half) | minHeap (right half)
    // Maintain: maxHeap.size() == minHeap.size() OR maxHeap.size() == minHeap.size() + 1
    static class MedianFinder {
        PriorityQueue<Integer> lower = new PriorityQueue<>(Collections.reverseOrder()); // max-heap for lower half
        PriorityQueue<Integer> upper = new PriorityQueue<>(); // min-heap for upper half

        void addNum(int num) {
            lower.offer(num);
            upper.offer(lower.poll()); // ensure all upper > all lower
            if (upper.size() > lower.size()) lower.offer(upper.poll()); // balance sizes
        }

        double findMedian() {
            if (lower.size() > upper.size()) return lower.peek();
            return (lower.peek() + upper.peek()) / 2.0;
        }
    }

    public static void main(String[] args) {
        // Max-Heap
        System.out.println("=== Max-Heap ===");
        MaxHeap heap = new MaxHeap(20);
        int[] nums = {5, 3, 7, 1, 9, 2, 8};
        for (int x : nums) heap.insert(x);
        System.out.print("Extract in order: ");
        while (!heap.isEmpty()) System.out.print(heap.extractMax() + " "); // 9 8 7 5 3 2 1
        System.out.println();

        // Heap Sort
        System.out.println("\n=== Heap Sort ===");
        int[] arr = {12, 11, 13, 5, 6, 7};
        System.out.println("Before: " + Arrays.toString(arr));
        heapSort(arr);
        System.out.println("After:  " + Arrays.toString(arr));

        // Kth Largest
        System.out.println("\n=== Kth Largest ===");
        int[] arr2 = {3, 2, 1, 5, 6, 4};
        for (int k = 1; k <= arr2.length; k++)
            System.out.println("k=" + k + " → " + kthLargest(arr2, k));

        // Java PriorityQueue (min-heap by default)
        System.out.println("\n=== Java PriorityQueue ===");
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        for (int x : new int[]{5, 1, 3, 2, 4}) pq.offer(x);
        System.out.print("Poll order (min-heap): ");
        while (!pq.isEmpty()) System.out.print(pq.poll() + " ");
        System.out.println();

        // Median from stream
        System.out.println("\n=== Median from Stream ===");
        MedianFinder mf = new MedianFinder();
        int[] stream = {5, 15, 1, 3, 2, 8, 7, 9, 10, 6, 11, 4};
        for (int x : stream) {
            mf.addNum(x);
            System.out.printf("Added %2d → median = %.1f%n", x, mf.findMedian());
        }
    }
}
