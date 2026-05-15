/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Adding Two Numbers from User Input
 * File: 8.add_two_number_better.rs
 *
 * CONCEPT:
 * Read two integers, print their sum. Minimal "read -> compute -> output".
 *
 * KEY POINTS:
 *  - Use `io::stdin().read_line(...)` then split + parse.
 *  - `?` propagates errors out of main (which returns `io::Result<()>`).
 *  - Single-statement print:  println!("{}", a + b);
 *
 * SYNTAX:
 *   let mut line = String::new();
 *   io::stdin().read_line(&mut line)?;
 *   let v: Vec<i32> = line.split_whitespace().map(|s| s.parse().unwrap()).collect();
 *   println!("{}", v[0] + v[1]);
 *
 * DRY RUN:
 *  Stdin: "10 25"  -> "35"
 *
 * COMPLEXITY: O(1).
 */

use std::io;

fn main() -> io::Result<()> {
    let mut line = String::new();
    io::stdin().read_line(&mut line)?;

    let parts: Vec<i32> = line
        .split_whitespace()
        .map(|t| t.parse::<i32>().expect("expected int"))
        .collect();

    if parts.len() < 2 {
        eprintln!("Two integers required.");
        return Ok(());
    }

    println!("{}", parts[0] + parts[1]);
    Ok(())
}

/*
 * NOTES:
 *  - Rust requires you to handle the Result from read_line; we use `?`.
 *  - Parsing failure also surfaces a Result; here we panic via `expect`.
 *  - In a real CLI, prefer collecting errors and reporting them properly.
 */
