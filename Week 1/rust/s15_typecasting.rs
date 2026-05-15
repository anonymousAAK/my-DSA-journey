/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Typecasting (Conversions with `as`, From, TryFrom)
 * File: 15.typecasting.rs
 *
 * CONCEPT:
 * Rust does NOT do any implicit numeric conversions — every conversion must
 * be explicit. There are three main flavours:
 *  1. `as`    — primitive cast (may truncate / wrap; never panics)
 *  2. From/Into  — lossless conversion (e.g., i32::from(127_i8))
 *  3. TryFrom/TryInto — fallible conversion (returns Result)
 *
 * KEY POINTS:
 *  - `as` is the equivalent of Java's `(type) value`.
 *  - Float -> int with `as` truncates toward zero, saturating at min/max
 *    (since Rust 1.45) rather than producing UB.
 *  - `i32::from(value)` only works when conversion is lossless.
 *  - `i32::try_from(value)` returns Err on out-of-range; great for `i64 -> i32`.
 *  - Brace init does not auto-convert (unlike C++); types must match exactly.
 *
 * SYNTAX:
 *   let l: i64 = i as i64;                  // widening
 *   let n: i32 = d as i32;                  // narrowing (truncates)
 *   let n: i32 = i32::from(127_i8);         // From (infallible)
 *   let n: i32 = i32::try_from(1_000_000_000_i64).unwrap();
 *
 * DRY RUN:
 *  i = 100_i32          -> l1 = 100_i64                  (widening)
 *  d = 100.04_f64        -> l2 = d as i64 = 100           (truncated)
 *  d = -100.99           -> d as i64 = -100               (truncates toward 0)
 *  i32::try_from(1<<40)  -> Err (out of range)
 */

fn main() {
    let i: i32 = 100;
    let l1: i64 = i as i64;            // widening via `as`
    let l1b: i64 = i64::from(i);        // widening via From (infallible)

    let d: f64 = 100.04;
    let l2: i64 = d as i64;            // narrowing -> truncates toward 0

    println!("i  = {i}");
    println!("l1 = {l1}  (i as i64)");
    println!("l1b= {l1b} (i64::from(i))");
    println!("d  = {d}");
    println!("l2 = {l2}  (d as i64; truncates)");

    // Truncation direction
    println!("(-100.99 as i64) = {}", (-100.99_f64) as i64);  // -100

    // TryFrom for fallible narrowing
    use std::convert::TryFrom;
    let big: i64 = 1_000_000_000_000;
    match i32::try_from(big) {
        Ok(n)  => println!("converted to i32: {n}"),
        Err(e) => println!("cannot fit in i32: {e}"),
    }

    let small: i64 = 42;
    match i32::try_from(small) {
        Ok(n)  => println!("converted to i32: {n}"),
        Err(e) => println!("cannot fit in i32: {e}"),
    }

    // f32 -> i32 saturating cast (since Rust 1.45)
    let huge: f64 = 1e20;
    println!("1e20 as i32 = {} (saturates at i32::MAX)", huge as i32);
}

/*
 * NOTES:
 *  - Java has implicit widening (int -> long -> double) and explicit narrowing
 *    via casts. Rust REQUIRES every conversion to be written out.
 *  - `as` never panics; out-of-range floats now saturate to min/max int.
 *  - For safety prefer `From` (infallible) or `TryFrom` (fallible) over `as`.
 *  - The orphan rule + trait coherence means you cannot retroactively add
 *    From impls between two foreign types.
 */
