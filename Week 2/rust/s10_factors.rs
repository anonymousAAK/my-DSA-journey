/*
 * WEEK 2 - RUST CONTROL FLOW
 * Topic: Factors of N (excluding 1 and N)
 * File: 10.factors.rs
 *
 * PROBLEM:
 *  Print every i in 2..=n/2 with n % i == 0.
 *
 * KEY POINTS:
 *  - `for i in 2..=n/2` is concise.
 *  - `n.is_multiple_of(i)` is nightly-only; portable test: `n % i == 0`.
 *  - sqrt(n) optimisation requires casting because i*i could overflow for large i.
 *
 * DRY RUN:
 *  n=12 -> 2 3 4 6
 *  n=7  -> (prime) nothing
 *
 * COMPLEXITY: O(n) brute; O(sqrt n) optimised.
 */

use std::io::Read;

fn brute(n: i64) -> Vec<i64> {
    (2..=n / 2).filter(|i| n % i == 0).collect()
}

fn sqrt_factors(n: i64) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    let mut i: i64 = 2;
    while i.saturating_mul(i) <= n {
        if n % i == 0 {
            out.push(i);
            if i != n / i {
                out.push(n / i);
            }
        }
        i += 1;
    }
    out.retain(|&x| x != n);
    out.sort();
    out
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: i64 = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(12);

    let bf = brute(n);
    print!("brute: ");
    for v in &bf { print!("{v} "); }
    println!();

    let sq = sqrt_factors(n);
    print!("sqrt : ");
    for v in &sq { print!("{v} "); }
    println!();
}

/*
 * NOTES:
 *  - `saturating_mul` prevents overflow when checking i*i <= n on large n.
 *  - For primality testing, return early as soon as a factor is found.
 */
