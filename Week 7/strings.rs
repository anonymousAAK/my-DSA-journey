//! # Week 7: Strings
//!
//! This module covers classic string algorithms implemented idiomatically in Rust.
//! Topics include:
//! - Palindrome check (two-pointer on `&str`)
//! - Anagram detection (sorting + frequency counting with HashMap)
//! - Reverse words in a string
//! - Run-length encoding
//! - KMP (Knuth-Morris-Pratt) string search
//!
//! ## Rust-Specific Notes for DSA Learners
//! - Rust strings are UTF-8 encoded. `&str` is a borrowed string slice; `String` is
//!   an owned, growable string. Neither supports O(1) random indexing by character —
//!   you must use `.as_bytes()` (for ASCII) or `.chars()` (for Unicode).
//! - For DSA problems that assume ASCII, working with `&[u8]` (byte slices) is both
//!   safe and efficient. We can index bytes directly with O(1) access.
//! - `HashMap` is Rust's hash map from `std::collections`. Keys must be `Hash + Eq`.

use std::collections::HashMap;

// ---------------------------------------------------------------------------
// Palindrome Check (Two Pointers)
// ---------------------------------------------------------------------------

/// Checks if a string is a palindrome using two pointers on the byte representation.
///
/// This assumes ASCII input. For full Unicode palindrome checking, use `.chars()`
/// with `.rev()` — but that's O(n) in both approaches anyway.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(1)
fn is_palindrome(s: &str) -> bool {
    let bytes = s.as_bytes();
    if bytes.is_empty() {
        return true;
    }
    let mut left = 0;
    let mut right = bytes.len() - 1;
    while left < right {
        if bytes[left] != bytes[right] {
            return false;
        }
        left += 1;
        right -= 1;
    }
    true
}

/// Checks if a string is a palindrome, ignoring non-alphanumeric characters and case.
///
/// Uses Rust iterators: `filter` + `map` to normalize, then compares with reverse.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(n) — we collect into a Vec for two-ended comparison
fn is_palindrome_alphanumeric(s: &str) -> bool {
    let cleaned: Vec<char> = s.chars()
        .filter(|c| c.is_alphanumeric())
        .map(|c| c.to_ascii_lowercase())
        .collect();
    // Compare the cleaned sequence with its reverse.
    cleaned.iter().eq(cleaned.iter().rev())
}

// ---------------------------------------------------------------------------
// Anagram Detection
// ---------------------------------------------------------------------------

/// Checks if two strings are anagrams by sorting their characters.
///
/// # Complexity
/// - Time:  O(n log n) — dominated by sorting
/// - Space: O(n) — the sorted character vectors
fn is_anagram_sort(a: &str, b: &str) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut chars_a: Vec<char> = a.chars().collect();
    let mut chars_b: Vec<char> = b.chars().collect();
    chars_a.sort_unstable();
    chars_b.sort_unstable();
    chars_a == chars_b
}

/// Checks if two strings are anagrams using frequency counting with a HashMap.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(k) where k = number of distinct characters
fn is_anagram_freq(a: &str, b: &str) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut freq: HashMap<char, i32> = HashMap::new();
    for ch in a.chars() {
        *freq.entry(ch).or_insert(0) += 1;
    }
    for ch in b.chars() {
        *freq.entry(ch).or_insert(0) -= 1;
    }
    // All counts must be zero for a valid anagram.
    freq.values().all(|&count| count == 0)
}

// ---------------------------------------------------------------------------
// Reverse Words
// ---------------------------------------------------------------------------

/// Reverses the order of words in a string.
///
/// Words are separated by whitespace. Leading/trailing whitespace is trimmed,
/// and multiple spaces between words are collapsed to a single space.
///
/// Uses Rust's `split_whitespace()` iterator which handles all of the above.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(n) — the output string
fn reverse_words(s: &str) -> String {
    let words: Vec<&str> = s.split_whitespace().collect();
    // `iter().rev()` reverses the iterator; `collect::<Vec<_>>` is needed
    // before `join` because `join` is defined on slices.
    words.into_iter().rev().collect::<Vec<&str>>().join(" ")
}

// ---------------------------------------------------------------------------
// Run-Length Encoding
// ---------------------------------------------------------------------------

/// Encodes a string using run-length encoding.
///
/// Consecutive identical characters are replaced by the character followed by
/// its count. E.g., "aaabbc" -> "a3b2c1".
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(n) — the output string
fn run_length_encode(s: &str) -> String {
    if s.is_empty() {
        return String::new();
    }

    let mut result = String::new();
    let mut chars = s.chars();
    let mut current = chars.next().unwrap();
    let mut count = 1u32;

    for ch in chars {
        if ch == current {
            count += 1;
        } else {
            result.push(current);
            result.push_str(&count.to_string());
            current = ch;
            count = 1;
        }
    }
    // Don't forget the last run.
    result.push(current);
    result.push_str(&count.to_string());

    result
}

/// Decodes a run-length encoded string back to the original.
///
/// E.g., "a3b2c1" -> "aaabbc"
///
/// # Complexity
/// - Time:  O(n) where n = length of decoded output
/// - Space: O(n)
fn run_length_decode(s: &str) -> String {
    let mut result = String::new();
    let mut chars = s.chars();

    while let Some(ch) = chars.next() {
        // Collect all consecutive digit characters for multi-digit counts.
        let mut count_str = String::new();
        // We need to peek — Rust iterators don't have peek built in here,
        // so we use a Peekable wrapper. For simplicity, we assume single-digit
        // counts or collect digits manually.
        // Actually, let's use the Peekable approach:
        // (But since we already consumed from `chars`, let's collect remaining
        //  and re-parse.)
        // Simpler approach: iterate with index on bytes (ASCII assumption).
        result.push(ch);
        // The next character(s) should be digits.
        let _ = count_str; // We'll re-approach below.
        // Let's use a cleaner method:
        break; // Break out — we'll implement differently.
    }

    // Cleaner implementation using peekable on chars.
    result.clear();
    let mut iter = s.chars().peekable();
    while let Some(ch) = iter.next() {
        if ch.is_alphabetic() {
            // Collect the following digits.
            let mut count_str = String::new();
            while let Some(&digit) = iter.peek() {
                if digit.is_ascii_digit() {
                    count_str.push(digit);
                    iter.next();
                } else {
                    break;
                }
            }
            let count: usize = count_str.parse().unwrap_or(1);
            for _ in 0..count {
                result.push(ch);
            }
        }
    }
    result
}

// ---------------------------------------------------------------------------
// KMP (Knuth-Morris-Pratt) String Search
// ---------------------------------------------------------------------------

/// Builds the Longest Proper Prefix which is also Suffix (LPS) array for KMP.
///
/// `lps[i]` = length of the longest proper prefix of `pattern[0..=i]` that is
/// also a suffix of `pattern[0..=i]`.
///
/// # Complexity
/// - Time:  O(m) where m = pattern length
/// - Space: O(m) for the LPS array
fn build_lps(pattern: &[u8]) -> Vec<usize> {
    let m = pattern.len();
    let mut lps = vec![0usize; m];
    let mut length = 0; // Length of the previous longest prefix suffix.
    let mut i = 1;

    while i < m {
        if pattern[i] == pattern[length] {
            length += 1;
            lps[i] = length;
            i += 1;
        } else if length != 0 {
            // Don't increment i — try the shorter prefix.
            length = lps[length - 1];
        } else {
            lps[i] = 0;
            i += 1;
        }
    }
    lps
}

/// Searches for all occurrences of `pattern` in `text` using the KMP algorithm.
///
/// Returns a `Vec<usize>` of starting indices where `pattern` matches in `text`.
///
/// KMP avoids redundant comparisons by using the LPS array to skip ahead when
/// a mismatch occurs, guaranteeing linear time.
///
/// # Complexity
/// - Time:  O(n + m) where n = text length, m = pattern length
/// - Space: O(m) for the LPS array + O(k) for k match positions
fn kmp_search(text: &str, pattern: &str) -> Vec<usize> {
    let mut matches = Vec::new();

    if pattern.is_empty() {
        return matches;
    }

    let text = text.as_bytes();
    let pattern = pattern.as_bytes();
    let n = text.len();
    let m = pattern.len();

    if m > n {
        return matches;
    }

    let lps = build_lps(pattern);

    let mut i = 0; // Index in text
    let mut j = 0; // Index in pattern

    while i < n {
        if text[i] == pattern[j] {
            i += 1;
            j += 1;
        }

        if j == m {
            // Full match found at index i - j.
            matches.push(i - j);
            j = lps[j - 1]; // Continue searching for overlapping matches.
        } else if i < n && text[i] != pattern[j] {
            if j != 0 {
                j = lps[j - 1]; // Skip ahead using LPS.
            } else {
                i += 1;
            }
        }
    }

    matches
}

// ===========================================================================
// Main — demonstrations and test assertions
// ===========================================================================

fn main() {
    println!("=== Week 7: Strings ===\n");

    // --- Palindrome ---
    println!("--- Palindrome Check ---");
    assert!(is_palindrome("racecar"));
    assert!(is_palindrome("abba"));
    assert!(is_palindrome("a"));
    assert!(is_palindrome(""));
    assert!(!is_palindrome("hello"));
    println!("is_palindrome(\"racecar\") = {}", is_palindrome("racecar"));

    assert!(is_palindrome_alphanumeric("A man, a plan, a canal: Panama"));
    assert!(!is_palindrome_alphanumeric("race a car"));
    println!(
        "is_palindrome_alphanumeric(\"A man, a plan, a canal: Panama\") = {}",
        is_palindrome_alphanumeric("A man, a plan, a canal: Panama")
    );

    // --- Anagram ---
    println!("\n--- Anagram Detection ---");
    assert!(is_anagram_sort("listen", "silent"));
    assert!(is_anagram_freq("listen", "silent"));
    assert!(!is_anagram_sort("hello", "world"));
    assert!(!is_anagram_freq("hello", "world"));
    assert!(is_anagram_freq("anagram", "nagaram"));
    println!("is_anagram(\"listen\", \"silent\") = true");
    println!("is_anagram(\"hello\", \"world\")   = false");

    // --- Reverse Words ---
    println!("\n--- Reverse Words ---");
    assert_eq!(reverse_words("the sky is blue"), "blue is sky the");
    assert_eq!(reverse_words("  hello   world  "), "world hello");
    assert_eq!(reverse_words("single"), "single");
    println!("reverse_words(\"the sky is blue\") = \"{}\"", reverse_words("the sky is blue"));

    // --- Run-Length Encoding ---
    println!("\n--- Run-Length Encoding ---");
    assert_eq!(run_length_encode("aaabbc"), "a3b2c1");
    assert_eq!(run_length_encode("a"), "a1");
    assert_eq!(run_length_encode(""), "");
    assert_eq!(run_length_encode("aabbccdd"), "a2b2c2d2");
    println!("encode(\"aaabbc\") = \"{}\"", run_length_encode("aaabbc"));

    assert_eq!(run_length_decode("a3b2c1"), "aaabbc");
    assert_eq!(run_length_decode("a1"), "a");
    println!("decode(\"a3b2c1\") = \"{}\"", run_length_decode("a3b2c1"));

    // Round-trip test
    let original = "aaabbbccccdd";
    let encoded = run_length_encode(original);
    let decoded = run_length_decode(&encoded);
    assert_eq!(decoded, original);
    println!("Round-trip: \"{}\" -> \"{}\" -> \"{}\"", original, encoded, decoded);

    // --- KMP Search ---
    println!("\n--- KMP String Search ---");
    let text = "ABABDABACDABABCABAB";
    let pattern = "ABABCABAB";
    let positions = kmp_search(text, pattern);
    assert_eq!(positions, vec![9]);
    println!("KMP search for \"{}\" in \"{}\": positions = {:?}", pattern, text, positions);

    // Multiple occurrences
    let text2 = "aaaaaa";
    let pattern2 = "aa";
    let positions2 = kmp_search(text2, pattern2);
    assert_eq!(positions2, vec![0, 1, 2, 3, 4]); // Overlapping matches
    println!("KMP search for \"{}\" in \"{}\": positions = {:?}", pattern2, text2, positions2);

    // No match
    let positions3 = kmp_search("hello", "xyz");
    assert!(positions3.is_empty());
    println!("KMP search for \"xyz\" in \"hello\": positions = {:?}", positions3);

    // LPS array demonstration
    let lps = build_lps("ABABCABAB".as_bytes());
    println!("LPS for \"ABABCABAB\": {:?}", lps);
    assert_eq!(lps, vec![0, 0, 1, 2, 0, 1, 2, 3, 4]);

    println!("\nAll assertions passed!");
}
