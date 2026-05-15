/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: Increment / Decrement (or lack thereof)
 * File: 6.increment_decrement_operator.rs
 *
 * CONCEPT:
 *  Rust HAS NO `++` / `--` operators (intentional design choice). Use
 *  `x += 1` and `x -= 1`. The omission removes the entire pre/post-fix
 *  evaluation-order debate.
 *
 * KEY POINTS:
 *  - `x += 1`, `x -= 1` are the only ways.
 *  - Mutability is required: `let mut x = 5;`.
 *  - Rust panics on overflow in debug; wraps in release. Use checked_add etc.
 */

fn main() {
    let mut a: i32 = 5;
    println!("initial a = {a}");

    a += 1;
    println!("after a += 1: {a}");

    a -= 1;
    println!("after a -= 1: {a}");

    // The Java post/pre demo translated:
    println!("\n--- Java post/pre translation ---");
    let mut a = 5;
    let snapshot = a;          // like a++ result (capture old)
    a += 1;
    println!("a++ result = {snapshot}, a now = {a}");
    a += 1;                    // like ++a (use new value)
    println!("++a result = {a}, a now = {a}");
    let snapshot = a;          // like a--
    a -= 1;
    println!("a-- result = {snapshot}, a now = {a}");
    a -= 1;                    // like --a
    println!("--a result = {a}, a now = {a}");

    // Loops -- iterate, don't manually count
    println!("\n--- idiomatic loop ---");
    let arr = [10, 20, 30, 40, 50];
    for (i, v) in arr.iter().enumerate() {
        println!("  arr[{i}] = {v}");
    }
}

/*
 * NOTES:
 *  - Rust devs intentionally omitted ++/-- for clarity and to avoid UB pitfalls.
 *  - Always declare `let mut` to allow modification; `let` alone is immutable.
 *  - For arithmetic that might overflow: checked_add returns Option<T>.
 */
