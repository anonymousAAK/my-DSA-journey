/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: Sum or Product of First N Naturals
 * File: 11.sum_or_product.rs
 *
 * PROBLEM:
 *  Read N and choice C: 1 -> sum, 2 -> product, else -> -1.
 *
 * KEY POINTS:
 *  - Sum: identity 0; closed form n*(n+1)/2.
 *  - Product (factorial): identity 1; grows VERY fast.
 *  - Iterator combinators: `(1..=n).sum::<i128>()`, `.product::<i128>()`.
 */

use std::io::Read;

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let mut it = buf.split_whitespace();
    let n: i128 = it.next().and_then(|s| s.parse().ok()).unwrap_or(5);
    let c: i32  = it.next().and_then(|s| s.parse().ok()).unwrap_or(1);

    match c {
        1 => {
            // Closed form
            let s = n * (n + 1) / 2;
            println!("{s}");
        }
        2 => {
            let p: i128 = (1..=n).product();
            println!("{p}");
        }
        _ => println!("-1"),
    }
}

/*
 * NOTES:
 *  - i128 covers up to 33! exactly; beyond that you need num-bigint.
 *  - `.sum()` and `.product()` need a turbofish (`::<i128>`) when the type
 *    can't be inferred.
 */
