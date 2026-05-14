/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: Nth Fibonacci Number
 * File: 9.nth_fibonacci_number.rs
 *
 * PROBLEM:
 *  Read N, output F(N). F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).
 *
 * KEY POINTS:
 *  - Iterative O(n) with two rolling variables.
 *  - Use u128 to push the overflow boundary (fib up to ~186 fits in u128).
 *  - For arbitrary precision, use the `num-bigint` crate.
 */

use std::io::Read;

fn fib(n: u32) -> u128 {
    let mut a: u128 = 0;
    let mut b: u128 = 1;
    for _ in 0..n {
        let c = a + b;
        a = b;
        b = c;
    }
    a
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: u32 = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(10);
    println!("fib({n}) = {}", fib(n));
    if n <= 10 {
        for i in 0..=10 { print!("{} ", fib(i)); }
        println!();
    }
}

/*
 * NOTES:
 *  - u128 covers fib up to ~186; beyond that need num-bigint.
 *  - Tuple swap idiom: `let (a, b) = (b, a + b);` is also clean.
 *  - For O(log n), use matrix exponentiation.
 */
