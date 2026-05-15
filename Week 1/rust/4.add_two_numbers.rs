/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Variables, Mutability, and Addition
 * File: 4.add_two_numbers.rs
 *
 * CONCEPT:
 * Rust variables are IMMUTABLE by default. Use the `mut` keyword to opt
 * into mutability. Types can be inferred or annotated. Rust's primitives
 * (i32, i64, f32, f64, bool, char) resemble C++ but with strict rules.
 *
 * KEY POINTS:
 *  - `let x = 10;`           -> immutable binding (cannot reassign)
 *  - `let mut x = 10;`       -> mutable; can reassign
 *  - `let x: i32 = 10;`      -> explicit type annotation
 *  - Default integer type is `i32`; default float is `f64`
 *  - Names: snake_case by convention; cannot start with digit
 *  - Shadowing is allowed: `let x = x + 1;` reuses the name (NEW binding)
 *  - Constants: `const NAME: TYPE = value;` (must be type-annotated, compile-time)
 *
 * SYNTAX:
 *   let a = 10;                 // i32 inferred
 *   let b: i32 = 25;            // explicit
 *   let c = a + b;               // 35
 *   let mut sum = 0;             // mutable; we can do `sum += a;` later
 *
 * DRY RUN:
 *  a=10, b=25
 *  c = a + b = 35
 *  println!("{}", c) -> "35"
 *
 * COMPLEXITY: O(1).
 */

fn main() {
    let a: i32 = 10;
    let b: i32 = 25;
    let c: i32 = a + b;
    println!("{}", c);                   // 35

    // Mutable binding
    let mut sum = 0;                     // i32 inferred
    sum += a;
    sum += b;
    println!("sum (mut) = {}", sum);

    // Shadowing — same name, NEW binding (can even change type)
    let x = 5;
    let x = x + 1;                       // new binding, value 6
    let x = format!("{x}");              // shadow with a String (different type!)
    println!("x (shadowed) = {x}");

    // Constants must be type-annotated and computable at compile time
    const MAX_SCORE: u32 = 100;
    println!("MAX_SCORE = {MAX_SCORE}");

    // No overflow for normal arithmetic; checked in debug builds!
    // For wrap-on-overflow use wrapping_add / overflowing_add.
    let big: i32 = 2_000_000_000;
    let wrapped = big.wrapping_add(big);
    println!("2e9 + 2e9 (wrapping i32) = {wrapped}");
}

/*
 * NOTES:
 *  - Java's `final` is similar to Rust's default `let` (immutable).
 *  - Java has no shadowing for local variables in the same scope; Rust permits it.
 *  - In DEBUG builds Rust panics on integer overflow; in RELEASE it wraps silently
 *    (per the spec). Use `i64`/`i128` or the explicit `checked_*` / `wrapping_*`
 *    methods to be precise.
 *  - Rust enforces "use only after init" — there is no "garbage value" hazard.
 */
