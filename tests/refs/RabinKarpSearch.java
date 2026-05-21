/*
 * Reference Java implementation for tests/cases/rabin_karp_search.json.
 *
 * Rabin-Karp rolling-hash all-occurrence search with verification on hash
 * collision. Returns sorted starting positions.
 */
import java.util.ArrayList;
import java.util.List;

public class RabinKarpSearch {
    private static final long BASE = 256;
    private static final long PRIME = 1_000_000_007L;

    public static List<Long> rabinKarpSearch(String text, String pattern) {
        List<Long> results = new ArrayList<>();
        int n = text.length(), m = pattern.length();
        if (m == 0 || m > n) return results;
        long h = 1;
        for (int i = 0; i < m - 1; ++i) h = (h * BASE) % PRIME;
        long pHash = 0, tHash = 0;
        for (int i = 0; i < m; ++i) {
            pHash = (BASE * pHash + pattern.charAt(i)) % PRIME;
            tHash = (BASE * tHash + text.charAt(i)) % PRIME;
        }
        for (int i = 0; i <= n - m; ++i) {
            if (pHash == tHash && text.regionMatches(i, pattern, 0, m)) {
                results.add((long) i);
            }
            if (i < n - m) {
                tHash = (BASE * (tHash - text.charAt(i) * h) + text.charAt(i + m)) % PRIME;
                if (tHash < 0) tHash += PRIME;
            }
        }
        return results;
    }
}
