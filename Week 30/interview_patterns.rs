// Week 30: Interview Patterns
use std::collections::{BinaryHeap, HashMap};
use std::cmp::Reverse;

// Two Sum II (LC 167) - O(n)
fn two_sum(nums: &[i32], target: i32) -> Vec<usize> {
    let (mut l, mut r) = (0, nums.len()-1);
    while l < r {
        let s = nums[l] + nums[r];
        if s == target { return vec![l, r]; }
        if s < target { l += 1; } else { r -= 1; }
    }
    vec![]
}

// Longest Substring Without Repeating (LC 3) - O(n)
fn length_of_longest_substring(s: &str) -> usize {
    let mut idx: HashMap<char, usize> = HashMap::new();
    let chars: Vec<char> = s.chars().collect();
    let (mut left, mut mx) = (0, 0);
    for r in 0..chars.len() {
        if let Some(&prev) = idx.get(&chars[r]) {
            if prev >= left { left = prev + 1; }
        }
        idx.insert(chars[r], r);
        mx = mx.max(r - left + 1);
    }
    mx
}

// Happy Number (LC 202) - O(log n)
fn next_num(mut n: i32) -> i32 {
    let mut t = 0;
    while n > 0 { let d = n % 10; t += d * d; n /= 10; }
    t
}
fn is_happy(n: i32) -> bool {
    let (mut slow, mut fast) = (n, next_num(n));
    while fast != 1 && slow != fast {
        slow = next_num(slow);
        fast = next_num(next_num(fast));
    }
    fast == 1
}

// Merge Intervals (LC 56) - O(n log n)
fn merge(intervals: &mut Vec<Vec<i32>>) -> Vec<Vec<i32>> {
    intervals.sort();
    let mut merged = vec![intervals[0].clone()];
    for interval in intervals.iter().skip(1) {
        let last = merged.last_mut().unwrap();
        if interval[0] <= last[1] { last[1] = last[1].max(interval[1]); }
        else { merged.push(interval.clone()); }
    }
    merged
}

// Kth Largest (LC 215) - O(n log k)
fn find_kth_largest(nums: &[i32], k: usize) -> i32 {
    let mut heap: BinaryHeap<Reverse<i32>> = BinaryHeap::new();
    for &n in nums { heap.push(Reverse(n)); if heap.len() > k { heap.pop(); } }
    heap.peek().unwrap().0
}

fn main() {
    println!("Two Sum: {:?}", two_sum(&[2,7,11,15], 9));
    println!("Longest substring: {}", length_of_longest_substring("abcabcbb"));
    println!("Happy 19: {}", is_happy(19));
    let mut intervals = vec![vec![1,3],vec![2,6],vec![8,10],vec![15,18]];
    println!("Merge: {:?}", merge(&mut intervals));
    println!("3rd largest: {}", find_kth_largest(&[3,2,1,5,6,4], 3));
}
