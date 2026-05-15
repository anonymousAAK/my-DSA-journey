/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: For Loop Basics
 * File: 1.for_loop.rs
 *
 * CONCEPT:
 *  Rust has only one form of `for`: `for pattern in iterator { body }`.
 *  There is no C-style `for(init; cond; update)`. To iterate a counter,
 *  use a Range like `0..n` (exclusive) or `0..=n` (inclusive).
 *
 * KEY POINTS:
 *  - `0..n`     -> 0, 1, ..., n-1 (Range)
 *  - `0..=n`    -> 0, 1, ..., n
 *  - `(0..n).rev()` -> n-1, ..., 0
 *  - `(0..n).step_by(k)` -> 0, k, 2k, ...
 *  - For containers: `for x in &vec { ... }` borrows; `for x in vec` consumes.
 *  - `.enumerate()` yields (index, value) pairs.
 *  - `.zip()` parallel iteration.
 *
 * SYNTAX:
 *   for i in 0..3 { println!("Inside for loop : {i}"); }
 *
 * DRY RUN:
 *   "Inside for loop : 0", ..., "Inside for loop : 2", "Done"
 *
 * COMPLEXITY: O(n).
 */

fn main() {
    for i in 0..3 {
        println!("Inside for loop : {i}");
    }
    println!("Done");

    println!("\n--- inclusive 1..=5 ---");
    for i in 1..=5 { println!("{i}"); }

    println!("\n--- step_by ---");
    for i in (0..10).step_by(2) { print!("{i} "); }
    println!();

    println!("\n--- reverse ---");
    for i in (0..5).rev() { print!("{i} "); }
    println!();

    println!("\n--- enumerate ---");
    let arr = ["a", "b", "c"];
    for (i, v) in arr.iter().enumerate() {
        println!("  index {i}: {v}");
    }

    println!("\n--- zip ---");
    let a = [1, 2, 3];
    let b = ["x", "y", "z"];
    for (x, y) in a.iter().zip(b.iter()) {
        println!("  pair {x}-{y}");
    }
}

/*
 * NOTES:
 *  - There is NO C-style `for(init; cond; update)`. Always iterate over an Iterator.
 *  - Borrowing matters: `for x in vec` MOVES the vector; `for x in &vec` borrows.
 *  - Iterator combinators (.filter, .map, .take, .collect) replace many loops.
 *  - `loop` is the unconditional infinite loop.
 */
