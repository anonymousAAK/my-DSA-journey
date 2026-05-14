/*
 * WEEK 13 - RUST DSA
 * Topic: Queue Implementations + Sliding Window Maximum
 * File: 1.QueueImplementation.rs
 *
 * CONCEPT:
 *   FIFO container. Rust's std::collections::VecDeque is a ring-buffer
 *   double-ended queue — the canonical queue/deque type.
 *
 * KEY POINTS:
 *   - CircularQueue<T>: hand-rolled fixed-capacity ring buffer.
 *   - QueueUsingStacks: classic two-stack queue.
 *   - sliding_window_max: monotonic deque using VecDeque<usize>.
 *
 * ALGORITHM / APPROACH:
 *   See Week 13 Java file. Same algorithms.
 *
 * RUST-SPECIFIC NOTES:
 *   - VecDeque<T>::push_back / pop_front give O(1) FIFO behavior.
 *   - The CircularQueue uses a Vec<Option<T>> so we don't require T: Default.
 *   - Operations return Option<T> rather than throwing.
 *
 * DRY RUN:
 *   Same examples as Java/Python files (sliding window of [1,3,-1,-3,5,3,6,7]
 *   with k=3 yields [3,3,5,5,6,7]).
 *
 * COMPLEXITY:
 *   CircularQueue ops: O(1)
 *   QueueUsingStacks ops: amortized O(1)
 *   sliding_window_max: O(n) total
 */

use std::collections::VecDeque;

pub struct CircularQueue<T> {
    cap: usize,
    data: Vec<Option<T>>,
    front: usize,
    rear: usize,
    sz: usize,
}

impl<T> CircularQueue<T> {
    pub fn new(capacity: usize) -> Self {
        let mut data: Vec<Option<T>> = Vec::with_capacity(capacity);
        for _ in 0..capacity { data.push(None); }
        Self { cap: capacity, data, front: 0, rear: 0, sz: 0 }
    }

    pub fn enqueue(&mut self, x: T) -> bool {
        if self.sz == self.cap { return false; }
        self.data[self.rear] = Some(x);
        self.rear = (self.rear + 1) % self.cap;
        self.sz += 1;
        true
    }

    pub fn dequeue(&mut self) -> Option<T> {
        if self.sz == 0 { return None; }
        let v = self.data[self.front].take();
        self.front = (self.front + 1) % self.cap;
        self.sz -= 1;
        v
    }

    pub fn peek(&self) -> Option<&T> {
        if self.sz == 0 { return None; }
        self.data[self.front].as_ref()
    }

    pub fn is_empty(&self) -> bool { self.sz == 0 }
    pub fn is_full(&self) -> bool { self.sz == self.cap }
    pub fn len(&self) -> usize { self.sz }
}

pub struct QueueUsingStacks {
    inbox: Vec<i32>,
    outbox: Vec<i32>,
}

impl QueueUsingStacks {
    pub fn new() -> Self { Self { inbox: vec![], outbox: vec![] } }

    pub fn enqueue(&mut self, x: i32) { self.inbox.push(x); }

    fn shift(&mut self) {
        if !self.outbox.is_empty() { return; }
        while let Some(v) = self.inbox.pop() { self.outbox.push(v); }
    }

    pub fn dequeue(&mut self) -> Option<i32> {
        self.shift();
        self.outbox.pop()
    }

    pub fn peek(&mut self) -> Option<i32> {
        self.shift();
        self.outbox.last().copied()
    }

    pub fn is_empty(&self) -> bool { self.inbox.is_empty() && self.outbox.is_empty() }
}

pub fn sliding_window_max(arr: &[i32], k: usize) -> Vec<i32> {
    let n = arr.len();
    if n == 0 || k == 0 { return Vec::new(); }
    let mut result = Vec::with_capacity(n - k + 1);
    let mut dq: VecDeque<usize> = VecDeque::new();
    for i in 0..n {
        while let Some(&front) = dq.front() {
            if (front as isize) < (i as isize) - (k as isize) + 1 { dq.pop_front(); }
            else { break; }
        }
        while let Some(&back) = dq.back() {
            if arr[back] < arr[i] { dq.pop_back(); } else { break; }
        }
        dq.push_back(i);
        if i + 1 >= k {
            result.push(arr[*dq.front().unwrap()]);
        }
    }
    result
}

fn main() {
    println!("=== Circular Queue ===");
    let mut cq: CircularQueue<i32> = CircularQueue::new(4);
    for v in [1, 2, 3, 4] { cq.enqueue(v); }
    println!("Full: {}", cq.is_full());
    println!("Dequeue: {:?}", cq.dequeue());
    cq.enqueue(5);
    println!("Peek: {:?}", cq.peek());

    println!("\n=== Queue using Two Stacks ===");
    let mut q = QueueUsingStacks::new();
    for v in [1, 2, 3] { q.enqueue(v); }
    println!("dequeue: {:?}", q.dequeue());
    println!("dequeue: {:?}", q.dequeue());
    q.enqueue(4);
    println!("peek: {:?}", q.peek());
    println!("dequeue: {:?}", q.dequeue());
    println!("dequeue: {:?}", q.dequeue());

    println!("\n=== VecDeque as Queue ===");
    let mut vd: VecDeque<i32> = VecDeque::new();
    for v in [10, 20, 30] { vd.push_back(v); }
    println!("peek: {:?}", vd.front());
    println!("poll: {:?}", vd.pop_front());
    println!("poll: {:?}", vd.pop_front());

    println!("\n=== Sliding Window Maximum ===");
    let arr = [1, 3, -1, -3, 5, 3, 6, 7];
    let k = 3;
    println!("Array: {:?} k={}", arr, k);
    println!("Max in each window: {:?}", sliding_window_max(&arr, k));

    let arr2 = [9, 11];
    println!("\nArray: {:?} k=2", arr2);
    println!("Max: {:?}", sliding_window_max(&arr2, 2));
}

/*
 * NOTES (vs. Java):
 * - VecDeque is Rust's analog of Java ArrayDeque (ring buffer).
 * - Operations return Option<T> rather than throwing exceptions.
 * - The two-stacks queue is identical conceptually; Vec is the stack.
 * - For the SWM we cast to isize when subtracting to handle the early-window
 *   case where i - k + 1 could be negative if computed with usize.
 */
