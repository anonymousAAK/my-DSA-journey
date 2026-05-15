/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Average of Three Numbers
 * File: 12.average_of_two_numbers.rs
 *
 * CONCEPT:
 * Read a name and three integers, print the name and the average. Like Java,
 * dividing three ints truncates. Cast to f64 with `as` for a precise result.
 *
 * KEY POINTS:
 *  - i32 / i32 -> i32 (truncated toward zero)
 *  - Cast with `as f64` for true division.
 *  - Use `{:.2}` in the format string for fixed-point output.
 *
 * SYNTAX:
 *   let avg_i: i32 = (a + b + c) / 3;
 *   let avg_f: f64 = (a + b + c) as f64 / 3.0;
 *
 * DRY RUN:
 *  Stdin: "Bob 10 11 12"  -> avg_i = 11, avg_f = 11.0
 *  Stdin: "Bob 10 11 11"  -> avg_i = 10, avg_f = 10.67
 *
 * COMPLEXITY: O(1).
 */

use std::io;

fn main() -> io::Result<()> {
    let mut line = String::new();
    io::stdin().read_line(&mut line)?;
    let mut it = line.split_whitespace();

    let name: String = it.next().unwrap_or("").to_string();
    let a: i32 = it.next().unwrap_or("0").parse().unwrap_or(0);
    let b: i32 = it.next().unwrap_or("0").parse().unwrap_or(0);
    let c: i32 = it.next().unwrap_or("0").parse().unwrap_or(0);

    let avg_i: i32 = (a + b + c) / 3;
    let avg_f: f64 = (a + b + c) as f64 / 3.0;

    println!("{name}");
    println!("int average    = {avg_i}");
    println!("float average  = {avg_f:.4}");

    Ok(())
}

/*
 * NOTES:
 *  - Rust does NOT implicitly promote int -> float; `as f64` is required.
 *  - The `{:.4}` formatter rounds to 4 decimal places (no trailing-zero trimming).
 *  - For overflow safety on the sum use checked_add or convert to i64 first.
 */
