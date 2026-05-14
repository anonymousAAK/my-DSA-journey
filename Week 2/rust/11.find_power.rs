/*
 * WEEK 2 - RUST CONTROL FLOW
 * Topic: x^n by Linear and Fast Exponentiation
 * File: 11.find_power.rs
 *
 * PROBLEM:
 *  Compute x^n; 0^0 == 1.
 *
 * KEY POINTS:
 *  - `i64::pow(x, n as u32)` is the standard library helper.
 *  - For very large n use the modular variant: `mod_pow(x, n, m)`.
 *  - Overflow PANICS in debug; use `.checked_pow` for safety.
 *
 * SYNTAX:
 *   let p: i64 = (x as i64).pow(n as u32);   // built-in
 *   let p = fast_pow(x, n);                  // hand-rolled O(log n)
 *
 * DRY RUN:
 *  x=2, n=10 -> 1024
 *
 * COMPLEXITY: O(n) linear, O(log n) fast.
 */

use std::io::Read;

fn linear_pow(x: i64, n: u32) -> i64 {
    let mut ans: i64 = 1;
    for _ in 0..n {
        ans *= x;
    }
    ans
}

fn fast_pow(x: i64, n: u32) -> i64 {
    if n == 0 { return 1; }
    if n % 2 == 0 {
        let h = fast_pow(x, n / 2);
        h * h
    } else {
        x * fast_pow(x, n - 1)
    }
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let mut it = buf.split_whitespace();
    let x: i64 = it.next().and_then(|s| s.parse().ok()).unwrap_or(2);
    let n: u32 = it.next().and_then(|s| s.parse().ok()).unwrap_or(10);

    println!("{x}^{n} = {} (linear)", linear_pow(x, n));
    println!("{x}^{n} = {} (fast)",   fast_pow(x, n));
    println!("{x}^{n} = {} (i64::pow)", x.pow(n));
}

/*
 * NOTES:
 *  - Java's BigInteger.pow gives arbitrary precision; Rust requires the
 *    `num-bigint` crate for the same.
 *  - For mod_pow use the well-known squaring algorithm with `(x % m)` reductions.
 *  - Rust's `i64::pow(u32)` is type-strict -- the exponent MUST be u32.
 */
