/*
 * WEEK 25 - JAVA ADVANCED DSA
 * Topic: Z-Algorithm for Pattern Matching
 * File: 3.ZAlgorithm.java
 *
 * CONCEPT:
 *     For a string S of length n, the Z-array satisfies:
 *         Z[0] = 0  (by convention)
 *         Z[i] = length of the longest substring starting at S[i] that is
 *                also a prefix of S.
 *     With Z computed in linear time, pattern matching reduces to building
 *     C = P + '$' + T (where '$' is a sentinel not in the alphabet) and
 *     reporting positions where Z[i] == |P|.
 *
 * KEY POINTS:
 *     - Maintain the "Z-box" [l, r) = the right-most prefix match seen so far.
 *     - If i < r, we can BORROW: Z[i] = min(r - i, Z[i - l]) before extending.
 *     - Each character of S is involved in at most two comparisons -> O(n).
 *     - The sentinel '$' guarantees Z[i] never exceeds |P| in the matching
 *       region, so we don't have to cap manually.
 *
 * ALGORITHM / APPROACH:
 *     z[0] = 0; l = r = 0
 *     for i in 1..n:
 *         if i < r: z[i] = min(r-i, z[i-l])
 *         while i+z[i] < n && s[z[i]] == s[i+z[i]]: z[i]++
 *         if i+z[i] > r: l = i; r = i+z[i]
 *
 *     search(T, P): build C = P + '$' + T; compute Z on C;
 *                   return [i - |P| - 1 for i where Z[i] == |P|].
 *
 * JAVA-SPECIFIC NOTES:
 *     - Math.min for the borrow step.
 *     - String concatenation via '+' is fine for small inputs; for huge
 *       inputs prefer StringBuilder.
 *
 * DRY RUN:
 *     S = "aabxaab"
 *         i=1: s[1]='a'==s[0]='a' -> extend to length 1; s[1+1]='b' != s[1]='a'.
 *              Z[1]=1; (l,r)=(1,2).
 *         i=2: s[2]='b' != s[0]='a'. Z[2]=0.
 *         i=3: s[3]='x' != s[0]='a'. Z[3]=0.
 *         i=4: extend "aab" matches prefix "aab" -> Z[4]=3; (l,r)=(4,7).
 *         i=5: i<r, Z[i-l]=Z[1]=1, Z[5]=min(2,1)=1; cannot extend.
 *         i=6: i<r, Z[i-l]=Z[2]=0, Z[6]=0.
 *     Z = [0,1,0,0,3,1,0].
 *
 *     Pattern search "ABABCABAB" in "ABABDABACDABABCABAB":
 *         C = "ABABCABAB$ABABDABACDABABCABAB"; Z[20] = 9 -> match at i = 20-9-1 = 10.
 *
 * COMPLEXITY:
 *     Time  : O(n + m).
 *     Space : O(n + m) for the concatenation and the Z-array.
 */

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ZAlgorithm {

    /** Compute the Z-array for s. */
    public static int[] zFunction(String s) {
        int n = s.length();
        int[] z = new int[n];
        int l = 0, r = 0;
        for (int i = 1; i < n; i++) {
            if (i < r) z[i] = Math.min(r - i, z[i - l]);
            while (i + z[i] < n && s.charAt(z[i]) == s.charAt(i + z[i])) z[i]++;
            if (i + z[i] > r) { l = i; r = i + z[i]; }
        }
        return z;
    }

    /** Pattern search via Z-array: returns starting indices in text. */
    public static List<Integer> search(String text, String pattern) {
        List<Integer> results = new ArrayList<>();
        if (pattern.isEmpty()) return results;
        String concat = pattern + "$" + text;
        int[] z = zFunction(concat);
        int m = pattern.length();
        for (int i = m + 1; i < concat.length(); i++) {
            if (z[i] == m) results.add(i - m - 1);
        }
        return results;
    }

    public static void main(String[] args) {
        System.out.println("=== Z-Algorithm (Java) ===");
        String demo = "aabxaab";
        System.out.println("String : " + demo);
        System.out.println("Z-array: " + Arrays.toString(zFunction(demo)));  // [0,1,0,0,3,1,0]

        String text = "ABABDABACDABABCABAB";
        String pattern = "ABABCABAB";
        System.out.println("\nText   : " + text);
        System.out.println("Pattern: " + pattern);
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
 *     - Python: identical logic; uses list and slicing.
 *     - C++: vector<int> z; uses std::min from <algorithm>.
 *     - Rust: operates on byte slices; std::cmp::min for the borrow.
 *     - Web/JS: Math.min and string indexing — straightforward translation.
 */
