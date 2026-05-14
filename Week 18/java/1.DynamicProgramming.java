/*
 * WEEK 18 - DYNAMIC PROGRAMMING (Introduction)
 * Topic: DP Fundamentals — Memoization vs Tabulation
 *
 * DYNAMIC PROGRAMMING (DP):
 * Solve a problem by breaking it into overlapping subproblems,
 * solving each subproblem ONCE and storing the result.
 *
 * WHEN TO USE DP:
 * 1. Optimal substructure: optimal solution contains optimal solutions to subproblems.
 * 2. Overlapping subproblems: same subproblems are solved multiple times.
 *
 * TWO APPROACHES:
 * 1. TOP-DOWN (Memoization): Recursion + cache. Natural to think about.
 * 2. BOTTOM-UP (Tabulation): Fill a table from smallest subproblems upward. Usually faster.
 *
 * PROBLEMS COVERED:
 * 1. 0/1 Knapsack — classic DP on subsets
 * 2. Longest Common Subsequence (LCS)
 * 3. Coin Change (minimum coins to make amount)
 * 4. Subset Sum
 * 5. Climbing Stairs (Fibonacci-style DP)
 *
 * 0/1 KNAPSACK:
 * n items with weights[i] and values[i], capacity W.
 * Maximize total value without exceeding capacity.
 * Each item: either take it (0/1) or don't.
 *
 * Recurrence: dp[i][w] = max(dp[i-1][w], dp[i-1][w-weights[i]] + values[i])
 * Time: O(n*W), Space: O(n*W) or O(W) optimized
 */

import java.util.Arrays;

public class DynamicProgramming {

    // =====================
    // 0/1 KNAPSACK
    // =====================
    static int knapsack(int[] weights, int[] values, int W) {
        int n = weights.length;
        // dp[i][w] = max value using first i items with capacity w
        int[][] dp = new int[n + 1][W + 1];
        for (int i = 1; i <= n; i++) {
            for (int w = 0; w <= W; w++) {
                dp[i][w] = dp[i-1][w]; // don't take item i
                if (weights[i-1] <= w)  // take item i (if it fits)
                    dp[i][w] = Math.max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1]);
            }
        }
        return dp[n][W];
    }

    // Space-optimized knapsack: O(W) space (process w in reverse!)
    static int knapsackOptimized(int[] weights, int[] values, int W) {
        int[] dp = new int[W + 1];
        for (int i = 0; i < weights.length; i++)
            for (int w = W; w >= weights[i]; w--) // REVERSE to avoid using item twice
                dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
        return dp[W];
    }

    // =====================
    // LONGEST COMMON SUBSEQUENCE (LCS)
    // =====================
    // Find length of longest subsequence present in both strings.
    // "ABCBDAB" and "BDCABA" → LCS length = 4 ("BCBA" or "BDAB")
    //
    // Recurrence:
    // dp[i][j] = dp[i-1][j-1] + 1              if s1[i-1] == s2[j-1]
    //          = max(dp[i-1][j], dp[i][j-1])    otherwise
    static int lcs(String s1, String s2) {
        int m = s1.length(), n = s2.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 1; i <= m; i++)
            for (int j = 1; j <= n; j++)
                if (s1.charAt(i-1) == s2.charAt(j-1))
                    dp[i][j] = dp[i-1][j-1] + 1;
                else
                    dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
        return dp[m][n];
    }

    // =====================
    // COIN CHANGE (Minimum coins)
    // =====================
    // Minimum number of coins to make amount 'target'.
    // dp[a] = min coins to make amount a
    // dp[a] = min(dp[a - coin] + 1) for all coins where coin <= a
    static int coinChange(int[] coins, int target) {
        int[] dp = new int[target + 1];
        Arrays.fill(dp, target + 1); // initialize to "impossible"
        dp[0] = 0; // base case: 0 coins to make amount 0
        for (int a = 1; a <= target; a++)
            for (int coin : coins)
                if (coin <= a) dp[a] = Math.min(dp[a], dp[a - coin] + 1);
        return dp[target] > target ? -1 : dp[target];
    }

    // =====================
    // SUBSET SUM
    // =====================
    // Can we select a subset of 'nums' that sums to 'target'?
    static boolean subsetSum(int[] nums, int target) {
        boolean[] dp = new boolean[target + 1];
        dp[0] = true; // empty subset sums to 0
        for (int x : nums)
            for (int t = target; t >= x; t--) // reverse to avoid reusing
                dp[t] = dp[t] || dp[t - x];
        return dp[target];
    }

    // =====================
    // CLIMBING STAIRS
    // =====================
    // Reach stair n taking 1 or 2 steps at a time. How many distinct ways?
    static int climbStairs(int n) {
        if (n <= 2) return n;
        int prev2 = 1, prev1 = 2;
        for (int i = 3; i <= n; i++) {
            int curr = prev1 + prev2;
            prev2 = prev1;
            prev1 = curr;
        }
        return prev1;
    }

    public static void main(String[] args) {
        // Knapsack
        System.out.println("=== 0/1 Knapsack ===");
        int[] weights = {2, 3, 4, 5};
        int[] values  = {3, 4, 5, 6};
        System.out.println("Max value (W=5):  " + knapsack(weights, values, 5));   // 7
        System.out.println("Max value (W=10): " + knapsack(weights, values, 10));  // 13
        System.out.println("Optimized (W=10): " + knapsackOptimized(weights, values, 10));

        // LCS
        System.out.println("\n=== LCS ===");
        System.out.println("LCS(\"ABCBDAB\",\"BDCABA\") = " + lcs("ABCBDAB","BDCABA")); // 4
        System.out.println("LCS(\"AGGTAB\",\"GXTXAYB\") = " + lcs("AGGTAB","GXTXAYB")); // 4

        // Coin Change
        System.out.println("\n=== Coin Change ===");
        System.out.println("coins=[1,2,5], amount=11: " + coinChange(new int[]{1,2,5}, 11)); // 3
        System.out.println("coins=[2], amount=3: " + coinChange(new int[]{2}, 3));            // -1
        System.out.println("coins=[1], amount=0: " + coinChange(new int[]{1}, 0));            // 0

        // Subset Sum
        System.out.println("\n=== Subset Sum ===");
        System.out.println("{3,1,5,9,12}, target=8:  " + subsetSum(new int[]{3,1,5,9,12}, 8));  // true
        System.out.println("{3,1,5,9,12}, target=7:  " + subsetSum(new int[]{3,1,5,9,12}, 7));  // false

        // Climbing Stairs
        System.out.println("\n=== Climbing Stairs ===");
        for (int i = 1; i <= 10; i++)
            System.out.println("climbStairs(" + i + ") = " + climbStairs(i));
        // 1,2,3,5,8,13,21,34,55,89 (Fibonacci!)
    }
}
