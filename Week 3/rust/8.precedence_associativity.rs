/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: Operator Precedence and Associativity
 * File: 8.precedence_associativity.rs
 *
 * CONCEPT:
 *  Rust's operator precedence is similar to C/C++/Java with a few twists:
 *   - There is NO `**` (exponentiation) -- use `i32::pow(...)`.
 *   - There is NO `>>>` (unsigned right shift).
 *   - Comparisons CANNOT be chained: `1 < x < 10` is a compile error.
 *   - `as` (cast) has its own precedence level (above mul, below unary).
 *
 * KEY POINTS:
 *  - Most binary operators are LEFT-TO-RIGHT.
 *  - Assignment operators (`=`, `+=`, etc.) are STATEMENTS, not expressions
 *    in Rust -- you cannot do `let z = (x = 5);`.
 *  - The borrow checker enforces strict evaluation rules; operand evaluation
 *    is left-to-right and well-defined.
 */

fn main() {
    // Precedence basics
    println!("10 + 20 * 30 = {}", 10 + 20 * 30);     // 610
    println!("(10+20)*30  = {}", (10 + 20) * 30);    // 900

    // No `**` -- use pow
    println!("2_i32.pow(10) = {}", 2_i32.pow(10));

    // Comparisons CANNOT be chained
    let x = 7;
    // let bad = 1 < x < 10;   // compile error
    let ok  = (1 < x) && (x < 10);
    println!("1 < {x} && {x} < 10 = {ok}");

    // Cast precedence: `as` binds tighter than the binary arithmetic
    let v = 5_i32;
    let f = v as f64 * 2.0;     // (v as f64) * 2.0 -> 10.0
    println!("v as f64 * 2.0 = {f}");

    // Assignment is a statement; you cannot assign-and-test in one expression.
    // let y = (x = 5);   // error: assignment is not an expression

    // Operand evaluation order is well-defined: left to right
    fn label(name: &str, val: i32) -> i32 {
        println!("  evaluating {name} -> {val}");
        val
    }
    let r = label("LHS", 1) + label("RHS", 2);
    println!("r = {r}");
}

/*
 * NOTES:
 *  - Rust eliminates several Java/C++ pitfalls (no chained comparisons, no
 *    assignment-in-condition, no unsigned-right-shift token, etc.).
 *  - For exponentiation, use `i32::pow(u32)`, `i64::pow`, `f64::powi`/`f64::powf`.
 *  - Operand evaluation order is GUARANTEED left-to-right (unlike C++).
 */
