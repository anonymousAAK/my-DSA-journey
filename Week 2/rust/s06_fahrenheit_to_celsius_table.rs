/*
 * WEEK 2 - RUST CONTROL FLOW
 * Topic: Fahrenheit -> Celsius Table
 * File: 6.fahrenheit_to_celsius_table.rs
 *
 * PROBLEM:
 *  Print (F, C) pairs for F in S..=E stepping by W; C = (F - 32) * 5 / 9.
 *
 * KEY POINTS:
 *  - Integer division truncates (matches Java).
 *  - `(F - 32) * 5 / 9` -> i32 result.
 *  - `(F - 32) as f64 * 5.0 / 9.0` -> precise f64.
 *  - Range with step: `(s..=e).step_by(w)` (requires usize, so cast).
 *
 * SYNTAX:
 *   for f in (s..=e).step_by(w as usize) { ... }
 *
 * DRY RUN:
 *  S=32, E=212, W=20 -> 32..=212 step 20 -> 32, 52, 72, ..., 212
 */

use std::io::Read;

fn main() {
    let (s, e, w): (i32, i32, i32) = read_three().unwrap_or((32, 212, 20));
    if w <= 0 {
        eprintln!("step W must be positive");
        return;
    }
    let mut f = s;
    while f <= e {
        let c_int = (f - 32) * 5 / 9;
        let c_dbl = (f - 32) as f64 * 5.0 / 9.0;
        println!("{f} {c_int}   (precise: {c_dbl:.4})");
        f += w;
    }
}

fn read_three() -> Option<(i32, i32, i32)> {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok()?;
    let mut it = buf.split_whitespace();
    let s: i32 = it.next()?.parse().ok()?;
    let e: i32 = it.next()?.parse().ok()?;
    let w: i32 = it.next()?.parse().ok()?;
    Some((s, e, w))
}

/*
 * NOTES:
 *  - Rust's integer division truncates toward zero, like Java/C++.
 *  - Use `as f64` to opt into floating-point precision.
 *  - `step_by` on ranges is a clean alternative to manual `while`.
 */
