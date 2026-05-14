/*
 * WEEK 2 - RUST CONTROL FLOW
 * Topic: Sum of Even / Odd Digits
 * File: 9.sum_of_even_odd.rs
 *
 * PROBLEM:
 *  Print "even_sum odd_sum" for digits of N.
 *
 * KEY POINTS:
 *  - `%` and `/` work on integers; same semantics as Java for non-negative values.
 *  - Take `.abs()` first to be safe.
 *  - Could also iterate digits as chars: `n.to_string().chars().for_each(...)`.
 *
 * DRY RUN:
 *  N=13245 -> even=6, odd=9 -> "6 9"
 *
 * COMPLEXITY: O(d).
 */

use std::io::Read;

fn sums(mut n: i64) -> (i64, i64) {
    n = n.abs();
    let (mut even, mut odd) = (0, 0);
    while n > 0 {
        let d = n % 10;
        if d % 2 == 0 { even += d; } else { odd += d; }
        n /= 10;
    }
    (even, odd)
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: i64 = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(13245);
    let (e, o) = sums(n);
    println!("{e} {o}");
}

/*
 * NOTES:
 *  - For n outside i64's range, use i128 or parse the digits as chars.
 *  - Pattern matching `match d % 2 { 0 => ..., _ => ... }` is an alternative.
 */
