// WEEK 30 - RUST ADVANCED TOPICS
// Topic: Sliding Window Pattern
// File: sliding_window.rs
//
// CONCEPT:
//   Maintain a window [l, r] over a sequence; grow on the right, shrink on
//   the left when an invariant breaks. Each element enters/leaves the
//   window at most once -> O(n).
//
// KEY POINTS:
//   - Common state: HashMap of counts, running sum, monotonic deque.
//   - Canonical: longest unique substring (LC 3), min window (LC 76),
//     longest k-distinct (LC 340), max sliding window (LC 239).
//
// ALGORITHM / APPROACH:
//   for r in 0..n: add a[r]; while invariant violated: remove a[l]; l+=1
//
// RUST-SPECIFIC NOTES:
//   - HashMap<char, i32> for count maps; VecDeque<usize> for indices.
//   - Use s.chars().enumerate() for index/char iteration; for byte-level
//     work convert to bytes() for O(1) lookup.
//
// DRY RUN / EXAMPLE:
//   "abcabcbb" -> 3.  min_window("ADOBECODEBANC","ABC") -> "BANC".
//   max_sliding_window([1,3,-1,-3,5,3,6,7], 3) -> [3,3,5,5,6,7].
//
// COMPLEXITY:
//   Time O(n). Space O(charset) or O(window).

use std::collections::{HashMap, VecDeque};

pub fn length_of_longest_substring(s: &str) -> usize {
    let bytes = s.as_bytes();
    let mut last: HashMap<u8, usize> = HashMap::new();
    let mut left = 0usize;
    let mut best = 0usize;
    for (r, &c) in bytes.iter().enumerate() {
        if let Some(&p) = last.get(&c) {
            if p >= left { left = p + 1; }
        }
        last.insert(c, r);
        if r - left + 1 > best { best = r - left + 1; }
    }
    best
}

pub fn min_window(s: &str, t: &str) -> String {
    let s = s.as_bytes(); let t = t.as_bytes();
    if t.is_empty() || s.len() < t.len() { return String::new(); }
    let mut need: HashMap<u8, i32> = HashMap::new();
    for &c in t { *need.entry(c).or_insert(0) += 1; }
    let required = need.len();
    let mut formed = 0;
    let mut window: HashMap<u8, i32> = HashMap::new();
    let mut left = 0usize;
    let mut best_len = usize::MAX;
    let mut best_left = 0usize;
    for (r, &c) in s.iter().enumerate() {
        *window.entry(c).or_insert(0) += 1;
        if let Some(&n) = need.get(&c) {
            if window[&c] == n { formed += 1; }
        }
        while formed == required {
            if r - left + 1 < best_len {
                best_len = r - left + 1;
                best_left = left;
            }
            let lc = s[left];
            *window.get_mut(&lc).unwrap() -= 1;
            if let Some(&n) = need.get(&lc) {
                if window[&lc] < n { formed -= 1; }
            }
            left += 1;
        }
    }
    if best_len == usize::MAX { String::new() }
    else { String::from_utf8_lossy(&s[best_left..best_left + best_len]).into_owned() }
}

pub fn longest_k_distinct(s: &str, k: usize) -> usize {
    if k == 0 || s.is_empty() { return 0; }
    let s = s.as_bytes();
    let mut counts: HashMap<u8, i32> = HashMap::new();
    let mut left = 0usize;
    let mut best = 0usize;
    for (r, &c) in s.iter().enumerate() {
        *counts.entry(c).or_insert(0) += 1;
        while counts.len() > k {
            let lc = s[left];
            *counts.get_mut(&lc).unwrap() -= 1;
            if counts[&lc] == 0 { counts.remove(&lc); }
            left += 1;
        }
        if r - left + 1 > best { best = r - left + 1; }
    }
    best
}

pub fn max_sliding_window(nums: &[i32], k: usize) -> Vec<i32> {
    let mut dq: VecDeque<usize> = VecDeque::new();
    let mut out = Vec::new();
    for (i, &x) in nums.iter().enumerate() {
        while let Some(&back) = dq.back() {
            if nums[back] <= x { dq.pop_back(); } else { break; }
        }
        dq.push_back(i);
        if let Some(&front) = dq.front() {
            if i >= k && front + k == i { dq.pop_front(); }
        }
        if i + 1 >= k { out.push(nums[*dq.front().unwrap()]); }
    }
    out
}

fn main() {
    println!("Longest unique 'abcabcbb': {}", length_of_longest_substring("abcabcbb"));
    println!("Min window 'ADOBECODEBANC','ABC': \"{}\"", min_window("ADOBECODEBANC", "ABC"));
    println!("Longest 2-distinct 'eceba': {}", longest_k_distinct("eceba", 2));
    println!("Max sliding window k=3: {:?}",
             max_sliding_window(&[1,3,-1,-3,5,3,6,7], 3));
}

// NOTES
// -----
// Differences from Java:
//   * HashMap<u8, i32> — operate on bytes for O(1) lookup; works for ASCII.
//   * VecDeque<usize> for the monotonic-index deque.
//   * Adds longest_k_distinct (LC 340) and max_sliding_window (LC 239).
