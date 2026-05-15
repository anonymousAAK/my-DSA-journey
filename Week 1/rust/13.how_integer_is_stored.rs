/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: How Integers are Stored in Memory
 * File: 13.how_integer_is_stored.rs
 *
 * CONCEPT:
 * Rust's signed integers (i8 .. i128) use two's-complement representation
 * (guaranteed by the language spec). Negative numbers can be inspected
 * with format!("{:032b}", value) — the cast to the matching unsigned type
 * shows the raw bit pattern.
 *
 * KEY POINTS:
 *  - sizeof i32 = 4 bytes, 32 bits.
 *  - Positive n  -> binary digits of n.
 *  - Negative n  -> two's complement (2^32 + n).
 *  - Use `as u32` to view the unsigned bit pattern of an i32.
 *  - `format!("{:032b}", value)` zero-pads to 32 bits.
 *
 * SYNTAX:
 *   println!("{:032b}", n as u32);
 *   let bytes = n.to_be_bytes();  // big-endian byte array
 *
 * DRY RUN — -4 in 32-bit two's complement:
 *  step 1) +4         = 0000_0000_..._0100
 *  step 2) ~4          = 1111_1111_..._1011
 *  step 3) +1          = 1111_1111_..._1100   (-> -4)
 */

fn main() {
    println!("size_of::<i32>() = {} bytes", std::mem::size_of::<i32>());
    println!("i32::MIN = {}", i32::MIN);
    println!("i32::MAX = {}", i32::MAX);

    let positive: i32 = 4;
    let negative: i32 = -4;

    println!("\n=== +4 ===");
    println!("decimal: {positive}");
    println!("32-bit : {:032b}", positive as u32);
    println!("bytes  : {:?}", positive.to_be_bytes());

    println!("\n=== -4 (two's complement) ===");
    println!("decimal: {negative}");
    println!("32-bit : {:032b}", negative as u32);
    println!("bytes  : {:?}", negative.to_be_bytes());

    println!("\n=== Step-by-step derivation of -4 ===");
    let step1: u32 = 4;
    let step2: u32 = !step1;             // ones-complement
    let step3: u32 = step2.wrapping_add(1); // twos-complement
    println!("step1) +4 binary       = {step1:032b}");
    println!("step2) invert all bits = {step2:032b}");
    println!("step3) plus 1          = {step3:032b}");
    println!("matches -4 ? {}", step3 == (negative as u32));

    println!("\n=== Larger integer: i128 ===");
    println!("i128::MAX bit length = {}", i128::MAX.count_ones() + i128::MAX.count_zeros());
}

/*
 * NOTES:
 *  - Java does the same two's-complement representation (and silently overflows).
 *  - Python `int` is arbitrary precision -- you must mask to get fixed-width bits.
 *  - Rust panics on integer overflow in DEBUG mode; in RELEASE it wraps.
 *  - Use `wrapping_add`, `checked_add`, `saturating_add`, `overflowing_add` to
 *    control behaviour explicitly.
 */
