/*
 * WEEK 16 - RUST DSA
 * Topic: Hashing Fundamentals + Classic HashMap Problems
 * File: 1.HashingAndHashMap.rs
 *
 * CONCEPT:
 *     A hash table maps keys to slots through a hash function so insert/lookup
 *     are O(1) average. Rust ships `std::collections::HashMap<K,V>` and
 *     `HashSet<T>` backed by Google's SwissTable (hashbrown), with SipHash
 *     as the default DOS-resistant hasher.
 *
 * KEY POINTS:
 *     - Keys must implement `Eq + Hash`.
 *     - Default hasher is SipHash-1-3 (slow but secure); use FxHash / AHash
 *       in performance-critical code.
 *     - `entry(key).or_insert(value)` is the idiomatic compute-if-absent.
 *     - `map.get(&k)` returns `Option<&V>` — the borrow-checker forces you
 *       to think about lifetimes.
 *     - To use a complex key (Vec<u8>, tuple, etc.), it just needs Eq+Hash.
 *
 * ALGORITHM / APPROACH:
 *     For each problem: pick a key that captures the invariant, probe via
 *     `entry()` or `get()`, update or insert.
 *
 * RUST-SPECIFIC NOTES:
 *     - Borrow checker: a single mutable reference at a time. The `entry()`
 *       API hands you a unique handle so you can read-modify-write safely.
 *     - String is heap-owned, &str is a slice borrow. Anagram keys are
 *       sorted byte vectors (`Vec<u8>`); HashMap lets us use them as keys.
 *     - Pattern matching with `if let Some(idx) = map.get(&x)` is concise.
 *     - `Vec::iter().enumerate()` mirrors Python; no manual index needed.
 *
 * DRY RUN:
 *     Example A — two_sum(&[2,7,11,15], 9)
 *         i=0 x=2  complement=7  not in seen -> insert 2:0
 *         i=1 x=7  complement=2  found  -> return Some([0,1])
 *
 *     Example B — group_anagrams(["eat","tea","tan","ate","nat","bat"])
 *         "eat" -> sorted bytes [97,101,116] -> ["eat"]
 *         "tea" -> [97,101,116] -> ["eat","tea"]
 *         "tan" -> [97,110,116] -> ["tan"]
 *         "ate" -> [97,101,116] -> ["eat","tea","ate"]
 *         "nat" -> [97,110,116] -> ["tan","nat"]
 *         "bat" -> [97,98,116]  -> ["bat"]
 *
 * COMPLEXITY:
 *     two_sum                O(n) time, O(n) space
 *     frequency              O(n) time, O(n) space
 *     group_anagrams         O(n * k log k) time, O(n*k) space
 *     has_zero_sum_subarray  O(n) time, O(n) space
 *     subarray_sum           O(n) time, O(n) space
 *     longest_consecutive    O(n) average time, O(n) space
 */

use std::collections::{HashMap, HashSet};

// PROBLEM 1: Two Sum
pub fn two_sum(nums: &[i32], target: i32) -> Option<[usize; 2]> {
    let mut seen: HashMap<i32, usize> = HashMap::with_capacity(nums.len());
    for (i, &x) in nums.iter().enumerate() {
        let complement = target - x;
        if let Some(&j) = seen.get(&complement) {
            return Some([j, i]);
        }
        seen.insert(x, i);
    }
    None
}

// PROBLEM 2: Frequency Count
pub fn frequency(arr: &[i32]) -> HashMap<i32, i32> {
    let mut freq = HashMap::new();
    for &x in arr {
        *freq.entry(x).or_insert(0) += 1;        // entry API = compute-if-absent
    }
    freq
}

// PROBLEM 3: Group Anagrams
pub fn group_anagrams(strs: &[&str]) -> Vec<Vec<String>> {
    let mut groups: HashMap<Vec<u8>, Vec<String>> = HashMap::new();
    for &s in strs {
        let mut key: Vec<u8> = s.bytes().collect();
        key.sort_unstable();
        groups.entry(key).or_insert_with(Vec::new).push(s.to_string());
    }
    groups.into_values().collect()
}

// PROBLEM 4: Subarray With Zero Sum
pub fn has_zero_sum_subarray(arr: &[i32]) -> bool {
    let mut seen: HashSet<i64> = HashSet::new();
    seen.insert(0);                              // empty prefix
    let mut sum: i64 = 0;
    for &x in arr {
        sum += x as i64;
        if !seen.insert(sum) {                   // insert returns false if present
            return true;
        }
    }
    false
}

pub fn subarray_sum(nums: &[i32], k: i32) -> i32 {
    let mut counts: HashMap<i64, i32> = HashMap::new();
    counts.insert(0, 1);
    let mut sum: i64 = 0;
    let mut total = 0i32;
    for &x in nums {
        sum += x as i64;
        if let Some(&c) = counts.get(&(sum - k as i64)) {
            total += c;
        }
        *counts.entry(sum).or_insert(0) += 1;
    }
    total
}

// PROBLEM 5: Longest Consecutive Sequence
pub fn longest_consecutive(nums: &[i32]) -> i32 {
    let s: HashSet<i32> = nums.iter().copied().collect();
    let mut best = 0;
    for &x in &s {
        if !s.contains(&(x - 1)) {               // start of a run
            let mut length = 1;
            while s.contains(&(x + length)) {
                length += 1;
            }
            if length > best {
                best = length;
            }
        }
    }
    best
}

fn main() {
    println!("=== Two Sum ===");
    println!("{:?}", two_sum(&[2, 7, 11, 15], 9));   // Some([0, 1])
    println!("{:?}", two_sum(&[3, 2, 4], 6));        // Some([1, 2])

    println!("\n=== Frequency Count ===");
    let freq = frequency(&[1, 3, 2, 3, 1, 1, 4]);
    let mut kvs: Vec<_> = freq.iter().collect();
    kvs.sort_by_key(|(k, _)| *k);                    // deterministic print
    for (k, v) in kvs {
        println!("  {} -> {}", k, v);
    }

    println!("\n=== Group Anagrams ===");
    for g in group_anagrams(&["eat", "tea", "tan", "ate", "nat", "bat"]) {
        println!("  {:?}", g);
    }

    println!("\n=== Subarray With Zero Sum ===");
    println!("{}", has_zero_sum_subarray(&[4, 2, -3, 1, 6]));   // true
    println!("{}", has_zero_sum_subarray(&[4, 2,  0, 1, 6]));   // true
    println!("{}", has_zero_sum_subarray(&[-3, 2, 3, 1, 6]));   // false

    println!("\n=== Subarray Sum == k ===");
    println!("{}", subarray_sum(&[1, 1, 1], 2));                // 2
    println!("{}", subarray_sum(&[1, 2, 3], 3));                // 2

    println!("\n=== Longest Consecutive Sequence ===");
    println!("{}", longest_consecutive(&[100, 4, 200, 1, 3, 2]));            // 4
    println!("{}", longest_consecutive(&[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]));    // 9
}

/*
 * NOTES (Rust vs Java):
 *   - Rust's HashMap returns Option<&V> from .get; Java returns null.
 *     Option forces you to handle the absent case at compile time.
 *   - The borrow checker forbids holding two simultaneous mutable references
 *     into a map; the entry() API is the workaround.
 *   - Java HashMap's default hash is the key's .hashCode(); Rust uses SipHash
 *     (DOS-resistant) — swap with FxHash / AHash for raw speed.
 *   - Iteration order is non-deterministic in both languages but Rust's order
 *     can change between runs because the hasher is seeded at startup.
 *   - Strings: Java has one immutable String; Rust has owned String + &str
 *     borrows. Both are valid HashMap keys.
 *   - or_insert_with(Vec::new) lazily constructs the default — cheaper than
 *     Java's computeIfAbsent which always builds the lambda result.
 */
