/*
 * WEEK 2 - RUST CONTROL FLOW
 * Topic: Total Salary Calculation
 * File: 7.total_salary.rs
 *
 * PROBLEM:
 *  total = basic + hra + da + allow - pf  (hra 20%, da 50%, pf 11%)
 *  allow = 1700 (A), 1500 (B), 1300 (else)
 *  Round and print integral part.
 *
 * KEY POINTS:
 *  - `f64::round()` rounds half AWAY FROM ZERO (matches Java's Math.round for positives).
 *  - `match` is a clean replacement for the grade if/else.
 *
 * SYNTAX:
 *   let allow = match grade {
 *       'A' => 1700,
 *       'B' => 1500,
 *       _   => 1300,
 *   };
 *
 * DRY RUN:
 *  basic=10000, grade='A' -> 17600
 *
 * COMPLEXITY: O(1).
 */

use std::io::Read;

fn total_salary(basic: i64, grade: char) -> i64 {
    let basic_f = basic as f64;
    let hra = 0.20 * basic_f;
    let da  = 0.50 * basic_f;
    let pf  = 0.11 * basic_f;
    let allow: i64 = match grade {
        'A' => 1700,
        'B' => 1500,
        _   => 1300,
    };
    let total = basic_f + hra + da + (allow as f64) - pf;
    total.round() as i64
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let mut it = buf.split_whitespace();

    let basic: i64 = it.next().and_then(|s| s.parse().ok()).unwrap_or(10000);
    let grade: char = it.next().and_then(|s| s.chars().next()).unwrap_or('A');

    println!("{}", total_salary(basic, grade));
}

/*
 * NOTES:
 *  - Rust's `round()` rounds half-away-from-zero (same as Java's Math.round
 *    for non-negative inputs).
 *  - `match` exhaustively handles all chars via the `_` arm.
 *  - For currency, use a decimal crate (`rust_decimal`) instead of f64.
 */
