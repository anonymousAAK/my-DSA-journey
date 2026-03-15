//! # Week 16: Hash Tables and Hashing
//!
//! Hash tables provide average O(1) lookup, insertion, and deletion by mapping
//! keys to array indices via a hash function.
//!
//! ## Rust's Standard Library
//! - `HashMap<K, V>` — key-value store with O(1) average operations
//! - `HashSet<T>` — set of unique values with O(1) average membership test
//!
//! Both use SipHash by default (DoS-resistant but slightly slower than
//! non-cryptographic hashes).
//!
//! ## Complexity Summary
//! | Operation                    | Time (avg) | Time (worst) | Space |
//! |-----------------------------|------------|--------------|-------|
//! | two_sum                     | O(n)       | O(n)         | O(n)  |
//! | frequency_count             | O(n)       | O(n)         | O(n)  |
//! | group_anagrams              | O(n*k log k)| O(n*k log k)| O(n*k)|
//! | subarray_sum_equals_k       | O(n)       | O(n)         | O(n)  |
//! | longest_consecutive_sequence| O(n)       | O(n)         | O(n)  |

use std::collections::{HashMap, HashSet};

// =============================================================================
// Two Sum — Classic HashMap one-pass approach
// =============================================================================

/// Given a slice of integers and a target sum, returns the indices of two
/// numbers that add up to the target.
///
/// # Algorithm
/// For each element, check if `target - element` is already in the map.
/// If yes, we found our pair. Otherwise, store `(element, index)`.
///
/// # Complexity
/// - Time: O(n) — single pass with O(1) hash lookups
/// - Space: O(n) — at most n entries in the map
///
/// # Ownership Note
/// Takes `&[i32]` (a shared slice reference) — we only need to read the data.
/// Returning `Option<(usize, usize)>` avoids needing to allocate.
fn two_sum(nums: &[i32], target: i32) -> Option<(usize, usize)> {
    let mut seen: HashMap<i32, usize> = HashMap::new();

    for (i, &num) in nums.iter().enumerate() {
        let complement = target - num;
        if let Some(&j) = seen.get(&complement) {
            return Some((j, i));
        }
        seen.insert(num, i);
    }

    None
}

// =============================================================================
// Frequency Count
// =============================================================================

/// Counts the frequency of each element in a slice.
///
/// # Complexity
/// - Time: O(n)
/// - Space: O(k) where k is the number of distinct elements
///
/// # Rust Idiom
/// The `entry` API avoids double lookups: `entry(key).or_insert(0)` returns
/// a mutable reference to the value, inserting a default if the key is absent.
fn frequency_count(nums: &[i32]) -> HashMap<i32, usize> {
    let mut freq: HashMap<i32, usize> = HashMap::new();
    for &num in nums {
        *freq.entry(num).or_insert(0) += 1;
    }
    freq
}

// =============================================================================
// Group Anagrams
// =============================================================================

/// Groups strings that are anagrams of each other.
///
/// # Algorithm
/// Two strings are anagrams if they have the same characters in sorted order.
/// Use the sorted string as a HashMap key to group anagrams together.
///
/// # Complexity
/// - Time: O(n * k log k) where n = number of strings, k = max string length
/// - Space: O(n * k)
///
/// # Ownership Note
/// Takes `&[String]` — borrows the input strings. We clone strings into the
/// result groups since we cannot move data out of a shared reference.
fn group_anagrams(strs: &[String]) -> Vec<Vec<String>> {
    let mut groups: HashMap<String, Vec<String>> = HashMap::new();

    for s in strs {
        // Sort the characters to create a canonical key
        let mut chars: Vec<char> = s.chars().collect();
        chars.sort_unstable();
        let key: String = chars.into_iter().collect();

        groups.entry(key).or_insert_with(Vec::new).push(s.clone());
    }

    // Collect all groups into a Vec (order is not guaranteed)
    groups.into_values().collect()
}

// =============================================================================
// Subarray Sum Equals K — Prefix sum + HashMap
// =============================================================================

/// Counts the number of contiguous subarrays whose elements sum to `k`.
///
/// # Algorithm
/// Maintain a running prefix sum. At each index, the number of subarrays
/// ending here with sum `k` equals the number of times `prefix_sum - k`
/// has appeared as a previous prefix sum.
///
/// Key insight: if `prefix[j] - prefix[i] == k`, then `sum(arr[i+1..=j]) == k`.
///
/// # Complexity
/// - Time: O(n) — single pass
/// - Space: O(n) — prefix sum counts in the map
fn subarray_sum_equals_k(nums: &[i32], k: i32) -> i32 {
    let mut count = 0;
    let mut prefix_sum = 0;
    // Map from prefix_sum value -> number of times it has occurred
    let mut prefix_counts: HashMap<i32, i32> = HashMap::new();

    // Base case: a prefix sum of 0 has occurred once (empty prefix)
    prefix_counts.insert(0, 1);

    for &num in nums {
        prefix_sum += num;

        // How many previous prefix sums equal (prefix_sum - k)?
        // Each one represents a subarray summing to k.
        if let Some(&c) = prefix_counts.get(&(prefix_sum - k)) {
            count += c;
        }

        *prefix_counts.entry(prefix_sum).or_insert(0) += 1;
    }

    count
}

// =============================================================================
// Longest Consecutive Sequence — HashSet approach
// =============================================================================

/// Finds the length of the longest consecutive element sequence.
///
/// # Algorithm
/// 1. Insert all numbers into a HashSet for O(1) lookups.
/// 2. For each number, check if it is the START of a sequence (i.e., `num - 1`
///    is NOT in the set). If so, count how far the sequence extends.
/// 3. This ensures each element is visited at most twice total → O(n).
///
/// # Complexity
/// - Time: O(n) — although there's a nested loop, each element is part of
///   exactly one sequence and visited at most twice across all iterations
/// - Space: O(n) — for the HashSet
fn longest_consecutive_sequence(nums: &[i32]) -> i32 {
    let num_set: HashSet<i32> = nums.iter().copied().collect();
    let mut best = 0;

    for &num in &num_set {
        // Only start counting from the beginning of a sequence
        if !num_set.contains(&(num - 1)) {
            let mut current = num;
            let mut length = 1;

            while num_set.contains(&(current + 1)) {
                current += 1;
                length += 1;
            }

            best = best.max(length);
        }
    }

    best
}

// =============================================================================
// Main — Test cases
// =============================================================================

fn main() {
    println!("=== Week 16: Hashing ===\n");

    // --- Two Sum ---
    println!("--- Two Sum ---");
    let nums = vec![2, 7, 11, 15];
    let result = two_sum(&nums, 9);
    println!("two_sum([2,7,11,15], 9) = {:?}", result);
    assert_eq!(result, Some((0, 1)));

    let result2 = two_sum(&[3, 2, 4], 6);
    println!("two_sum([3,2,4], 6) = {:?}", result2);
    assert_eq!(result2, Some((1, 2)));

    assert_eq!(two_sum(&[1, 2, 3], 10), None);
    println!("PASS: Two sum works correctly\n");

    // --- Frequency Count ---
    println!("--- Frequency Count ---");
    let freq = frequency_count(&[1, 2, 2, 3, 3, 3, 4, 4, 4, 4]);
    println!("Frequencies: {:?}", freq);
    assert_eq!(freq[&1], 1);
    assert_eq!(freq[&2], 2);
    assert_eq!(freq[&3], 3);
    assert_eq!(freq[&4], 4);
    println!("PASS: Frequency count works correctly\n");

    // --- Group Anagrams ---
    println!("--- Group Anagrams ---");
    let words: Vec<String> = vec!["eat", "tea", "tan", "ate", "nat", "bat"]
        .into_iter()
        .map(String::from)
        .collect();
    let mut groups = group_anagrams(&words);
    // Sort each group and the outer vec for deterministic comparison
    for g in &mut groups {
        g.sort();
    }
    groups.sort_by(|a, b| a[0].cmp(&b[0]));
    println!("Grouped anagrams: {:?}", groups);
    assert_eq!(groups.len(), 3);
    println!("PASS: Group anagrams works correctly\n");

    // --- Subarray Sum Equals K ---
    println!("--- Subarray Sum Equals K ---");
    let count = subarray_sum_equals_k(&[1, 1, 1], 2);
    println!("subarray_sum_equals_k([1,1,1], 2) = {}", count);
    assert_eq!(count, 2);

    let count2 = subarray_sum_equals_k(&[1, 2, 3], 3);
    println!("subarray_sum_equals_k([1,2,3], 3) = {}", count2);
    assert_eq!(count2, 2); // [1,2] and [3]

    let count3 = subarray_sum_equals_k(&[1, -1, 0], 0);
    println!("subarray_sum_equals_k([1,-1,0], 0) = {}", count3);
    assert_eq!(count3, 3); // [1,-1], [1,-1,0], [0]
    println!("PASS: Subarray sum equals k works correctly\n");

    // --- Longest Consecutive Sequence ---
    println!("--- Longest Consecutive Sequence ---");
    let result = longest_consecutive_sequence(&[100, 4, 200, 1, 3, 2]);
    println!("longest_consecutive([100,4,200,1,3,2]) = {}", result);
    assert_eq!(result, 4); // Sequence: 1,2,3,4

    let result2 = longest_consecutive_sequence(&[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]);
    println!("longest_consecutive([0,3,7,2,5,8,4,6,0,1]) = {}", result2);
    assert_eq!(result2, 9); // Sequence: 0-8

    let result3 = longest_consecutive_sequence(&[]);
    assert_eq!(result3, 0);
    println!("PASS: Longest consecutive sequence works correctly\n");

    println!("All Week 16 tests passed!");
}
