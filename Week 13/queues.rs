//! # Week 13: Queues
//!
//! This module covers queue data structures and queue-based algorithms in Rust.
//! Topics include:
//! - Queue using `VecDeque`
//! - Circular queue (fixed-capacity ring buffer)
//! - Queue implemented using two stacks
//! - Sliding window maximum (monotonic deque)
//!
//! ## Rust-Specific Notes for DSA Learners
//! - `std::collections::VecDeque<T>` is Rust's double-ended queue — a ring buffer
//!   with O(1) amortized push/pop at both ends. It's the go-to for queue operations.
//! - Unlike Java's `LinkedList`-based Queue, `VecDeque` is backed by a contiguous
//!   array, giving better cache performance.
//! - `VecDeque` supports indexing (`deque[i]`) but this is O(1) — the ring buffer
//!   handles the wrap-around internally.

use std::collections::VecDeque;
use std::fmt;

// ===========================================================================
// Queue using VecDeque
// ===========================================================================

/// A basic queue wrapping `VecDeque<i32>`.
///
/// In practice, you'd use `VecDeque<T>` directly. This wrapper makes the
/// queue interface explicit for learning purposes.
struct Queue {
    data: VecDeque<i32>,
}

impl Queue {
    fn new() -> Self {
        Queue {
            data: VecDeque::new(),
        }
    }

    /// Enqueues a value at the back.
    /// # Complexity: O(1) amortized
    fn enqueue(&mut self, value: i32) {
        self.data.push_back(value);
    }

    /// Dequeues a value from the front.
    /// # Complexity: O(1) amortized
    fn dequeue(&mut self) -> Option<i32> {
        self.data.pop_front()
    }

    /// Peeks at the front element without removing it.
    /// # Complexity: O(1)
    fn front(&self) -> Option<&i32> {
        self.data.front()
    }

    /// Peeks at the back element.
    /// # Complexity: O(1)
    fn back(&self) -> Option<&i32> {
        self.data.back()
    }

    fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    fn len(&self) -> usize {
        self.data.len()
    }
}

impl fmt::Display for Queue {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Queue[")?;
        for (i, val) in self.data.iter().enumerate() {
            if i > 0 {
                write!(f, ", ")?;
            }
            write!(f, "{}", val)?;
        }
        write!(f, "]")
    }
}

// ===========================================================================
// Circular Queue (Ring Buffer)
// ===========================================================================

/// A fixed-capacity circular queue (ring buffer).
///
/// Uses a fixed-size `Vec<Option<i32>>` with `front` and `rear` indices that
/// wrap around using modular arithmetic.
///
/// ## Why Circular?
/// A regular array-based queue wastes space as elements are dequeued from the front.
/// A circular queue reuses freed space by wrapping indices around.
///
/// # Complexity (all operations)
/// - Time:  O(1)
/// - Space: O(capacity)
struct CircularQueue {
    buffer: Vec<Option<i32>>,
    front: usize,
    rear: usize,
    size: usize,
    capacity: usize,
}

impl CircularQueue {
    fn new(capacity: usize) -> Self {
        CircularQueue {
            buffer: vec![None; capacity],
            front: 0,
            rear: 0,
            size: 0,
            capacity,
        }
    }

    /// Enqueues a value. Returns `false` if the queue is full.
    fn enqueue(&mut self, value: i32) -> bool {
        if self.is_full() {
            return false;
        }
        self.buffer[self.rear] = Some(value);
        self.rear = (self.rear + 1) % self.capacity;
        self.size += 1;
        true
    }

    /// Dequeues and returns the front value. Returns `None` if empty.
    fn dequeue(&mut self) -> Option<i32> {
        if self.is_empty() {
            return None;
        }
        let value = self.buffer[self.front].take(); // `take()` replaces with None.
        self.front = (self.front + 1) % self.capacity;
        self.size -= 1;
        value
    }

    /// Peeks at the front element.
    fn front(&self) -> Option<i32> {
        if self.is_empty() {
            None
        } else {
            self.buffer[self.front]
        }
    }

    /// Peeks at the rear element (most recently enqueued).
    fn rear(&self) -> Option<i32> {
        if self.is_empty() {
            None
        } else {
            // Rear points to the NEXT empty slot, so the last element is at rear - 1.
            let idx = if self.rear == 0 {
                self.capacity - 1
            } else {
                self.rear - 1
            };
            self.buffer[idx]
        }
    }

    fn is_empty(&self) -> bool {
        self.size == 0
    }

    fn is_full(&self) -> bool {
        self.size == self.capacity
    }

    fn len(&self) -> usize {
        self.size
    }
}

impl fmt::Display for CircularQueue {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "CircularQueue[")?;
        let mut count = 0;
        let mut idx = self.front;
        while count < self.size {
            if count > 0 {
                write!(f, ", ")?;
            }
            write!(f, "{}", self.buffer[idx].unwrap())?;
            idx = (idx + 1) % self.capacity;
            count += 1;
        }
        write!(f, "] (cap={})", self.capacity)
    }
}

// ===========================================================================
// Queue Using Two Stacks
// ===========================================================================

/// A queue implemented using two stacks (Vecs).
///
/// ## Strategy (Amortized O(1))
/// - `inbox`: receives all `enqueue` operations (push to top).
/// - `outbox`: serves all `dequeue` operations (pop from top).
/// - When `outbox` is empty and we need to dequeue, we pour all elements from
///   `inbox` into `outbox` (reversing the order, which gives us FIFO behavior).
///
/// Each element is moved at most twice (once into inbox, once into outbox),
/// so amortized cost per operation is O(1).
///
/// # Complexity
/// - `enqueue`: O(1)
/// - `dequeue`: O(1) amortized, O(n) worst case (when transfer needed)
struct QueueTwoStacks {
    inbox: Vec<i32>,
    outbox: Vec<i32>,
}

impl QueueTwoStacks {
    fn new() -> Self {
        QueueTwoStacks {
            inbox: Vec::new(),
            outbox: Vec::new(),
        }
    }

    fn enqueue(&mut self, value: i32) {
        self.inbox.push(value);
    }

    fn dequeue(&mut self) -> Option<i32> {
        if self.outbox.is_empty() {
            // Transfer all elements from inbox to outbox.
            while let Some(val) = self.inbox.pop() {
                self.outbox.push(val);
            }
        }
        self.outbox.pop()
    }

    fn front(&mut self) -> Option<&i32> {
        if self.outbox.is_empty() {
            while let Some(val) = self.inbox.pop() {
                self.outbox.push(val);
            }
        }
        self.outbox.last()
    }

    fn is_empty(&self) -> bool {
        self.inbox.is_empty() && self.outbox.is_empty()
    }

    fn len(&self) -> usize {
        self.inbox.len() + self.outbox.len()
    }
}

// ===========================================================================
// Sliding Window Maximum (Monotonic Deque)
// ===========================================================================

/// Finds the maximum element in each sliding window of size `k`.
///
/// Uses a **monotonic decreasing deque**: the front always holds the index of
/// the current window's maximum. We maintain the invariant that deque elements
/// are in decreasing order of their values.
///
/// ## Algorithm
/// For each element `arr[i]`:
/// 1. Remove indices from the back that point to values <= arr[i] (they can
///    never be the maximum while arr[i] is in the window).
/// 2. Add `i` to the back.
/// 3. Remove the front if it's outside the current window.
/// 4. The front of the deque is the maximum for the current window.
///
/// # Complexity
/// - Time:  O(n) — each element is pushed and popped from the deque at most once
/// - Space: O(k) for the deque
fn sliding_window_maximum(arr: &[i32], k: usize) -> Vec<i32> {
    if arr.is_empty() || k == 0 || k > arr.len() {
        return vec![];
    }

    let mut result = Vec::with_capacity(arr.len() - k + 1);
    let mut deque: VecDeque<usize> = VecDeque::new(); // Stores indices

    for i in 0..arr.len() {
        // Remove indices that are outside the current window [i-k+1, i].
        while let Some(&front) = deque.front() {
            if front + k <= i {
                deque.pop_front();
            } else {
                break;
            }
        }

        // Remove indices from the back whose values are <= arr[i].
        // These can never be the maximum while arr[i] is in the window.
        while let Some(&back) = deque.back() {
            if arr[back] <= arr[i] {
                deque.pop_back();
            } else {
                break;
            }
        }

        deque.push_back(i);

        // Once we've processed at least `k` elements, record the window maximum.
        if i >= k - 1 {
            // The front of the deque is the index of the maximum.
            result.push(arr[*deque.front().unwrap()]);
        }
    }

    result
}

// ===========================================================================
// Main — demonstrations and test assertions
// ===========================================================================

fn main() {
    println!("=== Week 13: Queues ===\n");

    // --- Queue using VecDeque ---
    println!("--- Queue (VecDeque) ---");
    let mut q = Queue::new();
    assert!(q.is_empty());

    q.enqueue(10);
    q.enqueue(20);
    q.enqueue(30);
    assert_eq!(q.front(), Some(&10));
    assert_eq!(q.back(), Some(&30));
    assert_eq!(q.len(), 3);
    println!("After enqueue(10, 20, 30): {}", q);

    assert_eq!(q.dequeue(), Some(10));
    assert_eq!(q.dequeue(), Some(20));
    println!("After two dequeues: {}", q);
    assert_eq!(q.front(), Some(&30));

    assert_eq!(q.dequeue(), Some(30));
    assert_eq!(q.dequeue(), None);
    println!("Dequeue from empty: {:?}", q.dequeue());

    // --- Circular Queue ---
    println!("\n--- Circular Queue ---");
    let mut cq = CircularQueue::new(4);
    assert!(cq.is_empty());

    assert!(cq.enqueue(1));
    assert!(cq.enqueue(2));
    assert!(cq.enqueue(3));
    assert!(cq.enqueue(4));
    assert!(!cq.enqueue(5)); // Full!
    assert!(cq.is_full());
    println!("Full queue: {}", cq);

    assert_eq!(cq.dequeue(), Some(1));
    assert_eq!(cq.dequeue(), Some(2));
    println!("After dequeue(1, 2): {}", cq);

    // Now there's space — wrap around.
    assert!(cq.enqueue(5));
    assert!(cq.enqueue(6));
    assert_eq!(cq.front(), Some(3));
    assert_eq!(cq.rear(), Some(6));
    println!("After enqueue(5, 6) [wraps around]: {}", cq);

    // Drain
    assert_eq!(cq.dequeue(), Some(3));
    assert_eq!(cq.dequeue(), Some(4));
    assert_eq!(cq.dequeue(), Some(5));
    assert_eq!(cq.dequeue(), Some(6));
    assert!(cq.is_empty());
    assert_eq!(cq.dequeue(), None);

    // --- Queue Using Two Stacks ---
    println!("\n--- Queue Using Two Stacks ---");
    let mut qs = QueueTwoStacks::new();
    qs.enqueue(1);
    qs.enqueue(2);
    qs.enqueue(3);
    assert_eq!(qs.len(), 3);
    assert_eq!(qs.front(), Some(&1));

    assert_eq!(qs.dequeue(), Some(1));
    assert_eq!(qs.dequeue(), Some(2));

    qs.enqueue(4);
    qs.enqueue(5);
    // Now outbox has [3], inbox has [4, 5]
    assert_eq!(qs.dequeue(), Some(3));
    assert_eq!(qs.dequeue(), Some(4)); // Triggers transfer of inbox to outbox
    assert_eq!(qs.dequeue(), Some(5));
    assert!(qs.is_empty());
    println!("Two-stack queue: all operations correct, queue is now empty");

    // Interleaved operations
    let mut qs2 = QueueTwoStacks::new();
    for i in 1..=5 {
        qs2.enqueue(i);
    }
    let mut results = Vec::new();
    for _ in 0..3 {
        results.push(qs2.dequeue().unwrap());
    }
    qs2.enqueue(6);
    qs2.enqueue(7);
    while !qs2.is_empty() {
        results.push(qs2.dequeue().unwrap());
    }
    assert_eq!(results, vec![1, 2, 3, 4, 5, 6, 7]);
    println!("Interleaved enqueue/dequeue: {:?}", results);

    // --- Sliding Window Maximum ---
    println!("\n--- Sliding Window Maximum ---");

    let arr = vec![1, 3, -1, -3, 5, 3, 6, 7];
    let k = 3;
    let maxes = sliding_window_maximum(&arr, k);
    assert_eq!(maxes, vec![3, 3, 5, 5, 6, 7]);
    println!("arr = {:?}, k = {}", arr, k);
    println!("Window maximums: {:?}", maxes);
    // Windows: [1,3,-1]=3, [3,-1,-3]=3, [-1,-3,5]=5, [-3,5,3]=5, [5,3,6]=6, [3,6,7]=7

    let arr2 = vec![1, -1];
    let maxes2 = sliding_window_maximum(&arr2, 1);
    assert_eq!(maxes2, vec![1, -1]);
    println!("arr = {:?}, k = 1, maxes = {:?}", arr2, maxes2);

    // All same
    let arr3 = vec![5, 5, 5, 5];
    let maxes3 = sliding_window_maximum(&arr3, 2);
    assert_eq!(maxes3, vec![5, 5, 5]);

    // Decreasing
    let arr4 = vec![9, 8, 7, 6, 5];
    let maxes4 = sliding_window_maximum(&arr4, 3);
    assert_eq!(maxes4, vec![9, 8, 7]);
    println!("Decreasing {:?}, k=3, maxes = {:?}", arr4, maxes4);

    // Increasing
    let arr5 = vec![1, 2, 3, 4, 5];
    let maxes5 = sliding_window_maximum(&arr5, 3);
    assert_eq!(maxes5, vec![3, 4, 5]);
    println!("Increasing {:?}, k=3, maxes = {:?}", arr5, maxes5);

    println!("\nAll assertions passed!");
}
