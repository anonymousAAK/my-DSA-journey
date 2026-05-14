/*
 * WEEK 5 - RUST FUNCTIONS & RECURSION
 * Topic: Function Basics
 * File: 1.method_basics.rs
 *
 * CONCEPT:
 *  Rust functions are declared with `fn name(params) -> ReturnType { body }`.
 *  No default arguments (use Option<T> + match, or builder pattern).
 *  Pass-by-value MOVES (or copies for Copy types); use `&T` to borrow,
 *  `&mut T` to allow mutation.
 *
 * KEY POINTS:
 *  - `fn add(a: i32, b: i32) -> i32`
 *  - Last expression (no semicolon) is the return value.
 *  - `&T` borrow, `&mut T` mutable borrow.
 *  - Closures: `|x| x * 2`.
 *
 * SYNTAX:
 *  fn add(a: i32, b: i32) -> i32 { a + b }
 *  fn try_to_change(mut n: i32) { n = 999; }       // mutates local copy
 *  fn try_to_change_ref(n: &mut i32) { *n = 999; } // mutates the original
 */

fn greet() {
    println!("Hello from a function!");
}

fn print_sum(a: i32, b: i32) {
    println!("Sum of {a} and {b} = {}", a + b);
}

fn add(a: i32, b: i32) -> i32 {
    a + b      // last expression -> implicit return
}

fn multiply(x: i32, y: i32) -> i32 {
    let result = x * y;
    result
}

fn try_to_change(mut n: i32) {
    n = 999;
    println!("  inside try_to_change (by value): n = {n}");
}

fn try_to_change_ref(n: &mut i32) {
    *n = 999;
}

fn mutate_vec(v: &mut Vec<i32>) {
    v.push(99);
}

fn main() {
    greet();
    print_sum(3, 7);
    println!("add(5, 6) = {}", add(5, 6));
    println!("multiply(4, 3) = {}", multiply(4, 3));

    let x = 42;
    try_to_change(x);
    println!("after by-value:    x = {x}");
    let mut x = 42;
    try_to_change_ref(&mut x);
    println!("after by-mut-ref:  x = {x}");

    let mut v = vec![1, 2, 3];
    mutate_vec(&mut v);
    println!("vector after mutate: {v:?}");
}

/*
 * NOTES:
 *  - Rust REQUIRES `&mut` for mutation; this is part of the borrow-checker contract.
 *  - i32 is Copy, so passing by value duplicates -- no move occurs.
 *  - String / Vec are NOT Copy -- passing by value MOVES them (the original
 *    becomes invalid). Use `&str` / `&[T]` to borrow read-only.
 *  - There are no default args; use Option<T> or builder pattern.
 */
