/*
 * WEEK 4 - RUST PATTERN PROBLEMS
 * Topic: Triangle Number Pattern
 * File: 3.tri_no_pattern.rs
 *
 * PATTERN (N=4): 1 / 22 / 333 / 4444
 */

use std::io::Read;

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: usize = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(4);

    for i in 1..=n {
        for _ in 0..i { print!("{i}"); }
        println!();
    }
    println!("--- string repeat ---");
    for i in 1..=n { println!("{}", i.to_string().repeat(i)); }
}

/*
 * NOTES:
 *  - For multi-digit i (>= 10), printed lines widen by additional digits.
 */
