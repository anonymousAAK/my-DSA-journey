/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Reading Mixed-Type Input
 * File: 10.multiple_input.rs
 *
 * CONCEPT:
 * Read an integer and a string from stdin and print them on the same line.
 * Demonstrates parsing different types from the same line of input.
 *
 * KEY POINTS:
 *  - `split_whitespace()` yields token slices.
 *  - Each `parse::<T>()` call needs the destination type (or explicit turbofish).
 *  - `print!(...)` keeps the cursor on the same line; finish with `println!()`.
 *
 * SYNTAX:
 *   let mut line = String::new();
 *   io::stdin().read_line(&mut line)?;
 *   let mut it = line.split_whitespace();
 *   let i: i32 = it.next().unwrap().parse().unwrap();
 *   let s: &str = it.next().unwrap();
 *
 * DRY RUN:
 *  Stdin: "42 hello"
 *    i=42, s="hello"
 *    -> "42hello"  then  "42 hello"
 */

use std::io;

fn main() -> io::Result<()> {
    let mut line = String::new();
    io::stdin().read_line(&mut line)?;
    let mut it = line.split_whitespace();

    let i: i32 = it.next().expect("missing int").parse().expect("not an int");
    let s: String = it.next().unwrap_or("").to_string();

    // No newline between -- Java's System.out.print(a) + println(s)
    print!("{i}");
    println!("{s}");

    // Same line with explicit space
    println!("{i} {s}");

    Ok(())
}

/*
 * NOTES:
 *  - Rust enforces ownership rules: `s` is owned by this function — we converted
 *    a borrowed &str into String via to_string().
 *  - You CANNOT mix types in println! without a format placeholder for each.
 *  - For high-performance batch input, prefer `read_to_string` + token iteration.
 */
