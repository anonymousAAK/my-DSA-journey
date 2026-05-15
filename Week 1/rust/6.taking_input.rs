/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Reading User Input
 * File: 6.taking_input.rs
 *
 * CONCEPT:
 * Rust's standard input is accessed via `std::io::stdin()`. Unlike Java's
 * Scanner or Python's input(), there is NO line-tokenising "next int"
 * helper — read a line into a String, trim it, and parse it manually.
 *
 * KEY POINTS:
 *  - `let stdin = io::stdin();`
 *  - `stdin.read_line(&mut buffer)?;`   reads ONE line (newline included)
 *  - `.trim()` removes leading/trailing whitespace (including the '\n')
 *  - `.parse::<i32>()` converts a &str into an int; returns `Result<i32, _>`
 *  - For multiple tokens on a line: `.split_whitespace()` -> iterator of &str
 *  - Error handling: use `.expect("msg")` to panic on parse failure, or `?` to propagate
 *
 * SYNTAX:
 *  let mut s = String::new();
 *  io::stdin().read_line(&mut s).expect("read");
 *  let n: i32 = s.trim().parse().expect("integer");
 *
 *  // multi-token line:
 *  let mut line = String::new();
 *  io::stdin().read_line(&mut line)?;
 *  let nums: Vec<i32> = line.trim().split_whitespace()
 *      .map(|t| t.parse().unwrap()).collect();
 *
 * DRY RUN:
 *  Stdin: "10 25\nhello"
 *    a=10, b=25, sum=35
 *    line="hello", ch='h'
 */

use std::io::{self, BufRead, Write};

fn read_line() -> io::Result<String> {
    let mut s = String::new();
    io::stdin().lock().read_line(&mut s)?;
    Ok(s.trim_end_matches('\n').trim_end_matches('\r').to_string())
}

fn main() -> io::Result<()> {
    // Prompt
    print!("Enter two integers separated by whitespace: ");
    io::stdout().flush()?;

    let line = read_line()?;
    let nums: Vec<i32> = line
        .split_whitespace()
        .map(|t| t.parse::<i32>().expect("expected integer"))
        .collect();

    if nums.len() < 2 {
        eprintln!("need two integers");
        return Ok(());
    }
    let (a, b) = (nums[0], nums[1]);
    let c = a + b;
    println!("a + b = {c}");

    print!("Enter any line of text: ");
    io::stdout().flush()?;
    let line = read_line()?;
    if let Some(ch) = line.chars().next() {
        println!("First character: {ch}");
    }

    // Reading a double
    print!("Enter a decimal value: ");
    io::stdout().flush()?;
    let line = read_line()?;
    let d: f64 = line.trim().parse().unwrap_or(0.0);
    println!("Double = {d}");

    // Reading a long (i64 in Rust)
    print!("Enter a large integer: ");
    io::stdout().flush()?;
    let line = read_line()?;
    let lo: i64 = line.trim().parse().unwrap_or(0);
    println!("i64 = {lo}");

    Ok(())
}

/*
 * NOTES:
 *  - Java's Scanner / Python's input() return tokens or whole lines respectively.
 *    Rust always reads a line; you split + parse manually.
 *  - Rust's strong typing means `parse()` needs a hint: `.parse::<i32>()` or
 *    let n: i32 = line.parse()?;
 *  - `.expect("msg")` panics with `msg` on Err; `?` returns the error to the caller.
 *  - Always flush stdout before reading interactive input or the prompt may not appear.
 */
