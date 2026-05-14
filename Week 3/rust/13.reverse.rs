/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: Reverse the Digits of an Integer
 * File: 13.reverse.rs
 *
 * PROBLEM:
 *  Reverse the digits of N. Sign preserved; trailing zeros become leading.
 *
 * KEY POINTS:
 *  - Standard digit-extraction loop.
 *  - String alternative: `s.chars().rev().collect::<String>().parse()`.
 *  - Use checked_mul/checked_add to detect overflow.
 */

use std::io::Read;

fn reverse_int(n: i64) -> i64 {
    let sign = if n < 0 { -1 } else { 1 };
    let mut n = n.abs();
    let mut rev: i64 = 0;
    while n > 0 {
        rev = rev * 10 + n % 10;
        n /= 10;
    }
    sign * rev
}

fn reverse_via_string(n: i64) -> i64 {
    let sign = if n < 0 { -1 } else { 1 };
    let s: String = n.abs().to_string().chars().rev().collect();
    sign * s.parse::<i64>().unwrap_or(0)
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    if buf.trim().is_empty() {
        for v in [1234, 10400, 7, -42] {
            println!("reverse({v:>6}) = {} (str: {})", reverse_int(v), reverse_via_string(v));
        }
        return;
    }
    let n: i64 = buf.trim().parse().unwrap_or(0);
    println!("{}", reverse_int(n));
}

/*
 * NOTES:
 *  - `.chars().rev().collect()` is the idiomatic Rust string reverse.
 *  - Beware UTF-8 multi-byte chars when reversing arbitrary strings; for digits
 *    this is fine because they're ASCII.
 */
