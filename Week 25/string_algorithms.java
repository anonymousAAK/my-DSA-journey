/**
 * Week 25: String Algorithms
 * ===========================
 * This file covers fundamental string matching and pattern search algorithms.
 *
 * Topics covered:
 *     1. KMP (Knuth-Morris-Pratt) Pattern Matching
 *     2. Rabin-Karp String Matching (rolling hash)
 *     3. Z-Algorithm for Pattern Matching
 *
 * Each algorithm includes:
 *     - Problem statement
 *     - Step-by-step approach explanation
 *     - Time / space complexity analysis
 *     - Example usage via main driver
 */

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class string_algorithms {

    // -----------------------------------------------------------------------
    // 1. KMP (Knuth-Morris-Pratt) Pattern Matching
    // -----------------------------------------------------------------------
    // Problem:
    //   Given a text T of length n and a pattern P of length m, find all
    //   occurrences of P in T.
    //
    // Approach:
    //   1. Build the LPS (Longest Proper Prefix which is also a Suffix) array
    //      for the pattern.
    //      lps[i] = length of the longest proper prefix of P[0..i] that is
    //      also a suffix of P[0..i].
    //   2. Scan text with two pointers (i for text, j for pattern).
    //      On a mismatch after j matches, set j = lps[j-1] and continue,
    //      skipping characters we already know must match.
    //
    // Complexity:
    //   Time  : O(n + m)  — linear in the combined length
    //   Space : O(m)      — for the LPS array

    /**
     * Build the LPS (failure function) array for the given pattern.
     *
     * lps[i] = length of the longest proper prefix of pattern[0..i]
     * that is also a suffix of that substring.
     *
     * Time : O(m)
     * Space: O(m)
     */
    public static int[] kmpBuildLPS(String pattern) {
        int m = pattern.length();
        int[] lps = new int[m];
        int length = 0;  // length of previous longest prefix-suffix
        int i = 1;

        while (i < m) {
            if (pattern.charAt(i) == pattern.charAt(length)) {
                length++;
                lps[i] = length;
                i++;
            } else {
                if (length != 0) {
                    // Fall back — do NOT increment i
                    length = lps[length - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        return lps;
    }

    /**
     * Return a list of starting indices where pattern occurs in text
     * using the Knuth-Morris-Pratt algorithm.
     *
     * Time : O(n + m)
     * Space: O(m)
     */
    public static List<Integer> kmpSearch(String text, String pattern) {
        List<Integer> results = new ArrayList<>();
        int n = text.length(), m = pattern.length();
        if (m == 0) return results;

        int[] lps = kmpBuildLPS(pattern);
        int i = 0;  // index into text
        int j = 0;  // index into pattern

        while (i < n) {
            if (text.charAt(i) == pattern.charAt(j)) {
                i++;
                j++;
            }

            if (j == m) {
                // Full match found at index i - j
                results.add(i - j);
                j = lps[j - 1];  // look for next overlapping match
            } else if (i < n && text.charAt(i) != pattern.charAt(j)) {
                if (j != 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }
        return results;
    }

    // -----------------------------------------------------------------------
    // 2. Rabin-Karp String Matching
    // -----------------------------------------------------------------------
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
    //   Space : O(1) extra (besides the output list)

    /**
     * Return a list of starting indices where pattern occurs in text
     * using the Rabin-Karp rolling-hash algorithm.
     *
     * Time : O(n + m) expected
     * Space: O(1) extra
     */
    public static List<Integer> rabinKarpSearch(String text, String pattern) {
        final int BASE = 256;
        final long PRIME = 1_000_000_007L;

        List<Integer> results = new ArrayList<>();
        int n = text.length(), m = pattern.length();
        if (m == 0 || m > n) return results;

        // h = BASE^(m-1) mod PRIME — used to remove the leading digit
        long h = 1;
        for (int i = 0; i < m - 1; i++) {
            h = (h * BASE) % PRIME;
        }

        // Compute initial hashes for pattern and first window of text
        long pHash = 0, tHash = 0;
        for (int i = 0; i < m; i++) {
            pHash = (BASE * pHash + pattern.charAt(i)) % PRIME;
            tHash = (BASE * tHash + text.charAt(i)) % PRIME;
        }

        // Slide the window over the text
        for (int i = 0; i <= n - m; i++) {
            // If hashes match, verify character by character
            if (pHash == tHash) {
                boolean match = true;
                for (int j = 0; j < m; j++) {
                    if (text.charAt(i + j) != pattern.charAt(j)) {
                        match = false;
                        break;
                    }
                }
                if (match) {
                    results.add(i);
                }
            }

            // Compute hash for the next window (if there is one)
            if (i < n - m) {
                tHash = (BASE * (tHash - text.charAt(i) * h) + text.charAt(i + m)) % PRIME;
                if (tHash < 0) tHash += PRIME;
            }
        }
        return results;
    }

    // -----------------------------------------------------------------------
    // 3. Z-Algorithm for Pattern Matching
    // -----------------------------------------------------------------------
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

    /**
     * Compute the Z-array for string s.
     *
     * Z[0] is defined as 0.
     * Z[i] = length of the longest substring starting at s[i]
     *        that matches a prefix of s.
     *
     * Time : O(n)
     * Space: O(n)
     */
    public static int[] zFunction(String s) {
        int n = s.length();
        int[] z = new int[n];
        int l = 0, r = 0;  // Z-box boundaries [l, r)

        for (int i = 1; i < n; i++) {
            if (i < r) {
                // Inside the current Z-box; reuse known info
                z[i] = Math.min(r - i, z[i - l]);
            }

            // Try to extend the match
            while (i + z[i] < n && s.charAt(z[i]) == s.charAt(i + z[i])) {
                z[i]++;
            }

            // Update the Z-box if we went past r
            if (i + z[i] > r) {
                l = i;
                r = i + z[i];
            }
        }
        return z;
    }

    /**
     * Find all occurrences of pattern in text using the Z-algorithm.
     *
     * Builds the concatenated string pattern + '$' + text and checks
     * positions where Z[i] == pattern.length().
     *
     * Time : O(n + m)
     * Space: O(n + m)
     */
    public static List<Integer> zSearch(String text, String pattern) {
        List<Integer> results = new ArrayList<>();
        if (pattern.isEmpty()) return results;

        String concat = pattern + "$" + text;
        int[] z = zFunction(concat);
        int m = pattern.length();

        for (int i = m + 1; i < concat.length(); i++) {
            if (z[i] == m) {
                results.add(i - m - 1);  // map back to text index
            }
        }
        return results;
    }

    // -----------------------------------------------------------------------
    // Driver / demo
    // -----------------------------------------------------------------------
    public static void main(String[] args) {
        String text = "ABABDABACDABABCABAB";
        String pattern = "ABABCABAB";

        System.out.println("============================================================");
        System.out.println("Week 25 — String Algorithms  (Java)");
        System.out.println("============================================================");
        System.out.println("\nText   : " + text);
        System.out.println("Pattern: " + pattern + "\n");

        // KMP
        List<Integer> kmpResult = kmpSearch(text, pattern);
        System.out.println("[KMP]        Matches at indices : " + kmpResult);

        // Rabin-Karp
        List<Integer> rkResult = rabinKarpSearch(text, pattern);
        System.out.println("[Rabin-Karp] Matches at indices : " + rkResult);

        // Z-algorithm
        List<Integer> zResult = zSearch(text, pattern);
        System.out.println("[Z-algo]     Matches at indices : " + zResult);

        // Overlapping matches example
        System.out.println("\n--- Overlapping-match example ---");
        String text2 = "AAAAAA";
        String pattern2 = "AAA";
        System.out.println("Text   : " + text2);
        System.out.println("Pattern: " + pattern2);
        System.out.println("[KMP]        Matches at indices : " + kmpSearch(text2, pattern2));
        System.out.println("[Rabin-Karp] Matches at indices : " + rabinKarpSearch(text2, pattern2));
        System.out.println("[Z-algo]     Matches at indices : " + zSearch(text2, pattern2));

        // Z-array demo
        System.out.println("\n--- Z-array demo ---");
        String demo = "aabxaab";
        int[] zArr = zFunction(demo);
        System.out.println("String  : " + demo);
        System.out.println("Z-array : " + Arrays.toString(zArr));
    }
}
