/*
 * WEEK 13 - QUEUES
 * Topic: Queue Implementations + Sliding Window Maximum
 *
 * QUEUE: FIFO (First In, First Out) data structure.
 * Think of a line at a store — first to arrive, first to be served.
 *
 * CORE OPERATIONS (all O(1)):
 * - enqueue(x) / offer(x): add to rear
 * - dequeue() / poll():    remove from front
 * - peek() / front():      view front element
 * - isEmpty()
 *
 * VARIANTS:
 * - Circular Queue: efficient array-based queue
 * - Deque (Double-Ended Queue): insert/delete at BOTH ends
 * - Priority Queue: element with highest priority dequeued first
 *
 * In Java: use ArrayDeque as the Queue implementation.
 *
 * APPLICATIONS:
 * 1. BFS (Week 17)
 * 2. Sliding window maximum (monotonic deque)
 * 3. Level-order tree traversal
 * 4. Task scheduling
 *
 * SLIDING WINDOW MAXIMUM (hard problem):
 * Given array of n integers and window size k,
 * find the maximum in each window of size k.
 * Naive: O(n*k). Optimal with monotonic deque: O(n).
 */

import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.LinkedList;
import java.util.Queue;

public class QueueImplementation {

    // Circular Queue implementation (array-based)
    static class CircularQueue {
        int[] data;
        int front, rear, size, capacity;

        CircularQueue(int capacity) {
            this.capacity = capacity;
            data = new int[capacity];
            front = rear = size = 0;
        }

        boolean enqueue(int x) {
            if (size == capacity) return false; // full
            data[rear] = x;
            rear = (rear + 1) % capacity; // wrap around
            size++;
            return true;
        }

        int dequeue() {
            if (size == 0) throw new RuntimeException("Queue empty");
            int val = data[front];
            front = (front + 1) % capacity;
            size--;
            return val;
        }

        int peek() {
            if (size == 0) throw new RuntimeException("Queue empty");
            return data[front];
        }

        boolean isEmpty() { return size == 0; }
        boolean isFull() { return size == capacity; }
    }

    // Queue using two stacks (classic interview problem)
    // amortized O(1) per operation
    static class QueueUsingStacks {
        Deque<Integer> inbox = new ArrayDeque<>();  // for enqueue
        Deque<Integer> outbox = new ArrayDeque<>(); // for dequeue

        void enqueue(int x) { inbox.push(x); }

        int dequeue() {
            if (outbox.isEmpty()) {
                // Transfer all from inbox to outbox (reverses order)
                while (!inbox.isEmpty()) outbox.push(inbox.pop());
            }
            if (outbox.isEmpty()) throw new RuntimeException("Queue empty");
            return outbox.pop();
        }

        int peek() {
            if (outbox.isEmpty()) while (!inbox.isEmpty()) outbox.push(inbox.pop());
            return outbox.peek();
        }

        boolean isEmpty() { return inbox.isEmpty() && outbox.isEmpty(); }
    }

    // Sliding Window Maximum using Monotonic Deque
    // Time: O(n), Space: O(k)
    // Maintain a deque of INDICES where values are in DECREASING order.
    // Front of deque always has the index of the maximum for current window.
    static int[] slidingWindowMax(int[] arr, int k) {
        int n = arr.length;
        if (n == 0 || k == 0) return new int[0];
        int[] result = new int[n - k + 1];
        Deque<Integer> deque = new ArrayDeque<>(); // stores indices

        for (int i = 0; i < n; i++) {
            // Remove indices outside window
            while (!deque.isEmpty() && deque.peekFirst() < i - k + 1)
                deque.pollFirst();

            // Remove indices of elements smaller than current (they can't be future maxima)
            while (!deque.isEmpty() && arr[deque.peekLast()] < arr[i])
                deque.pollLast();

            deque.offerLast(i);

            // Window is full starting at index k-1
            if (i >= k - 1) result[i - k + 1] = arr[deque.peekFirst()];
        }
        return result;
    }

    public static void main(String[] args) {
        // Circular Queue
        System.out.println("=== Circular Queue ===");
        CircularQueue cq = new CircularQueue(4);
        cq.enqueue(1); cq.enqueue(2); cq.enqueue(3); cq.enqueue(4);
        System.out.println("Full: " + cq.isFull());
        System.out.println("Dequeue: " + cq.dequeue()); // 1
        cq.enqueue(5);
        System.out.println("Peek: " + cq.peek()); // 2

        // Queue using two stacks
        System.out.println("\n=== Queue using Two Stacks ===");
        QueueUsingStacks q = new QueueUsingStacks();
        q.enqueue(1); q.enqueue(2); q.enqueue(3);
        System.out.println("dequeue: " + q.dequeue()); // 1 (FIFO)
        System.out.println("dequeue: " + q.dequeue()); // 2
        q.enqueue(4);
        System.out.println("peek: " + q.peek());       // 3
        System.out.println("dequeue: " + q.dequeue()); // 3
        System.out.println("dequeue: " + q.dequeue()); // 4

        // Java's built-in Queue
        System.out.println("\n=== Java ArrayDeque as Queue ===");
        Queue<Integer> jQueue = new LinkedList<>();
        jQueue.offer(10); jQueue.offer(20); jQueue.offer(30);
        System.out.println("peek: " + jQueue.peek());  // 10
        System.out.println("poll: " + jQueue.poll());  // 10
        System.out.println("poll: " + jQueue.poll());  // 20

        // Sliding Window Maximum
        System.out.println("\n=== Sliding Window Maximum ===");
        int[] arr = {1, 3, -1, -3, 5, 3, 6, 7};
        int k = 3;
        System.out.println("Array: " + Arrays.toString(arr));
        System.out.println("Window size k=" + k);
        System.out.println("Max in each window: " + Arrays.toString(slidingWindowMax(arr, k)));
        // Expected: [3, 3, 5, 5, 6, 7]

        int[] arr2 = {9, 11};
        System.out.println("\nArray: " + Arrays.toString(arr2) + ", k=2");
        System.out.println("Max: " + Arrays.toString(slidingWindowMax(arr2, 2)));
        // Expected: [11]
    }
}
