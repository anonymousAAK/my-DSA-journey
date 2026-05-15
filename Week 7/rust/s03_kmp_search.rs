/*
 * WEEK 7 - RUST DSA
 * Topic: KMP String Search
 * File: 3.kmp_search.rs
 *
 * CONCEPT:
 *     Find all occurrences of pattern in text in O(n + m) using KMP and
 *     its longest-proper-prefix-suffix (LPS) array.
 *
 * KEY POINTS:
 *     - lps[i] = length of the longest proper prefix of pat[0..=i] that
 *       is also a suffix.
 *     - On mismatch: jump j = lps[j-1] instead of restarting.
 *     - We use byte slices (.as_bytes()) for O(1) indexing — KMP is
 *       byte-level on ASCII; use Vec<char> for general Unicode.
 *
 * ALGORITHM / APPROACH:
 *     See build_lps and kmp_search; identical logic to Java/C++ versions.
 *
 * RUST-SPECIFIC NOTES:
 *     - Vec<usize> for positions; Vec<usize> for lps.
 *     - Pattern access via &[u8] (bytes), so works for ASCII inputs.
 *
 * DRY RUN:
 *     pat = "AABA"  -> lps = [0,1,0,1]
 *     text "AABAACAADAABAABA" -> matches at [0, 9, 12]
 *
 * COMPLEXITY:
 *     build_lps : O(m) time, O(m) space
 *     kmp_search: O(n + m) time
 */

fn build_lps(pattern: &[u8]) -> Vec<usize> {
    let m = pattern.len();
    let mut lps = vec![0usize; m];
    if m == 0 {
        return lps;
    }
    let mut len: usize = 0;
    let mut i: usize = 1;
    while i < m {
        if pattern[i] == pattern[len] {
            len += 1;
            lps[i] = len;
            i += 1;
        } else if len != 0 {
            len = lps[len - 1];
        } else {
            lps[i] = 0;
            i += 1;
        }
    }
    lps
}

fn kmp_search(text: &str, pattern: &str) -> Vec<usize> {
    let mut positions: Vec<usize> = Vec::new();
    let t = text.as_bytes();
    let p = pattern.as_bytes();
    let n = t.len();
    let m = p.len();
    if m == 0 || m > n {
        return positions;
    }
    let lps = build_lps(p);
    let mut i: usize = 0;
    let mut j: usize = 0;
    while i < n {
        if t[i] == p[j] {
            i += 1;
            j += 1;
        }
        if j == m {
            positions.push(i - j);
            j = lps[j - 1];
        } else if i < n && t[i] != p[j] {
            if j != 0 {
                j = lps[j - 1];
            } else {
                i += 1;
            }
        }
    }
    positions
}

fn naive_search(text: &str, pattern: &str) -> Vec<usize> {
    let mut positions: Vec<usize> = Vec::new();
    let t = text.as_bytes();
    let p = pattern.as_bytes();
    let n = t.len();
    let m = p.len();
    if m == 0 || m > n {
        return positions;
    }
    for i in 0..=n - m {
        let mut ok = true;
        for j in 0..m {
            if t[i + j] != p[j] {
                ok = false;
                break;
            }
        }
        if ok {
            positions.push(i);
        }
    }
    positions
}

fn main() {
    let text1 = "AABAACAADAABAABA";
    let pat1 = "AABA";
    println!("Text:    {}", text1);
    println!("Pattern: {}", pat1);
    println!("KMP found at:   {:?}", kmp_search(text1, pat1));
    println!("Naive found at: {:?}", naive_search(text1, pat1));

    let text2 = "AAAAABAAABA";
    let pat2 = "AAAA";
    println!("\nText:    {}", text2);
    println!("Pattern: {}", pat2);
    println!("LPS: {:?}", build_lps(pat2.as_bytes()));
    println!("KMP found at: {:?}", kmp_search(text2, pat2));

    println!("\nKMP(\"hello\",\"xyz\") = {:?}", kmp_search("hello", "xyz"));
    println!("KMP(\"hi\",\"hello\") = {:?}", kmp_search("hi", "hello"));
}

/*
 * NOTES — Rust vs Java:
 *     - .as_bytes() returns an &[u8] giving O(1) indexing on ASCII.
 *     - For full Unicode KMP, collect chars: text.chars().collect::<Vec<_>>().
 *     - Vec<usize> is the natural type for indices.
 *     - The std lib's text.match_indices(pattern) gives a higher-level API.
 */
