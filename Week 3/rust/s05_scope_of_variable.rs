/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: Scope of Variables
 * File: 5.scope_of_variable.rs
 *
 * CONCEPT:
 *  Rust uses LEXICAL block scope -- like Java/C++. A variable declared
 *  inside `{ ... }` is dropped when the block ends. The borrow checker
 *  uses scopes to determine when references become invalid.
 *
 * KEY POINTS:
 *  - Variables declared in for/while/if are scoped to that block.
 *  - SHADOWING is allowed: `let x = ...; let x = ...;` creates a NEW binding.
 *  - `{ expr }` is itself an expression -- the last value becomes the result.
 *  - Variables are dropped (RAII) at end of scope; this is when destructors run.
 */

fn main() {
    // for-loop variable scoped to body
    for i in 0..3 {
        let j = i * 2;
        println!("inside for: i={i} j={j}");
    }
    // i and j are out of scope here.

    // Block as expression
    let result = {
        let x = 5;
        let y = 7;
        x + y      // last expression -> block evaluates to 12
    };
    println!("result = {result}");

    // Shadowing
    let v = 5;
    let v = v + 1;       // new binding, value 6
    let v = format!("{v}");  // shadow with String (different type!)
    println!("v = {v}");

    // Lifetime / borrowing across scope
    let big_string = String::from("hello");
    {
        let r = &big_string;          // borrow
        println!("borrowed: {r}");
    }   // r goes out of scope here
    // big_string still exists -- only `r` was scoped to the inner block
    println!("still have: {big_string}");
}

/*
 * NOTES:
 *  - Rust's borrow checker enforces that references don't outlive the data.
 *  - Shadowing is a Rust feature (Java/C++ disallow it within the same scope).
 *  - Drop order: variables go out of scope in REVERSE order of declaration.
 */
