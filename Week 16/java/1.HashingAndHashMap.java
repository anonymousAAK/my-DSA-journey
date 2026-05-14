/*
 * WEEK 16 - HASH TABLES & MAPS
 * Topic: Hashing Fundamentals + Classic HashMap Problems
 *
 * HASHING:
 * Map a key to an array index using a hash function.
 * Goal: O(1) average time for insert, delete, lookup.
 *
 * HASH FUNCTION requirements:
 * - Deterministic: same key → same hash
 * - Uniform: distribute keys evenly
 * - Fast to compute
 *
 * COLLISION RESOLUTION:
 * 1. Chaining: each bucket holds a linked list. O(1+α) avg (α = load factor)
 * 2. Open Addressing: find next open slot (linear, quadratic, double hashing)
 *
 * LOAD FACTOR α = n/m (n=elements, m=buckets). Rehash when α > threshold.
 *
 * Java HashMap:
 * - Initial capacity: 16 buckets
 * - Load factor threshold: 0.75
 * - Resize: double buckets, rehash all
 * - Collision: chaining with linked list → tree (TreeMap) when chain length > 8
 * - Time: O(1) average, O(n) worst (all keys hash to same bucket)
 *
 * PROBLEMS COVERED:
 * 1. Two Sum
 * 2. Count frequency of elements
 * 3. Group anagrams
 * 4. Subarray with zero sum
 * 5. Longest consecutive sequence
 */

import java.util.*;

public class HashingAndHashMap {

    // PROBLEM 1: Two Sum
    // Given array and target, return indices of two numbers that sum to target.
    // Time: O(n), Space: O(n)
    static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>(); // value → index
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) return new int[]{map.get(complement), i};
            map.put(nums[i], i);
        }
        return new int[]{-1, -1}; // no solution
    }

    // PROBLEM 2: Count element frequencies
    static Map<Integer, Integer> frequency(int[] arr) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int x : arr) freq.merge(x, 1, Integer::sum);
        return freq;
    }

    // PROBLEM 3: Group Anagrams
    // Group strings that are anagrams of each other.
    // Time: O(n * k log k) where k = max string length
    static List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            char[] chars = s.toCharArray();
            Arrays.sort(chars); // sorted key identifies anagram group
            String key = new String(chars);
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(map.values());
    }

    // PROBLEM 4: Subarray with zero sum
    // Does any contiguous subarray have sum == 0?
    // Key insight: prefix[i] == prefix[j] means arr[i+1..j] sums to 0.
    // Time: O(n), Space: O(n)
    static boolean hasZeroSumSubarray(int[] arr) {
        Set<Integer> prefixSums = new HashSet<>();
        prefixSums.add(0); // empty subarray has sum 0
        int sum = 0;
        for (int x : arr) {
            sum += x;
            if (prefixSums.contains(sum)) return true;
            prefixSums.add(sum);
        }
        return false;
    }

    // Find all subarrays with sum == k (generalization)
    static int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> prefixCount = new HashMap<>();
        prefixCount.put(0, 1);
        int sum = 0, count = 0;
        for (int x : nums) {
            sum += x;
            count += prefixCount.getOrDefault(sum - k, 0);
            prefixCount.merge(sum, 1, Integer::sum);
        }
        return count;
    }

    // PROBLEM 5: Longest Consecutive Sequence
    // Given unsorted array, find longest sequence of consecutive integers.
    // Example: [100,4,200,1,3,2] → 4 (sequence 1,2,3,4)
    // Time: O(n), Space: O(n)
    static int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int x : nums) set.add(x);
        int longest = 0;
        for (int x : set) {
            // Only start a sequence from its smallest element
            if (!set.contains(x - 1)) {
                int curr = x, length = 1;
                while (set.contains(curr + 1)) { curr++; length++; }
                longest = Math.max(longest, length);
            }
        }
        return longest;
    }

    public static void main(String[] args) {
        // Two Sum
        System.out.println("=== Two Sum ===");
        System.out.println(Arrays.toString(twoSum(new int[]{2, 7, 11, 15}, 9)));  // [0, 1]
        System.out.println(Arrays.toString(twoSum(new int[]{3, 2, 4}, 6)));       // [1, 2]

        // Frequency
        System.out.println("\n=== Frequency Count ===");
        int[] arr = {1, 3, 2, 3, 1, 1, 4};
        System.out.println(frequency(arr)); // {1=3, 2=1, 3=2, 4=1}

        // Group Anagrams
        System.out.println("\n=== Group Anagrams ===");
        String[] words = {"eat", "tea", "tan", "ate", "nat", "bat"};
        List<List<String>> groups = groupAnagrams(words);
        for (List<String> g : groups) System.out.println(g);

        // Subarray sum
        System.out.println("\n=== Subarray with Zero Sum ===");
        System.out.println(hasZeroSumSubarray(new int[]{4, 2, -3, 1, 6}));   // true  (2,-3,1)
        System.out.println(hasZeroSumSubarray(new int[]{4, 2, 0, 1, 6}));    // true  (0 itself)
        System.out.println(hasZeroSumSubarray(new int[]{-3, 2, 3, 1, 6}));   // false

        System.out.println("\n=== Subarray Sum == k ===");
        System.out.println(subarraySum(new int[]{1, 1, 1}, 2));              // 2
        System.out.println(subarraySum(new int[]{1, 2, 3}, 3));              // 2

        // Longest Consecutive
        System.out.println("\n=== Longest Consecutive Sequence ===");
        System.out.println(longestConsecutive(new int[]{100, 4, 200, 1, 3, 2})); // 4
        System.out.println(longestConsecutive(new int[]{0, 3, 7, 2, 5, 8, 4, 6, 0, 1})); // 9
    }
}
