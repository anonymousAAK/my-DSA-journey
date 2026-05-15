/*
 * WEEK 5 - RUST FUNCTIONS & RECURSION
 * Topic: Recursion Basics
 * File: 3.recursion_basics.rs
 *
 * CONCEPT:
 *  Rust supports recursion but does NOT guarantee tail-call optimisation
 *  (although LLVM may do it in release mode for tail-recursive forms).
 *  Stack size is OS-default (~8 MB on Linux); deep recursion may overflow.
 *
 * KEY POINTS:
 *  - Mutability for accumulators -- pass `&mut Vec` etc.
 *  - For very deep recursion, prefer loops or explicit stacks.
 */

fn print_desc(n: i32) {
    if n == 0 { return; }
    print!("{n} ");
    print_desc(n - 1);
}

fn print_asc(n: i32) {
    if n == 0 { return; }
    print_asc(n - 1);
    print!("{n} ");
}

fn factorial(n: u64) -> u64 {
    if n <= 1 { 1 } else { n * factorial(n - 1) }
}

fn sum_n(n: i64) -> i64 {
    if n == 0 { 0 } else { n + sum_n(n - 1) }
}

fn power(base: i64, exp: u32) -> i64 {
    if exp == 0 { 1 } else { base * power(base, exp - 1) }
}

fn fast_power(base: i64, exp: u32) -> i64 {
    if exp == 0 { return 1; }
    if exp % 2 == 0 {
        let h = fast_power(base, exp / 2);
        h * h
    } else {
        base * fast_power(base, exp - 1)
    }
}

fn main() {
    print!("Descending 5..1: "); print_desc(5); println!();
    print!("Ascending  1..5: "); print_asc(5);  println!();

    println!("5!  = {}", factorial(5));
    println!("10! = {}", factorial(10));

    println!("sum(10) = {}", sum_n(10));
    println!("2^10 = {}", power(2, 10));
    println!("2^10 (fast) = {}", fast_power(2, 10));
    println!("3^20 (fast) = {}", fast_power(3, 20));
}

/*
 * NOTES:
 *  - u64 holds factorial up to 20!; beyond that switch to u128 or num-bigint.
 *  - Default stack is ample for ~10000-frame depths; for more, use std::thread::Builder
 *    to set a custom stack size.
 */
