// Week 30: Interview Patterns - Two Pointers, Sliding Window, Fast&Slow, Merge Intervals, Top-K
import java.util.*;

public class interview_patterns {

    // Two Sum II (LC 167) - O(n)
    static int[] twoSum(int[] nums, int target) {
        int l = 0, r = nums.length - 1;
        while (l < r) {
            int s = nums[l] + nums[r];
            if (s == target) return new int[]{l, r};
            else if (s < target) l++; else r--;
        }
        return new int[]{};
    }

    // Longest Substring Without Repeating (LC 3) - O(n)
    static int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> idx = new HashMap<>();
        int left = 0, max = 0;
        for (int r = 0; r < s.length(); r++) {
            if (idx.containsKey(s.charAt(r)) && idx.get(s.charAt(r)) >= left)
                left = idx.get(s.charAt(r)) + 1;
            idx.put(s.charAt(r), r);
            max = Math.max(max, r - left + 1);
        }
        return max;
    }

    // Happy Number (LC 202) - O(log n)
    static boolean isHappy(int n) {
        int slow = n, fast = nextNum(n);
        while (fast != 1 && slow != fast) {
            slow = nextNum(slow);
            fast = nextNum(nextNum(fast));
        }
        return fast == 1;
    }
    static int nextNum(int n) { int t = 0; while (n > 0) { int d = n%10; t += d*d; n /= 10; } return t; }

    // Merge Intervals (LC 56) - O(n log n)
    static int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, (a,b) -> a[0]-b[0]);
        List<int[]> merged = new ArrayList<>();
        merged.add(intervals[0]);
        for (int i = 1; i < intervals.length; i++) {
            int[] last = merged.get(merged.size()-1);
            if (intervals[i][0] <= last[1]) last[1] = Math.max(last[1], intervals[i][1]);
            else merged.add(intervals[i]);
        }
        return merged.toArray(new int[0][]);
    }

    // Kth Largest (LC 215) - O(n log k)
    static int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        for (int n : nums) { heap.offer(n); if (heap.size() > k) heap.poll(); }
        return heap.peek();
    }

    public static void main(String[] args) {
        System.out.println("Two Sum: " + Arrays.toString(twoSum(new int[]{2,7,11,15}, 9)));
        System.out.println("Longest substring: " + lengthOfLongestSubstring("abcabcbb"));
        System.out.println("Happy 19: " + isHappy(19));
        int[][] merged = merge(new int[][]{{1,3},{2,6},{8,10},{15,18}});
        System.out.print("Merge: "); for (int[] m : merged) System.out.print(Arrays.toString(m)); System.out.println();
        System.out.println("3rd largest: " + findKthLargest(new int[]{3,2,1,5,6,4}, 3));
    }
}
