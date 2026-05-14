/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: continue Statement
 * File: 4.continue.rs
 *
 * CONCEPT:
 *  `continue` skips to the next iteration. Like Rust's `break`, it can be
 *  labelled to apply to an outer loop: `continue 'outer;`.
 *
 * KEY POINTS:
 *  - `continue;` re-tests innermost loop's condition (or advances iterator).
 *  - `continue 'label;` goes to the next iteration of the labelled loop.
 *  - In `while`, ensure the counter is updated BEFORE continue (same pitfall as Java).
 */

fn main() {
    // continue in for
    for i in 1..=5 {
        if i == 3 { continue; }
        println!("{i}");
    }
    println!("---");

    // continue in while -- update first!
    let mut i = 1;
    while i <= 5 {
        if i == 3 {
            i += 1;        // CRITICAL
            continue;
        }
        println!("{i}");
        i += 1;
    }

    // Labelled continue
    println!("--- labelled continue ---");
    'outer: for x in 1..=3 {
        for y in 1..=3 {
            if x == y { continue 'outer; }   // skip rest of inner AND outer-iter
            println!("(x={x}, y={y})");
        }
    }
}

/*
 * NOTES:
 *  - Without label, `continue` only affects the innermost loop.
 *  - For functional style, use `.filter(...)` on iterators instead.
 */
