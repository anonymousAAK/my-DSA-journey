//! # Week 6: Arrays
//!
//! This module covers fundamental array algorithms implemented idiomatically in Rust.
//! Topics include:
//! - Reverse array (two-pointer technique on slices)
//! - Rotate array (reversal algorithm)
//! - Prefix sum and range sum query
//! - Kadane's algorithm (max subarray sum with indices)
//! - Dutch National Flag (sort 0s/1s/2s)
//! - Missing number (sum formula + XOR)
//! - Find duplicate (Floyd's cycle detection)
//!
//! ## Rust-Specific Notes for DSA Learners
//! - Rust slices (`&[T]` / `&mut [T]`) are the idiomatic way to work with contiguous
//!   sequences. They carry length information and are bounds-checked by default.
//! - The `swap` method on slices is safe and avoids manual temp-variable juggling.
//! - Iterators (`.iter()`, `.enumerate()`, `.windows()`) are zero-cost abstractions
//!   that often produce code as fast as hand-written loops.

// ---------------------------------------------------------------------------
// Reverse Array (Two Pointers)
// ---------------------------------------------------------------------------

/// Reverses a mutable slice in place using two pointers.
///
/// Rust's `slice::swap(i, j)` is the idiomatic way to swap elements without
/// needing `unsafe` or a temporary variable.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(1)
fn reverse_array(arr: &mut [i32]) {
    if arr.is_empty() {
        return;
    }
    let mut left = 0;
    let mut right = arr.len() - 1;
    while left < right {
        arr.swap(left, right);
        left += 1;
        right -= 1;
    }
}

// ---------------------------------------------------------------------------
// Rotate Array (Reversal Algorithm)
// ---------------------------------------------------------------------------

/// Rotates array to the right by `k` positions using the reversal algorithm.
///
/// Algorithm:
///   1. Reverse the entire array.
///   2. Reverse the first `k` elements.
///   3. Reverse the remaining `n - k` elements.
///
/// This works because reversing distributes elements into two correct-but-reversed
/// groups, and the second/third reverses fix each group.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(1)
fn rotate_array(arr: &mut [i32], k: usize) {
    let n = arr.len();
    if n == 0 {
        return;
    }
    let k = k % n; // Handle k > n
    if k == 0 {
        return;
    }
    arr.reverse();
    arr[..k].reverse();
    arr[k..].reverse();
}

// ---------------------------------------------------------------------------
// Prefix Sum + Range Sum Query
// ---------------------------------------------------------------------------

/// Builds a prefix-sum array where `prefix[i] = arr[0] + arr[1] + ... + arr[i-1]`.
///
/// We use `prefix[0] = 0` so that `range_sum(l, r) = prefix[r+1] - prefix[l]`.
///
/// # Complexity
/// - Time:  O(n) to build
/// - Space: O(n)
fn build_prefix_sum(arr: &[i32]) -> Vec<i64> {
    // Using `scan` — an iterator adaptor that carries state. Very idiomatic Rust.
    let mut prefix = Vec::with_capacity(arr.len() + 1);
    prefix.push(0i64);
    for &val in arr {
        let last = *prefix.last().unwrap();
        prefix.push(last + val as i64);
    }
    prefix
}

/// Returns the sum of elements in `arr[left..=right]` using a precomputed prefix sum.
///
/// # Complexity
/// - Time:  O(1) per query (after O(n) preprocessing)
/// - Space: O(1)
fn range_sum_query(prefix: &[i64], left: usize, right: usize) -> i64 {
    prefix[right + 1] - prefix[left]
}

// ---------------------------------------------------------------------------
// Kadane's Algorithm (Max Subarray Sum with Indices)
// ---------------------------------------------------------------------------

/// Finds the maximum subarray sum and returns `(max_sum, start_index, end_index)`.
///
/// Kadane's insight: at each position, either extend the current subarray or start
/// a new one. We track indices by recording where the current subarray began.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(1)
fn kadanes_algorithm(arr: &[i32]) -> (i64, usize, usize) {
    assert!(!arr.is_empty(), "Array must not be empty");

    let mut max_sum = arr[0] as i64;
    let mut current_sum = arr[0] as i64;
    let mut start = 0usize;
    let mut end = 0usize;
    let mut temp_start = 0usize;

    for i in 1..arr.len() {
        if current_sum + arr[i] as i64 < arr[i] as i64 {
            // Starting fresh from index i is better.
            current_sum = arr[i] as i64;
            temp_start = i;
        } else {
            current_sum += arr[i] as i64;
        }

        if current_sum > max_sum {
            max_sum = current_sum;
            start = temp_start;
            end = i;
        }
    }

    (max_sum, start, end)
}

// ---------------------------------------------------------------------------
// Dutch National Flag (Sort 0s, 1s, 2s)
// ---------------------------------------------------------------------------

/// Sorts an array containing only 0, 1, and 2 in a single pass.
///
/// Uses three pointers: `low`, `mid`, `high`.
/// - Elements before `low` are 0.
/// - Elements between `low` and `mid` are 1.
/// - Elements after `high` are 2.
/// - `mid` scans left to right, swapping elements into place.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(1)
fn dutch_national_flag(arr: &mut [i32]) {
    if arr.is_empty() {
        return;
    }
    let mut low: usize = 0;
    let mut mid: usize = 0;
    let mut high: usize = arr.len() - 1;

    // `while mid <= high` — note: since high is usize, underflow would wrap,
    // so we also check `high > 0 || mid == 0` implicitly via the condition.
    while mid <= high {
        match arr[mid] {
            0 => {
                arr.swap(low, mid);
                low += 1;
                mid += 1;
            }
            1 => {
                mid += 1;
            }
            2 => {
                arr.swap(mid, high);
                // Don't increment mid — the swapped element needs inspection.
                if high == 0 {
                    break; // Prevent usize underflow.
                }
                high -= 1;
            }
            _ => panic!("Array must contain only 0, 1, or 2"),
        }
    }
}

// ---------------------------------------------------------------------------
// Missing Number
// ---------------------------------------------------------------------------

/// Finds the missing number in `[0, n]` using the sum formula.
///
/// Given an array of `n` distinct numbers from `0..=n`, exactly one is missing.
/// `expected_sum - actual_sum = missing`.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(1)
fn missing_number_sum(nums: &[i32]) -> i32 {
    let n = nums.len() as i64;
    let expected_sum = n * (n + 1) / 2;
    let actual_sum: i64 = nums.iter().map(|&x| x as i64).sum();
    (expected_sum - actual_sum) as i32
}

/// Finds the missing number using XOR.
///
/// XOR of all numbers `0..=n` XOR all elements in the array leaves only the missing
/// number, because `x ^ x = 0` for every number that appears in both sets.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(1)
fn missing_number_xor(nums: &[i32]) -> i32 {
    let n = nums.len() as i32;
    let mut xor_all = 0i32;
    let mut xor_arr = 0i32;
    for i in 0..=n {
        xor_all ^= i;
    }
    for &num in nums {
        xor_arr ^= num;
    }
    xor_all ^ xor_arr
}

// ---------------------------------------------------------------------------
// Find Duplicate (Floyd's Cycle Detection)
// ---------------------------------------------------------------------------

/// Finds a duplicate number in an array of `n+1` integers where each integer is
/// in `[1, n]`. Uses Floyd's tortoise-and-hare algorithm — the array is treated
/// as a linked list where `arr[i]` points to the next node.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(1) — no extra data structures
fn find_duplicate(nums: &[i32]) -> i32 {
    // Phase 1: Detect cycle.
    let mut slow = nums[0] as usize;
    let mut fast = nums[0] as usize;
    loop {
        slow = nums[slow] as usize;
        fast = nums[nums[fast] as usize] as usize;
        if slow == fast {
            break;
        }
    }

    // Phase 2: Find the entrance to the cycle (= the duplicate).
    let mut slow = nums[0] as usize;
    while slow != fast {
        slow = nums[slow] as usize;
        fast = nums[fast] as usize;
    }
    slow as i32
}

// ===========================================================================
// Main — demonstrations and test assertions
// ===========================================================================

fn main() {
    println!("=== Week 6: Arrays ===\n");

    // --- Reverse Array ---
    println!("--- Reverse Array ---");
    let mut arr = vec![1, 2, 3, 4, 5];
    reverse_array(&mut arr);
    assert_eq!(arr, vec![5, 4, 3, 2, 1]);
    println!("Reversed: {:?}", arr);

    let mut single = vec![42];
    reverse_array(&mut single);
    assert_eq!(single, vec![42]);

    let mut empty: Vec<i32> = vec![];
    reverse_array(&mut empty);
    assert_eq!(empty, vec![]);

    // --- Rotate Array ---
    println!("\n--- Rotate Array ---");
    let mut arr = vec![1, 2, 3, 4, 5, 6, 7];
    rotate_array(&mut arr, 3);
    assert_eq!(arr, vec![5, 6, 7, 1, 2, 3, 4]);
    println!("Rotated right by 3: {:?}", arr);

    let mut arr2 = vec![1, 2, 3];
    rotate_array(&mut arr2, 5); // k > n, effectively rotate by 2
    assert_eq!(arr2, vec![2, 3, 1]);
    println!("Rotated right by 5 (mod 3 = 2): {:?}", arr2);

    // --- Prefix Sum ---
    println!("\n--- Prefix Sum & Range Sum Query ---");
    let data = vec![1, 3, 5, 7, 9, 11];
    let prefix = build_prefix_sum(&data);
    assert_eq!(range_sum_query(&prefix, 0, 2), 9);  // 1 + 3 + 5
    assert_eq!(range_sum_query(&prefix, 1, 4), 24); // 3 + 5 + 7 + 9
    assert_eq!(range_sum_query(&prefix, 0, 5), 36); // entire array
    println!("sum(data[0..=2]) = {}", range_sum_query(&prefix, 0, 2));
    println!("sum(data[1..=4]) = {}", range_sum_query(&prefix, 1, 4));

    // --- Kadane's Algorithm ---
    println!("\n--- Kadane's Algorithm ---");
    let arr = vec![-2, 1, -3, 4, -1, 2, 1, -5, 4];
    let (max_sum, start, end) = kadanes_algorithm(&arr);
    assert_eq!(max_sum, 6); // subarray [4, -1, 2, 1]
    assert_eq!(start, 3);
    assert_eq!(end, 6);
    println!(
        "Max subarray sum = {}, indices [{}, {}], subarray = {:?}",
        max_sum, start, end, &arr[start..=end]
    );

    // All negative
    let arr_neg = vec![-5, -3, -8, -1, -4];
    let (max_sum_neg, s, e) = kadanes_algorithm(&arr_neg);
    assert_eq!(max_sum_neg, -1);
    println!("All negative: max = {}, subarray = {:?}", max_sum_neg, &arr_neg[s..=e]);

    // --- Dutch National Flag ---
    println!("\n--- Dutch National Flag ---");
    let mut colors = vec![2, 0, 1, 2, 0, 1, 1, 0, 2];
    dutch_national_flag(&mut colors);
    assert_eq!(colors, vec![0, 0, 0, 1, 1, 1, 2, 2, 2]);
    println!("Sorted colors: {:?}", colors);

    let mut colors2 = vec![0];
    dutch_national_flag(&mut colors2);
    assert_eq!(colors2, vec![0]);

    // --- Missing Number ---
    println!("\n--- Missing Number ---");
    let nums = vec![3, 0, 1]; // missing 2
    assert_eq!(missing_number_sum(&nums), 2);
    assert_eq!(missing_number_xor(&nums), 2);
    println!("Missing from [3,0,1]: {} (sum), {} (xor)", missing_number_sum(&nums), missing_number_xor(&nums));

    let nums2 = vec![0, 1, 2, 3, 5]; // missing 4
    assert_eq!(missing_number_sum(&nums2), 4);
    assert_eq!(missing_number_xor(&nums2), 4);
    println!("Missing from [0,1,2,3,5]: {}", missing_number_sum(&nums2));

    // --- Find Duplicate ---
    println!("\n--- Find Duplicate (Floyd's Cycle Detection) ---");
    let nums = vec![1, 3, 4, 2, 2];
    assert_eq!(find_duplicate(&nums), 2);
    println!("Duplicate in [1,3,4,2,2]: {}", find_duplicate(&nums));

    let nums2 = vec![3, 1, 3, 4, 2];
    assert_eq!(find_duplicate(&nums2), 3);
    println!("Duplicate in [3,1,3,4,2]: {}", find_duplicate(&nums2));

    println!("\nAll assertions passed!");
}
