/*
 * WEEK 2 - RUST CONTROL FLOW
 * Topic: Data Types Review
 * File: 1.data_types_review.rs
 *
 * CONCEPT:
 *  Re-examine type behaviour with arithmetic and relational operators.
 *  1. Narrow types: i8 overflow (Rust panics in debug, wraps in release).
 *  2. Integer division stored in f64.
 *  3. Modulo on i32 and f64 (via `%` -- which works for both).
 *  4. Relational ops return bool.
 *
 * KEY POINTS:
 *  - Rust has NO implicit numeric conversions; cast with `as`.
 *  - 6 / 4 == 1 (i32 / i32 truncates toward zero).
 *  - 6.0 / 4.0 == 1.5 (f64 / f64).
 *  - `%` works on integers AND floats in Rust (unlike C++ which needs fmod).
 *
 * SYNTAX:
 *   let q: i32 = 6 / 4;     // 1
 *   let r: f64 = 6.0 / 4.0; // 1.5
 *   let m: f64 = 55.5 % 10.0; // 5.5
 *
 * DRY RUN:
 *   (6/4) -> 1; stored as f64 -> 1.0
 *   55.5 % 10.0 -> 5.5
 *   5 > 6 -> false
 *
 * COMPLEXITY: O(1).
 */

fn main() {
    // Example 1: i8 overflow
    let small: i8 = 50;
    // In DEBUG mode, the next line PANICS (overflow):
    // let prod: i8 = small * 50;
    // In RELEASE it wraps. The safe explicit forms:
    let prod_wrap = small.wrapping_mul(50);
    let prod_checked = small.checked_mul(50);  // Option<i8>
    println!("50 * 50 (i8 wrapping)  = {prod_wrap}");
    println!("50 * 50 (i8 checked)   = {prod_checked:?}");

    // Example 2: integer division stored in f64 doesn't recover precision
    let a: f64 = (6 / 4) as f64;     // 1.0
    let b: i32 = 6 / 4;               // 1
    let c: f64 = a + b as f64;        // 2.0
    println!("(6/4) as f64 + (6/4) = {c}");

    // Example 3: modulo for both int and float
    let x: f64 = 55.5;
    let y: i32 = 55;
    println!("55.5 % 10.0 = {}", x % 10.0);  // 5.5
    println!("55  %  10  = {}", y % 10);     // 5

    // Example 4: relational ops return bool
    let (v1, v2) = (5, 6);
    println!("(5 > 6) = {}", v1 > v2);       // false
}

/*
 * NOTES:
 *  - Java's int silently wraps on overflow; Rust PANICS in debug, wraps in release.
 *    Use `.wrapping_*`, `.checked_*`, `.saturating_*`, `.overflowing_*` to be explicit.
 *  - Unlike C++, Rust's `%` works on floats natively.
 *  - `as` casts are explicit -- no implicit numeric coercion.
 */
