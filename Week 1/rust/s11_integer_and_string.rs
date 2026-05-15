/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Mixing Integer and String + Concatenation
 * File: 11.integer_and_string.rs
 *
 * CONCEPT:
 * Rust's `+` for String concatenation is restrictive — only `String + &str`
 * works. The common idiom is `format!` (analogous to Python f-strings or
 * Java's String.format).
 *
 * KEY POINTS:
 *  - `format!("{} {}", name, n)` builds a String at runtime.
 *  - Direct concatenation: `let s: String = name.clone() + " " + &n.to_string();`
 *  - `n.to_string()` is the canonical numeric-to-string conversion.
 *  - `&str` is a slice reference; `String` is owned/growable.
 *  - Avoid clone() unless necessary — ownership transfer is preferred.
 *
 * SYNTAX:
 *   let s: String = format!("{} {}", name, n);
 *
 * DRY RUN:
 *  Stdin: "Alice 30"
 *    name = "Alice"; n = 30
 *    output: "Alice 30"
 */

use std::io;

fn main() -> io::Result<()> {
    let mut line = String::new();
    io::stdin().read_line(&mut line)?;
    let mut it = line.split_whitespace();

    let name: &str = it.next().unwrap_or("");
    let n: i32 = it.next().unwrap_or("0").parse().unwrap_or(0);

    // Streaming-style print
    println!("{name} {n}");

    // format! returns a String
    let joined: String = format!("{name} {n}");
    println!("{joined}");

    // Manual concat — note the &str on the right
    let mut acc: String = name.to_string();
    acc.push(' ');
    acc.push_str(&n.to_string());
    println!("{acc}");

    Ok(())
}

/*
 * NOTES:
 *  - Rust's `+` for strings consumes the left String (ownership) and borrows
 *    the right &str. This avoids accidental clones but feels strict.
 *  - Java's `+` is overloaded for String concatenation with any operand.
 *  - For loops of concatenations, push into a single String (mutate, don't
 *    reallocate per step) for O(n) cost.
 */
