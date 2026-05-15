/*
 * WEEK 6 - RUST DSA
 * Topic: Prefix Sum & Kadane's Algorithm
 * File: 4.prefix_sum_and_kadane.rs
 *
 * CONCEPT:
 *     A) Prefix sum: P[i] = arr[0]+...+arr[i]; range sum is O(1).
 *     B) Kadane: maximum contiguous subarray sum in O(n).
 *
 * KEY POINTS:
 *     - Use i64 for prefix sums; reduces overflow risk.
 *     - Kadane handles all-negative input by seeding with arr[0].
 *     - Extended Kadane returns (sum, start, end).
 *
 * ALGORITHM / APPROACH:
 *     Build prefix:
 *         prefix[0] = arr[0]; prefix[i] = prefix[i-1] + arr[i]
 *     range_sum(l,r):
 *         (l == 0) ? prefix[r] : prefix[r] - prefix[l-1]
 *     Kadane:
 *         best = current = arr[0]
 *         for i in 1..n:
 *             current = max(arr[i], current + arr[i])
 *             best    = max(best, current)
 *
 * RUST-SPECIFIC NOTES:
 *     - i32::max(a, b) is the in-prelude max for two i32 values.
 *     - Iterators: arr.iter().scan(0, |acc, &x| { *acc += x; Some(*acc) })
 *       lazily yields a prefix-sum iterator.
 *
 * DRY RUN:
 *     arr = [3,-1,2,4,-3,7]
 *     P   = [3, 2,4,8, 5,12]
 *     range_sum(1,4) = 5 - 3 = 2
 *
 *     Kadane on [-2,1,-3,4,-1,2,1,-5,4] -> 6 from [4,-1,2,1].
 *
 * COMPLEXITY:
 *     Prefix : O(n) build, O(1) per query
 *     Kadane : O(n) time, O(1) space
 */

fn build_prefix(arr: &[i64]) -> Vec<i64> {
    let n = arr.len();
    let mut prefix = vec![0_i64; n];
    if n == 0 {
        return prefix;
    }
    prefix[0] = arr[0];
    for i in 1..n {
        prefix[i] = prefix[i - 1] + arr[i];
    }
    prefix
}

fn range_sum(prefix: &[i64], l: usize, r: usize) -> i64 {
    if l == 0 {
        prefix[r]
    } else {
        prefix[r] - prefix[l - 1]
    }
}

fn max_subarray_sum(arr: &[i64]) -> i64 {
    let mut best = arr[0];
    let mut current = arr[0];
    for i in 1..arr.len() {
        current = std::cmp::max(arr[i], current + arr[i]);
        best = std::cmp::max(best, current);
    }
    best
}

fn max_subarray_with_indices(arr: &[i64]) -> (i64, usize, usize) {
    let mut best = arr[0];
    let mut current = arr[0];
    let mut start: usize = 0;
    let mut end: usize = 0;
    let mut temp_start: usize = 0;

    for i in 1..arr.len() {
        if arr[i] > current + arr[i] {
            current = arr[i];
            temp_start = i;
        } else {
            current += arr[i];
        }
        if current > best {
            best = current;
            start = temp_start;
            end = i;
        }
    }
    (best, start, end)
}

fn main() {
    let arr: Vec<i64> = vec![3, -1, 2, 4, -3, 7];
    let prefix = build_prefix(&arr);
    println!("Array:  {:?}", arr);
    println!("Prefix: {:?}", prefix);
    println!("Sum of arr[1..4] = {}", range_sum(&prefix, 1, 4));
    println!("Sum of arr[0..5] = {}", range_sum(&prefix, 0, 5));
    println!("Sum of arr[2..2] = {}", range_sum(&prefix, 2, 2));

    let test1: Vec<i64> = vec![-2, 1, -3, 4, -1, 2, 1, -5, 4];
    println!("\nArray: {:?}", test1);
    println!("Max subarray sum: {}", max_subarray_sum(&test1));
    let (best, s, e) = max_subarray_with_indices(&test1);
    println!(
        "Max sum: {} | Subarray arr[{}..{}] = {:?}",
        best,
        s,
        e,
        &test1[s..=e]
    );

    let all_neg: Vec<i64> = vec![-5, -1, -8, -3];
    println!("\nAll-negative: {:?}", all_neg);
    println!("Max sum: {}", max_subarray_sum(&all_neg));

    let single: Vec<i64> = vec![42];
    println!("\nSingle element {:?}: max sum = {}", single, max_subarray_sum(&single));
}

/*
 * NOTES — Rust vs Java:
 *     - i64 instead of int gives a comfortable overflow margin.
 *     - Tuple returns (i64, usize, usize) replace the Java int[] trick.
 *     - Slicing &test1[s..=e] is range-inclusive and zero-copy.
 *     - std::cmp::max works for any Ord type; built into the prelude.
 */
