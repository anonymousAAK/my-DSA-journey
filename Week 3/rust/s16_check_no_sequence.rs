/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: Decreasing-then-Increasing Sequence Check
 * File: 16.check_no_sequence.rs
 *
 * PROBLEM:
 *  Sequence is valid iff strictly decreasing then strictly increasing
 *  (transition once). Equal consecutive values -> false.
 *
 * KEY POINTS:
 *  - Walk pairs with `windows(2)` or zip(seq, seq[1..]).
 *  - State: bool `is_dec` (initially true).
 *
 * COMPLEXITY: O(n) time, O(1) space.
 */

use std::io::Read;

fn check(s: &[i64]) -> bool {
    if s.len() < 2 { return true; }
    let mut is_dec = true;
    for w in s.windows(2) {
        let (a, b) = (w[0], w[1]);
        if a == b { return false; }
        if b < a {
            if !is_dec { return false; }    // already increasing
        } else {
            if is_dec { is_dec = false; }    // transition once
        }
    }
    true
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    if buf.trim().is_empty() {
        for v in [
            vec![5, 3, 1, 2, 4],
            vec![1, 2, 3, 4, 5],
            vec![5, 4, 3, 2, 1],
            vec![1, 2, 3, 2, 1],
            vec![1, 2, 2, 3],
        ] {
            println!("{v:?} -> {}", check(&v));
        }
        return;
    }
    let mut it = buf.split_whitespace();
    let n: usize = it.next().and_then(|s| s.parse().ok()).unwrap_or(0);
    let s: Vec<i64> = it.take(n).map(|s| s.parse().unwrap()).collect();
    println!("{}", check(&s));
}

/*
 * NOTES:
 *  - `slice.windows(2)` yields overlapping pairs efficiently.
 *  - For STREAMED input keep only `prev` -- O(1) memory.
 */
