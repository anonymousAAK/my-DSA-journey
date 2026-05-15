/*
 * WEEK 2 - RUST CONTROL FLOW
 * Topic: Infinite Loop Demonstration
 * File: 5.infinite_loop.rs
 *
 * CONCEPT:
 *  Rust's canonical infinite loop is `loop { }`. The compiler recognises it
 *  as such and even allows the loop to return a value via `break value;`.
 *
 * KEY POINTS:
 *  - `loop { body }` is infinite unless `break` is reached.
 *  - `break expr;` returns `expr` from the loop expression.
 *  - `continue;` skips to the next iteration.
 *  - Labels: `'outer: loop { 'inner: loop { break 'outer; } }`
 *
 * SYNTAX:
 *   let result: i32 = loop {
 *       if cond { break 42; }
 *   };
 *
 * DRY RUN:
 *  x=y=5; loop body fires once and we increment both equally -> infinite.
 *  We cap at 5 iterations.
 */

fn main() {
    let mut x = 5;
    let mut y = 5;
    let mut safety = 0;

    loop {
        if x != y { break; }
        println!("Hello");
        x += 1;
        y += 1;
        safety += 1;
        if safety >= 5 {
            println!("(safety cap reached)");
            break;
        }
    }

    // Loop that returns a value
    let mut n = 0;
    let captured = loop {
        n += 1;
        if n >= 10 {
            break n * n;     // value comes out of the loop
        }
    };
    println!("loop returned {captured}");
}

/*
 * NOTES:
 *  - Java's infinite-loop idiom is `while (true)`; Rust prefers `loop { }`.
 *  - `loop` is the only Rust construct that the compiler treats as "always
 *    diverging" without a condition -- handy for never-return functions.
 *  - You can return values from a loop, unique among Java/C++/Python/Rust.
 */
