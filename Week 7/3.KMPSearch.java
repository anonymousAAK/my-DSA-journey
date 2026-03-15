/*
 * WEEK 7 - STRINGS
 * Topic: KMP String Search Algorithm
 *
 * PROBLEM: Find all occurrences of a pattern P in text T.
 * Naive approach: O(n * m) — for each position, try matching all of P.
 *
 * KMP (Knuth-Morris-Pratt) ALGORITHM: O(n + m)
 * Key insight: When a mismatch occurs, we already know some characters
 * of the text that we've matched. We can skip re-examining those.
 *
 * LPS ARRAY (Longest Proper Prefix which is also Suffix):
 * For pattern "AAACAAAA":
 * i=0: A       → lps[0] = 0 (no proper prefix)
 * i=1: AA      → lps[1] = 1 (prefix "A" = suffix "A")
 * i=2: AAA     → lps[2] = 2
 * i=3: AAAC    → lps[3] = 0 (no match)
 * i=4: AAACA   → lps[4] = 1
 * ...
 *
 * SEARCH ALGORITHM:
 * - Compare text[i] with pattern[j]
 * - Match: advance both i and j
 * - Full match (j == m): record position, jump j = lps[j-1]
 * - Mismatch: if j > 0, jump j = lps[j-1] (don't advance i)
 *             else advance i
 *
 * Time: O(n + m)  where n = |text|, m = |pattern|
 * Space: O(m) for lps array
 */

import java.util.ArrayList;
import java.util.List;

public class KMPSearch {

    // Build LPS (failure function) array for pattern
    static int[] buildLPS(String pattern) {
        int m = pattern.length();
        int[] lps = new int[m];
        lps[0] = 0; // by definition

        int len = 0; // length of previous longest prefix-suffix
        int i = 1;
        while (i < m) {
            if (pattern.charAt(i) == pattern.charAt(len)) {
                len++;
                lps[i] = len;
                i++;
            } else {
                if (len != 0) {
                    len = lps[len - 1]; // try shorter prefix-suffix
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        return lps;
    }

    // KMP search: returns list of 0-indexed start positions of pattern in text
    static List<Integer> kmpSearch(String text, String pattern) {
        List<Integer> positions = new ArrayList<>();
        int n = text.length(), m = pattern.length();
        if (m == 0 || m > n) return positions;

        int[] lps = buildLPS(pattern);

        int i = 0; // index into text
        int j = 0; // index into pattern
        while (i < n) {
            if (text.charAt(i) == pattern.charAt(j)) {
                i++;
                j++;
            }
            if (j == m) {
                positions.add(i - j); // found at index (i - j)
                j = lps[j - 1];       // look for next occurrence
            } else if (i < n && text.charAt(i) != pattern.charAt(j)) {
                if (j != 0) {
                    j = lps[j - 1]; // skip to known good position
                } else {
                    i++;
                }
            }
        }
        return positions;
    }

    // Naive search for comparison
    static List<Integer> naiveSearch(String text, String pattern) {
        List<Integer> positions = new ArrayList<>();
        int n = text.length(), m = pattern.length();
        for (int i = 0; i <= n - m; i++) {
            boolean match = true;
            for (int j = 0; j < m; j++) {
                if (text.charAt(i + j) != pattern.charAt(j)) { match = false; break; }
            }
            if (match) positions.add(i);
        }
        return positions;
    }

    public static void main(String[] args) {
        // Test 1
        String text1 = "AABAACAADAABAABA";
        String pat1 = "AABA";
        System.out.println("Text:    " + text1);
        System.out.println("Pattern: " + pat1);
        System.out.println("KMP found at: " + kmpSearch(text1, pat1));
        System.out.println("Naive found at: " + naiveSearch(text1, pat1));

        // Test 2
        String text2 = "AAAAABAAABA";
        String pat2 = "AAAA";
        System.out.println("\nText:    " + text2);
        System.out.println("Pattern: " + pat2);
        int[] lps = buildLPS(pat2);
        System.out.print("LPS: ");
        for (int x : lps) System.out.print(x + " ");
        System.out.println();
        System.out.println("KMP found at: " + kmpSearch(text2, pat2));

        // Test 3: no match
        System.out.println("\nKMP(\"hello\", \"xyz\") = " + kmpSearch("hello", "xyz"));

        // Test 4: pattern longer than text
        System.out.println("KMP(\"hi\", \"hello\") = " + kmpSearch("hi", "hello"));
    }
}
