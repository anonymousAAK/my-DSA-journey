/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Arithmetic Operations & Operator Precedence
 * File: 5.arithmetic_operation.rs
 *
 * CONCEPT:
 * Rust uses the standard +, -, *, /, % operators. Unlike Python, `/`
 * follows the SAME RULE as Java/C++: integer-by-integer division
 * truncates toward zero. Mixing integer and float types is NOT implicit
 * — you must cast with `as`.
 *
 * KEY POINTS:
 *  - i32 / i32  -> i32 (truncated toward zero)
 *  - f64 / f64  -> f64
 *  - To mix:    `i as f64 / 2.0`
 *  - No `**` operator — use `i32::pow(base, exp)` or `f64::powi/f64::powf`
 *  - Division/modulo by zero with integers PANICS (Rust's term for crash)
 *  - For float: division by zero gives `inf` or `nan` (IEEE 754)
 *
 * SYNTAX:
 *   let c = b / (2 * a);            // i32 / i32 -> i32
 *   let d = b as f64 / (2 * a) as f64;
 *   let p = 2_i32.pow(10);          // 1024
 *   let q = 2_f64.powi(10);          // 1024.0
 *
 * DRY RUN:
 *  a=3, b=10
 *  c = b / (2*a) = 10 / 6 = 1  (truncated)
 *  d = b as f64 / (2.0 * 3.0) = 1.6666...
 */

fn main() {
    let a: i32 = 3;
    let b: i32 = 10;

    let c = b / (2 * a);                 // 1
    println!("b / (2*a) = {c}");

    let d = b as f64 / (2.0 * a as f64); // 1.6666...
    println!("b/(2.0*a) = {d}");

    println!("b % (2*a) = {}", b % (2 * a));   // 4

    println!("10 + 20 * 30  = {}", 10 + 20 * 30);
    println!("(10+20) * 30 = {}", (10 + 20) * 30);

    // Exponentiation — separate functions for integer/float
    println!("2_i32.pow(10)   = {}", 2_i32.pow(10));      // 1024
    println!("2_f64.powi(10) = {}", 2_f64.powi(10));     // 1024.0
    println!("2_f64.powf(0.5) = {}", 2_f64.powf(0.5));   // 1.4142...

    // Division-by-zero behaviour
    let zero = 0;
    // let bad = 1 / zero;             // would PANIC at runtime
    let inf = 1.0_f64 / 0.0;            // IEEE inf
    let nan = 0.0_f64 / 0.0;            // IEEE NaN
    println!("1.0 / 0.0 = {inf}, 0.0/0.0 = {nan}");

    // Overflow checking differences (debug vs release)
    let big: i32 = i32::MAX;
    let wrapped = big.wrapping_add(1);
    println!("i32::MAX.wrapping_add(1) = {wrapped}");

    let _ = zero;  // silence unused warning
}

/*
 * NOTES:
 *  - Rust matches Java in truncating integer division (Python uses // for this).
 *  - Implicit conversions: NONE. You must write `x as f64` or similar.
 *  - In debug builds, integer overflow PANICS; in release it wraps. Use
 *    `checked_*` (returns Option), `saturating_*`, or `wrapping_*` explicitly.
 *  - `%` follows the sign of the dividend (like Java), not the divisor.
 *  - For exact decimal arithmetic, use the `rust_decimal` crate (no std equivalent).
 */
