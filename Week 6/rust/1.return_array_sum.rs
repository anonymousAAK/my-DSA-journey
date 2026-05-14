/*
 * WEEK 6 - RUST DSA
 * Topic: Return Array Sum
 * File: 1.return_array_sum.rs
 *
 * CONCEPT:
 *     Compute the sum of all integers in a Vec<i64>.
 *
 * KEY POINTS:
 *     - Vec<T> is Rust's growable array; slices (&[T]) are read-only views.
 *     - The iterator method .iter().sum() sums in O(n).
 *     - Recursive form shown for didactic completeness.
 *
 * ALGORITHM / APPROACH:
 *     Iterative:
 *         let mut total = 0_i64;
 *         for &v in arr { total += v; }
 *         total
 *     Recursive:
 *         f(arr, i) = 0 when i == arr.len(), else arr[i] + f(arr, i+1)
 *
 * RUST-SPECIFIC NOTES:
 *     - Pass slices (`&[i64]`) for read-only access; pass `Vec<i64>` only
 *       when transferring ownership.
 *     - Use `i64` (or `i128`) for accumulator to avoid overflow without
 *       enabling wrapping arithmetic.
 *     - Iterator chaining (.iter().sum::<i64>()) is the idiomatic form.
 *
 * DRY RUN:
 *     [1,2,3,4,5]    -> 1,3,6,10,15
 *     [-1,0,5,-3,10] -> -1,-1,4,1,11
 *     []             -> 0
 *
 * COMPLEXITY:
 *     Iterative : O(n) time, O(1) space
 *     Recursive : O(n) time, O(n) stack
 */

fn array_sum(arr: &[i64]) -> i64 {
    let mut total: i64 = 0;
    for &v in arr {
        total += v;
    }
    total
}

fn array_sum_recursive(arr: &[i64], index: usize) -> i64 {
    if index == arr.len() {
        return 0;
    }
    arr[index] + array_sum_recursive(arr, index + 1)
}

fn array_sum_iter(arr: &[i64]) -> i64 {
    arr.iter().sum()
}

fn main() {
    let test1: Vec<i64> = vec![1, 2, 3, 4, 5];
    println!("Array: {:?}", test1);
    println!("Sum (iterative): {}", array_sum(&test1));
    println!("Sum (recursive): {}", array_sum_recursive(&test1, 0));
    println!("Sum (iterator):  {}", array_sum_iter(&test1));

    let test2: Vec<i64> = vec![-1, 0, 5, -3, 10];
    println!("\nArray: {:?}", test2);
    println!("Sum: {}", array_sum(&test2));

    let test3: Vec<i64> = vec![];
    println!("\nEmpty array sum: {}", array_sum(&test3));
}

/*
 * NOTES — Rust vs Java:
 *     - Borrow with `&[i64]` instead of consuming a `Vec`.
 *     - Pattern `for &v in arr` destructures the reference to give a value.
 *     - Iterator adapters (.iter().sum()) handle empty input naturally.
 *     - No exceptions; the recursive function uses a base case rather than
 *       relying on bounds-check panics.
 */
