//! # Week 5: Recursion
//!
//! This module covers fundamental recursion patterns and techniques in Rust.
//! Topics include:
//! - Factorial (iterative + recursive)
//! - Fibonacci (naive, memoized with HashMap, iterative)
//! - Tower of Hanoi
//! - Fast exponentiation (binary exponentiation)
//! - String recursion: reverse, digit sum, palindrome check
//! - Subset generation (power set)
//!
//! ## Rust-Specific Notes for DSA Learners
//! - Rust has no garbage collector; recursion that allocates (e.g., Vec, String) must
//!   be mindful of ownership. We pass `&mut` references to avoid unnecessary cloning.
//! - `HashMap` is used for memoization — keys must implement `Hash + Eq`.
//! - Pattern matching (`match`) replaces if-else chains and is exhaustive.

use std::collections::HashMap;

// ---------------------------------------------------------------------------
// Factorial
// ---------------------------------------------------------------------------

/// Computes `n!` iteratively.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(1)
fn factorial_iterative(n: u64) -> u64 {
    // Rust ranges are zero-cost iterators; `fold` accumulates the product.
    (1..=n).fold(1u64, |acc, x| acc * x)
}

/// Computes `n!` recursively.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(n) — call-stack depth
fn factorial_recursive(n: u64) -> u64 {
    match n {
        0 | 1 => 1,
        _ => n * factorial_recursive(n - 1),
    }
}

// ---------------------------------------------------------------------------
// Fibonacci
// ---------------------------------------------------------------------------

/// Naive recursive Fibonacci — exponential time, included for pedagogical contrast.
///
/// # Complexity
/// - Time:  O(2^n)
/// - Space: O(n) — call-stack depth
fn fib_naive(n: u32) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => fib_naive(n - 1) + fib_naive(n - 2),
    }
}

/// Memoized Fibonacci using a `HashMap`.
///
/// The memo map is passed by `&mut` reference so the caller owns the cache and
/// can reuse it across calls (common Rust pattern for top-down DP).
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(n) — HashMap entries + call-stack depth
fn fib_memo(n: u32, memo: &mut HashMap<u32, u64>) -> u64 {
    if let Some(&val) = memo.get(&n) {
        return val;
    }
    let result = match n {
        0 => 0,
        1 => 1,
        _ => fib_memo(n - 1, memo) + fib_memo(n - 2, memo),
    };
    memo.insert(n, result);
    result
}

/// Iterative (bottom-up) Fibonacci — optimal for single queries.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(1)
fn fib_iterative(n: u32) -> u64 {
    if n == 0 {
        return 0;
    }
    let (mut a, mut b) = (0u64, 1u64);
    for _ in 2..=n {
        let temp = a + b;
        a = b;
        b = temp;
    }
    b
}

// ---------------------------------------------------------------------------
// Tower of Hanoi
// ---------------------------------------------------------------------------

/// Solves the Tower of Hanoi puzzle, printing each move.
///
/// Moves `n` disks from `source` to `target` using `auxiliary`.
///
/// # Complexity
/// - Time:  O(2^n) — the minimum number of moves is 2^n - 1
/// - Space: O(n) — call-stack depth
fn tower_of_hanoi(n: u32, source: &str, target: &str, auxiliary: &str, moves: &mut Vec<String>) {
    if n == 0 {
        return;
    }
    tower_of_hanoi(n - 1, source, auxiliary, target, moves);
    moves.push(format!("Move disk {} from {} to {}", n, source, target));
    tower_of_hanoi(n - 1, auxiliary, target, source, moves);
}

// ---------------------------------------------------------------------------
// Fast Power (Binary Exponentiation)
// ---------------------------------------------------------------------------

/// Computes `base^exp` using binary exponentiation.
///
/// Works for non-negative integer exponents. Uses the identity:
///   base^exp = (base^(exp/2))^2           if exp is even
///   base^exp = base * (base^(exp/2))^2    if exp is odd
///
/// # Complexity
/// - Time:  O(log exp)
/// - Space: O(1) (iterative version)
fn fast_power(mut base: i64, mut exp: u32) -> i64 {
    let mut result: i64 = 1;
    while exp > 0 {
        if exp % 2 == 1 {
            result *= base;
        }
        base *= base;
        exp /= 2;
    }
    result
}

/// Recursive version of fast power — included for comparison.
///
/// # Complexity
/// - Time:  O(log exp)
/// - Space: O(log exp) — call-stack depth
fn fast_power_recursive(base: i64, exp: u32) -> i64 {
    match exp {
        0 => 1,
        _ if exp % 2 == 0 => {
            let half = fast_power_recursive(base, exp / 2);
            half * half
        }
        _ => {
            let half = fast_power_recursive(base, exp / 2);
            base * half * half
        }
    }
}

// ---------------------------------------------------------------------------
// String Recursion: reverse, digit_sum, is_palindrome
// ---------------------------------------------------------------------------

/// Reverses a string recursively.
///
/// In Rust, strings are UTF-8 encoded. We work with `char` iterators to handle
/// multi-byte characters correctly. This version builds a new `String`.
///
/// # Complexity
/// - Time:  O(n^2) due to string concatenation at each level
/// - Space: O(n^2) total allocated strings across recursive calls
fn reverse_string(s: &str) -> String {
    if s.is_empty() {
        return String::new();
    }
    // `chars()` gives an iterator over Unicode scalar values.
    let mut chars = s.chars();
    let first = chars.next().unwrap();
    let rest: String = chars.collect();
    let mut reversed = reverse_string(&rest);
    reversed.push(first);
    reversed
}

/// Sums the digits of a non-negative integer recursively.
///
/// # Complexity
/// - Time:  O(d) where d = number of digits
/// - Space: O(d) — call-stack depth
fn digit_sum(n: u64) -> u64 {
    if n < 10 {
        return n;
    }
    (n % 10) + digit_sum(n / 10)
}

/// Checks if a string is a palindrome recursively.
///
/// Compares the first and last characters, then recurses on the inner substring.
/// We use byte slices for ASCII; for full Unicode you'd use `chars()`.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(n) — call-stack depth (could be O(1) with iteration)
fn is_palindrome(s: &str) -> bool {
    let bytes = s.as_bytes();
    if bytes.len() <= 1 {
        return true;
    }
    if bytes[0] != bytes[bytes.len() - 1] {
        return false;
    }
    // Slice the inner portion — this is O(1) because slices are just pointer + length.
    is_palindrome(&s[1..s.len() - 1])
}

// ---------------------------------------------------------------------------
// Subset Generation (Power Set)
// ---------------------------------------------------------------------------

/// Generates all subsets of the given slice using backtracking.
///
/// Each element is either included or excluded — classic "pick / skip" pattern.
///
/// # Complexity
/// - Time:  O(n * 2^n) — 2^n subsets, each up to length n
/// - Space: O(n * 2^n) — to store all subsets; O(n) call-stack depth
fn generate_subsets(nums: &[i32]) -> Vec<Vec<i32>> {
    let mut result: Vec<Vec<i32>> = Vec::new();
    let mut current: Vec<i32> = Vec::new();
    backtrack(nums, 0, &mut current, &mut result);
    result
}

/// Backtracking helper for subset generation.
///
/// # Rust Ownership Note
/// `current` is passed as `&mut Vec<i32>` — we push before recursing and pop
/// after, so the same vector is reused (no cloning on recursive calls).
/// We only `clone()` when storing a complete subset into `result`.
fn backtrack(nums: &[i32], index: usize, current: &mut Vec<i32>, result: &mut Vec<Vec<i32>>) {
    if index == nums.len() {
        result.push(current.clone()); // Clone here to snapshot current state.
        return;
    }
    // Include nums[index]
    current.push(nums[index]);
    backtrack(nums, index + 1, current, result);
    current.pop(); // Backtrack — undo the choice.

    // Exclude nums[index]
    backtrack(nums, index + 1, current, result);
}

// ===========================================================================
// Main — demonstrations and test assertions
// ===========================================================================

fn main() {
    println!("=== Week 5: Recursion ===\n");

    // --- Factorial ---
    println!("--- Factorial ---");
    assert_eq!(factorial_iterative(0), 1);
    assert_eq!(factorial_iterative(5), 120);
    assert_eq!(factorial_recursive(0), 1);
    assert_eq!(factorial_recursive(5), 120);
    assert_eq!(factorial_iterative(10), factorial_recursive(10));
    println!("5! = {} (iterative)", factorial_iterative(5));
    println!("10! = {} (recursive)", factorial_recursive(10));

    // --- Fibonacci ---
    println!("\n--- Fibonacci ---");
    assert_eq!(fib_naive(0), 0);
    assert_eq!(fib_naive(1), 1);
    assert_eq!(fib_naive(10), 55);

    let mut memo = HashMap::new();
    assert_eq!(fib_memo(10, &mut memo), 55);
    assert_eq!(fib_memo(20, &mut memo), 6765);
    // The memo map now contains cached values from both calls.
    println!("fib(10) = {} (memoized)", fib_memo(10, &mut memo));

    assert_eq!(fib_iterative(0), 0);
    assert_eq!(fib_iterative(10), 55);
    assert_eq!(fib_iterative(20), 6765);
    println!("fib(20) = {} (iterative)", fib_iterative(20));

    // --- Tower of Hanoi ---
    println!("\n--- Tower of Hanoi (3 disks) ---");
    let mut moves = Vec::new();
    tower_of_hanoi(3, "A", "C", "B", &mut moves);
    assert_eq!(moves.len(), 7); // 2^3 - 1 = 7 moves
    for m in &moves {
        println!("  {}", m);
    }

    // --- Fast Power ---
    println!("\n--- Fast Power ---");
    assert_eq!(fast_power(2, 10), 1024);
    assert_eq!(fast_power(3, 0), 1);
    assert_eq!(fast_power(5, 3), 125);
    assert_eq!(fast_power_recursive(2, 10), 1024);
    assert_eq!(fast_power_recursive(5, 3), 125);
    println!("2^10 = {}", fast_power(2, 10));
    println!("5^3  = {}", fast_power(5, 3));

    // --- String Recursion ---
    println!("\n--- String Recursion ---");
    assert_eq!(reverse_string("hello"), "olleh");
    assert_eq!(reverse_string(""), "");
    assert_eq!(reverse_string("a"), "a");
    println!("reverse(\"hello\") = \"{}\"", reverse_string("hello"));

    assert_eq!(digit_sum(12345), 15);
    assert_eq!(digit_sum(0), 0);
    assert_eq!(digit_sum(9), 9);
    println!("digit_sum(12345) = {}", digit_sum(12345));

    assert!(is_palindrome("racecar"));
    assert!(is_palindrome("abba"));
    assert!(is_palindrome("a"));
    assert!(is_palindrome(""));
    assert!(!is_palindrome("hello"));
    println!("is_palindrome(\"racecar\") = {}", is_palindrome("racecar"));

    // --- Subset Generation ---
    println!("\n--- Subset Generation ---");
    let subsets = generate_subsets(&[1, 2, 3]);
    assert_eq!(subsets.len(), 8); // 2^3 = 8 subsets
    println!("Subsets of [1, 2, 3]:");
    for s in &subsets {
        println!("  {:?}", s);
    }

    // Edge case: empty set
    let empty_subsets = generate_subsets(&[]);
    assert_eq!(empty_subsets.len(), 1); // Only the empty subset
    assert_eq!(empty_subsets[0], vec![]);

    println!("\nAll assertions passed!");
}
