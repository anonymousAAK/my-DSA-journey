/*
 * WEEK 7 - STRINGS
 * Topic: Palindrome Check & Anagram Check
 *
 * PALINDROME: A string that reads the same forwards and backwards.
 * Examples: "racecar", "madam", "level", "A man a plan a canal Panama"
 *
 * APPROACH: Two pointers — one from start, one from end, move inward.
 * Time: O(n), Space: O(1)
 *
 * ANAGRAM: Two strings are anagrams if one is a rearrangement of the other.
 * Examples: "listen" and "silent", "eat" and "tea"
 *
 * APPROACH 1: Sort both strings and compare. O(n log n), O(1) extra.
 * APPROACH 2: Frequency count array. O(n), O(1) space (fixed 26-element array).
 * APPROACH 3: HashMap for unicode/general characters. O(n), O(k) space (k = unique chars).
 */

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class PalindromeAndAnagram {

    // --- PALINDROME ---

    // Simple palindrome check (two-pointer)
    static boolean isPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            if (s.charAt(left) != s.charAt(right)) return false;
            left++;
            right--;
        }
        return true;
    }

    // Palindrome ignoring non-alphanumeric characters and case
    // Example: "A man, a plan, a canal: Panama" → true
    static boolean isPalindromeIgnoreNonAlpha(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            // Skip non-alphanumeric from left
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
            // Skip non-alphanumeric from right
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;
            if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right)))
                return false;
            left++;
            right--;
        }
        return true;
    }

    // --- ANAGRAM ---

    // Approach 1: Sort and compare — O(n log n)
    static boolean isAnagramSort(String a, String b) {
        if (a.length() != b.length()) return false;
        char[] ca = a.toCharArray(), cb = b.toCharArray();
        Arrays.sort(ca);
        Arrays.sort(cb);
        return Arrays.equals(ca, cb);
    }

    // Approach 2: Frequency count — O(n), O(1) space (26-char array)
    static boolean isAnagramFreq(String a, String b) {
        if (a.length() != b.length()) return false;
        int[] freq = new int[26];
        for (char c : a.toCharArray()) freq[c - 'a']++;
        for (char c : b.toCharArray()) {
            freq[c - 'a']--;
            if (freq[c - 'a'] < 0) return false;
        }
        return true;
    }

    // Approach 3: HashMap — works for any characters including unicode
    static boolean isAnagramMap(String a, String b) {
        if (a.length() != b.length()) return false;
        Map<Character, Integer> map = new HashMap<>();
        for (char c : a.toCharArray()) map.merge(c, 1, Integer::sum);
        for (char c : b.toCharArray()) {
            if (!map.containsKey(c) || map.get(c) == 0) return false;
            map.merge(c, -1, Integer::sum);
        }
        return true;
    }

    public static void main(String[] args) {
        // --- Palindrome tests ---
        System.out.println("=== Palindrome ===");
        String[] tests = {"racecar", "hello", "level", "madam", "a", ""};
        for (String t : tests) {
            System.out.printf("isPalindrome(\"%s\") = %b%n", t, isPalindrome(t));
        }

        System.out.println("\nisPalindromeIgnoreNonAlpha:");
        System.out.println("\"A man, a plan, a canal: Panama\" = " +
            isPalindromeIgnoreNonAlpha("A man, a plan, a canal: Panama")); // true
        System.out.println("\"race a car\" = " +
            isPalindromeIgnoreNonAlpha("race a car")); // false

        // --- Anagram tests ---
        System.out.println("\n=== Anagram ===");
        String[][] pairs = {{"listen", "silent"}, {"eat", "tea"}, {"hello", "world"}, {"anagram", "nagaram"}};
        for (String[] p : pairs) {
            System.out.printf("\"%s\" vs \"%s\":%n", p[0], p[1]);
            System.out.println("  Sort:  " + isAnagramSort(p[0], p[1]));
            System.out.println("  Freq:  " + isAnagramFreq(p[0], p[1]));
            System.out.println("  Map:   " + isAnagramMap(p[0], p[1]));
        }
    }
}
