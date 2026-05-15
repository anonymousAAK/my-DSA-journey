/*
 * WEEK 25 - JAVA ADVANCED DSA
 * Topic: KMP (Knuth-Morris-Pratt) Pattern Matching
 * File: 1.KMP.java
 *
 * CONCEPT:
 *     Given a text T of length n and a pattern P of length m, find every
 *     index i in T where P occurs. Naive scanning costs O(n*m). KMP achieves
 *     O(n + m) by precomputing a "failure function" / LPS array on P so that
 *     after a partial match of length j fails, we can resume matching at
 *     P[lps[j-1]] instead of restarting from P[0].
 *
 * KEY POINTS:
 *     - lps[i] = length of the longest PROPER prefix of P[0..i] that is also
 *       a suffix of P[0..i].
 *     - The text pointer i never moves backwards; that is the secret behind
 *       the linear-time guarantee.
 *     - To collect OVERLAPPING matches, on a full match set j = lps[j-1] and
 *       continue scanning instead of resetting j to 0.
 *     - Building lps is essentially KMP applied to the pattern against itself.
 *
 * ALGORITHM / APPROACH:
 *     buildLPS(P):
 *         length = 0; i = 1
 *         while i < m:
 *             if P[i] == P[length]: length++; lps[i] = length; i++
 *             else if length != 0:  length = lps[length - 1]      // fall back
 *             else:                 lps[i] = 0; i++
 *
 *     search(T, P):
 *         lps = buildLPS(P); i = j = 0
 *         while i < n:
 *             if T[i] == P[j]: i++; j++
 *             if j == m: report match at i-j; j = lps[j-1]
 *             else if i < n && T[i] != P[j]: j = (j!=0 ? lps[j-1] : 0); if j==0: i++
 *
 * JAVA-SPECIFIC NOTES:
 *     - String.charAt(i) for character access; int[] for the lps array.
 *     - ArrayList<Integer> collects the result indices.
 *
 * DRY RUN:
 *     P = "ABABCABAB", lps = [0,0,1,2,0,1,2,3,4]
 *     T = "ABABDABACDABABCABAB"
 *         Match starts to slide; mismatch at T[4]='D' vs P[4]='C' falls back
 *         using lps[3]=2, then again to lps[1]=0. Eventually full match found
 *         beginning at index 10. Final result: [10].
 *
 *     P = "AAA", T = "AAAAAA"
 *         lps = [0,1,2]; overlapping matches at [0,1,2,3].
 *
 * COMPLEXITY:
 *     Time  : O(n + m) — each text index advances or j strictly decreases.
 *     Space : O(m)     — lps array.
 */

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class KMP {

    /** Build the LPS (failure) array for the given pattern.  O(m). */
    public static int[] buildLPS(String pattern) {
        int m = pattern.length();
        int[] lps = new int[m];
        int length = 0;
        int i = 1;
        while (i < m) {
            if (pattern.charAt(i) == pattern.charAt(length)) {
                length++;
                lps[i] = length;
                i++;
            } else if (length != 0) {
                length = lps[length - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
        return lps;
    }

    /** Return starting indices of every (possibly overlapping) match of pattern in text. */
    public static List<Integer> search(String text, String pattern) {
        List<Integer> results = new ArrayList<>();
        int n = text.length(), m = pattern.length();
        if (m == 0) return results;

        int[] lps = buildLPS(pattern);
        int i = 0, j = 0;

        while (i < n) {
            if (text.charAt(i) == pattern.charAt(j)) {
                i++;
                j++;
            }
            if (j == m) {
                results.add(i - j);
                j = lps[j - 1];
            } else if (i < n && text.charAt(i) != pattern.charAt(j)) {
                if (j != 0) j = lps[j - 1];
                else i++;
            }
        }
        return results;
    }

    public static void main(String[] args) {
        System.out.println("=== KMP Pattern Matching (Java) ===");
        String text = "ABABDABACDABABCABAB";
        String pattern = "ABABCABAB";
        System.out.println("Text   : " + text);
        System.out.println("Pattern: " + pattern);
        System.out.println("LPS    : " + Arrays.toString(buildLPS(pattern)));
        System.out.println("Matches: " + search(text, pattern));   // [10]

        System.out.println("\n--- Overlapping matches ---");
        String t2 = "AAAAAA", p2 = "AAA";
        System.out.println("Text   : " + t2);
        System.out.println("Pattern: " + p2);
        System.out.println("Matches: " + search(t2, p2));          // [0,1,2,3]
    }
}

/*
 * NOTES (vs Java baseline):
 *     - Pure self-comparison — this IS the Java baseline.
 *     - Python uses identical logic with list/str primitives.
 *     - C++ swaps String/charAt for std::string indexing; vector<int> for lps.
 *     - Rust prefers &[u8] byte slices to avoid char-boundary headaches.
 *     - Web/JS uses === character comparison on string indices.
 */
