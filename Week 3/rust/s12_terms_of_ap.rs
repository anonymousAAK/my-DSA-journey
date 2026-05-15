/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: First X Terms of 3N+2 Not Divisible by 4
 * File: 12.terms_of_ap.rs
 *
 * PROBLEM:
 *  Print the first X terms of (3N+2) where N=1,2,3,..., skipping those
 *  divisible by 4.
 *
 * KEY POINTS:
 *  - Imperative: two counters (count, n).
 *  - Functional: an infinite range piped through .filter and .take:
 *      (1..).map(|n| 3*n + 2).filter(|t| t % 4 != 0).take(x).for_each(...)
 */

use std::io::Read;

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let x: usize = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(5);

    // Imperative
    let mut count = 0_usize;
    let mut n = 1_i64;
    while count < x {
        let t = 3 * n + 2;
        if t % 4 != 0 {
            print!("{t} ");
            count += 1;
        }
        n += 1;
    }
    println!();

    // Functional
    let collected: Vec<i64> = (1..)
        .map(|n: i64| 3 * n + 2)
        .filter(|t| t % 4 != 0)
        .take(x)
        .collect();
    println!("{:?}", collected);
}

/*
 * NOTES:
 *  - The `(1..)` infinite range is lazy -- combine with `.take(x)`.
 *  - Iterator pipelines compile to tight loops; performance matches imperative.
 */
