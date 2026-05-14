/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Hello World - First Rust Program
 * File: 2.hello_world.rs
 *
 * CONCEPT:
 * Every Rust executable starts at `fn main()`. The `println!` macro writes
 * a formatted line to stdout (note the trailing `!` — `println` is a MACRO,
 * not a function). No class wrapper, no manual newline, just a single line.
 *
 * KEY POINTS:
 *  - `fn` declares a function; `main` is the entry point.
 *  - `println!` (with `!`) is a MACRO — expands to formatted I/O at compile time.
 *  - Strings use double quotes; single quotes are for the `char` type.
 *  - Statements end with a semicolon; the last expression in a block has none if it returns a value.
 *  - Rust is statically typed but uses TYPE INFERENCE so explicit types are rarely needed in main.
 *
 * SYNTAX:
 *  println!("text");           // newline included
 *  print!("text");              // no newline
 *  eprintln!("error message");  // to stderr
 *  println!("x = {}", x);       // {} is the default placeholder
 *
 * DRY RUN:
 *  Run -> stdout shows three "Hello World" lines.
 *
 * COMPLEXITY: O(1).
 */

fn main() {
    println!("Hello World");
    println!("Hello World");
    println!("Hello World");

    // print! omits the newline (like Java's print, Python's end="")
    print!("Hello ");
    print!("World ");
    println!("on the same line.");

    // Stderr counterpart
    eprintln!("(this goes to stderr)");

    // Formatted output — {} is the default formatter (Display trait)
    let name = "Rust";
    println!("Hello, {}!", name);
}

/*
 * NOTES:
 *  - Java requires `System.out.println(...)`; Rust uses `println!(...)`.
 *  - `println!` is a MACRO; it accepts a variable number of arguments and
 *    parses the format string at compile time.
 *  - Strings (`&str`) are UTF-8 by default; `char` is a 32-bit Unicode scalar.
 *  - Rust has NO null pointer; use `Option<T>` for "may be absent" values.
 */
