// Week 30: Interview Patterns & Mastery
// Two Pointers, Sliding Window, Fast & Slow Pointers, Merge Intervals, Top-K Elements

use std::collections::{BinaryHeap, HashMap};
use std::cmp::Reverse;

// =========================================================================
// TWO POINTERS
// =========================================================================

/// Two Sum II - sorted array (LC 167) - Time: O(n), Space: O(1)
fn two_sum_ii(nums: &[i32], target: i32) -> Vec<i32> {
    let (mut l, mut r) = (0usize, nums.len() - 1);
    while l < r {
        let s = nums[l] + nums[r];
        if s == target { return vec![l as i32 + 1, r as i32 + 1]; } // 1-indexed
        if s < target { l += 1; } else { r -= 1; }
    }
    vec![]
}

/// 3Sum (LC 15) - Time: O(n^2), Space: O(1) extra
fn three_sum(nums: &mut Vec<i32>) -> Vec<Vec<i32>> {
    let mut result = Vec::new();
    nums.sort();
    let n = nums.len();
    for i in 0..n.saturating_sub(2) {
        if i > 0 && nums[i] == nums[i - 1] { continue; }
        let (mut l, mut r) = (i + 1, n - 1);
        while l < r {
            let s = nums[i] + nums[l] + nums[r];
            if s == 0 {
                result.push(vec![nums[i], nums[l], nums[r]]);
                while l < r && nums[l] == nums[l + 1] { l += 1; }
                while l < r && nums[r] == nums[r - 1] { r -= 1; }
                l += 1; r -= 1;
            } else if s < 0 { l += 1; }
            else { r -= 1; }
        }
    }
    result
}

/// Container With Most Water (LC 11) - Time: O(n), Space: O(1)
fn max_area(height: &[i32]) -> i32 {
    let (mut l, mut r) = (0usize, height.len() - 1);
    let mut best = 0;
    while l < r {
        best = best.max((r - l) as i32 * height[l].min(height[r]));
        if height[l] < height[r] { l += 1; } else { r -= 1; }
    }
    best
}

// =========================================================================
// SLIDING WINDOW
// =========================================================================

/// Longest Substring Without Repeating Characters (LC 3) - Time: O(n), Space: O(min(n, charset))
fn length_of_longest_substring(s: &str) -> usize {
    let mut idx: HashMap<u8, usize> = HashMap::new();
    let bytes = s.as_bytes();
    let (mut left, mut mx) = (0usize, 0usize);
    for r in 0..bytes.len() {
        if let Some(&prev) = idx.get(&bytes[r]) {
            if prev >= left { left = prev + 1; }
        }
        idx.insert(bytes[r], r);
        mx = mx.max(r - left + 1);
    }
    mx
}

/// Minimum Window Substring (LC 76) - Time: O(n + m), Space: O(m)
fn min_window(s: &str, t: &str) -> String {
    if s.len() < t.len() { return String::new(); }
    let sb = s.as_bytes();
    let mut need: HashMap<u8, i32> = HashMap::new();
    for &b in t.as_bytes() { *need.entry(b).or_insert(0) += 1; }

    let required = need.len();
    let mut formed = 0usize;
    let mut window: HashMap<u8, i32> = HashMap::new();
    let mut left = 0usize;
    let mut best_len = usize::MAX;
    let mut best_left = 0usize;

    for r in 0..sb.len() {
        let c = sb[r];
        *window.entry(c).or_insert(0) += 1;
        if let Some(&needed) = need.get(&c) {
            if window[&c] == needed { formed += 1; }
        }
        while formed == required {
            if r - left + 1 < best_len {
                best_len = r - left + 1;
                best_left = left;
            }
            let lc = sb[left];
            *window.get_mut(&lc).unwrap() -= 1;
            if let Some(&needed) = need.get(&lc) {
                if window[&lc] < needed { formed -= 1; }
            }
            left += 1;
        }
    }
    if best_len == usize::MAX { String::new() }
    else { s[best_left..best_left + best_len].to_string() }
}

// =========================================================================
// FAST & SLOW POINTERS
// =========================================================================

// Note: Rust ownership makes linked-list cycles unsafe. We use array-based
// simulation for cycle detection and demonstrate Happy Number naturally.

/// Linked List Cycle Detection - array-based (LC 141) - Time: O(n), Space: O(1)
/// nums[i] gives index of next node; -1 means null.
fn has_cycle_array(nums: &[i32], head: usize) -> bool {
    let (mut slow, mut fast) = (head as i32, head as i32);
    loop {
        if slow < 0 || slow as usize >= nums.len() { return false; }
        slow = nums[slow as usize];
        if fast < 0 || fast as usize >= nums.len() { return false; }
        fast = nums[fast as usize];
        if fast < 0 || fast as usize >= nums.len() { return false; }
        fast = nums[fast as usize];
        if slow == fast { return true; }
    }
}

/// Cycle Start Detection - array-based (LC 142) - Time: O(n), Space: O(1)
fn detect_cycle_start_array(nums: &[i32], head: usize) -> i32 {
    let (mut slow, mut fast) = (head as i32, head as i32);
    loop {
        if slow < 0 || slow as usize >= nums.len() { return -1; }
        slow = nums[slow as usize];
        if fast < 0 || fast as usize >= nums.len() { return -1; }
        fast = nums[fast as usize];
        if fast < 0 || fast as usize >= nums.len() { return -1; }
        fast = nums[fast as usize];
        if slow == fast {
            let mut entry = head as i32;
            while entry != slow {
                entry = nums[entry as usize];
                slow = nums[slow as usize];
            }
            return entry;
        }
    }
}

/// Happy Number (LC 202) - Time: O(log n), Space: O(1)
fn is_happy(n: i32) -> bool {
    fn digit_square_sum(mut x: i32) -> i32 {
        let mut t = 0;
        while x > 0 { let d = x % 10; t += d * d; x /= 10; }
        t
    }
    let (mut slow, mut fast) = (n, n);
    loop {
        slow = digit_square_sum(slow);
        fast = digit_square_sum(digit_square_sum(fast));
        if slow == fast { break; }
    }
    slow == 1
}

// =========================================================================
// MERGE INTERVALS
// =========================================================================

/// Merge Intervals (LC 56) - Time: O(n log n), Space: O(n)
fn merge_intervals(intervals: &mut Vec<Vec<i32>>) -> Vec<Vec<i32>> {
    intervals.sort();
    let mut merged = vec![intervals[0].clone()];
    for iv in intervals.iter().skip(1) {
        let last = merged.last_mut().unwrap();
        if iv[0] <= last[1] { last[1] = last[1].max(iv[1]); }
        else { merged.push(iv.clone()); }
    }
    merged
}

/// Insert Interval (LC 57) - Time: O(n), Space: O(n)
fn insert_interval(intervals: &[Vec<i32>], new_interval: &[i32]) -> Vec<Vec<i32>> {
    let mut result: Vec<Vec<i32>> = Vec::new();
    let (mut new_s, mut new_e) = (new_interval[0], new_interval[1]);
    let (mut i, n) = (0, intervals.len());

    // Add intervals ending before new_interval starts
    while i < n && intervals[i][1] < new_s { result.push(intervals[i].clone()); i += 1; }

    // Merge overlapping
    while i < n && intervals[i][0] <= new_e {
        new_s = new_s.min(intervals[i][0]);
        new_e = new_e.max(intervals[i][1]);
        i += 1;
    }
    result.push(vec![new_s, new_e]);

    // Add remaining
    while i < n { result.push(intervals[i].clone()); i += 1; }
    result
}

// =========================================================================
// TOP-K ELEMENTS
// =========================================================================

/// Kth Largest Element (LC 215) - Time: O(n log k), Space: O(k)
fn find_kth_largest(nums: &[i32], k: usize) -> i32 {
    let mut heap: BinaryHeap<Reverse<i32>> = BinaryHeap::new();
    for &n in nums {
        heap.push(Reverse(n));
        if heap.len() > k { heap.pop(); }
    }
    heap.peek().unwrap().0
}

/// Top K Frequent Elements (LC 347) - Time: O(n log k), Space: O(n)
fn top_k_frequent(nums: &[i32], k: usize) -> Vec<i32> {
    let mut freq: HashMap<i32, usize> = HashMap::new();
    for &n in nums { *freq.entry(n).or_insert(0) += 1; }

    let mut heap: BinaryHeap<Reverse<(usize, i32)>> = BinaryHeap::new();
    for (&val, &cnt) in &freq {
        heap.push(Reverse((cnt, val)));
        if heap.len() > k { heap.pop(); }
    }
    heap.into_iter().map(|Reverse((_, v))| v).collect()
}

/// Top K Frequent - Bucket Sort (LC 347) - Time: O(n), Space: O(n)
fn top_k_frequent_bucket(nums: &[i32], k: usize) -> Vec<i32> {
    let mut freq: HashMap<i32, usize> = HashMap::new();
    for &n in nums { *freq.entry(n).or_insert(0) += 1; }

    let n = nums.len();
    let mut buckets: Vec<Vec<i32>> = vec![Vec::new(); n + 1];
    for (&val, &cnt) in &freq { buckets[cnt].push(val); }

    let mut result = Vec::new();
    for i in (0..=n).rev() {
        for &val in &buckets[i] {
            result.push(val);
            if result.len() == k { return result; }
        }
    }
    result
}

// =========================================================================
// MAIN
// =========================================================================

fn main() {
    println!("=== TWO POINTERS ===");
    println!("Two Sum II [2,7,11,15] t=9: {:?}", two_sum_ii(&[2, 7, 11, 15], 9));
    let mut nums3 = vec![-1, 0, 1, 2, -1, -4];
    println!("3Sum: {:?}", three_sum(&mut nums3));
    println!("Max Area [1,8,6,2,5,4,8,3,7]: {}", max_area(&[1, 8, 6, 2, 5, 4, 8, 3, 7]));

    println!("\n=== SLIDING WINDOW ===");
    println!("Longest unique 'abcabcbb': {}", length_of_longest_substring("abcabcbb"));
    println!("Min window 'ADOBECODEBANC','ABC': {}", min_window("ADOBECODEBANC", "ABC"));

    println!("\n=== FAST & SLOW ===");
    println!("Happy 19: {}", is_happy(19));
    println!("Happy 2: {}", is_happy(2));
    // Array-based linked list: 0->1->2->1 (cycle at index 1)
    let linked = vec![1, 2, 1]; // next pointers
    println!("Cycle: {}, starts at index: {}", has_cycle_array(&linked, 0), detect_cycle_start_array(&linked, 0));

    println!("\n=== MERGE INTERVALS ===");
    let mut intervals = vec![vec![1,3], vec![2,6], vec![8,10], vec![15,18]];
    println!("Merged: {:?}", merge_intervals(&mut intervals));
    println!("Inserted: {:?}", insert_interval(&[vec![1,3], vec![6,9]], &[2, 5]));

    println!("\n=== TOP-K ===");
    println!("Kth largest k=2: {}", find_kth_largest(&[3,2,1,5,6,4], 2));
    println!("Top 2 frequent: {:?}", top_k_frequent(&[1,1,1,2,2,3], 2));
    println!("Top 2 bucket: {:?}", top_k_frequent_bucket(&[1,1,1,2,2,3], 2));
}
