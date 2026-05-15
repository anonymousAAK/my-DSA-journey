// WEEK 25 - RUST ADVANCED DSA
// Topic: Z-Algorithm for Pattern Matching
// File: 3.z_algorithm.rs
//
// CONCEPT:
//     For a string S the Z-array Z[i] = length of the longest prefix of S
//     that starts at S[i]. Computed in O(n) by reusing previously found
//     matches inside a moving "Z-box". Pattern matching becomes:
//         build C = P + '$' + T, compute Z(C), report Z[i] == |P|.
//
// KEY POINTS:
//     - The Z-box [l, r) is the right-most match of a prefix encountered.
//     - If i < r, Z[i] = min(r - i, Z[i - l]) BEFORE attempting to extend.
//     - Each character of S participates in at most two char-comparisons.
//
// ALGORITHM / APPROACH:
//     z[0] = 0; l = r = 0
//     for i in 1..n:
//         if i < r: z[i] = min(r-i, z[i-l])
//         while i+z[i] < n and s[z[i]] == s[i+z[i]]: z[i] += 1
//         if i+z[i] > r: l = i; r = i+z[i]
//
// RUST-SPECIFIC NOTES vs JAVA:
//     - Work on &[u8] byte slices.
//     - std::cmp::min for the borrow.
//     - format!() is the simplest way to build the concat string.
//
// DRY RUN:
//     S = "aabxaab" -> Z = [0,1,0,0,3,1,0].
//     C = "ABABCABAB$ABABDABACDABABCABAB"; Z[20] = 9 -> match at 10.
//
// COMPLEXITY:
//     Time  : O(n + m)
//     Space : O(n + m)

fn z_function(s: &[u8]) -> Vec<usize> {
    let n = s.len();
    if n == 0 {
        return vec![];
    }
    let mut z = vec![0usize; n];
    let mut l = 0usize;
    let mut r = 0usize;
    for i in 1..n {
        if i < r {
            z[i] = std::cmp::min(r - i, z[i - l]);
        }
        while i + z[i] < n && s[z[i]] == s[i + z[i]] {
            z[i] += 1;
        }
        if i + z[i] > r {
            l = i;
            r = i + z[i];
        }
    }
    z
}

fn search(text: &str, pattern: &str) -> Vec<usize> {
    if pattern.is_empty() {
        return vec![];
    }
    let concat = format!("{}${}", pattern, text);
    let z = z_function(concat.as_bytes());
    let m = pattern.len();
    let mut results = Vec::new();
    for i in (m + 1)..concat.len() {
        if z[i] == m {
            results.push(i - m - 1);
        }
    }
    results
}

fn main() {
    println!("=== Z-Algorithm (Rust) ===");
    let demo = "aabxaab";
    println!("String : {}", demo);
    println!("Z-array: {:?}", z_function(demo.as_bytes()));   // [0, 1, 0, 0, 3, 1, 0]

    let text = "ABABDABACDABABCABAB";
    let pattern = "ABABCABAB";
    println!("\nText   : {}", text);
    println!("Pattern: {}", pattern);
    println!("Matches: {:?}", search(text, pattern));         // [10]

    println!("\n--- Overlapping matches ---");
    let t2 = "AAAAAA";
    let p2 = "AAA";
    println!("Text   : {}", t2);
    println!("Pattern: {}", p2);
    println!("Matches: {:?}", search(t2, p2));                // [0, 1, 2, 3]
}

// NOTES (vs Java baseline):
//     - Pure translation; std::cmp::min vs Math.min, &[u8] vs char[].
//     - format!() builds the concat in one go, replacing Java's '+' operator.
