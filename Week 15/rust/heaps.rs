//! # Week 15: Heaps and Priority Queues
//!
//! A heap is a complete binary tree stored in an array where each parent node
//! satisfies the heap property relative to its children.
//!
//! ## Key Concepts
//! - **Max-Heap**: parent >= children (root is maximum)
//! - **Min-Heap**: parent <= children (root is minimum)
//! - **Complete Binary Tree**: all levels filled except possibly the last,
//!   which is filled left to right
//!
//! ## Array Representation
//! For a node at index `i` (0-indexed):
//! - Parent: `(i - 1) / 2`
//! - Left child: `2 * i + 1`
//! - Right child: `2 * i + 2`
//!
//! ## Complexity Summary
//! | Operation    | Time       | Space |
//! |-------------|------------|-------|
//! | Insert      | O(log n)   | O(1)  |
//! | Extract Max | O(log n)   | O(1)  |
//! | Peek        | O(1)       | O(1)  |
//! | Heap Sort   | O(n log n) | O(1)  |
//! | Build Heap  | O(n)       | O(1)  |

use std::collections::BinaryHeap;
use std::cmp::Reverse;

// =============================================================================
// MaxHeap — Custom implementation using Vec<i32>
// =============================================================================

/// A max-heap backed by a `Vec<i32>`.
///
/// # Ownership Note
/// The heap *owns* its data via `Vec<i32>`. Methods like `insert` take `i32`
/// by value (it's `Copy`), while `extract_max` moves the root value out.
struct MaxHeap {
    data: Vec<i32>,
}

impl MaxHeap {
    /// Creates a new empty max-heap.
    fn new() -> Self {
        MaxHeap { data: Vec::new() }
    }

    /// Returns the number of elements in the heap.
    fn len(&self) -> usize {
        self.data.len()
    }

    /// Returns `true` if the heap contains no elements.
    fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    /// Peeks at the maximum element without removing it.
    ///
    /// # Complexity
    /// - Time: O(1)
    fn peek(&self) -> Option<i32> {
        self.data.first().copied()
    }

    /// Inserts a value into the heap, maintaining the max-heap property.
    ///
    /// # Complexity
    /// - Time: O(log n) — sifts up at most the height of the tree
    /// - Space: O(1) amortized (Vec may reallocate)
    fn insert(&mut self, val: i32) {
        self.data.push(val);
        let idx = self.data.len() - 1;
        self.sift_up(idx);
    }

    /// Removes and returns the maximum element from the heap.
    ///
    /// # Complexity
    /// - Time: O(log n) — sifts down from root
    /// - Space: O(1)
    fn extract_max(&mut self) -> Option<i32> {
        if self.data.is_empty() {
            return None;
        }
        let n = self.data.len();
        self.data.swap(0, n - 1);
        let max_val = self.data.pop(); // Remove last element (was root)
        if !self.data.is_empty() {
            self.sift_down(0);
        }
        max_val
    }

    /// Restores the max-heap property by moving a node upward.
    ///
    /// After an insert at the end, the new element may be larger than its
    /// parent, so we repeatedly swap it upward until the property holds.
    ///
    /// # Complexity
    /// - Time: O(log n)
    fn sift_up(&mut self, mut idx: usize) {
        while idx > 0 {
            let parent = (idx - 1) / 2;
            if self.data[idx] > self.data[parent] {
                self.data.swap(idx, parent);
                idx = parent;
            } else {
                break;
            }
        }
    }

    /// Restores the max-heap property by moving a node downward.
    ///
    /// After extracting the root (replaced by last element), the new root
    /// may be smaller than its children, so we swap it down with the larger
    /// child until the property holds.
    ///
    /// # Complexity
    /// - Time: O(log n)
    fn sift_down(&mut self, mut idx: usize) {
        let n = self.data.len();
        loop {
            let left = 2 * idx + 1;
            let right = 2 * idx + 2;
            let mut largest = idx;

            if left < n && self.data[left] > self.data[largest] {
                largest = left;
            }
            if right < n && self.data[right] > self.data[largest] {
                largest = right;
            }
            if largest != idx {
                self.data.swap(idx, largest);
                idx = largest;
            } else {
                break;
            }
        }
    }
}

// =============================================================================
// Heap Sort — In-place, O(n log n), not stable
// =============================================================================

/// Sorts a vector in ascending order using heap sort.
///
/// # Algorithm
/// 1. **Build a max-heap** in-place using bottom-up heapification — O(n).
/// 2. **Repeatedly extract the max**: swap root with the last unsorted element,
///    reduce the heap size by one, and sift down the new root.
///
/// # Complexity
/// - Time: O(n log n) in all cases
/// - Space: O(1) — sorts in-place
///
/// # Ownership Note
/// Takes `&mut Vec<i32>` — borrows the vector mutably so we can sort in-place
/// without allocating a new collection.
fn heap_sort(arr: &mut Vec<i32>) {
    let n = arr.len();
    if n <= 1 {
        return;
    }

    // Phase 1: Build max-heap (bottom-up).
    // Start from the last non-leaf node and sift down each one.
    // This is O(n) due to the geometric sum of work at each level.
    for i in (0..n / 2).rev() {
        sift_down_range(arr, i, n);
    }

    // Phase 2: Extract elements one by one.
    // After each swap, the largest element is at the end (sorted position),
    // and we restore the heap property on the reduced heap.
    for end in (1..n).rev() {
        arr.swap(0, end);
        sift_down_range(arr, 0, end);
    }
}

/// Helper: sift down within a subarray `arr[0..size]`.
fn sift_down_range(arr: &mut Vec<i32>, mut idx: usize, size: usize) {
    loop {
        let left = 2 * idx + 1;
        let right = 2 * idx + 2;
        let mut largest = idx;

        if left < size && arr[left] > arr[largest] {
            largest = left;
        }
        if right < size && arr[right] > arr[largest] {
            largest = right;
        }
        if largest != idx {
            arr.swap(idx, largest);
            idx = largest;
        } else {
            break;
        }
    }
}

// =============================================================================
// Kth Largest Element — Using std::collections::BinaryHeap
// =============================================================================

/// Finds the k-th largest element in a slice using a min-heap of size k.
///
/// # Algorithm
/// Maintain a min-heap of the k largest elements seen so far. For each new
/// element, if it's larger than the heap's minimum, replace the minimum.
/// The root of the min-heap is the k-th largest.
///
/// # Complexity
/// - Time: O(n log k) — each of n elements may cause a heap operation of O(log k)
/// - Space: O(k) — the min-heap holds at most k elements
///
/// # Rust Note
/// `BinaryHeap` in Rust is a max-heap by default. We use `Reverse(x)` to
/// turn it into a min-heap. `Reverse` is a newtype wrapper from `std::cmp`.
fn kth_largest(nums: &[i32], k: usize) -> Option<i32> {
    if k == 0 || k > nums.len() {
        return None;
    }

    // Min-heap of size k (using Reverse for min-heap behavior)
    let mut min_heap: BinaryHeap<Reverse<i32>> = BinaryHeap::with_capacity(k + 1);

    for &num in nums {
        min_heap.push(Reverse(num));
        if min_heap.len() > k {
            min_heap.pop(); // Remove the smallest — keeps k largest
        }
    }

    // The root of the min-heap is the k-th largest
    min_heap.peek().map(|&Reverse(val)| val)
}

// =============================================================================
// MedianFinder — Two-heap approach
// =============================================================================

/// Maintains a running median using two heaps.
///
/// # Design
/// - `lower`: a max-heap storing the smaller half of numbers
/// - `upper`: a min-heap (via `Reverse`) storing the larger half
///
/// Invariant: `lower.len()` is equal to or one more than `upper.len()`.
/// The median is either the top of `lower` (odd count) or the average of
/// both tops (even count).
///
/// # Complexity
/// - `add_num`: O(log n) per insertion
/// - `find_median`: O(1)
/// - Space: O(n)
struct MedianFinder {
    lower: BinaryHeap<i32>,            // Max-heap for the smaller half
    upper: BinaryHeap<Reverse<i32>>,   // Min-heap for the larger half
}

impl MedianFinder {
    fn new() -> Self {
        MedianFinder {
            lower: BinaryHeap::new(),
            upper: BinaryHeap::new(),
        }
    }

    /// Adds a number to the data structure.
    ///
    /// Strategy: always add to `lower` first (via `upper` to ensure ordering),
    /// then rebalance so `lower` never has more than one extra element.
    fn add_num(&mut self, num: i32) {
        // Push to lower (max-heap)
        self.lower.push(num);

        // Ensure max of lower <= min of upper
        // Move the max of lower to upper
        if let Some(max_lower) = self.lower.pop() {
            self.upper.push(Reverse(max_lower));
        }

        // Rebalance: lower should have >= upper elements
        if self.upper.len() > self.lower.len() {
            if let Some(Reverse(min_upper)) = self.upper.pop() {
                self.lower.push(min_upper);
            }
        }
    }

    /// Returns the current median as a floating-point number.
    fn find_median(&self) -> f64 {
        if self.lower.len() > self.upper.len() {
            // Odd total count — median is top of lower
            *self.lower.peek().unwrap() as f64
        } else {
            // Even total count — median is average of both tops
            let max_lower = *self.lower.peek().unwrap() as f64;
            let min_upper = self.upper.peek().unwrap().0 as f64;
            (max_lower + min_upper) / 2.0
        }
    }
}

// =============================================================================
// Main — Test cases
// =============================================================================

fn main() {
    println!("=== Week 15: Heaps ===\n");

    // --- MaxHeap tests ---
    println!("--- Custom MaxHeap ---");
    let mut heap = MaxHeap::new();
    for &val in &[3, 1, 6, 5, 2, 4] {
        heap.insert(val);
    }
    println!("Heap size after inserting [3,1,6,5,2,4]: {}", heap.len());
    println!("Peek (max): {:?}", heap.peek());

    let mut extracted = Vec::new();
    while !heap.is_empty() {
        extracted.push(heap.extract_max().unwrap());
    }
    println!("Extracted in order: {:?}", extracted);
    assert_eq!(extracted, vec![6, 5, 4, 3, 2, 1]);
    println!("PASS: Elements extracted in descending order\n");

    // --- Heap Sort tests ---
    println!("--- Heap Sort ---");
    let mut arr = vec![12, 11, 13, 5, 6, 7];
    println!("Before: {:?}", arr);
    heap_sort(&mut arr);
    println!("After:  {:?}", arr);
    assert_eq!(arr, vec![5, 6, 7, 11, 12, 13]);

    let mut arr2 = vec![1];
    heap_sort(&mut arr2);
    assert_eq!(arr2, vec![1]);

    let mut arr3: Vec<i32> = vec![];
    heap_sort(&mut arr3);
    assert_eq!(arr3, Vec::<i32>::new());
    println!("PASS: Heap sort works correctly\n");

    // --- Kth Largest tests ---
    println!("--- Kth Largest ---");
    let nums = vec![3, 2, 1, 5, 6, 4];
    assert_eq!(kth_largest(&nums, 2), Some(5));
    println!("kth_largest([3,2,1,5,6,4], k=2) = {:?}", kth_largest(&nums, 2));

    let nums2 = vec![3, 2, 3, 1, 2, 4, 5, 5, 6];
    assert_eq!(kth_largest(&nums2, 4), Some(4));
    println!("kth_largest([3,2,3,1,2,4,5,5,6], k=4) = {:?}", kth_largest(&nums2, 4));

    assert_eq!(kth_largest(&nums, 0), None);
    assert_eq!(kth_largest(&nums, 100), None);
    println!("PASS: Kth largest works correctly\n");

    // --- MedianFinder tests ---
    println!("--- MedianFinder ---");
    let mut mf = MedianFinder::new();
    mf.add_num(1);
    println!("After adding 1: median = {}", mf.find_median());
    assert_eq!(mf.find_median(), 1.0);

    mf.add_num(2);
    println!("After adding 2: median = {}", mf.find_median());
    assert_eq!(mf.find_median(), 1.5);

    mf.add_num(3);
    println!("After adding 3: median = {}", mf.find_median());
    assert_eq!(mf.find_median(), 2.0);

    mf.add_num(4);
    println!("After adding 4: median = {}", mf.find_median());
    assert_eq!(mf.find_median(), 2.5);

    mf.add_num(5);
    println!("After adding 5: median = {}", mf.find_median());
    assert_eq!(mf.find_median(), 3.0);
    println!("PASS: MedianFinder works correctly\n");

    println!("All Week 15 tests passed!");
}
