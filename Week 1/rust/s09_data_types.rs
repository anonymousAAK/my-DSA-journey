/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Data Types in Rust
 * File: 9.data_types.rs
 *
 * CONCEPT:
 * Rust's scalar (primitive) types are explicit and fixed-width:
 *   Signed integers:  i8, i16, i32, i64, i128, isize  (isize == ptr width)
 *   Unsigned ints:    u8, u16, u32, u64, u128, usize
 *   Floats:           f32, f64
 *   Boolean:          bool       (true / false)
 *   Character:        char       (4 bytes, Unicode scalar value)
 *   Unit:             ()         (used like Java's `void`)
 *
 * Compound types: tuple `(T1, T2)`, array `[T; N]`, slice `&[T]`, str / String.
 *
 * KEY POINTS:
 *  - Default integer type: i32; default float: f64.
 *  - `usize` / `isize` are used for indexing (platform-dependent width).
 *  - `char` is 4 bytes (any Unicode scalar value), NOT 1 byte ASCII.
 *  - `String` is a growable, heap-allocated, UTF-8 sequence.
 *  - `&str` is a borrowed string slice (fixed-size view into a UTF-8 buffer).
 *  - `bool` is exactly 1 byte but logically `true`/`false`.
 *  - `std::mem::size_of::<T>()` returns the byte size.
 *
 * SYNTAX:
 *   let i: i32 = 42;
 *   let f: f64 = 3.14;
 *   let b: bool = true;
 *   let c: char = 'A';            // 'A' as char (NOT u8)
 *   let s: &str = "hello";        // string slice (Display-friendly)
 *   let owned: String = String::from("world");
 *
 * DRY RUN:
 *  size_of::<i32>() = 4
 *  size_of::<f64>() = 8
 *  size_of::<char>() = 4
 *  size_of::<bool>() = 1
 */

fn main() {
    use std::mem::size_of;

    println!(
        "{:<12}{:<8}",
        "type", "bytes"
    );
    println!("--------------------");
    println!("{:<12}{:<8}", "i8",    size_of::<i8>());
    println!("{:<12}{:<8}", "i16",   size_of::<i16>());
    println!("{:<12}{:<8}", "i32",   size_of::<i32>());
    println!("{:<12}{:<8}", "i64",   size_of::<i64>());
    println!("{:<12}{:<8}", "i128",  size_of::<i128>());
    println!("{:<12}{:<8}", "isize", size_of::<isize>());
    println!("{:<12}{:<8}", "u32",   size_of::<u32>());
    println!("{:<12}{:<8}", "f32",   size_of::<f32>());
    println!("{:<12}{:<8}", "f64",   size_of::<f64>());
    println!("{:<12}{:<8}", "bool",  size_of::<bool>());
    println!("{:<12}{:<8}", "char",  size_of::<char>());
    println!("{:<12}{:<8}", "()",    size_of::<()>());

    let max_i32 = i32::MAX;
    let min_i32 = i32::MIN;
    println!("\ni32::MAX = {max_i32}, i32::MIN = {min_i32}");

    // No overflow for i128 unless you EXCEED its range; otherwise it panics in debug.
    let big: i128 = i128::MAX;
    println!("i128::MAX = {big}");

    // char vs u8
    let ch: char = 'Z';
    println!("char 'Z' code point = {}", ch as u32);

    // Tuple and array
    let tup: (i32, f64, char) = (1, 2.0, '3');
    let arr: [i32; 4] = [10, 20, 30, 40];
    println!("tuple = {tup:?}, array = {arr:?}");
}

/*
 * NOTES:
 *  - Java has 32-bit int and 64-bit long; Rust spells these i32 / i64.
 *  - Java's char is UTF-16 (2 bytes); Rust's char is full Unicode (4 bytes).
 *  - Rust has NO implicit conversions between numeric types — use `as`.
 *  - Use `{:?}` (Debug) to print compound types like tuples and arrays.
 *  - `String` is owning + growable; `&str` is borrowed + read-only.
 */
