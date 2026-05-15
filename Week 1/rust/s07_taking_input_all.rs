/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Reading All Common Input Types
 * File: 7.taking_input_all.rs
 *
 * CONCEPT:
 * Read several different value types from stdin, each on its own line or
 * separated by whitespace. Rust uses the same `read_line` + `parse` flow
 * for every type; the only difference is the destination type annotation.
 *
 * KEY POINTS:
 *  - `let n: i32 = line.trim().parse()?;`        -> nextInt
 *  - `let lo: i64 = line.trim().parse()?;`       -> nextLong
 *  - `let d: f64 = line.trim().parse()?;`        -> nextDouble
 *  - `let tok = line.split_whitespace().next();` -> next() / first token
 *  - `line.chars().next()`                        -> first char (no nextChar() in Java either)
 *
 * SYNTAX (helper pattern):
 *   fn read<T: FromStr>() -> T { ... }
 *
 * DRY RUN:
 *  Stdin (one line):  "10 5 hello 3.14 12345678901234567890"
 *    a=10, b=5, c=15, word="hello", d=3.14, lo=very_big
 */

use std::io::{self, Read};
use std::str::FromStr;

fn read_all() -> io::Result<String> {
    let mut s = String::new();
    io::stdin().read_to_string(&mut s)?;
    Ok(s)
}

fn parse_token<T: FromStr>(tok: &str) -> T
where
    <T as FromStr>::Err: std::fmt::Debug,
{
    tok.parse::<T>().expect("parse failed")
}

fn main() -> io::Result<()> {
    let buf = read_all()?;
    let mut tokens = buf.split_whitespace();

    let a: i32 = parse_token(tokens.next().unwrap_or("0"));
    let b: i32 = parse_token(tokens.next().unwrap_or("0"));
    let c = a + b;
    println!("a + b = {c}");

    let word = tokens.next().unwrap_or("");
    let ch = word.chars().next().unwrap_or('?');
    println!("First char of '{word}' = '{ch}'");

    let d: f64 = parse_token(tokens.next().unwrap_or("0.0"));
    println!("f64 = {d}");

    let lo: i64 = parse_token(tokens.next().unwrap_or("0"));
    println!("i64 = {lo}");

    Ok(())
}

/*
 * NOTES:
 *  - Java has nextInt / nextLong / nextDouble. Rust has parse::<i32> /
 *    parse::<i64> / parse::<f64> using the FromStr trait.
 *  - `read_to_string` slurps all stdin in one go — convenient for batch input.
 *  - `split_whitespace` returns an iterator that lazily yields tokens.
 *  - The generic helper `parse_token<T>` mirrors the Scanner API in a single place.
 */
