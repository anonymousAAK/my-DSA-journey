/*
 * WEEK 2 - RUST CONTROL FLOW
 * Topic: While Loop Basics
 * File: 4.while_loop.rs
 *
 * CONCEPT:
 *  Rust's `while` looks like Java's, but assignment-in-condition is forbidden
 *  (`=` is a statement). The condition must be a `bool`.
 *
 * KEY POINTS:
 *  - `while cond { body }`
 *  - Rust has a `loop { ... break ...; }` for infinite loops, with optional
 *    label syntax `'outer: loop { break 'outer; }`.
 *  - There is NO `do-while` (workaround: `loop { ... if !cond { break } }`).
 *  - `while let Some(x) = iter.next() { ... }` is a pattern-matching while.
 *
 * SYNTAX:
 *   while x < n { x += 1; }
 *   loop { if done { break; } }
 *
 * DRY RUN (Java's quirky example):
 *  x=5, y=5
 *  Rust forbids `(x = 5) == y` -- assignment is not an expression.
 *  We re-create the semantics by setting x = 5 at the top of the body.
 */

fn main() {
    let mut x = 5;
    let mut y = 5;
    let mut iterations = 0;

    loop {
        x = 5;             // mimic Java's `(x = 5)`
        if x != y { break; }
        println!("Hello");
        x += 1;
        y += 1;
        iterations += 1;
        if iterations >= 5 { break; }     // safety cap
    }
    println!("ran {iterations} iteration(s)");

    // Clean while loop
    let mut i = 1;
    while i <= 5 {
        println!("i = {i}");
        i += 1;
    }

    // `while let` pattern
    let mut stack = vec![1, 2, 3, 4, 5];
    while let Some(top) = stack.pop() {
        print!("{top} ");
    }
    println!();
}

/*
 * NOTES:
 *  - Rust's `=` is a STATEMENT, not an expression -- no "assign in condition" idiom.
 *  - `loop { }` is the canonical infinite loop; prefer it to `while true { }`.
 *  - `loop` can be labelled for multi-level break/continue (Java has labels too).
 *  - `while let` is amazing for iterator-driven loops.
 */
