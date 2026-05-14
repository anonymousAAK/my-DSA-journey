/// Week 25: String Algorithms
/// ===========================
/// This file covers fundamental string matching and pattern search algorithms.
///
/// Topics covered:
///     1. KMP (Knuth-Morris-Pratt) Pattern Matching
///     2. Rabin-Karp String Matching (rolling hash)
///     3. Z-Algorithm for Pattern Matching
///
/// Each algorithm includes:
///     - Problem statement
///     - Step-by-step approach explanation
///     - Time / space complexity analysis
///     - Example usage via main driver
///
/// Compile: rustc -O string_algorithms.rs

// ===========================================================================
// 1. KMP (Knuth-Morris-Pratt) Pattern Matching
// ===========================================================================
// Problem:
//   Given a text T of length n and a pattern P of length m, find all
//   occurrences of P in T.
//
// Approach:
//   1. Build the LPS (Longest Proper Prefix which is also a Suffix) array
//      for the pattern.
//      lps[i] = length of the longest proper prefix of P[0..i] that is
//      also a suffix of P[0..i].
//   2. Scan the text with two pointers (i for text, j for pattern).
//      On a mismatch after j matches, set j = lps[j-1] and continue,
//      skipping characters we already know must match.
//
// Complexity:
//   Time  : O(n + m)  — linear in the combined length
//   Space : O(m)      — for the LPS array

/// Build the LPS (failure function) array for the given pattern.
///
/// lps[i] = length of the longest proper prefix of pattern[0..i]
/// that is also a suffix of that substring.
///
/// Time : O(m)
/// Space: O(m)
fn kmp_build_lps(pattern: &[u8]) -> Vec<usize> {
    let m = pattern.len();
    let mut lps = vec![0usize; m];
    let mut length = 0usize; // length of previous longest prefix-suffix
    let mut i = 1;

    while i < m {
        if pattern[i] == pattern[length] {
            length += 1;
            lps[i] = length;
            i += 1;
        } else if length != 0 {
            // Fall back — do NOT increment i
            length = lps[length - 1];
        } else {
            lps[i] = 0;
            i += 1;
        }
    }
    lps
}

/// Return a vector of starting indices where `pattern` occurs in `text`
/// using the Knuth-Morris-Pratt algorithm.
///
/// Time : O(n + m)
/// Space: O(m)
fn kmp_search(text: &str, pattern: &str) -> Vec<usize> {
    let t = text.as_bytes();
    let p = pattern.as_bytes();
    let (n, m) = (t.len(), p.len());
    if m == 0 {
        return vec![];
    }

    let lps = kmp_build_lps(p);
    let mut results = Vec::new();
    let mut i = 0usize; // index into text
    let mut j = 0usize; // index into pattern

    while i < n {
        if t[i] == p[j] {
            i += 1;
            j += 1;
        }

        if j == m {
            // Full match found at index i - j
            results.push(i - j);
            j = lps[j - 1]; // look for next overlapping match
        } else if i < n && t[i] != p[j] {
            if j != 0 {
                j = lps[j - 1];
            } else {
                i += 1;
            }
        }
    }
    results
}

// ===========================================================================
// 2. Rabin-Karp String Matching
// ===========================================================================
// Problem:
//   Find all occurrences of pattern P in text T using a rolling hash
//   to achieve expected linear time.
//
// Approach:
//   1. Compute the hash of the pattern and the first window of text.
//   2. Slide the window one character at a time. Update the hash in O(1)
//      by removing the outgoing character and adding the incoming one.
//   3. On hash match, verify character by character to rule out
//      spurious hits (hash collisions).
//
// Hash function:
//   H(s) = (s[0]*d^(m-1) + s[1]*d^(m-2) + ... + s[m-1]) mod q
//   d = 256 (alphabet size), q = a large prime.
//
// Complexity:
//   Time  : O(n + m) expected, O(n*m) worst-case (many collisions)
//   Space : O(1) extra (besides the output vector)

/// Return a vector of starting indices where `pattern` occurs in `text`
/// using the Rabin-Karp rolling-hash algorithm.
///
/// Time : O(n + m) expected
/// Space: O(1) extra
fn rabin_karp_search(text: &str, pattern: &str) -> Vec<usize> {
    const BASE: u64 = 256;
    const PRIME: u64 = 1_000_000_007;

    let t = text.as_bytes();
    let p = pattern.as_bytes();
    let (n, m) = (t.len(), p.len());
    if m == 0 || m > n {
        return vec![];
    }

    let mut results = Vec::new();

    // h = BASE^(m-1) mod PRIME — used to remove the leading digit
    let mut h: u64 = 1;
    for _ in 0..m - 1 {
        h = (h * BASE) % PRIME;
    }

    // Compute initial hashes for pattern and first window of text
    let mut p_hash: u64 = 0;
    let mut t_hash: u64 = 0;
    for i in 0..m {
        p_hash = (BASE * p_hash + p[i] as u64) % PRIME;
        t_hash = (BASE * t_hash + t[i] as u64) % PRIME;
    }

    // Slide the window over the text
    for i in 0..=n - m {
        // If hashes match, verify character by character
        if p_hash == t_hash && &t[i..i + m] == p {
            results.push(i);
        }

        // Compute hash for the next window (if there is one)
        if i < n - m {
            // Add PRIME before subtraction to avoid underflow in unsigned arithmetic
            t_hash = (BASE * ((t_hash + PRIME) - (t[i] as u64 * h) % PRIME) + t[i + m] as u64)
                % PRIME;
        }
    }
    results
}

// ===========================================================================
// 3. Z-Algorithm for Pattern Matching
// ===========================================================================
// Problem:
//   Given a string S, compute the Z-array where Z[i] is the length of
//   the longest substring starting at index i that is also a prefix of S.
//   For pattern matching: build P + '$' + T and check where Z[i] == |P|.
//
// Approach:
//   Maintain a "Z-box" [l, r) — the interval of the rightmost substring
//   matching a prefix. For each new position i:
//     - If i < r, reuse previously computed info: Z[i] = min(r-i, Z[i-l]).
//     - Extend character by character.
//     - Update [l, r) if extended past r.
//
// Complexity:
//   Time  : O(n)  — each character compared at most twice
//   Space : O(n)  — for the Z-array

/// Compute the Z-array for byte slice `s`.
///
/// Z[0] is defined as 0.
/// Z[i] = length of the longest substring starting at s[i]
///        that matches a prefix of s.
///
/// Time : O(n)
/// Space: O(n)
fn z_function(s: &[u8]) -> Vec<usize> {
    let n = s.len();
    if n == 0 {
        return vec![];
    }

    let mut z = vec![0usize; n];
    let mut l = 0usize;
    let mut r = 0usize; // Z-box boundaries [l, r)

    for i in 1..n {
        if i < r {
            // Inside the current Z-box; reuse known info
            z[i] = std::cmp::min(r - i, z[i - l]);
        }

        // Try to extend the match
        while i + z[i] < n && s[z[i]] == s[i + z[i]] {
            z[i] += 1;
        }

        // Update the Z-box if we went past r
        if i + z[i] > r {
            l = i;
            r = i + z[i];
        }
    }
    z
}

/// Find all occurrences of `pattern` in `text` using the Z-algorithm.
///
/// Builds the concatenated string pattern + '$' + text and checks
/// positions where Z[i] == pattern.len().
///
/// Time : O(n + m)
/// Space: O(n + m)
fn z_search(text: &str, pattern: &str) -> Vec<usize> {
    if pattern.is_empty() {
        return vec![];
    }

    let concat = format!("{}${}", pattern, text);
    let z = z_function(concat.as_bytes());
    let m = pattern.len();

    let mut results = Vec::new();
    for i in (m + 1)..concat.len() {
        if z[i] == m {
            results.push(i - m - 1); // map back to text index
        }
    }
    results
}

// ===========================================================================
// Driver / demo
// ===========================================================================
fn main() {
    let text = "ABABDABACDABABCABAB";
    let pattern = "ABABCABAB";

    println!("============================================================");
    println!("Week 25 — String Algorithms  (Rust)");
    println!("============================================================");
    println!("\nText   : {}", text);
    println!("Pattern: {}\n", pattern);

    // KMP
    let kmp_res = kmp_search(text, pattern);
    println!("[KMP]        Matches at indices : {:?}", kmp_res);

    // Rabin-Karp
    let rk_res = rabin_karp_search(text, pattern);
    println!("[Rabin-Karp] Matches at indices : {:?}", rk_res);

    // Z-algorithm
    let z_res = z_search(text, pattern);
    println!("[Z-algo]     Matches at indices : {:?}", z_res);

    // Overlapping matches example
    println!("\n--- Overlapping-match example ---");
    let text2 = "AAAAAA";
    let pattern2 = "AAA";
    println!("Text   : {}", text2);
    println!("Pattern: {}", pattern2);
    println!(
        "[KMP]        Matches at indices : {:?}",
        kmp_search(text2, pattern2)
    );
    println!(
        "[Rabin-Karp] Matches at indices : {:?}",
        rabin_karp_search(text2, pattern2)
    );
    println!(
        "[Z-algo]     Matches at indices : {:?}",
        z_search(text2, pattern2)
    );

    // Z-array demo
    println!("\n--- Z-array demo ---");
    let demo = "aabxaab";
    let z_arr = z_function(demo.as_bytes());
    println!("String  : {}", demo);
    println!("Z-array : {:?}", z_arr);
}
