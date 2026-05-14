//! # Week 9: Sorting
//!
//! This module covers classic sorting algorithms implemented in Rust.
//! Topics include:
//! - Bubble sort, selection sort, insertion sort (quadratic sorts)
//! - Merge sort (with inversion count)
//! - Quicksort (Lomuto partition + randomized pivot)
//! - Quickselect (kth smallest element)
//! - Counting sort
//!
//! ## Rust-Specific Notes for DSA Learners
//! - We sort `&mut Vec<i32>` or `&mut [i32]` in place where possible.
//! - Rust's ownership model means we can't have two mutable references to overlapping
//!   parts of a slice. `split_at_mut()` is the safe way to get two disjoint `&mut` slices.
//! - For merge sort, we return a new `Vec` because merging in place is complex; this
//!   mirrors the typical textbook approach.
//! - `rand` is an external crate — for randomized quicksort we use a simple inline
//!   pseudo-random approach to stay within std only.

// ---------------------------------------------------------------------------
// Bubble Sort
// ---------------------------------------------------------------------------

/// Sorts the vector in place using bubble sort.
///
/// Repeatedly steps through the list, swaps adjacent out-of-order elements.
/// The `swapped` flag enables early termination if the array is already sorted.
///
/// # Complexity
/// - Time:  O(n^2) worst/average, O(n) best (already sorted)
/// - Space: O(1)
fn bubble_sort(arr: &mut Vec<i32>) {
    let n = arr.len();
    for i in 0..n {
        let mut swapped = false;
        for j in 0..n.saturating_sub(i + 1) {
            if arr[j] > arr[j + 1] {
                arr.swap(j, j + 1);
                swapped = true;
            }
        }
        if !swapped {
            break; // Array is sorted — no swaps in this pass.
        }
    }
}

// ---------------------------------------------------------------------------
// Selection Sort
// ---------------------------------------------------------------------------

/// Sorts the vector in place using selection sort.
///
/// Finds the minimum element in the unsorted portion and swaps it to the front.
///
/// # Complexity
/// - Time:  O(n^2) always (even if sorted)
/// - Space: O(1)
fn selection_sort(arr: &mut Vec<i32>) {
    let n = arr.len();
    for i in 0..n {
        // Find the index of the minimum element in arr[i..].
        // Rust iterators make this clean:
        let min_idx = (i..n).min_by_key(|&j| arr[j]).unwrap();
        arr.swap(i, min_idx);
    }
}

// ---------------------------------------------------------------------------
// Insertion Sort
// ---------------------------------------------------------------------------

/// Sorts the vector in place using insertion sort.
///
/// Builds a sorted portion from left to right; each new element is inserted
/// into its correct position by shifting larger elements right.
///
/// # Complexity
/// - Time:  O(n^2) worst/average, O(n) best (already sorted)
/// - Space: O(1)
fn insertion_sort(arr: &mut Vec<i32>) {
    for i in 1..arr.len() {
        let key = arr[i];
        let mut j = i;
        // Shift elements of arr[0..i] that are greater than key.
        while j > 0 && arr[j - 1] > key {
            arr[j] = arr[j - 1];
            j -= 1;
        }
        arr[j] = key;
    }
}

// ---------------------------------------------------------------------------
// Merge Sort (with inversion count)
// ---------------------------------------------------------------------------

/// Sorts a slice using merge sort and returns the sorted `Vec` along with
/// the number of inversions.
///
/// An inversion is a pair `(i, j)` where `i < j` but `arr[i] > arr[j]`.
/// Merge sort naturally counts inversions during the merge step.
///
/// # Complexity
/// - Time:  O(n log n)
/// - Space: O(n) — temporary arrays during merging
fn merge_sort(arr: &[i32]) -> (Vec<i32>, u64) {
    if arr.len() <= 1 {
        return (arr.to_vec(), 0);
    }

    let mid = arr.len() / 2;
    let (left_sorted, left_inv) = merge_sort(&arr[..mid]);
    let (right_sorted, right_inv) = merge_sort(&arr[mid..]);
    let (merged, split_inv) = merge(&left_sorted, &right_sorted);

    (merged, left_inv + right_inv + split_inv)
}

/// Merges two sorted slices into one sorted `Vec`, counting split inversions.
///
/// A split inversion occurs when an element from the right half is placed before
/// remaining elements from the left half.
fn merge(left: &[i32], right: &[i32]) -> (Vec<i32>, u64) {
    let mut result = Vec::with_capacity(left.len() + right.len());
    let mut inversions: u64 = 0;
    let mut i = 0;
    let mut j = 0;

    while i < left.len() && j < right.len() {
        if left[i] <= right[j] {
            result.push(left[i]);
            i += 1;
        } else {
            result.push(right[j]);
            // All remaining elements in left[i..] form inversions with right[j].
            inversions += (left.len() - i) as u64;
            j += 1;
        }
    }

    // Append remaining elements.
    result.extend_from_slice(&left[i..]);
    result.extend_from_slice(&right[j..]);

    (result, inversions)
}

// ---------------------------------------------------------------------------
// Quicksort (Lomuto Partition)
// ---------------------------------------------------------------------------

/// Sorts a mutable slice in place using quicksort with Lomuto partitioning.
///
/// Lomuto picks the last element as pivot and partitions so that all elements
/// less than the pivot come before it, and all greater come after.
///
/// # Complexity
/// - Time:  O(n log n) average, O(n^2) worst (sorted input, poor pivot)
/// - Space: O(log n) average call-stack depth
fn quicksort(arr: &mut [i32]) {
    if arr.len() <= 1 {
        return;
    }
    let pivot_idx = lomuto_partition(arr);
    // Sort left half (elements before pivot).
    quicksort(&mut arr[..pivot_idx]);
    // Sort right half (elements after pivot).
    if pivot_idx + 1 < arr.len() {
        quicksort(&mut arr[pivot_idx + 1..]);
    }
}

/// Lomuto partition scheme: picks the last element as pivot.
///
/// Returns the final index of the pivot after partitioning.
fn lomuto_partition(arr: &mut [i32]) -> usize {
    let n = arr.len();
    let pivot = arr[n - 1];
    let mut i = 0; // Boundary: elements < pivot are in arr[0..i].

    for j in 0..n - 1 {
        if arr[j] < pivot {
            arr.swap(i, j);
            i += 1;
        }
    }
    arr.swap(i, n - 1); // Place pivot in its correct position.
    i
}

/// Quicksort with a randomized pivot to avoid O(n^2) on sorted input.
///
/// We use a simple pseudo-random number generator (xorshift) to stay within std.
///
/// # Complexity
/// - Time:  O(n log n) expected
/// - Space: O(log n) expected call-stack depth
fn quicksort_randomized(arr: &mut [i32]) {
    // Simple seed based on slice length and first element.
    let seed = if arr.is_empty() { 42 } else { (arr[0] as u64).wrapping_mul(arr.len() as u64).wrapping_add(17) };
    quicksort_rand_helper(arr, seed);
}

fn quicksort_rand_helper(arr: &mut [i32], mut seed: u64) {
    if arr.len() <= 1 {
        return;
    }
    // XorShift64 for a quick pseudo-random index.
    seed ^= seed << 13;
    seed ^= seed >> 7;
    seed ^= seed << 17;
    let rand_idx = (seed as usize) % arr.len();

    // Swap random element to end (so Lomuto picks it as pivot).
    let last = arr.len() - 1;
    arr.swap(rand_idx, last);

    let pivot_idx = lomuto_partition(arr);
    quicksort_rand_helper(&mut arr[..pivot_idx], seed.wrapping_add(1));
    if pivot_idx + 1 < arr.len() {
        quicksort_rand_helper(&mut arr[pivot_idx + 1..], seed.wrapping_add(2));
    }
}

// ---------------------------------------------------------------------------
// Quickselect (Kth Smallest)
// ---------------------------------------------------------------------------

/// Finds the kth smallest element (0-indexed) using quickselect.
///
/// This is a partial sorting algorithm based on the quicksort partition step.
/// After partitioning, the pivot is at its final sorted position — if that
/// position equals `k`, we're done. Otherwise, recurse on the correct side.
///
/// # Complexity
/// - Time:  O(n) average, O(n^2) worst
/// - Space: O(1) auxiliary (iterative version via tail-call elimination)
fn quickselect(arr: &mut [i32], k: usize) -> i32 {
    assert!(k < arr.len(), "k must be within array bounds");

    if arr.len() == 1 {
        return arr[0];
    }

    let pivot_idx = lomuto_partition(arr);

    match k.cmp(&pivot_idx) {
        std::cmp::Ordering::Equal => arr[pivot_idx],
        std::cmp::Ordering::Less => quickselect(&mut arr[..pivot_idx], k),
        std::cmp::Ordering::Greater => quickselect(&mut arr[pivot_idx + 1..], k - pivot_idx - 1),
    }
}

// ---------------------------------------------------------------------------
// Counting Sort
// ---------------------------------------------------------------------------

/// Sorts an array of non-negative integers using counting sort.
///
/// Counting sort is not comparison-based — it counts occurrences and reconstructs
/// the sorted array. It's efficient when the range of values (k) is small.
///
/// # Complexity
/// - Time:  O(n + k) where k = max value
/// - Space: O(k) for the count array
fn counting_sort(arr: &mut Vec<i32>) {
    if arr.is_empty() {
        return;
    }

    let &max_val = arr.iter().max().unwrap();
    let &min_val = arr.iter().min().unwrap();
    let range = (max_val - min_val + 1) as usize;

    let mut count = vec![0usize; range];

    // Count occurrences.
    for &val in arr.iter() {
        count[(val - min_val) as usize] += 1;
    }

    // Reconstruct sorted array.
    let mut idx = 0;
    for i in 0..range {
        for _ in 0..count[i] {
            arr[idx] = i as i32 + min_val;
            idx += 1;
        }
    }
}

// ===========================================================================
// Main — demonstrations and test assertions
// ===========================================================================

fn main() {
    println!("=== Week 9: Sorting ===\n");

    let test_cases: Vec<Vec<i32>> = vec![
        vec![64, 34, 25, 12, 22, 11, 90],
        vec![5, 4, 3, 2, 1],           // Reverse sorted
        vec![1, 2, 3, 4, 5],           // Already sorted
        vec![1],                        // Single element
        vec![],                         // Empty
        vec![3, 3, 3, 3],              // All same
    ];

    // --- Bubble Sort ---
    println!("--- Bubble Sort ---");
    for case in &test_cases {
        let mut arr = case.clone();
        bubble_sort(&mut arr);
        let mut expected = case.clone();
        expected.sort();
        assert_eq!(arr, expected);
    }
    let mut demo = vec![64, 34, 25, 12, 22, 11, 90];
    bubble_sort(&mut demo);
    println!("Bubble sorted: {:?}", demo);

    // --- Selection Sort ---
    println!("\n--- Selection Sort ---");
    for case in &test_cases {
        let mut arr = case.clone();
        selection_sort(&mut arr);
        let mut expected = case.clone();
        expected.sort();
        assert_eq!(arr, expected);
    }
    let mut demo = vec![64, 34, 25, 12, 22, 11, 90];
    selection_sort(&mut demo);
    println!("Selection sorted: {:?}", demo);

    // --- Insertion Sort ---
    println!("\n--- Insertion Sort ---");
    for case in &test_cases {
        let mut arr = case.clone();
        insertion_sort(&mut arr);
        let mut expected = case.clone();
        expected.sort();
        assert_eq!(arr, expected);
    }
    let mut demo = vec![64, 34, 25, 12, 22, 11, 90];
    insertion_sort(&mut demo);
    println!("Insertion sorted: {:?}", demo);

    // --- Merge Sort ---
    println!("\n--- Merge Sort (with inversion count) ---");
    let (sorted, inv_count) = merge_sort(&[2, 4, 1, 3, 5]);
    assert_eq!(sorted, vec![1, 2, 3, 4, 5]);
    assert_eq!(inv_count, 3); // (2,1), (4,1), (4,3)
    println!("merge_sort([2,4,1,3,5]) = {:?}, inversions = {}", sorted, inv_count);

    let (sorted2, inv2) = merge_sort(&[5, 4, 3, 2, 1]);
    assert_eq!(sorted2, vec![1, 2, 3, 4, 5]);
    assert_eq!(inv2, 10); // Fully reversed: n*(n-1)/2 = 10
    println!("merge_sort([5,4,3,2,1]) = {:?}, inversions = {}", sorted2, inv2);

    let (sorted3, inv3) = merge_sort(&[1, 2, 3]);
    assert_eq!(inv3, 0);
    println!("merge_sort([1,2,3]) = {:?}, inversions = {}", sorted3, inv3);

    // --- Quicksort ---
    println!("\n--- Quicksort (Lomuto) ---");
    for case in &test_cases {
        let mut arr = case.clone();
        quicksort(&mut arr);
        let mut expected = case.clone();
        expected.sort();
        assert_eq!(arr, expected);
    }
    let mut demo = vec![10, 80, 30, 90, 40, 50, 70];
    quicksort(&mut demo);
    println!("Quicksorted: {:?}", demo);

    // --- Quicksort Randomized ---
    println!("\n--- Quicksort (Randomized) ---");
    for case in &test_cases {
        let mut arr = case.clone();
        quicksort_randomized(&mut arr);
        let mut expected = case.clone();
        expected.sort();
        assert_eq!(arr, expected);
    }
    let mut demo = vec![10, 80, 30, 90, 40, 50, 70];
    quicksort_randomized(&mut demo);
    println!("Randomized quicksorted: {:?}", demo);

    // --- Quickselect ---
    println!("\n--- Quickselect (Kth Smallest) ---");
    let arr = vec![3, 2, 1, 5, 6, 4];
    let k2 = quickselect(&mut arr.clone(), 1); // 2nd smallest (0-indexed)
    assert_eq!(k2, 2);
    println!("2nd smallest in [3,2,1,5,6,4] = {}", k2);

    let mut arr2 = vec![7, 10, 4, 3, 20, 15];
    let k3 = quickselect(&mut arr2, 3); // 4th smallest
    assert_eq!(k3, 10);
    println!("4th smallest in [7,10,4,3,20,15] = {}", k3);

    // --- Counting Sort ---
    println!("\n--- Counting Sort ---");
    let mut arr = vec![4, 2, 2, 8, 3, 3, 1];
    counting_sort(&mut arr);
    assert_eq!(arr, vec![1, 2, 2, 3, 3, 4, 8]);
    println!("Counting sorted: {:?}", arr);

    // With negative numbers
    let mut arr_neg = vec![3, -1, 0, -3, 2, 1];
    counting_sort(&mut arr_neg);
    assert_eq!(arr_neg, vec![-3, -1, 0, 1, 2, 3]);
    println!("Counting sorted (with negatives): {:?}", arr_neg);

    println!("\nAll assertions passed!");
}
