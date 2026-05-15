/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: Binary to Decimal
 * File: 14.binary_to_decimal.rs
 *
 * KEY POINTS:
 *  - Manual loop: take last digit (% 10), accumulate digit * 2^position.
 *  - Built-in: `i64::from_str_radix(s, 2)` parses a string in any base.
 *  - `i64::to_str_radix` doesn't exist in std; use format!("{:b}", n).
 */

use std::io::Read;

fn bin_to_dec(mut n: i64) -> i64 {
    let mut dec = 0_i64;
    let mut p = 1_i64;
    while n > 0 {
        let bit = n % 10;
        dec += bit * p;
        p *= 2;
        n /= 10;
    }
    dec
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    if buf.trim().is_empty() {
        for v in [1100_i64, 1, 0, 11111111, 10101010] {
            let parsed = i64::from_str_radix(&v.to_string(), 2).unwrap_or(-1);
            println!("{v} (binary) -> {}    [from_str_radix: {}]", bin_to_dec(v), parsed);
        }
        return;
    }
    let n: i64 = buf.trim().parse().unwrap_or(0);
    println!("{}", bin_to_dec(n));
}

/*
 * NOTES:
 *  - Prefer `i64::from_str_radix(s, 2)` when input is a STRING.
 *  - The numeric form here mirrors Java's loop exactly.
 */
