// Week 30: Interview Patterns & Mastery
// Two Pointers, Sliding Window, Fast & Slow Pointers, Merge Intervals, Top-K Elements
import java.util.*;

public class interview_patterns {

    // =====================================================================
    // TWO POINTERS
    // =====================================================================

    // Two Sum II - sorted array (LC 167) - Time: O(n), Space: O(1)
    static int[] twoSumII(int[] nums, int target) {
        int l = 0, r = nums.length - 1;
        while (l < r) {
            int s = nums[l] + nums[r];
            if (s == target) return new int[]{l + 1, r + 1}; // 1-indexed
            else if (s < target) l++;
            else r--;
        }
        return new int[]{};
    }

    // 3Sum (LC 15) - Time: O(n^2), Space: O(1) extra
    static List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        Arrays.sort(nums);
        for (int i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            int l = i + 1, r = nums.length - 1;
            while (l < r) {
                int s = nums[i] + nums[l] + nums[r];
                if (s == 0) {
                    result.add(Arrays.asList(nums[i], nums[l], nums[r]));
                    while (l < r && nums[l] == nums[l + 1]) l++;
                    while (l < r && nums[r] == nums[r - 1]) r--;
                    l++; r--;
                } else if (s < 0) l++;
                else r--;
            }
        }
        return result;
    }

    // Container With Most Water (LC 11) - Time: O(n), Space: O(1)
    static int maxArea(int[] height) {
        int l = 0, r = height.length - 1, best = 0;
        while (l < r) {
            best = Math.max(best, (r - l) * Math.min(height[l], height[r]));
            if (height[l] < height[r]) l++;
            else r--;
        }
        return best;
    }

    // =====================================================================
    // SLIDING WINDOW
    // =====================================================================

    // Longest Substring Without Repeating Characters (LC 3) - Time: O(n), Space: O(min(n, charset))
    static int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> idx = new HashMap<>();
        int left = 0, maxLen = 0;
        for (int r = 0; r < s.length(); r++) {
            char c = s.charAt(r);
            if (idx.containsKey(c) && idx.get(c) >= left)
                left = idx.get(c) + 1;
            idx.put(c, r);
            maxLen = Math.max(maxLen, r - left + 1);
        }
        return maxLen;
    }

    // Minimum Window Substring (LC 76) - Time: O(n + m), Space: O(m)
    static String minWindow(String s, String t) {
        if (s.length() < t.length()) return "";
        Map<Character, Integer> need = new HashMap<>();
        for (char c : t.toCharArray()) need.merge(c, 1, Integer::sum);

        int required = need.size(), formed = 0, left = 0;
        int bestLen = Integer.MAX_VALUE, bestLeft = 0;
        Map<Character, Integer> window = new HashMap<>();

        for (int r = 0; r < s.length(); r++) {
            char c = s.charAt(r);
            window.merge(c, 1, Integer::sum);
            if (need.containsKey(c) && window.get(c).intValue() == need.get(c).intValue())
                formed++;

            while (formed == required) {
                if (r - left + 1 < bestLen) {
                    bestLen = r - left + 1;
                    bestLeft = left;
                }
                char lc = s.charAt(left);
                window.merge(lc, -1, Integer::sum);
                if (need.containsKey(lc) && window.get(lc) < need.get(lc))
                    formed--;
                left++;
            }
        }
        return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestLeft, bestLeft + bestLen);
    }

    // =====================================================================
    // FAST & SLOW POINTERS
    // =====================================================================

    static class ListNode {
        int val;
        ListNode next;
        ListNode(int v) { val = v; }
    }

    // Linked List Cycle Detection (LC 141) - Time: O(n), Space: O(1)
    static boolean hasCycle(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }

    // Cycle Start Detection (LC 142) - Time: O(n), Space: O(1)
    static ListNode detectCycleStart(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                ListNode entry = head;
                while (entry != slow) { entry = entry.next; slow = slow.next; }
                return entry;
            }
        }
        return null;
    }

    // Happy Number (LC 202) - Time: O(log n), Space: O(1)
    static int digitSquareSum(int n) {
        int t = 0;
        while (n > 0) { int d = n % 10; t += d * d; n /= 10; }
        return t;
    }

    static boolean isHappy(int n) {
        int slow = n, fast = n;
        do {
            slow = digitSquareSum(slow);
            fast = digitSquareSum(digitSquareSum(fast));
        } while (slow != fast);
        return slow == 1;
    }

    // =====================================================================
    // MERGE INTERVALS
    // =====================================================================

    // Merge Intervals (LC 56) - Time: O(n log n), Space: O(n)
    static int[][] mergeIntervals(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
        List<int[]> merged = new ArrayList<>();
        merged.add(intervals[0]);
        for (int i = 1; i < intervals.length; i++) {
            int[] last = merged.get(merged.size() - 1);
            if (intervals[i][0] <= last[1])
                last[1] = Math.max(last[1], intervals[i][1]);
            else
                merged.add(intervals[i]);
        }
        return merged.toArray(new int[0][]);
    }

    // Insert Interval (LC 57) - Time: O(n), Space: O(n)
    static int[][] insertInterval(int[][] intervals, int[] newIv) {
        List<int[]> result = new ArrayList<>();
        int i = 0, n = intervals.length;

        // Add intervals ending before newIv starts
        while (i < n && intervals[i][1] < newIv[0]) result.add(intervals[i++]);

        // Merge overlapping intervals with newIv
        while (i < n && intervals[i][0] <= newIv[1]) {
            newIv[0] = Math.min(newIv[0], intervals[i][0]);
            newIv[1] = Math.max(newIv[1], intervals[i][1]);
            i++;
        }
        result.add(newIv);

        // Add remaining
        while (i < n) result.add(intervals[i++]);
        return result.toArray(new int[0][]);
    }

    // =====================================================================
    // TOP-K ELEMENTS
    // =====================================================================

    // Kth Largest Element (LC 215) - Time: O(n log k), Space: O(k)
    static int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        for (int num : nums) {
            heap.offer(num);
            if (heap.size() > k) heap.poll();
        }
        return heap.peek();
    }

    // Top K Frequent Elements (LC 347) - Time: O(n log k), Space: O(n)
    static int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) freq.merge(num, 1, Integer::sum);

        PriorityQueue<Map.Entry<Integer, Integer>> heap =
            new PriorityQueue<>(Comparator.comparingInt(Map.Entry::getValue));
        for (var entry : freq.entrySet()) {
            heap.offer(entry);
            if (heap.size() > k) heap.poll();
        }

        int[] result = new int[k];
        for (int i = 0; i < k; i++) result[i] = heap.poll().getKey();
        return result;
    }

    // Top K Frequent - Bucket Sort (LC 347) - Time: O(n), Space: O(n)
    @SuppressWarnings("unchecked")
    static int[] topKFrequentBucket(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) freq.merge(num, 1, Integer::sum);

        List<Integer>[] buckets = new List[nums.length + 1];
        for (var entry : freq.entrySet()) {
            int f = entry.getValue();
            if (buckets[f] == null) buckets[f] = new ArrayList<>();
            buckets[f].add(entry.getKey());
        }

        int[] result = new int[k];
        int idx = 0;
        for (int i = buckets.length - 1; i >= 0 && idx < k; i--) {
            if (buckets[i] != null)
                for (int num : buckets[i]) { result[idx++] = num; if (idx == k) break; }
        }
        return result;
    }

    // =====================================================================
    // DEMO
    // =====================================================================

    public static void main(String[] args) {
        System.out.println("=== TWO POINTERS ===");
        System.out.println("Two Sum II [2,7,11,15] t=9: " + Arrays.toString(twoSumII(new int[]{2,7,11,15}, 9)));
        System.out.println("3Sum [-1,0,1,2,-1,-4]: " + threeSum(new int[]{-1,0,1,2,-1,-4}));
        System.out.println("Max Area [1,8,6,2,5,4,8,3,7]: " + maxArea(new int[]{1,8,6,2,5,4,8,3,7}));

        System.out.println("\n=== SLIDING WINDOW ===");
        System.out.println("Longest unique 'abcabcbb': " + lengthOfLongestSubstring("abcabcbb"));
        System.out.println("Min window 'ADOBECODEBANC','ABC': " + minWindow("ADOBECODEBANC", "ABC"));

        System.out.println("\n=== FAST & SLOW ===");
        System.out.println("Happy 19: " + isHappy(19));
        System.out.println("Happy 2: " + isHappy(2));
        ListNode a = new ListNode(1), b = new ListNode(2), c = new ListNode(3);
        a.next = b; b.next = c; c.next = b;
        System.out.println("Cycle: " + hasCycle(a) + ", starts at: " + detectCycleStart(a).val);

        System.out.println("\n=== MERGE INTERVALS ===");
        int[][] merged = mergeIntervals(new int[][]{{1,3},{2,6},{8,10},{15,18}});
        System.out.print("Merged: "); for (int[] m : merged) System.out.print(Arrays.toString(m)); System.out.println();
        int[][] inserted = insertInterval(new int[][]{{1,3},{6,9}}, new int[]{2,5});
        System.out.print("Inserted: "); for (int[] m : inserted) System.out.print(Arrays.toString(m)); System.out.println();

        System.out.println("\n=== TOP-K ===");
        System.out.println("Kth largest k=2: " + findKthLargest(new int[]{3,2,1,5,6,4}, 2));
        System.out.println("Top 2 frequent: " + Arrays.toString(topKFrequent(new int[]{1,1,1,2,2,3}, 2)));
        System.out.println("Top 2 bucket: " + Arrays.toString(topKFrequentBucket(new int[]{1,1,1,2,2,3}, 2)));
    }
}
