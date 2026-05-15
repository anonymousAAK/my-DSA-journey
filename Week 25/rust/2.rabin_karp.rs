// WEEK 25 - RUST ADVANCED DSA
// Topic: Rabin-Karp String Matching (rolling hash)
// File: 2.rabin_karp.rs
//
// CONCEPT:
//     Slide a fixed-size window of T and compare its rolling-hash fingerprint
//     to the hash of P. On a hash collision verify literally. Expected
//     runtime is O(n + m).
//
// KEY POINTS:
//     - Polynomial rolling hash mod a 1e9+7 prime; BASE = 256.
//     - h = BASE^(m-1) mod PRIME used to subtract the outgoing character.
//     - Use u64 so the multiplication BASE * hash never overflows.
//     - Because u64 underflows wrap around, add PRIME explicitly before any
//       subtraction in the update step.
//
// ALGORITHM / APPROACH:
//     h = BASE^(m-1) mod PRIME
//     compute p_hash and the first t_hash
//     for i in 0..=n-m:
//         if p_hash == t_hash and T[i..i+m] == P: report i
//         t_hash = (BASE * ((t_hash + PRIME) - (T[i]*h) % PRIME) + T[i+m]) mod PRIME
//
// RUST-SPECIFIC NOTES vs JAVA:
//     - No signed `long`; unsigned arithmetic requires explicit underflow
//       protection by adding PRIME before subtraction.
//     - Operate on &[u8] for clean indexing.
//     - vec![] returned when m == 0 || m > n.
//
// DRY RUN:
//     P = "AAA", T = "AAAAAA". Each window shares the same fingerprint, so
//     all four positions [0,1,2,3] are reported after a literal check.
//
// COMPLEXITY:
//     Time  : O(n + m) expected, O(n*m) worst.
//     Space : O(1) extra.

fn search(text: &str, pattern: &str) -> Vec<usize> {
    const BASE: u64 = 256;
    const PRIME: u64 = 1_000_000_007;

    let t = text.as_bytes();
    let p = pattern.as_bytes();
    let (n, m) = (t.len(), p.len());
    if m == 0 || m > n {
        return vec![];
    }

    let mut h: u64 = 1;
    for _ in 0..m - 1 {
        h = (h * BASE) % PRIME;
    }

    let mut p_hash: u64 = 0;
    let mut t_hash: u64 = 0;
    for i in 0..m {
        p_hash = (BASE * p_hash + p[i] as u64) % PRIME;
        t_hash = (BASE * t_hash + t[i] as u64) % PRIME;
    }

    let mut results = Vec::new();
    for i in 0..=n - m {
        if p_hash == t_hash && &t[i..i + m] == p {
            results.push(i);
        }
        if i < n - m {
            // Add PRIME before subtraction to avoid unsigned underflow.
            t_hash = (BASE * ((t_hash + PRIME) - (t[i] as u64 * h) % PRIME)
                      + t[i + m] as u64) % PRIME;
        }
    }
    results
}

fn main() {
    println!("=== Rabin-Karp Pattern Matching (Rust) ===");
    let text = "ABABDABACDABABCABAB";
    let pattern = "ABABCABAB";
    println!("Text   : {}", text);
    println!("Pattern: {}", pattern);
    println!("Matches: {:?}", search(text, pattern));    // [10]

    println!("\n--- Overlapping matches ---");
    let t2 = "AAAAAA";
    let p2 = "AAA";
    println!("Text   : {}", t2);
    println!("Pattern: {}", p2);
    println!("Matches: {:?}", search(t2, p2));           // [0, 1, 2, 3]
}

// NOTES (vs Java baseline):
//     - Java's signed `long` allows negative intermediate values that we
//       correct by adding PRIME. Rust's u64 wraps on underflow, so we add
//       PRIME *before* subtracting.
//     - For mission-critical use add a second (BASE, PRIME) pair (double
//       hashing) to drive collision probability to ~1/PRIME^2.
