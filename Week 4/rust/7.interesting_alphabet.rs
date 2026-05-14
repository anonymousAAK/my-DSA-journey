/*
 * WEEK 4 - RUST PATTERN PROBLEMS
 * Topic: Interesting Alphabet Pattern
 * File: 7.interesting_alphabet.rs
 *
 * PATTERN (N=4): D / CD / BCD / ABCD
 */

use std::io::Read;

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: usize = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(4);

    for i in 1..=n {
        let start = b'A' + (n - i) as u8;
        for j in 0..i {
            print!("{}", (start + j as u8) as char);
        }
        println!();
    }
}

/*
 * NOTES:
 *  - Start letter shifts EARLIER as i grows; bottom row begins at 'A'.
 *  - Same column-offset pattern as char_pattern; only the start formula differs.
 */
