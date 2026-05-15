/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: Decimal to Binary
 * File: 15.decimal_to_binary.rs
 *
 * KEY POINTS:
 *  - Manual loop encodes binary digits as decimal place values.
 *  - Built-in for STRING output: format!("{:b}", n).
 *  - For padded width: format!("{:08b}", n).
 */

use std::io::Read;

fn dec_to_bin(mut n: i64) -> i64 {
    if n == 0 { return 0; }
    let mut binary: i64 = 0;
    let mut p: i64 = 1;
    while n > 0 {
        let bit = n % 2;
        binary += bit * p;
        p *= 10;
        n /= 2;
    }
    binary
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    if buf.trim().is_empty() {
        for v in [0_i64, 1, 2, 12, 255, 1024] {
            println!("{v} -> {}    [{:b}]", dec_to_bin(v), v);
        }
        return;
    }
    let n: i64 = buf.trim().parse().unwrap_or(0);
    println!("{}", dec_to_bin(n));
}

/*
 * NOTES:
 *  - For text-mode binary use `format!("{n:b}")`.
 *  - The decimal-encoded form quickly overflows for large n; switch to a string.
 */
