/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: Bitwise Operators
 * File: 7.bitwise_operator.rs
 *
 * CONCEPT:
 *  Rust supports & | ^ ! << >> on integers. Bitwise NOT is `!` (same token
 *  as logical NOT) -- the operand's type determines which interpretation.
 *  There is NO `>>>` (unsigned right shift) -- cast to the unsigned type
 *  and use `>>`.
 *
 * KEY POINTS:
 *  - i32::pow, count_ones, count_zeros, leading_zeros etc. are useful methods.
 *  - {:032b} format spec prints 32-bit binary.
 *  - Right shift on signed Rust integers is ARITHMETIC (preserves sign);
 *    cast to unsigned for logical shift.
 */

fn main() {
    let a: i32 = 19;     // 10011
    let b: i32 = 28;     // 11100

    println!("a       = {a:>5b}  ({a})");
    println!("b       = {b:>5b}  ({b})");
    println!("a & b   = {} ({:>5b})", a & b, a & b);
    println!("a | b   = {} ({:>5b})", a | b, a | b);
    println!("a ^ b   = {} ({:>5b})", a ^ b, a ^ b);
    println!("!a      = {}     // bitwise NOT (since a is integer)", !a);
    println!("a << 2  = {}", a << 2);
    println!("a >> 2  = {}", a >> 2);

    // Java's >>> emulation
    let n: i32 = -4;
    let urs: u32 = (n as u32) >> 28;
    println!("(-4 as u32) >> 28 = {urs}");

    // Useful methods
    println!("\n--- handy bit methods ---");
    let x: u32 = 0b10110;
    println!("x.count_ones()      = {}", x.count_ones());
    println!("x.leading_zeros()   = {}", x.leading_zeros());
    println!("x.trailing_zeros()  = {}", x.trailing_zeros());
    println!("x.is_power_of_two() = {}", x.is_power_of_two());
}

/*
 * NOTES:
 *  - Rust uses `!` for both logical and bitwise NOT (no `~`).
 *  - For unsigned right shift, cast to u32/u64 first.
 *  - Integer methods (count_ones, leading_zeros, ...) are zero-cost and very useful.
 *  - For 64-bit constants, use suffixes like `0xFFFFFFFFu64`.
 */
