/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Operators in Rust (Arithmetic, Relational, Logical, Bitwise)
 * File: 16.operators.rs
 *
 * CONCEPT:
 * Rust supports virtually the same operator set as C++ / Java, with a few
 * twists:
 *  - No `**` (use `pow` methods).
 *  - No `>>>` (unsigned-right-shift); cast to unsigned and use `>>`.
 *  - No implicit numeric conversion between operands — types must match.
 *  - Logical AND/OR/NOT are `&&` `||` `!` (same as Java/C++).
 *
 * KEY POINTS:
 *  - Arithmetic: + - * / %
 *  - Relational: == != > < >= <=  (operands must be the SAME type; PartialOrd)
 *  - Logical:    && || !          (short-circuiting, on bool only)
 *  - Bitwise:    & | ^ ! << >>    (NOT is `!` on integers too — equivalent to ~)
 *  - Range:      a..b (exclusive), a..=b (inclusive)
 *  - Reference:  & for borrow, &mut for mutable borrow, * for dereference
 *
 * SYNTAX:
 *   if a > b && c < d { ... }
 *   let m = if a > b { a } else { b };
 *   for i in 0..n { ... }                 // 0,1,...,n-1
 *   for i in 0..=n { ... }                // 0,1,...,n
 *
 * DRY RUN:
 *  19 & 28 -> 16; 19 | 28 -> 31; 19 ^ 28 -> 15; !19_i32 -> -20
 *  19 << 2 -> 76; 19 >> 2 -> 4
 *  (5 > 6) && (true) -> false
 */

fn main() {
    println!("=== Arithmetic ===");
    println!("10 + 3 = {}", 10 + 3);
    println!("10 / 3 = {}  (i32 -> truncates)", 10 / 3);
    println!("10.0 / 3.0 = {}", 10.0_f64 / 3.0_f64);
    println!("10 % 3 = {}", 10 % 3);
    println!("2_i32.pow(10) = {}", 2_i32.pow(10));

    println!("\n=== Relational ===");
    let a = 5; let b = 6;
    println!("a == b: {}", a == b);
    println!("a != b: {}", a != b);
    println!("a > b : {}", a > b);
    println!("a < b : {}", a < b);

    println!("\n=== Logical ===");
    let x = true; let y = false;
    println!("x && y: {}", x && y);
    println!("x || y: {}", x || y);
    println!("!x    : {}", !x);

    println!("\n=== Bitwise ===");
    let p: i32 = 19;
    let q: i32 = 28;
    println!("p     = {:08b}", p);
    println!("q     = {:08b}", q);
    println!("p & q = {}  (== {:08b})", p & q, p & q);
    println!("p | q = {}", p | q);
    println!("p ^ q = {}", p ^ q);
    println!("!p    = {}  (Rust's bitwise NOT for ints)", !p);
    println!("p<<2  = {}", p << 2);
    println!("p>>2  = {}", p >> 2);

    // Unsigned-right-shift emulation
    let n: i32 = -4;
    let urs: u32 = (n as u32) >> 28;
    println!("(-4 as u32) >> 28 = {urs}");

    println!("\n=== Conditional expression ===");
    let m = if a > b { a } else { b };
    println!("max(a,b) via if = {m}");

    println!("\n=== Ranges ===");
    let mut sum = 0;
    for i in 1..=5 {                  // inclusive 1..=5 -> 1,2,3,4,5
        sum += i;
    }
    println!("1+2+3+4+5 = {sum}");
}

/*
 * NOTES:
 *  - Rust's bitwise NOT for ints is `!`, not `~` as in Java/C++.
 *  - The logical NOT and bitwise NOT share the same `!` operator — context
 *    (operand type) tells the compiler which to apply.
 *  - No implicit conversions: `1 + 2.0` is a compile error in Rust.
 *  - `if`/`match` are expressions and can return values directly.
 *  - Range types (`0..n`, `0..=n`) are the idiomatic loop drivers.
 */
