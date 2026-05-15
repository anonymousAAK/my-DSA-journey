/*
 * WEEK 4 - RUST PATTERN PROBLEMS
 * Topic: Reverse Number Pattern
 * File: 4.reverse_num_pattern.rs
 *
 * PATTERN (N=4): 1 / 21 / 321 / 4321
 */

use std::io::Read;

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: usize = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(4);

    for i in 1..=n {
        for j in (1..=i).rev() {
            print!("{j}");
        }
        println!();
    }
}

/*
 * NOTES:
 *  - .rev() on a Range yields the reverse iterator.
 *  - For inclusive descending you can also use (1..=i).rev() or step_by + map.
 */
