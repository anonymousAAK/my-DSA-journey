/*
 * Reference Java implementation for tests/cases/valid_anagram.json.
 * Character-frequency anagram check.
 */
import java.util.HashMap;
import java.util.Map;

public class ValidAnagram {
    public static boolean isAnagram(String a, String b) {
        if (a.length() != b.length()) return false;
        Map<Character, Integer> count = new HashMap<>();
        for (int i = 0; i < a.length(); ++i) {
            count.merge(a.charAt(i), 1, Integer::sum);
        }
        for (int i = 0; i < b.length(); ++i) {
            char c = b.charAt(i);
            Integer v = count.get(c);
            if (v == null) return false;
            if (v == 1) count.remove(c);
            else count.put(c, v - 1);
        }
        return count.isEmpty();
    }
}
