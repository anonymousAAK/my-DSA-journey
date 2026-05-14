/*
 * WEEK 4 - RUST PATTERN PROBLEMS
 * Topic: Mirror Image Number Pattern (right-aligned)
 * File: 8.mirror_image.rs
 *
 * PATTERN (N=4):
 *      1
 *     12
 *    123
 *   1234
 */

use std::io::Read;
use std::fmt::Write;

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: usize = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(4);

    for i in 1..=n {
        for _ in 0..(n - i) { print!(" "); }
        for j in 1..=i { print!("{j}"); }
        println!();
    }

    println!("--- format-width variant ---");
    for i in 1..=n {
        let mut body = String::new();
        for j in 1..=i { write!(&mut body, "{j}").unwrap(); }
        println!("{:>width$}", body, width = n);
    }
}

/*
 * NOTES:
 *  - `{:>width$}` formatter right-aligns to a runtime width.
 *  - `write!` lets you build a String incrementally without re-allocating each step.
 */
