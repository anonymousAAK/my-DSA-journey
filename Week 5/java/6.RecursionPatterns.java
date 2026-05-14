/*
 * WEEK 5 - FUNCTIONS & RECURSION
 * Topic: Common Recursion Patterns
 *
 * Master these patterns and you can solve 90% of recursive problems:
 *
 * PATTERN 1: Linear Recursion — one recursive call per invocation
 *   Example: factorial, sum, reverse string
 *
 * PATTERN 2: Binary Recursion — two recursive calls per invocation
 *   Example: Fibonacci, binary search, merge sort
 *
 * PATTERN 3: Tail Recursion — recursive call is the LAST operation
 *   Advantage: can be optimized by compiler to use O(1) stack space
 *   (Java doesn't optimize this automatically, but it's a good concept)
 *
 * PATTERN 4: Mutual Recursion — function A calls B, B calls A
 *   Example: isEven/isOdd check
 *
 * PATTERN 5: Helper / Accumulator pattern — carry state in parameters
 *
 * Time/Space: varies by problem (shown per example)
 */

public class RecursionPatterns {

    // PATTERN 1: Linear Recursion — Reverse a string
    // Time: O(n), Space: O(n) stack + O(n) output
    static String reverse(String s) {
        if (s.isEmpty()) return "";
        return reverse(s.substring(1)) + s.charAt(0);
    }

    // PATTERN 3: Tail Recursion — Factorial with accumulator
    // tail-recursive because the last operation is the recursive call itself
    static long factTail(int n, long acc) {
        if (n <= 1) return acc;
        return factTail(n - 1, n * acc); // accumulate result into 'acc'
    }
    // Wrapper: start accumulator at 1
    static long factorial(int n) { return factTail(n, 1); }

    // PATTERN 4: Mutual Recursion
    static boolean isEven(int n) {
        if (n == 0) return true;
        return isOdd(n - 1);
    }
    static boolean isOdd(int n) {
        if (n == 0) return false;
        return isEven(n - 1);
    }

    // PATTERN 5: Helper / Accumulator — Sum digits of a number
    static int digitSum(int n) {
        if (n == 0) return 0;
        return (n % 10) + digitSum(n / 10);
    }

    // BONUS: Recursion to generate all subsets (2^n subsets)
    // This is the foundation of backtracking
    static void subsets(int[] arr, int idx, String current) {
        if (idx == arr.length) {
            System.out.println("{" + current + "}");
            return;
        }
        // Choice 1: EXCLUDE arr[idx]
        subsets(arr, idx + 1, current);
        // Choice 2: INCLUDE arr[idx]
        String sep = current.isEmpty() ? "" : ",";
        subsets(arr, idx + 1, current + sep + arr[idx]);
    }

    // BONUS: Check if a string is a palindrome using recursion
    static boolean isPalindrome(String s, int left, int right) {
        if (left >= right) return true;
        if (s.charAt(left) != s.charAt(right)) return false;
        return isPalindrome(s, left + 1, right - 1);
    }

    public static void main(String[] args) {
        // Pattern 1
        System.out.println("reverse(\"hello\") = " + reverse("hello"));

        // Pattern 3
        System.out.println("factorial(5) [tail] = " + factorial(5));
        System.out.println("factorial(10) [tail] = " + factorial(10));

        // Pattern 4
        System.out.println("isEven(4) = " + isEven(4));
        System.out.println("isOdd(7) = " + isOdd(7));

        // Pattern 5
        System.out.println("digitSum(1234) = " + digitSum(1234)); // 10

        // Subsets
        System.out.println("\nAll subsets of {1, 2, 3}:");
        subsets(new int[]{1, 2, 3}, 0, "");

        // Palindrome
        System.out.println("\nisPalindrome(\"racecar\") = " + isPalindrome("racecar", 0, 6));
        System.out.println("isPalindrome(\"hello\") = " + isPalindrome("hello", 0, 4));
    }
}
