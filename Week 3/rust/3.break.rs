/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: break Statement
 * File: 3.break.rs
 *
 * CONCEPT:
 *  Rust `break` exits the innermost loop. Unlike Java, Rust supports
 *  LABELLED loops, so `break 'outer;` can escape multiple levels of nesting.
 *  `break value;` (in `loop`) yields a value out of the loop expression.
 *
 * KEY POINTS:
 *  - Labels start with a lifetime-style apostrophe: `'outer: loop { ... }`.
 *  - `break;` exits innermost; `break 'outer;` exits the labelled one.
 *  - `loop` is special -- it can return a value via `break value;`.
 */

fn main() {
    // break in `for`
    for i in 1..10 {
        println!("{i}");
        if i == 5 { break; }
    }

    // break in `while`
    let mut i = 1;
    while i <= 10 {
        println!("{i}");
        if i == 5 { break; }
        i += 1;
    }

    // Nested break only escapes inner
    for x in 1..=3 {
        println!("outer {x}");
        for y in 1..=5 {
            println!("  in (y={y})");
            if y == 1 { break; }
        }
    }

    // Labelled break -- escape multiple loops
    'outer: for x in 1..=3 {
        for y in 1..=5 {
            if x * y == 4 {
                println!("found pair (x={x}, y={y}); breaking outer");
                break 'outer;
            }
        }
    }

    // loop returns a value
    let result = loop {
        break 42;
    };
    println!("result = {result}");
}

/*
 * NOTES:
 *  - Labels: `'name: loop { ... break 'name; }` (Java has the same idea).
 *  - `loop { ... break val; }` returns a value; `for` and `while` cannot.
 *  - Use labels sparingly; deep nesting is usually a refactoring smell.
 */
