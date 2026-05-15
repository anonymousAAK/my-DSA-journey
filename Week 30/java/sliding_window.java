/*
 * WEEK 30 - JAVA ADVANCED TOPICS
 * Topic: Sliding Window Pattern
 * File: sliding_window.java
 *
 * CONCEPT:
 *     The sliding-window pattern processes contiguous subarrays / substrings
 *     by maintaining a window [left, right] that grows on the right and
 *     shrinks on the left as needed. Each element enters / leaves the
 *     window at most once, yielding O(n) algorithms for problems that are
 *     otherwise O(n^2) or worse.
 *
 * KEY POINTS:
 *     - Fixed-size window: slide by one each step, drop the outgoing left.
 *     - Variable-size window: grow right; shrink left while invariant
 *       violated.
 *     - Common state: counter / hash map / sum / monotonic deque.
 *     - Canonical problems: longest substring without repeats (LC 3),
 *       minimum window substring (LC 76), longest substring with at most
 *       k distinct characters (LC 340), maximum sliding window (LC 239).
 *
 * ALGORITHM / APPROACH (variable size):
 *     left = 0
 *     for right in 0..n:
 *         update window state with arr[right]
 *         while window invariant violated:
 *             remove arr[left] from state
 *             left++
 *         record best so far
 *
 * DRY RUN / EXAMPLE:
 *     s = "abcabcbb" (LC 3): walk right; on first repeat reset left = idx+1;
 *     best length = 3 ("abc").
 *     Min window "ADOBECODEBANC" for "ABC" -> "BANC".
 *
 * COMPLEXITY:
 *     Time:  O(n) for most variants.
 *     Space: O(charset) or O(window size).
 */

// snake_case filename is fine; class SlidingWindow is package-private.

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class SlidingWindow {

    /** LC 3 - Longest Substring Without Repeating Characters. */
    static int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> last = new HashMap<>();
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            if (last.containsKey(c) && last.get(c) >= left) left = last.get(c) + 1;
            last.put(c, right);
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    /** LC 76 - Minimum Window Substring. */
    static String minWindow(String s, String t) {
        if (t == null || t.isEmpty() || s.length() < t.length()) return "";
        Map<Character, Integer> need = new HashMap<>();
        for (char c : t.toCharArray()) need.merge(c, 1, Integer::sum);
        int required = need.size(), formed = 0;
        Map<Character, Integer> window = new HashMap<>();
        int left = 0, bestLen = Integer.MAX_VALUE, bestLeft = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            window.merge(c, 1, Integer::sum);
            if (need.containsKey(c) && window.get(c).intValue() == need.get(c).intValue())
                formed++;
            while (formed == required) {
                if (right - left + 1 < bestLen) {
                    bestLen = right - left + 1;
                    bestLeft = left;
                }
                char lc = s.charAt(left);
                window.merge(lc, -1, Integer::sum);
                if (need.containsKey(lc) && window.get(lc) < need.get(lc)) formed--;
                left++;
            }
        }
        return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestLeft, bestLeft + bestLen);
    }

    /** LC 340 - Longest substring with at most k distinct characters. */
    static int longestKDistinct(String s, int k) {
        if (k == 0 || s == null || s.isEmpty()) return 0;
        Map<Character, Integer> counts = new HashMap<>();
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            counts.merge(s.charAt(right), 1, Integer::sum);
            while (counts.size() > k) {
                char lc = s.charAt(left);
                int c = counts.get(lc) - 1;
                if (c == 0) counts.remove(lc); else counts.put(lc, c);
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    /** LC 239 - Maximum in each window of size k via monotonic deque. */
    static int[] maxSlidingWindow(int[] nums, int k) {
        Deque<Integer> dq = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        for (int i = 0; i < nums.length; i++) {
            while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[i]) dq.pollLast();
            dq.offerLast(i);
            if (dq.peekFirst() == i - k) dq.pollFirst();
            if (i >= k - 1) out.add(nums[dq.peekFirst()]);
        }
        int[] result = new int[out.size()];
        for (int i = 0; i < out.size(); i++) result[i] = out.get(i);
        return result;
    }

    public static void main(String[] args) {
        System.out.println("Longest unique 'abcabcbb': " + lengthOfLongestSubstring("abcabcbb"));
        System.out.println("Min window 'ADOBECODEBANC','ABC': " + minWindow("ADOBECODEBANC", "ABC"));
        System.out.println("Longest 2-distinct 'eceba': " + longestKDistinct("eceba", 2));
        System.out.println("Max sliding window [1,3,-1,-3,5,3,6,7] k=3: "
            + Arrays.toString(maxSlidingWindow(new int[]{1, 3, -1, -3, 5, 3, 6, 7}, 3)));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in sliding_window.py:
 *   - HashMap<Character,Integer> replaces collections.Counter.
 *   - ArrayDeque<Integer> replaces collections.deque for the monotonic-deque
 *     maximum trick.
 *   - longestKDistinct and maxSlidingWindow are *additional* to what the
 *     companion interview_patterns.java covers (which only has LC 3 + LC 76).
 */
