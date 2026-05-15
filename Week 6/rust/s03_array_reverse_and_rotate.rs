/*
 * WEEK 6 - RUST DSA
 * Topic: Array Reverse and Rotate
 * File: 3.array_reverse_and_rotate.rs
 *
 * CONCEPT:
 *     - Reverse a Vec<i32> in place using two pointers.
 *     - Left/right rotate by k via the reversal algorithm
 *       (3 sub-reversals; O(n) time, O(1) space).
 *
 * KEY POINTS:
 *     - Reduce k modulo n before rotating.
 *     - Reversal trick beats the naive O(n*k) shift loop.
 *     - Vec already has .reverse() and .rotate_left() / .rotate_right().
 *
 * ALGORITHM / APPROACH:
 *     reverse(arr, l, r): swap, l++, r--, while l < r
 *     left_rotate(arr,k): k%=n;
 *         reverse(arr, 0, k-1)
 *         reverse(arr, k, n-1)
 *         reverse(arr, 0, n-1)
 *
 * RUST-SPECIFIC NOTES:
 *     - .swap(i, j) is a slice method that swaps two indices.
 *     - Care needed because indices are usize; we use i32 internally
 *       for the reverse pointer arithmetic to avoid underflow.
 *
 * DRY RUN:
 *     [1,2,3,4,5] reversed -> [5,4,3,2,1]
 *     [1,2,3,4,5] left rotate by 2:
 *         rev(0,1):  [2,1,3,4,5]
 *         rev(2,4):  [2,1,5,4,3]
 *         rev(0,4):  [3,4,5,1,2]
 *
 * COMPLEXITY:
 *     Reverse : O(n) time, O(1) space
 *     Rotate  : O(n) time, O(1) space
 */

fn reverse_range(arr: &mut [i32], mut l: usize, mut r: usize) {
    while l < r {
        arr.swap(l, r);
        l += 1;
        r -= 1;
    }
}

fn reverse_array(arr: &mut [i32]) {
    if !arr.is_empty() {
        reverse_range(arr, 0, arr.len() - 1);
    }
}

fn left_rotate(arr: &mut [i32], k: usize) {
    let n = arr.len();
    if n == 0 {
        return;
    }
    let k = k % n;
    if k == 0 {
        return;
    }
    reverse_range(arr, 0, k - 1);
    reverse_range(arr, k, n - 1);
    reverse_range(arr, 0, n - 1);
}

fn right_rotate(arr: &mut [i32], k: usize) {
    let n = arr.len();
    if n == 0 {
        return;
    }
    left_rotate(arr, n - (k % n));
}

fn main() {
    // Reverse
    let mut arr1 = vec![1, 2, 3, 4, 5];
    println!("Original: {:?}", arr1);
    reverse_array(&mut arr1);
    println!("Reversed: {:?}", arr1);

    // Left rotate
    let mut arr2 = vec![1, 2, 3, 4, 5];
    println!("\nOriginal:         {:?}", arr2);
    left_rotate(&mut arr2, 2);
    println!("Left Rotate by 2: {:?}", arr2);

    // Right rotate
    let mut arr3 = vec![1, 2, 3, 4, 5];
    println!("\nOriginal:          {:?}", arr3);
    right_rotate(&mut arr3, 2);
    println!("Right Rotate by 2: {:?}", arr3);

    // Edge cases
    let mut single = vec![42];
    left_rotate(&mut single, 5);
    println!("\nSingle element rotated: {:?}", single);

    let mut empty: Vec<i32> = vec![];
    left_rotate(&mut empty, 3);
    println!("Empty array: {:?}", empty);

    // Standard library shortcut
    let mut alt = vec![1, 2, 3, 4, 5];
    alt.rotate_left(2);
    println!("\nVec::rotate_left(2): {:?}", alt);
}

/*
 * NOTES — Rust vs Java:
 *     - &mut [i32] mirrors Java's int[] but with explicit mutability.
 *     - .swap(i, j) avoids manual temporaries.
 *     - usize is unsigned; we guard subtractions to avoid underflow panics.
 *     - Vec::rotate_left / rotate_right are STL-style standard library
 *       conveniences.
 */
