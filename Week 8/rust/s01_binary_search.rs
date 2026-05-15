/*
 * WEEK 8 - RUST DSA
 * Topic: Binary Search
 * File: 1.binary_search.rs
 *
 * CONCEPT:
 *     Locate a value in a sorted slice in O(log n) by halving the
 *     interval.
 *
 * KEY POINTS:
 *     - Slice must be sorted.
 *     - Use i64/isize for half-open arithmetic when high may go below 0.
 *     - Variants: first/last occurrence, count, search in rotated array.
 *
 * ALGORITHM / APPROACH:
 *     Standard iterative as in Java/C++/Python files.
 *
 * RUST-SPECIFIC NOTES:
 *     - The standard library offers slice::binary_search returning
 *       Result<usize, usize>: Ok(index) or Err(insert_position).
 *     - Convert to Option<usize> or -1 sentinel for parity with Java.
 *
 * DRY RUN:
 *     [-5,-2,0,1,3,5,7,9,11], target=5 -> index 5.
 *     Rotated [4,5,6,7,0,1,2], target=0 -> index 4.
 *
 * COMPLEXITY:
 *     Time:  O(log n)
 *     Space: O(1) iterative, O(log n) recursive
 */

fn binary_search(arr: &[i32], target: i32) -> i64 {
    let mut low: i64 = 0;
    let mut high: i64 = arr.len() as i64 - 1;
    while low <= high {
        let mid = low + (high - low) / 2;
        let v = arr[mid as usize];
        if v == target {
            return mid;
        } else if v < target {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    -1
}

fn binary_search_rec(arr: &[i32], target: i32, low: i64, high: i64) -> i64 {
    if low > high {
        return -1;
    }
    let mid = low + (high - low) / 2;
    let v = arr[mid as usize];
    if v == target {
        mid
    } else if v < target {
        binary_search_rec(arr, target, mid + 1, high)
    } else {
        binary_search_rec(arr, target, low, mid - 1)
    }
}

fn first_occurrence(arr: &[i32], target: i32) -> i64 {
    let mut low: i64 = 0;
    let mut high: i64 = arr.len() as i64 - 1;
    let mut result: i64 = -1;
    while low <= high {
        let mid = low + (high - low) / 2;
        let v = arr[mid as usize];
        if v == target {
            result = mid;
            high = mid - 1;
        } else if v < target {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    result
}

fn last_occurrence(arr: &[i32], target: i32) -> i64 {
    let mut low: i64 = 0;
    let mut high: i64 = arr.len() as i64 - 1;
    let mut result: i64 = -1;
    while low <= high {
        let mid = low + (high - low) / 2;
        let v = arr[mid as usize];
        if v == target {
            result = mid;
            low = mid + 1;
        } else if v < target {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    result
}

fn count_occurrences(arr: &[i32], target: i32) -> i64 {
    let first = first_occurrence(arr, target);
    if first == -1 {
        return 0;
    }
    last_occurrence(arr, target) - first + 1
}

fn search_rotated(arr: &[i32], target: i32) -> i64 {
    let mut low: i64 = 0;
    let mut high: i64 = arr.len() as i64 - 1;
    while low <= high {
        let mid = low + (high - low) / 2;
        let v = arr[mid as usize];
        if v == target {
            return mid;
        }
        if arr[low as usize] <= v {
            // left half sorted
            if arr[low as usize] <= target && target < v {
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        } else {
            // right half sorted
            if v < target && target <= arr[high as usize] {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
    }
    -1
}

fn main() {
    let sorted = vec![-5, -2, 0, 1, 3, 5, 7, 9, 11];
    println!("Array: {:?}", sorted);
    println!("binary_search(5) = {}", binary_search(&sorted, 5));
    println!("binary_search(0) = {}", binary_search(&sorted, 0));
    println!("binary_search(4) = {}", binary_search(&sorted, 4));
    println!(
        "binary_search_rec(7) = {}",
        binary_search_rec(&sorted, 7, 0, sorted.len() as i64 - 1)
    );

    let with_dups = vec![1, 2, 2, 2, 3, 4, 4, 5];
    println!("\nArray with duplicates: {:?}", with_dups);
    println!("first_occurrence(2) = {}", first_occurrence(&with_dups, 2));
    println!("last_occurrence(2)  = {}", last_occurrence(&with_dups, 2));
    println!("count_occurrences(2) = {}", count_occurrences(&with_dups, 2));
    println!("count_occurrences(4) = {}", count_occurrences(&with_dups, 4));
    println!("count_occurrences(6) = {}", count_occurrences(&with_dups, 6));

    let rotated = vec![4, 5, 6, 7, 0, 1, 2];
    println!("\nRotated array: {:?}", rotated);
    println!("search_rotated(0) = {}", search_rotated(&rotated, 0));
    println!("search_rotated(6) = {}", search_rotated(&rotated, 6));
    println!("search_rotated(3) = {}", search_rotated(&rotated, 3));

    // Standard library
    let std = sorted.binary_search(&5);
    println!("\nslice::binary_search(5) = {:?}", std);
}

/*
 * NOTES — Rust vs Java:
 *     - The slice API offers binary_search natively returning Result.
 *     - usize underflows at 0; we use i64 indices to safely handle "high = -1".
 *     - Pattern matching makes Result/Option-based standard search ergonomic.
 */
