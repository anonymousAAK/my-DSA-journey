/*
 * WEEK 7 - RUST DSA
 * Topic: Palindrome & Anagram
 * File: 2.palindrome_and_anagram.rs
 *
 * CONCEPT:
 *     Palindrome: same forwards and backwards.
 *     Anagram   : same characters with same multiplicities.
 *
 * KEY POINTS:
 *     - For ASCII inputs the .as_bytes() view enables O(1) random access.
 *     - For arbitrary UTF-8, materialise a Vec<char> first.
 *     - Frequency-array (26) for ASCII letters; HashMap for any chars.
 *
 * ALGORITHM / APPROACH:
 *     Palindrome (two-pointer over bytes):
 *         let bytes = s.as_bytes();
 *         let (mut l, mut r) = (0usize, bytes.len() - 1);
 *         while l < r {
 *             if bytes[l] != bytes[r] { return false; }
 *             l += 1; r -= 1;
 *         }
 *         true
 *
 * RUST-SPECIFIC NOTES:
 *     - char::is_alphanumeric is Unicode-aware; for ASCII use is_ascii_alphanumeric.
 *     - sort a Vec<char> with .sort() then compare slices.
 *     - Use std::collections::HashMap for the map approach.
 *
 * DRY RUN:
 *     "racecar" -> palindrome (true)
 *     "race a car" ignore non-alpha -> false
 *     "listen"/"silent" sorted both = "eilnst" -> anagram
 *
 * COMPLEXITY:
 *     Palindrome  : O(n)
 *     Sort anagram: O(n log n)
 *     Freq anagram: O(n)
 *     Map  anagram: O(n)
 */

use std::collections::HashMap;

fn is_palindrome(s: &str) -> bool {
    let bytes = s.as_bytes();
    if bytes.is_empty() {
        return true;
    }
    let mut l: usize = 0;
    let mut r: usize = bytes.len() - 1;
    while l < r {
        if bytes[l] != bytes[r] {
            return false;
        }
        l += 1;
        r -= 1;
    }
    true
}

fn is_palindrome_ignore_non_alpha(s: &str) -> bool {
    let chars: Vec<char> = s.chars().collect();
    if chars.is_empty() {
        return true;
    }
    let mut l: i64 = 0;
    let mut r: i64 = chars.len() as i64 - 1;
    while l < r {
        while l < r && !chars[l as usize].is_alphanumeric() {
            l += 1;
        }
        while l < r && !chars[r as usize].is_alphanumeric() {
            r -= 1;
        }
        let a = chars[l as usize].to_ascii_lowercase();
        let b = chars[r as usize].to_ascii_lowercase();
        if a != b {
            return false;
        }
        l += 1;
        r -= 1;
    }
    true
}

fn is_anagram_sort(a: &str, b: &str) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut va: Vec<char> = a.chars().collect();
    let mut vb: Vec<char> = b.chars().collect();
    va.sort();
    vb.sort();
    va == vb
}

fn is_anagram_freq(a: &str, b: &str) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut freq = [0i32; 26];
    for c in a.bytes() {
        freq[(c - b'a') as usize] += 1;
    }
    for c in b.bytes() {
        let i = (c - b'a') as usize;
        freq[i] -= 1;
        if freq[i] < 0 {
            return false;
        }
    }
    true
}

fn is_anagram_map(a: &str, b: &str) -> bool {
    if a.chars().count() != b.chars().count() {
        return false;
    }
    let mut m: HashMap<char, i32> = HashMap::new();
    for c in a.chars() {
        *m.entry(c).or_insert(0) += 1;
    }
    for c in b.chars() {
        let entry = m.entry(c).or_insert(0);
        if *entry == 0 {
            return false;
        }
        *entry -= 1;
    }
    true
}

fn main() {
    println!("=== Palindrome ===");
    for t in ["racecar", "hello", "level", "madam", "a", ""] {
        println!("is_palindrome(\"{}\") = {}", t, is_palindrome(t));
    }

    println!("\nis_palindrome_ignore_non_alpha:");
    let s1 = "A man, a plan, a canal: Panama";
    println!("\"{}\" = {}", s1, is_palindrome_ignore_non_alpha(s1));
    let s2 = "race a car";
    println!("\"{}\" = {}", s2, is_palindrome_ignore_non_alpha(s2));

    println!("\n=== Anagram ===");
    let pairs = [
        ("listen", "silent"),
        ("eat", "tea"),
        ("hello", "world"),
        ("anagram", "nagaram"),
    ];
    for (a, b) in pairs {
        println!("\"{}\" vs \"{}\":", a, b);
        println!("  Sort: {}", is_anagram_sort(a, b));
        println!("  Freq: {}", is_anagram_freq(a, b));
        println!("  Map:  {}", is_anagram_map(a, b));
    }
}

/*
 * NOTES — Rust vs Java:
 *     - .as_bytes() gives O(1) ASCII indexing; .chars() iterates UTF-8 code points.
 *     - HashMap::entry().or_insert(...) replaces map.merge() pattern.
 *     - char::is_alphanumeric is Unicode-aware; use is_ascii_* for ASCII-only.
 *     - We use i64 for the alphanumeric two-pointer to avoid usize underflow.
 */
