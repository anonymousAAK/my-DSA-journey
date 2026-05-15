/*
 * WEEK 4 - RUST PATTERN PROBLEMS
 * Topic: Alpha Pattern
 * File: 5.alpha_pattern.rs
 *
 * PATTERN (N=4): A / BB / CCC / DDDD
 *
 * KEY POINTS:
 *  - Compute the char from the row number via offset arithmetic.
 *  - Rust's char is Unicode; `(b'A' + i as u8) as char` works for ASCII letters.
 */

use std::io::Read;

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: usize = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(4);

    for i in 1..=n {
        let ch = (b'A' + (i - 1) as u8) as char;
        for _ in 0..i { print!("{ch}"); }
        println!();
    }
    println!("--- repeat ---");
    for i in 1..=n {
        let ch = (b'A' + (i - 1) as u8) as char;
        println!("{}", ch.to_string().repeat(i));
    }
}

/*
 * NOTES:
 *  - b'A' is a byte literal (u8); cast to char for printing.
 *  - For Unicode characters use char::from_u32(code).unwrap().
 *  - Watch out for n > 26 -- the cast to char is still valid but produces non-letters.
 */
