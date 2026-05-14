/*
 * WEEK 2 - RUST CONTROL FLOW
 * Topic: Multiplication Table
 * File: 8.multiplication_table.rs
 *
 * PROBLEM:
 *  Read n, print 1*n, 2*n, ..., 10*n each on its own line.
 *
 * KEY POINTS:
 *  - `for i in 1..=10` iterates inclusive.
 *  - Rust's for is range-based; no traditional C-style for(...) form.
 *
 * SYNTAX:
 *  for i in 1..=10 { println!("{}", i * n); }
 *
 * DRY RUN:
 *  n=4 -> 4, 8, 12, ..., 40
 */

use std::io::Read;

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: i32 = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(4);

    for i in 1..=10 {
        println!("{}", i * n);
    }
}

/*
 * NOTES:
 *  - Rust's ranges (`1..n` exclusive, `1..=n` inclusive) make counting clean.
 *  - For descending counts: `(1..=10).rev()`.
 *  - No traditional C-style for; this is the idiomatic Rust pattern.
 */
