/*
 * WEEK 6 - RUST DSA
 * Topic: Linear Search
 * File: 2.linear_search.rs
 *
 * CONCEPT:
 *     Sequentially scan a slice for a target. Works on any ordering.
 *
 * KEY POINTS:
 *     - Use Option<usize> rather than -1 sentinels — Rust's idiomatic
 *       way to express "value or absence".
 *     - Variants: last index, count, single-pass min/max.
 *
 * ALGORITHM / APPROACH:
 *     for (i, &v) in arr.iter().enumerate() {
 *         if v == target { return Some(i); }
 *     }
 *     None
 *
 * RUST-SPECIFIC NOTES:
 *     - .iter().position(|&v| v == target) is the standard library version.
 *     - .iter().rposition(...) gives the last match.
 *     - .iter().filter(...).count() counts occurrences in one chain.
 *     - .iter().min()/.max() returns Option<&T>.
 *
 * DRY RUN:
 *     arr = [4,2,7,1,9,3,7,5]
 *     search(7) -> Some(2)
 *     search(6) -> None
 *     last(7)   -> Some(6)
 *
 * COMPLEXITY:
 *     Best  : O(1)
 *     Avg   : O(n)
 *     Worst : O(n)
 *     Space : O(1)
 */

fn linear_search(arr: &[i32], target: i32) -> Option<usize> {
    for (i, &v) in arr.iter().enumerate() {
        if v == target {
            return Some(i);
        }
    }
    None
}

fn linear_search_last(arr: &[i32], target: i32) -> Option<usize> {
    let mut last: Option<usize> = None;
    for (i, &v) in arr.iter().enumerate() {
        if v == target {
            last = Some(i);
        }
    }
    last
}

fn count_occurrences(arr: &[i32], target: i32) -> usize {
    arr.iter().filter(|&&v| v == target).count()
}

fn find_min_max(arr: &[i32]) -> Option<(i32, i32)> {
    if arr.is_empty() {
        return None;
    }
    let mut mn = arr[0];
    let mut mx = arr[0];
    for &v in arr {
        if v < mn { mn = v; }
        if v > mx { mx = v; }
    }
    Some((mn, mx))
}

fn fmt(opt: Option<usize>) -> String {
    match opt {
        Some(i) => i.to_string(),
        None => String::from("-1"),
    }
}

fn main() {
    let arr: Vec<i32> = vec![4, 2, 7, 1, 9, 3, 7, 5];
    println!("Array: {:?}", arr);

    println!("linear_search(7) = {}", fmt(linear_search(&arr, 7)));      // 2
    println!("linear_search(6) = {}", fmt(linear_search(&arr, 6)));      // -1
    println!("linear_search_last(7) = {}", fmt(linear_search_last(&arr, 7))); // 6

    println!("count_occurrences(7) = {}", count_occurrences(&arr, 7));   // 2
    println!("count_occurrences(6) = {}", count_occurrences(&arr, 6));   // 0

    if let Some((mn, mx)) = find_min_max(&arr) {
        println!("Min = {}, Max = {}", mn, mx);                          // 1, 9
    }

    // Standard library equivalents
    println!(
        "iter().position(7) = {}",
        fmt(arr.iter().position(|&v| v == 7))
    );
}

/*
 * NOTES — Rust vs Java:
 *     - Option<usize> replaces the -1 sentinel entirely; the type system
 *       forces callers to handle the missing case.
 *     - Pattern matching (`if let Some(...) = ...`) destructures cleanly.
 *     - Closures (|&&v| v == target) and the iterator pipeline replace
 *       most explicit loops.
 *     - usize is the indexing type in Rust (cannot be negative).
 */
