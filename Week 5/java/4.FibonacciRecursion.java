/*
 * WEEK 5 - FUNCTIONS & RECURSION
 * Topic: Fibonacci with Recursion, Memoization, and Iteration
 *
 * FIBONACCI SEQUENCE: 0, 1, 1, 2, 3, 5, 8, 13, 21, ...
 * Definition: fib(n) = fib(n-1) + fib(n-2)
 * Base cases: fib(0) = 0, fib(1) = 1
 *
 * APPROACH 1 — Naive Recursion:
 * Simple but recomputes the same values many times.
 * Time: O(2^n) — exponential! (very slow for large n)
 * Space: O(n) call stack depth
 *
 * APPROACH 2 — Memoization (Top-Down DP):
 * Store results of subproblems to avoid recomputation.
 * Time: O(n)
 * Space: O(n) for memo array + O(n) call stack
 *
 * APPROACH 3 — Iterative (Bottom-Up DP):
 * Fill a table from the smallest subproblem upward.
 * Time: O(n)
 * Space: O(n) for table, or O(1) with two variables
 *
 * This problem is a CLASSIC introduction to Dynamic Programming thinking!
 */

import java.util.Arrays;

public class FibonacciRecursion {

    // APPROACH 1: Naive recursion — simple but O(2^n)
    static long fibNaive(int n) {
        if (n <= 1) return n;
        return fibNaive(n - 1) + fibNaive(n - 2);
    }

    // APPROACH 2: Memoization — O(n) time, O(n) space
    static long[] memo = new long[100];

    static long fibMemo(int n) {
        if (n <= 1) return n;
        if (memo[n] != -1) return memo[n]; // already computed
        memo[n] = fibMemo(n - 1) + fibMemo(n - 2);
        return memo[n];
    }

    // APPROACH 3: Iterative — O(n) time, O(1) space
    static long fibIterative(int n) {
        if (n <= 1) return n;
        long prev2 = 0, prev1 = 1;
        for (int i = 2; i <= n; i++) {
            long curr = prev1 + prev2;
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }

    public static void main(String[] args) {
        Arrays.fill(memo, -1); // initialize memo with -1 (sentinel)

        // Print first 10 Fibonacci numbers
        System.out.print("First 10 Fibonacci numbers: ");
        for (int i = 0; i < 10; i++) {
            System.out.print(fibIterative(i) + " ");
        }
        System.out.println();

        // Compare approaches for n = 10
        int n = 10;
        System.out.println("\nfib(" + n + "):");
        System.out.println("  Naive:     " + fibNaive(n));
        System.out.println("  Memo:      " + fibMemo(n));
        System.out.println("  Iterative: " + fibIterative(n));

        // For large n, naive is impossibly slow; memoization & iterative are fine
        int big = 45;
        System.out.println("\nfib(" + big + ") iterative = " + fibIterative(big));
        // fibNaive(45) would take ~30 seconds; fibMemo(45) is instant
        Arrays.fill(memo, -1);
        System.out.println("fib(" + big + ") memoized  = " + fibMemo(big));

        // Key lesson: always think about overlapping subproblems!
        System.out.println("\nKEY INSIGHT:");
        System.out.println("fibNaive(5) makes " + countCalls(5) + " recursive calls.");
        System.out.println("With memoization, it makes only 9 calls (2*5 - 1).");
    }

    // Helper to count how many calls naive recursion makes
    static int calls = 0;
    static long countCalls(int n) {
        calls = 0;
        fibCount(n);
        return calls;
    }
    static long fibCount(int n) {
        calls++;
        if (n <= 1) return n;
        return fibCount(n - 1) + fibCount(n - 2);
    }
}
