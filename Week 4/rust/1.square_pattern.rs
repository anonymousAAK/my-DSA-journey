/*
 * WEEK 4 - RUST PATTERN PROBLEMS
 * Topic: Square Pattern
 * File: 1.square_pattern.rs
 *
 * PATTERN (N=4): 4444 x 4 rows
 *
 * KEY POINTS:
 *  - Two nested for loops over 1..=n.
 *  - Idiomatic shortcut: n.to_string().repeat(n) for the row.
 */

use std::io::Read;

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: usize = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(4);

    for _ in 0..n {
        for _ in 0..n {
            print!("{n}");
        }
        println!();
    }
    println!("--- string repeat ---");
    let row = n.to_string().repeat(n);
    for _ in 0..n { println!("{row}"); }
}

/*
 * NOTES:
 *  - String::repeat is O(len*count) -- builds in one allocation.
 *  - For very large patterns, write to a BufWriter to avoid per-print syscalls.
 */
