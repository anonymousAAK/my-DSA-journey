/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: print! / println! / eprintln! / format!
 * File: 3.better_hello_world.rs
 *
 * CONCEPT:
 * Rust offers a family of formatting macros instead of separate `print` and
 * `println` methods:
 *  - print!     -> stdout, no newline
 *  - println!   -> stdout, with newline
 *  - eprint!    -> stderr, no newline
 *  - eprintln!  -> stderr, with newline
 *  - format!    -> returns a String instead of printing
 *
 * KEY POINTS:
 *  - Macros use `!` syntax: println!(...)
 *  - Format string uses `{}` for positional args (Display trait) or `{:?}` for Debug
 *  - Width, precision, alignment: `{:>10}`, `{:.3}`, `{:0>5}`, etc.
 *  - Named arguments: `println!("{name} {age}", name="Bob", age=30)`
 *  - From Rust 1.58+ you can also CAPTURE local variables directly: `println!("{x}")`.
 *
 * SYNTAX:
 *  println!("hello");
 *  print!("no newline");
 *  let s = format!("x = {}", 42);   // returns a String
 *
 * DRY RUN:
 *  Output 1: three "Hello World" on three lines.
 *  Output 2: three on the same line (using print!).
 *  Output 3: a formatted string built with format!.
 */

fn main() {
    // println!-style: three lines
    println!("Hello World");
    println!("Hello World");
    println!("Hello World");

    println!();   // empty newline

    // print!-style: same line
    print!("Hello World");
    print!("Hello World");
    print!("Hello World");
    println!();   // close the line

    println!();

    // format! returns a String (no I/O)
    let greeting: String = format!("Hello, {}!", "Rust");
    println!("{}", greeting);

    // Named captures (Rust 1.58+)
    let x = 7;
    let y = 11;
    println!("x = {x}, y = {y}, x+y = {}", x + y);
}

/*
 * NOTES:
 *  - Java has println / print methods on System.out / System.err.
 *  - Python has one `print()` function with an `end=` keyword arg.
 *  - Rust splits the choice into separate macros (`print!`, `println!`, ...).
 *  - `format!` is the analogue of `String.format(...)` (Java) or f-strings (Python).
 *  - For binary printing use `{:b}`, for hex `{:x}`, for debug-pretty `{:#?}`.
 */
