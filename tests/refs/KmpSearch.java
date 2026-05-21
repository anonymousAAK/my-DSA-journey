/*
 * Reference Java implementation for tests/cases/kmp_search.json.
 * KMP all-occurrence search; returns sorted starting indices.
 */
import java.util.ArrayList;
import java.util.List;

public class KmpSearch {
    private static int[] buildLps(String pattern) {
        int m = pattern.length();
        int[] lps = new int[m];
        if (m == 0) return lps;
        int length = 0, i = 1;
        while (i < m) {
            if (pattern.charAt(i) == pattern.charAt(length)) {
                length++;
                lps[i++] = length;
            } else if (length != 0) {
                length = lps[length - 1];
            } else {
                lps[i++] = 0;
            }
        }
        return lps;
    }

    public static List<Long> kmpSearch(String text, String pattern) {
        List<Long> positions = new ArrayList<>();
        int n = text.length(), m = pattern.length();
        if (m == 0 || m > n) return positions;
        int[] lps = buildLps(pattern);
        int i = 0, j = 0;
        while (i < n) {
            if (text.charAt(i) == pattern.charAt(j)) { i++; j++; }
            if (j == m) {
                positions.add((long) (i - j));
                j = lps[j - 1];
            } else if (i < n && text.charAt(i) != pattern.charAt(j)) {
                if (j != 0) j = lps[j - 1];
                else i++;
            }
        }
        return positions;
    }
}
