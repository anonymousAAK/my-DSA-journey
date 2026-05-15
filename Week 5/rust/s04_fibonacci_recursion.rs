/*
 * WEEK 5 - RUST FUNCTIONS & RECURSION
 * Topic: Fibonacci -- Naive, Memoised, Iterative
 * File: 4.fibonacci_recursion.rs
 *
 * APPROACHES:
 *  1. Naive recursion: O(2^n).
 *  2. Memoisation with HashMap: O(n).
 *  3. Iterative bottom-up: O(n) time, O(1) space.
 */

use std::collections::HashMap;

fn fib_naive(n: u32) -> u128 {
    if n <= 1 { return n as u128; }
    fib_naive(n - 1) + fib_naive(n - 2)
}

fn fib_memo(n: u32, memo: &mut HashMap<u32, u128>) -> u128 {
    if n <= 1 { return n as u128; }
    if let Some(&v) = memo.get(&n) { return v; }
    let v = fib_memo(n - 1, memo) + fib_memo(n - 2, memo);
    memo.insert(n, v);
    v
}

fn fib_iter(n: u32) -> u128 {
    if n <= 1 { return n as u128; }
    let (mut a, mut b) = (0_u128, 1_u128);
    for _ in 2..=n {
        let c = a + b;
        a = b;
        b = c;
    }
    b
}

fn count_calls(n: u32, calls: &mut u64) -> u128 {
    *calls += 1;
    if n <= 1 { return n as u128; }
    count_calls(n - 1, calls) + count_calls(n - 2, calls)
}

fn main() {
    print!("first 10 fibs: ");
    for i in 0..10 { print!("{} ", fib_iter(i)); }
    println!();

    let n = 10_u32;
    println!("\nfib({n}):");
    println!("  Naive    : {}", fib_naive(n));
    let mut memo = HashMap::new();
    println!("  Memo     : {}", fib_memo(n, &mut memo));
    println!("  Iter     : {}", fib_iter(n));

    let big = 90_u32;
    println!("\nfib({big}) iter = {}", fib_iter(big));
    let mut memo = HashMap::new();
    println!("fib({big}) memo = {}", fib_memo(big, &mut memo));

    let mut calls = 0;
    count_calls(5, &mut calls);
    println!("\nfib_naive(5) makes {calls} recursive calls");
}

/*
 * NOTES:
 *  - u128 supports fib up to ~186; switch to num-bigint beyond that.
 *  - HashMap-based memoisation is general; for fixed n a Vec is faster.
 *  - Tuple swap idiom: `let (a, b) = (b, a + b);` is also clean.
 */
