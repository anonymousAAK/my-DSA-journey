// WEEK 25 - RUST ADVANCED DSA
// Topic: KMP (Knuth-Morris-Pratt) Pattern Matching
// File: 1.kmp.rs
//
// CONCEPT:
//     Find all occurrences of pattern P (length m) in text T (length n) in
//     O(n + m) time by precomputing an LPS / failure-function array so the
//     text pointer never moves backwards.
//
// KEY POINTS:
//     - lps[i] = length of the longest PROPER prefix of P[0..=i] that is
//       also a suffix of P[0..=i].
//     - On full match, j = lps[j-1] keeps overlapping matches alive.
//     - Operate on &[u8] byte slices so we don't have to deal with UTF-8
//       grapheme boundaries inside the inner loop.
//
// ALGORITHM / APPROACH:
//     build_lps:
//         length = 0; i = 1
//         while i < m:
//             if P[i] == P[length]: length++; lps[i] = length; i++
//             else if length != 0:  length = lps[length - 1]
//             else:                 lps[i] = 0; i++
//
//     search:
//         i = j = 0
//         while i < n:
//             if T[i] == P[j]: i++; j++
//             if j == m: result.push(i - j); j = lps[j-1]
//             else if i < n and T[i] != P[j]: j = if j != 0 { lps[j-1] } else { i++; 0 }
//
// RUST-SPECIFIC NOTES vs JAVA:
//     - usize is unsigned -> guard subtractions like `length - 1` with checks.
//     - We index byte slices (u8). For Unicode you'd switch to char vectors.
//     - Vec<usize> serves as both lps and the result list.
//
// DRY RUN:
//     P = "ABABCABAB" -> lps = [0,0,1,2,0,1,2,3,4]
//     T = "ABABDABACDABABCABAB" -> single match at index 10.
//     P = "AAA", T = "AAAAAA" -> matches [0,1,2,3].
//
// COMPLEXITY:
//     Time  : O(n + m)
//     Space : O(m)

fn build_lps(pattern: &[u8]) -> Vec<usize> {
    let m = pattern.len();
    let mut lps = vec![0usize; m];
    let mut length = 0usize;
    let mut i = 1usize;
    while i < m {
        if pattern[i] == pattern[length] {
            length += 1;
            lps[i] = length;
            i += 1;
        } else if length != 0 {
            length = lps[length - 1];
        } else {
            lps[i] = 0;
            i += 1;
        }
    }
    lps
}

fn search(text: &str, pattern: &str) -> Vec<usize> {
    let t = text.as_bytes();
    let p = pattern.as_bytes();
    let (n, m) = (t.len(), p.len());
    if m == 0 {
        return vec![];
    }
    let lps = build_lps(p);
    let mut results = Vec::new();
    let mut i = 0usize;
    let mut j = 0usize;
    while i < n {
        if t[i] == p[j] {
            i += 1;
            j += 1;
        }
        if j == m {
            results.push(i - j);
            j = lps[j - 1];
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

fn main() {
    println!("=== KMP Pattern Matching (Rust) ===");
    let text = "ABABDABACDABABCABAB";
    let pattern = "ABABCABAB";
    println!("Text   : {}", text);
    println!("Pattern: {}", pattern);
    println!("LPS    : {:?}", build_lps(pattern.as_bytes()));
    println!("Matches: {:?}", search(text, pattern));         // [10]

    println!("\n--- Overlapping matches ---");
    let t2 = "AAAAAA";
    let p2 = "AAA";
    println!("Text   : {}", t2);
    println!("Pattern: {}", p2);
    println!("Matches: {:?}", search(t2, p2));                // [0, 1, 2, 3]
}

// NOTES (vs Java baseline):
//     - Same control flow as the Java version. usize forces us to be careful
//       around `length - 1` (only taken when `length != 0`, so it's safe).
//     - Byte-slice indexing avoids the UTF-8 cost of string slicing in Rust.
//     - For Unicode text, collect into Vec<char> first and index that.
