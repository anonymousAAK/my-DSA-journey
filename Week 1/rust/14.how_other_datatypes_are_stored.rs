/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: How f32/f64 and char are Stored
 * File: 14.how_other_datatypes_are_stored.rs
 *
 * CONCEPT:
 * Rust's f32 (32-bit IEEE 754) and f64 (64-bit IEEE 754) mirror Java's float
 * and double. Rust's `char` is FOUR bytes and represents any Unicode scalar
 * value (NOT a 1-byte ASCII char like C++ or a 2-byte UTF-16 unit like Java).
 *
 * KEY POINTS:
 *  - `1.5`   -> f64 by default;  `1.5_f32` selects f32.
 *  - No `f` suffix is required for f64 literals (it is the default).
 *  - char literals: 'A', '\n', '🚀' (any single Unicode scalar).
 *  - `'A' as u32` gives the code point (65).
 *  - `char::from_u32(65)` returns Option<char>.
 *  - Char + int does NOT compile — must cast: `(ch as u32) + 1`.
 *  - To iterate bytes use `.bytes()`; for chars use `.chars()`.
 *
 * SYNTAX:
 *  let f: f32 = 1.5_f32;
 *  let d: f64 = 1.5;
 *  let c: char = 'X';
 *  let code: u32 = c as u32;            // 88
 *  let next = char::from_u32(code + 1); // Some('Y')
 *
 * DRY RUN:
 *  ('a' as u32) + 1 == 98          (Java: 'a' + 1 == 98)
 *  ('a' as u32) + ('b' as u32) == 195
 *  char::from_u32(88).unwrap() == 'X'
 */

fn main() {
    use std::mem::size_of;
    println!("size_of::<f32>()  = {}", size_of::<f32>());
    println!("size_of::<f64>()  = {}", size_of::<f64>());
    println!("size_of::<char>() = {}", size_of::<char>());
    println!("size_of::<u8>()   = {}", size_of::<u8>());

    // Float vs double precision
    let f: f32 = 10.4;
    let d: f64 = 10.4;
    println!("\nf32 10.4 = {f:.20}");
    println!("f64 10.4 = {d:.20}");

    // Char arithmetic — cast through integer
    let ch1: char = char::from_u32(88).unwrap();     // 'X'
    let ch2: char = 'Y';
    println!("\n{ch1} {ch2}");

    let a_plus_1: u32 = ('a' as u32) + 1;
    println!("'a' + 1     = {a_plus_1} (-> '{}')", char::from_u32(a_plus_1).unwrap());

    let a_plus_b: u32 = ('a' as u32) + ('b' as u32);
    println!("'a' + 'b'   = {a_plus_b}");

    // Demonstrate that char holds multi-byte Unicode
    let rocket = '🚀';
    println!("\n'🚀' code point = U+{:X}", rocket as u32);
    println!("UTF-8 byte length: {} bytes", rocket.len_utf8());
}

/*
 * NOTES:
 *  - Rust's char is 4 bytes (a full Unicode scalar value). Java uses two 16-bit
 *    UTF-16 code units to represent a char; some characters need TWO Java chars.
 *  - Rust's String is a UTF-8 byte sequence — indexing by character is O(k).
 *  - For decimal-exact math, use the `rust_decimal` crate.
 *  - `f64::EPSILON`, `f64::INFINITY`, `f64::NAN` are useful constants.
 */
