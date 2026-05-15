// WEEK 30 - RUST ADVANCED TOPICS
// Topic: Top-K Elements Pattern
// File: top_k_elements.rs
//
// CONCEPT:
//   Find the K largest / smallest / most-frequent elements:
//     - Min-heap of size K (keep largest): O(n log K).
//     - Bucket sort by frequency: O(n).
//     - Quickselect: O(n) expected.
//
// KEY POINTS:
//   - BinaryHeap is a max-heap; Reverse(...) wraps to a min-heap.
//   - For top-K frequent integer elements, bucket sort is asymptotically
//     optimal.
//
// ALGORITHM / APPROACH:
//   See per-function code.
//
// RUST-SPECIFIC NOTES:
//   - Use std::cmp::Reverse to invert ordering for a min-heap.
//   - HashMap<i32, i32> for the frequency table.
//
// DRY RUN / EXAMPLE:
//   find_kth_largest [3,2,1,5,6,4], k=2 -> 5.
//   top_k_frequent  [1,1,1,2,2,3], k=2 -> [1, 2].
//
// COMPLEXITY:
//   Heap O(n log K); Bucket O(n); Quickselect O(n) expected.

use std::collections::{BinaryHeap, HashMap};
use std::cmp::Reverse;

pub fn find_kth_largest(nums: &[i32], k: usize) -> i32 {
    let mut heap: BinaryHeap<Reverse<i32>> = BinaryHeap::new();
    for &x in nums {
        heap.push(Reverse(x));
        if heap.len() > k { heap.pop(); }
    }
    heap.peek().map(|Reverse(v)| *v).unwrap_or_default()
}

pub fn top_k_frequent_heap(nums: &[i32], k: usize) -> Vec<i32> {
    let mut freq: HashMap<i32, i32> = HashMap::new();
    for &x in nums { *freq.entry(x).or_insert(0) += 1; }
    let mut heap: BinaryHeap<Reverse<(i32, i32)>> = BinaryHeap::new();
    for (v, c) in freq {
        heap.push(Reverse((c, v)));
        if heap.len() > k { heap.pop(); }
    }
    let mut out = Vec::new();
    while let Some(Reverse((_, v))) = heap.pop() { out.push(v); }
    out
}

pub fn top_k_frequent_bucket(nums: &[i32], k: usize) -> Vec<i32> {
    let mut freq: HashMap<i32, i32> = HashMap::new();
    for &x in nums { *freq.entry(x).or_insert(0) += 1; }
    let mut buckets: Vec<Vec<i32>> = vec![Vec::new(); nums.len() + 1];
    for (v, c) in freq { buckets[c as usize].push(v); }
    let mut out = Vec::new();
    for i in (0..buckets.len()).rev() {
        for &v in &buckets[i] {
            out.push(v);
            if out.len() == k { return out; }
        }
    }
    out
}

pub fn quickselect_kth_largest(mut nums: Vec<i32>, k: usize) -> i32 {
    let target = nums.len() - k;
    fn partition(nums: &mut [i32], lo: usize, hi: usize) -> usize {
        let pivot = nums[(lo + hi) / 2];
        let (mut i, mut j) = (lo as isize, hi as isize);
        while i <= j {
            while (nums[i as usize]) < pivot { i += 1; }
            while (nums[j as usize]) > pivot { j -= 1; }
            if i <= j {
                nums.swap(i as usize, j as usize);
                i += 1; j -= 1;
            }
        }
        i as usize
    }
    let (mut lo, mut hi) = (0usize, nums.len() - 1);
    while lo < hi {
        let idx = partition(&mut nums, lo, hi);
        if idx <= target { lo = idx; } else { hi = idx - 1; }
    }
    nums[target]
}

fn main() {
    println!("Kth largest k=2: {}", find_kth_largest(&[3,2,1,5,6,4], 2));
    let mut a = top_k_frequent_heap(&[1,1,1,2,2,3], 2);
    a.sort();
    println!("Top 2 frequent (heap): {:?}", a);
    let mut b = top_k_frequent_bucket(&[1,1,1,2,2,3], 2);
    b.sort();
    println!("Top 2 frequent (bucket): {:?}", b);
    println!("Quickselect kth=2: {}", quickselect_kth_largest(vec![3,2,1,5,6,4], 2));
}

// NOTES
// -----
// Differences from Java:
//   * BinaryHeap + Reverse for min-heap ordering.
//   * Adds quickselect (Hoare partition) as a third top-K technique.
