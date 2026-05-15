/*
 * WEEK 5 - RUST FUNCTIONS & RECURSION
 * Topic: Method Overloading
 * File: 2.method_overloading.rs
 *
 * CONCEPT:
 *  RUST DOES NOT HAVE TRADITIONAL OVERLOADING. To get similar behaviour,
 *  use one of:
 *   - Generics + traits (compile-time, like C++ templates).
 *   - Multiple methods with different names (idiomatic in Rust).
 *   - Enum dispatch when the variants are known.
 *
 * KEY POINTS:
 *  - `fn add<T: Add>(a: T, b: T) -> T::Output { a + b }` -- generic.
 *  - Functions with the SAME name in the same scope CONFLICT (compile error).
 *  - Trait methods can be implemented per type, giving polymorphism.
 */

use std::ops::Add;
use std::fmt::Display;

// Generic function -- one definition for many types
fn add_generic<T: Add<Output = T> + Display + Copy>(a: T, b: T) -> T {
    let r = a + b;
    println!("add_generic: {a} + {b} = {r}");
    r
}

// Distinct names for distinct overloads
fn add_three(a: i32, b: i32, c: i32) -> i32 { a + b + c }

// Print collection (generic)
fn print_array<T: Display>(label: &str, arr: &[T]) {
    print!("{label}: ");
    for x in arr { print!("{x} "); }
    println!();
}

fn main() {
    let _ = add_generic(2, 3);            // i32
    let _ = add_generic(1.5, 2.5);         // f64
    let _ = add_generic(10_u8, 20);        // u8 (after default-int rule)

    println!("add_three(1,2,3) = {}", add_three(1, 2, 3));

    print_array("ints  ", &[1, 2, 3]);
    print_array("floats", &[1.1, 2.2, 3.3]);
    print_array("chars ", &['a', 'b', 'c']);
    print_array("strs  ", &["hi", "ho"]);
}

/*
 * NOTES:
 *  - Rust prefers GENERICS + TRAITS over name overloading -- one function works
 *    for many types as long as the trait bounds are met.
 *  - For runtime dispatch, use `dyn Trait` (analogous to Java interfaces).
 *  - The orphan rule restricts where you can implement traits across crates.
 */
