//! # Week 8: Searching
//!
//! This module covers binary search and its applications in Rust.
//! Topics include:
//! - Binary search (iterative + recursive on `&[i32]`)
//! - First and last occurrence in a sorted array
//! - Count occurrences of a target
//! - Search in a rotated sorted array
//! - Binary search on answer: integer sqrt, min eating speed, min ship capacity
//!
//! ## Rust-Specific Notes for DSA Learners
//! - Slices (`&[i32]`) carry their length and support range indexing `&arr[l..r]`.
//! - Rust's standard library has `slice::binary_search()` but we implement from scratch.
//! - `usize` is unsigned — be careful with `mid - 1` when `mid == 0` (underflow!).
//!   We handle this by using checked arithmetic or restructuring bounds.
//! - Return types use `Option<usize>` to represent "not found" — much safer than
//!   returning -1 like in C/Java.

// ---------------------------------------------------------------------------
// Binary Search — Iterative
// ---------------------------------------------------------------------------

/// Standard binary search on a sorted slice. Returns `Some(index)` if found.
///
/// # Complexity
/// - Time:  O(log n)
/// - Space: O(1)
fn binary_search(arr: &[i32], target: i32) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }
    let mut left = 0usize;
    let mut right = arr.len() - 1;

    while left <= right {
        // Use `left + (right - left) / 2` to avoid potential overflow (though
        // usize on 64-bit can hold any realistic array index).
        let mid = left + (right - left) / 2;

        match arr[mid].cmp(&target) {
            std::cmp::Ordering::Equal => return Some(mid),
            std::cmp::Ordering::Less => left = mid + 1,
            std::cmp::Ordering::Greater => {
                if mid == 0 {
                    break; // Prevent usize underflow
                }
                right = mid - 1;
            }
        }
    }
    None
}

// ---------------------------------------------------------------------------
// Binary Search — Recursive
// ---------------------------------------------------------------------------

/// Recursive binary search. Returns `Some(index)` if found.
///
/// Note: We pass the original offset so we can return the index relative to the
/// full array, not the sub-slice.
///
/// # Complexity
/// - Time:  O(log n)
/// - Space: O(log n) — call-stack depth
fn binary_search_recursive(arr: &[i32], target: i32, offset: usize) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }
    let mid = arr.len() / 2;

    match arr[mid].cmp(&target) {
        std::cmp::Ordering::Equal => Some(offset + mid),
        std::cmp::Ordering::Less => {
            binary_search_recursive(&arr[mid + 1..], target, offset + mid + 1)
        }
        std::cmp::Ordering::Greater => {
            binary_search_recursive(&arr[..mid], target, offset)
        }
    }
}

// ---------------------------------------------------------------------------
// First Occurrence
// ---------------------------------------------------------------------------

/// Finds the index of the first occurrence of `target` in a sorted array.
///
/// Even when we find `target`, we keep searching left to find the earliest index.
///
/// # Complexity
/// - Time:  O(log n)
/// - Space: O(1)
fn first_occurrence(arr: &[i32], target: i32) -> Option<usize> {
    let mut left = 0usize;
    let mut right = arr.len();
    let mut result: Option<usize> = None;

    while left < right {
        let mid = left + (right - left) / 2;
        match arr[mid].cmp(&target) {
            std::cmp::Ordering::Equal => {
                result = Some(mid);
                right = mid; // Keep searching left
            }
            std::cmp::Ordering::Less => left = mid + 1,
            std::cmp::Ordering::Greater => right = mid,
        }
    }
    result
}

// ---------------------------------------------------------------------------
// Last Occurrence
// ---------------------------------------------------------------------------

/// Finds the index of the last occurrence of `target` in a sorted array.
///
/// # Complexity
/// - Time:  O(log n)
/// - Space: O(1)
fn last_occurrence(arr: &[i32], target: i32) -> Option<usize> {
    let mut left = 0usize;
    let mut right = arr.len();
    let mut result: Option<usize> = None;

    while left < right {
        let mid = left + (right - left) / 2;
        match arr[mid].cmp(&target) {
            std::cmp::Ordering::Equal => {
                result = Some(mid);
                left = mid + 1; // Keep searching right
            }
            std::cmp::Ordering::Less => left = mid + 1,
            std::cmp::Ordering::Greater => right = mid,
        }
    }
    result
}

// ---------------------------------------------------------------------------
// Count Occurrences
// ---------------------------------------------------------------------------

/// Counts how many times `target` appears in a sorted array.
///
/// Uses `first_occurrence` and `last_occurrence` to compute the range.
///
/// # Complexity
/// - Time:  O(log n)
/// - Space: O(1)
fn count_occurrences(arr: &[i32], target: i32) -> usize {
    match (first_occurrence(arr, target), last_occurrence(arr, target)) {
        (Some(first), Some(last)) => last - first + 1,
        _ => 0,
    }
}

// ---------------------------------------------------------------------------
// Search in Rotated Sorted Array
// ---------------------------------------------------------------------------

/// Searches for `target` in a rotated sorted array (no duplicates).
///
/// A rotated sorted array is like `[4, 5, 6, 7, 0, 1, 2]` — it was sorted, then
/// rotated at some pivot. We determine which half is sorted and narrow the search.
///
/// # Complexity
/// - Time:  O(log n)
/// - Space: O(1)
fn search_rotated(arr: &[i32], target: i32) -> Option<usize> {
    if arr.is_empty() {
        return None;
    }
    let mut left = 0usize;
    let mut right = arr.len() - 1;

    while left <= right {
        let mid = left + (right - left) / 2;

        if arr[mid] == target {
            return Some(mid);
        }

        // Determine which half is sorted.
        if arr[left] <= arr[mid] {
            // Left half [left..mid] is sorted.
            if arr[left] <= target && target < arr[mid] {
                // Target is in the sorted left half.
                if mid == 0 {
                    break;
                }
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        } else {
            // Right half [mid..right] is sorted.
            if arr[mid] < target && target <= arr[right] {
                left = mid + 1;
            } else {
                if mid == 0 {
                    break;
                }
                right = mid - 1;
            }
        }
    }
    None
}

// ---------------------------------------------------------------------------
// Binary Search on Answer: Integer Square Root
// ---------------------------------------------------------------------------

/// Computes the integer square root of `n` (floor of sqrt(n)).
///
/// Binary search for the largest `x` such that `x * x <= n`.
///
/// # Complexity
/// - Time:  O(log n)
/// - Space: O(1)
fn integer_sqrt(n: u64) -> u64 {
    if n < 2 {
        return n;
    }
    let mut left: u64 = 1;
    let mut right: u64 = n / 2 + 1;
    let mut result: u64 = 1;

    while left <= right {
        let mid = left + (right - left) / 2;
        // Use mid <= n / mid instead of mid * mid <= n to avoid overflow.
        if mid <= n / mid {
            result = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    result
}

// ---------------------------------------------------------------------------
// Binary Search on Answer: Minimum Eating Speed (Koko's Bananas)
// ---------------------------------------------------------------------------

/// Given piles of bananas and `h` hours, find the minimum eating speed `k` such
/// that all bananas can be eaten within `h` hours.
///
/// At speed `k`, a pile of size `p` takes `ceil(p / k)` hours.
/// We binary search over possible speeds `[1, max(piles)]`.
///
/// # Complexity
/// - Time:  O(n * log(max_pile)) where n = number of piles
/// - Space: O(1)
fn min_eating_speed(piles: &[i32], h: i32) -> i32 {
    let mut left = 1i32;
    let mut right = *piles.iter().max().unwrap();

    while left < right {
        let mid = left + (right - left) / 2;
        // Calculate total hours needed at speed `mid`.
        let hours: i64 = piles.iter()
            .map(|&p| ((p as i64) + (mid as i64) - 1) / (mid as i64)) // ceil division
            .sum();

        if hours <= h as i64 {
            right = mid; // Can eat fast enough — try slower.
        } else {
            left = mid + 1; // Too slow — must eat faster.
        }
    }
    left
}

// ---------------------------------------------------------------------------
// Binary Search on Answer: Minimum Ship Capacity
// ---------------------------------------------------------------------------

/// Given packages with weights and a deadline of `days`, find the minimum ship
/// capacity to ship all packages in order within `days` days.
///
/// Each day, we load packages in order until the next one would exceed capacity.
/// Binary search over `[max(weights), sum(weights)]`.
///
/// # Complexity
/// - Time:  O(n * log(sum - max)) where n = number of packages
/// - Space: O(1)
fn min_ship_capacity(weights: &[i32], days: i32) -> i32 {
    let mut left = *weights.iter().max().unwrap();
    let mut right: i32 = weights.iter().sum();

    while left < right {
        let mid = left + (right - left) / 2;

        // Simulate shipping: count days needed with capacity `mid`.
        let mut days_needed = 1;
        let mut current_load = 0;
        for &w in weights {
            if current_load + w > mid {
                days_needed += 1;
                current_load = 0;
            }
            current_load += w;
        }

        if days_needed <= days {
            right = mid; // Capacity sufficient — try smaller.
        } else {
            left = mid + 1; // Need more capacity.
        }
    }
    left
}

// ===========================================================================
// Main — demonstrations and test assertions
// ===========================================================================

fn main() {
    println!("=== Week 8: Searching ===\n");

    // --- Binary Search ---
    println!("--- Binary Search ---");
    let sorted = vec![1, 3, 5, 7, 9, 11, 13, 15];

    assert_eq!(binary_search(&sorted, 7), Some(3));
    assert_eq!(binary_search(&sorted, 1), Some(0));
    assert_eq!(binary_search(&sorted, 15), Some(7));
    assert_eq!(binary_search(&sorted, 6), None);
    assert_eq!(binary_search(&[], 5), None);
    println!("binary_search([1,3,5,7,9,11,13,15], 7) = {:?}", binary_search(&sorted, 7));

    // Recursive
    assert_eq!(binary_search_recursive(&sorted, 7, 0), Some(3));
    assert_eq!(binary_search_recursive(&sorted, 6, 0), None);
    println!("binary_search_recursive(_, 7) = {:?}", binary_search_recursive(&sorted, 7, 0));

    // --- First / Last Occurrence ---
    println!("\n--- First / Last Occurrence ---");
    let arr = vec![1, 2, 2, 2, 3, 4, 4, 5];
    assert_eq!(first_occurrence(&arr, 2), Some(1));
    assert_eq!(last_occurrence(&arr, 2), Some(3));
    assert_eq!(first_occurrence(&arr, 4), Some(5));
    assert_eq!(last_occurrence(&arr, 4), Some(6));
    assert_eq!(first_occurrence(&arr, 6), None);
    println!("first_occurrence of 2: {:?}", first_occurrence(&arr, 2));
    println!("last_occurrence  of 2: {:?}", last_occurrence(&arr, 2));

    // --- Count Occurrences ---
    println!("\n--- Count Occurrences ---");
    assert_eq!(count_occurrences(&arr, 2), 3);
    assert_eq!(count_occurrences(&arr, 4), 2);
    assert_eq!(count_occurrences(&arr, 5), 1);
    assert_eq!(count_occurrences(&arr, 6), 0);
    println!("count(2) = {}", count_occurrences(&arr, 2));

    // --- Search in Rotated Sorted Array ---
    println!("\n--- Search in Rotated Sorted Array ---");
    let rotated = vec![4, 5, 6, 7, 0, 1, 2];
    assert_eq!(search_rotated(&rotated, 0), Some(4));
    assert_eq!(search_rotated(&rotated, 4), Some(0));
    assert_eq!(search_rotated(&rotated, 7), Some(3));
    assert_eq!(search_rotated(&rotated, 3), None);
    println!("search_rotated([4,5,6,7,0,1,2], 0) = {:?}", search_rotated(&rotated, 0));

    let rotated2 = vec![2, 1]; // Edge case
    assert_eq!(search_rotated(&rotated2, 1), Some(1));

    // --- Integer Square Root ---
    println!("\n--- Binary Search on Answer ---");
    assert_eq!(integer_sqrt(0), 0);
    assert_eq!(integer_sqrt(1), 1);
    assert_eq!(integer_sqrt(4), 2);
    assert_eq!(integer_sqrt(8), 2);
    assert_eq!(integer_sqrt(100), 10);
    assert_eq!(integer_sqrt(101), 10);
    println!("integer_sqrt(100) = {}", integer_sqrt(100));
    println!("integer_sqrt(101) = {}", integer_sqrt(101));

    // --- Min Eating Speed ---
    println!("\n--- Koko's Bananas (Min Eating Speed) ---");
    assert_eq!(min_eating_speed(&[3, 6, 7, 11], 8), 4);
    assert_eq!(min_eating_speed(&[30, 11, 23, 4, 20], 5), 30);
    assert_eq!(min_eating_speed(&[30, 11, 23, 4, 20], 6), 23);
    println!("min_eating_speed([3,6,7,11], h=8) = {}", min_eating_speed(&[3, 6, 7, 11], 8));

    // --- Min Ship Capacity ---
    println!("\n--- Ship Within Days (Min Capacity) ---");
    assert_eq!(min_ship_capacity(&[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), 15);
    assert_eq!(min_ship_capacity(&[3, 2, 2, 4, 1, 4], 3), 6);
    assert_eq!(min_ship_capacity(&[1, 2, 3, 1, 1], 4), 3);
    println!(
        "min_ship_capacity([1..=10], days=5) = {}",
        min_ship_capacity(&[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)
    );

    println!("\nAll assertions passed!");
}
