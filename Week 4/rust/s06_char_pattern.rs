/*
 * WEEK 4 - RUST PATTERN PROBLEMS
 * Topic: Consecutive Character Pattern
 * File: 6.char_pattern.rs
 *
 * PATTERN (N=4): A / BC / CDE / DEFG
 */

use std::io::Read;

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: usize = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(4);

    for i in 1..=n {
        let start = b'A' + (i - 1) as u8;
        for j in 0..i {
            let ch = (start + j as u8) as char;
            print!("{ch}");
        }
        println!();
    }
}

/*
 * NOTES:
 *  - The character depends on BOTH row (start) and column (offset).
 *  - For wide-Unicode use char arithmetic via u32 instead of u8.
 */
