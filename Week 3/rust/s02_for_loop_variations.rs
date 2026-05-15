/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: For Loop Variations
 * File: 2.for_loop_variations.rs
 *
 * CONCEPT:
 *  Since Rust's `for` is iterator-based, the Java "omit init / omit cond"
 *  trick doesn't translate verbatim. Instead, you swap iterators:
 *   - `0..3`           -> 0, 1, 2
 *   - `(0..).take(5)`  -> 0, 1, 2, 3, 4 (infinite range, take first N)
 *   - `iter::repeat(x)`-> infinite stream of x
 *   - `loop { ... break; }` -> uncoditional infinite
 *
 * KEY POINTS:
 *  - Two-counter Java loops -> use `iter1.zip(iter2)`.
 *  - Endless range `0..` is supported as an Iterator (yields 0, 1, 2, ...).
 *  - For descending: `(0..n).rev()` or `(0..=n).rev()`.
 */

fn main() {
    // 1) Plain count
    for i in 0..3 { print!("{i} "); }
    println!();

    // 2) Step by 2
    for i in (0..10).step_by(2) { print!("{i} "); }
    println!();

    // 3) Equivalent of "no condition" (infinite) with .take()
    for i in (0..).take(3) { print!("{i} "); }
    println!();

    // 4) Two counters via zip
    for (a, b) in (0..5).zip((0..5).rev()) {
        println!("  {a} {b}");
    }

    // 5) The unconditional infinite loop with manual break
    let mut n = 0;
    loop {
        if n >= 3 { println!("stopped at n={n}"); break; }
        print!("{n} ");
        n += 1;
    }
    println!();
}

/*
 * NOTES:
 *  - Rust ranges are IMPLEMENTED AS ITERATORS, so all combinators apply.
 *  - `0..` (no upper bound) is infinite; combine with `.take(n)`, `.filter(...)`.
 *  - `loop` is the canonical infinite loop; can return a value via `break value;`.
 */
