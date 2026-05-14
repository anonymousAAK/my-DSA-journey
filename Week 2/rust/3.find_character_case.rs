/*
 * WEEK 2 - RUST CONTROL FLOW
 * Topic: Character Case Detection via Unicode
 * File: 3.find_character_case.rs
 *
 * PROBLEM:
 *  Output 1 for uppercase, 0 for lowercase, -1 otherwise.
 *
 * CONCEPT:
 *  Rust's `char` (4-byte Unicode scalar) has built-in methods:
 *  `is_ascii_uppercase()`, `is_ascii_lowercase()`, `is_uppercase()`,
 *  `is_lowercase()`. The first pair is byte-level ASCII; the second pair
 *  handles full Unicode (e.g. Greek, Cyrillic).
 *
 * KEY POINTS:
 *  - `char` is Unicode; `.is_ascii_uppercase()` matches Java's char range A-Z.
 *  - To get the code point as integer: `ch as u32`.
 *  - For a string `s`, the first char is `s.chars().next().unwrap()`.
 *
 * SYNTAX:
 *   if ch.is_ascii_uppercase() { 1 } else if ch.is_ascii_lowercase() { 0 } else { -1 }
 *
 * DRY RUN:
 *  'Q' -> 1; 'q' -> 0; '7' -> -1
 *
 * COMPLEXITY: O(1).
 */

use std::io::Read;

fn classify(ch: char) -> i32 {
    if ch.is_ascii_uppercase() { 1 }
    else if ch.is_ascii_lowercase() { 0 }
    else { -1 }
}

fn main() {
    let mut buf = String::new();
    if std::io::stdin().read_to_string(&mut buf).unwrap_or(0) == 0 || buf.trim().is_empty() {
        // Demo mode
        for c in ['Q', 'q', '7', '!'] {
            println!("'{c}' -> {}", classify(c));
        }
        return;
    }
    let ch = buf.trim().chars().next().unwrap();
    println!("{}", classify(ch));
}

/*
 * NOTES:
 *  - Rust char methods cover both ASCII and full Unicode -- choose the right pair.
 *  - Indexing a Rust string by integer is forbidden (UTF-8 may make it ambiguous);
 *    always iterate via `.chars()` or use byte indices for ASCII-only data.
 *  - There's no implicit char-to-int conversion; use `ch as u32`.
 */
