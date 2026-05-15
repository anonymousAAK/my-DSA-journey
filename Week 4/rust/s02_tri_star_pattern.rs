/*
 * WEEK 4 - RUST PATTERN PROBLEMS
 * Topic: Triangular Star Pattern
 * File: 2.tri_star_pattern.rs
 *
 * PATTERN (N=4): * / ** / *** / ****
 */

use std::io::Read;

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: usize = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(4);

    for i in 1..=n {
        for _ in 0..i { print!("*"); }
        println!();
    }
    println!("--- string repeat ---");
    for i in 1..=n {
        println!("{}", "*".repeat(i));
    }
}

/*
 * NOTES:
 *  - "*".repeat(i) is the idiomatic single-allocation row builder.
 *  - Format width specifier: format!("{:*<width$}", "", width = i).
 */
