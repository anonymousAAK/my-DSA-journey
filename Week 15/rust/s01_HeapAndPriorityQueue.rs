/*
 * WEEK 15 - RUST DSA
 * Topic: Heap, Heap Sort, Priority Queue Applications
 * File: 1.HeapAndPriorityQueue.rs
 *
 * CONCEPT:
 *   A heap is a complete binary tree stored as an array satisfying the
 *   heap property (max-heap: parent >= children).
 *
 * KEY POINTS:
 *   - parent(i)=(i-1)/2; left=2i+1; right=2i+2.
 *   - Rust's std::collections::BinaryHeap is a MAX-heap.
 *   - For a min-heap, wrap values in std::cmp::Reverse(x).
 *
 * ALGORITHM / APPROACH:
 *   Hand-rolled MaxHeap mirrors the Java/Python/C++ versions.
 *   Heap sort: build max-heap, repeatedly pull max to the end.
 *   kth largest: maintain a min-heap of size k.
 *   Median: two heaps (Reverse-wrapped min-heap + max-heap).
 *
 * RUST-SPECIFIC NOTES:
 *   - Vec<T>::swap(i, j) is the in-place swap (no temp).
 *   - BinaryHeap<Reverse<T>> is the canonical min-heap idiom.
 *   - No exceptions; we expose .extract_max() -> Option<i32>.
 *
 * DRY RUN:
 *   Same as the other languages:
 *   Build max-heap [5,3,7,1,9,2,8] -> extract 9,8,7,5,3,2,1.
 *   heap_sort([12,11,13,5,6,7]) -> [5,6,7,11,12,13].
 *   kth_largest([3,2,1,5,6,4], 2) -> 5.
 *
 * COMPLEXITY:
 *   insert/extract O(log n); buildHeap O(n); heap sort O(n log n);
 *   kth largest O(n log k); median stream O(log n) per insert.
 */

use std::cmp::Reverse;
use std::collections::BinaryHeap;

pub struct MaxHeap {
    data: Vec<i32>,
}

impl MaxHeap {
    pub fn new() -> Self { Self { data: Vec::new() } }

    pub fn is_empty(&self) -> bool { self.data.is_empty() }
    pub fn peek_max(&self) -> Option<i32> { self.data.first().copied() }

    fn parent(i: usize) -> usize { (i.saturating_sub(1)) / 2 }
    fn left(i: usize) -> usize { 2 * i + 1 }
    fn right(i: usize) -> usize { 2 * i + 2 }

    fn sift_up(&mut self, mut i: usize) {
        while i > 0 {
            let p = Self::parent(i);
            if self.data[p] < self.data[i] {
                self.data.swap(p, i);
                i = p;
            } else { break; }
        }
    }

    fn sift_down(&mut self, mut i: usize) {
        let n = self.data.len();
        loop {
            let l = Self::left(i); let r = Self::right(i);
            let mut largest = i;
            if l < n && self.data[l] > self.data[largest] { largest = l; }
            if r < n && self.data[r] > self.data[largest] { largest = r; }
            if largest == i { return; }
            self.data.swap(i, largest);
            i = largest;
        }
    }

    pub fn insert(&mut self, x: i32) {
        self.data.push(x);
        let last = self.data.len() - 1;
        self.sift_up(last);
    }

    pub fn extract_max(&mut self) -> Option<i32> {
        if self.data.is_empty() { return None; }
        let top = self.data[0];
        let last = self.data.pop().unwrap();
        if !self.data.is_empty() {
            self.data[0] = last;
            self.sift_down(0);
        }
        Some(top)
    }
}

fn sift_down_arr(a: &mut [i32], n: usize, mut i: usize) {
    loop {
        let l = 2*i+1; let r = 2*i+2;
        let mut largest = i;
        if l < n && a[l] > a[largest] { largest = l; }
        if r < n && a[r] > a[largest] { largest = r; }
        if largest == i { return; }
        a.swap(i, largest);
        i = largest;
    }
}

pub fn heap_sort(a: &mut [i32]) {
    let n = a.len();
    if n < 2 { return; }
    for i in (0..(n/2)).rev() { sift_down_arr(a, n, i); }
    for end in (1..n).rev() {
        a.swap(0, end);
        sift_down_arr(a, end, 0);
    }
}

pub fn kth_largest(arr: &[i32], k: usize) -> i32 {
    let mut mh: BinaryHeap<Reverse<i32>> = BinaryHeap::new();
    for &x in arr {
        mh.push(Reverse(x));
        if mh.len() > k { mh.pop(); }
    }
    mh.peek().unwrap().0
}

pub struct MedianFinder {
    lower: BinaryHeap<i32>,                 // max-heap, holds lower half
    upper: BinaryHeap<Reverse<i32>>,        // min-heap, holds upper half
}

impl MedianFinder {
    pub fn new() -> Self { Self { lower: BinaryHeap::new(), upper: BinaryHeap::new() } }

    pub fn add_num(&mut self, x: i32) {
        self.lower.push(x);
        let top = self.lower.pop().unwrap();
        self.upper.push(Reverse(top));
        if self.upper.len() > self.lower.len() {
            let Reverse(v) = self.upper.pop().unwrap();
            self.lower.push(v);
        }
    }

    pub fn find_median(&self) -> f64 {
        if self.lower.len() > self.upper.len() {
            *self.lower.peek().unwrap() as f64
        } else {
            let lo = *self.lower.peek().unwrap() as f64;
            let hi = self.upper.peek().unwrap().0 as f64;
            (lo + hi) / 2.0
        }
    }
}

fn main() {
    println!("=== Max-Heap ===");
    let mut heap = MaxHeap::new();
    for x in [5, 3, 7, 1, 9, 2, 8] { heap.insert(x); }
    print!("Extract in order: ");
    while !heap.is_empty() { print!("{} ", heap.extract_max().unwrap()); }
    println!();

    println!("\n=== Heap Sort ===");
    let mut arr = vec![12, 11, 13, 5, 6, 7];
    println!("Before: {:?}", arr);
    heap_sort(&mut arr);
    println!("After:  {:?}", arr);

    println!("\n=== Kth Largest ===");
    let arr2 = [3, 2, 1, 5, 6, 4];
    for k in 1..=arr2.len() {
        println!("k={} -> {}", k, kth_largest(&arr2, k));
    }

    println!("\n=== BinaryHeap (max-heap by default) ===");
    let mut pq: BinaryHeap<i32> = BinaryHeap::new();
    for x in [5, 1, 3, 2, 4] { pq.push(x); }
    print!("Pop order (max-heap): ");
    while let Some(v) = pq.pop() { print!("{} ", v); }
    println!();

    println!("\n=== Min-heap via Reverse ===");
    let mut mh: BinaryHeap<Reverse<i32>> = BinaryHeap::new();
    for x in [5, 1, 3, 2, 4] { mh.push(Reverse(x)); }
    print!("Pop order (min): ");
    while let Some(Reverse(v)) = mh.pop() { print!("{} ", v); }
    println!();

    println!("\n=== Median from Stream ===");
    let mut mf = MedianFinder::new();
    for x in [5, 15, 1, 3, 2, 8, 7, 9, 10, 6, 11, 4] {
        mf.add_num(x);
        println!("Added {:2} -> median = {:.1}", x, mf.find_median());
    }
}

/*
 * NOTES (vs. Java):
 * - Rust's BinaryHeap defaults to MAX-heap; opposite of Java's PriorityQueue
 *   (and the same as C++'s priority_queue).
 * - For a min-heap, wrap in std::cmp::Reverse — type-safe and zero cost.
 * - Median finder uses two heaps; pattern matches Java/Python/C++ exactly.
 */
