/*
 * WEEK 25 - JAVA ADVANCED DSA
 * Topic: Rabin-Karp String Matching (rolling hash)
 * File: 2.RabinKarp.java
 *
 * CONCEPT:
 *     Compare every length-m window of T to P via a numeric fingerprint
 *     instead of a character-by-character comparison. By choosing a hash that
 *     can be updated incrementally in O(1) as the window slides, the
 *     expected runtime is O(n + m). On hash hits we verify literally to
 *     guard against collisions.
 *
 * KEY POINTS:
 *     - Polynomial rolling hash modulo a large prime:
 *         H(s) = (s[0]*B^(m-1) + s[1]*B^(m-2) + ... + s[m-1]) mod Q
 *       with B = 256 (extended ASCII) and Q a 32-bit-safe prime.
 *     - Update: t_hash = (B * (t_hash - T[i]*h) + T[i+m]) mod Q,
 *       where h = B^(m-1) mod Q (precomputed once).
 *     - Always verify the candidate window on hash match — collisions exist.
 *     - Worst case is O(n*m) (pathological hash inputs); expected O(n+m).
 *
 * ALGORITHM / APPROACH:
 *     1. Compute h = B^(m-1) mod Q
 *     2. Compute pHash for P and tHash for T[0..m-1]
 *     3. For i in 0..n-m:
 *            if pHash == tHash and T[i..i+m] == P: report i
 *            slide: tHash = (B * (tHash - T[i]*h) + T[i+m]) mod Q
 *
 * JAVA-SPECIFIC NOTES:
 *     - Use `long` for the hash to avoid signed-int overflow before mod.
 *     - text.charAt(i) returns char promoted to int as needed.
 *     - Add PRIME after subtraction so the result is non-negative.
 *
 * DRY RUN:
 *     P = "AAA", T = "AAAAAA", B = 256, Q = 1_000_000_007.
 *     h = 256^2 = 65_536
 *     pHash = ((65*256 + 65)*256 + 65) = 4_276_545
 *     First window T[0..2] = "AAA" -> tHash matches; record 0.
 *     Slide once: tHash = (256*(tHash - 65*h) + 65) mod Q. Unchanged numerically (same chars).
 *     Records [0,1,2,3].
 *
 * COMPLEXITY:
 *     Time  : O(n + m) expected, O(n*m) worst-case.
 *     Space : O(1) extra besides the output list.
 */

import java.util.ArrayList;
import java.util.List;

class RabinKarp {

    private static final int BASE  = 256;
    private static final long PRIME = 1_000_000_007L;

    public static List<Integer> search(String text, String pattern) {
        List<Integer> results = new ArrayList<>();
        int n = text.length(), m = pattern.length();
        if (m == 0 || m > n) return results;

        // h = BASE^(m-1) mod PRIME
        long h = 1;
        for (int i = 0; i < m - 1; i++) h = (h * BASE) % PRIME;

        long pHash = 0, tHash = 0;
        for (int i = 0; i < m; i++) {
            pHash = (BASE * pHash + pattern.charAt(i)) % PRIME;
            tHash = (BASE * tHash + text.charAt(i)) % PRIME;
        }

        for (int i = 0; i <= n - m; i++) {
            if (pHash == tHash) {
                boolean ok = true;
                for (int j = 0; j < m; j++) {
                    if (text.charAt(i + j) != pattern.charAt(j)) { ok = false; break; }
                }
                if (ok) results.add(i);
            }
            if (i < n - m) {
                tHash = (BASE * (tHash - text.charAt(i) * h) + text.charAt(i + m)) % PRIME;
                if (tHash < 0) tHash += PRIME;
            }
        }
        return results;
    }

    public static void main(String[] args) {
        System.out.println("=== Rabin-Karp Pattern Matching (Java) ===");
        String text = "ABABDABACDABABCABAB";
        String pattern = "ABABCABAB";
        System.out.println("Text   : " + text);
        System.out.println("Pattern: " + pattern);
        System.out.println("Matches: " + search(text, pattern));    // [10]

        System.out.println("\n--- Overlapping matches ---");
        String t2 = "AAAAAA", p2 = "AAA";
        System.out.println("Text   : " + t2);
        System.out.println("Pattern: " + p2);
        System.out.println("Matches: " + search(t2, p2));           // [0,1,2,3]
    }
}

/*
 * NOTES (vs Java baseline):
 *     - Python uses ord() to get char codes and `pow(b,e,m)` for h.
 *     - C++ stores hashes in long long; uses text.substr for verification.
 *     - Rust uses u64 hashes and explicitly adds PRIME before subtraction
 *       to avoid unsigned underflow.
 *     - Web/JS keeps everything in Number — safe while m*BASE*PRIME stays
 *       within 2^53.
 */
