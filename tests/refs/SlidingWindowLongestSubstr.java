/*
 * Reference Java implementation for tests/cases/sliding_window_longest_substr.json.
 * Length of the longest substring without repeating characters (LC 3).
 */
import java.util.HashMap;
import java.util.Map;

public class SlidingWindowLongestSubstr {
    public static long longestUniqueSubstring(String s) {
        Map<Character, Integer> last = new HashMap<>();
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); ++right) {
            char c = s.charAt(right);
            Integer prev = last.get(c);
            if (prev != null && prev >= left) left = prev + 1;
            last.put(c, right);
            best = Math.max(best, right - left + 1);
        }
        return best;
    }
}
