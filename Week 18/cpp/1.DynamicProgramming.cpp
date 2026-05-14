/*
 * WEEK 18 - C++ DSA
 * Topic: Dynamic Programming Fundamentals
 * File: 1.DynamicProgramming.cpp
 *
 * CONCEPT:
 *     DP solves a problem by decomposing it into overlapping subproblems and
 *     storing each sub-answer to avoid recomputation. Two preconditions:
 *         1. Optimal substructure.
 *         2. Overlapping subproblems.
 *     Two implementation styles:
 *         TOP-DOWN  : recursion + memo (std::vector cache or std::unordered_map).
 *         BOTTOM-UP : tabulate from base case upward (usually faster, often
 *                     space-optimisable).
 *
 * KEY POINTS:
 *     - Identify state, recurrence, base case, and evaluation order.
 *     - Space-optimise when the recurrence depends only on a few prior rows.
 *     - For DP on subsets/knapsack-style, iterating capacity in REVERSE
 *       on the 1-D rolling array prevents reusing the current item.
 *
 * ALGORITHM / APPROACH:
 *     Five canonical problems:
 *         1. 0/1 Knapsack             (2-D and space-optimised 1-D)
 *         2. Longest Common Subseq.   (2-D)
 *         3. Coin change (min coins)  (1-D)
 *         4. Subset sum               (1-D boolean)
 *         5. Climbing stairs          (Fibonacci, O(1) state)
 *
 * C++-SPECIFIC NOTES:
 *     - std::vector<std::vector<int>> for 2-D DP tables.
 *     - INT_MAX from <climits>, or use a large sentinel; std::min works.
 *     - Pass arrays by const& to avoid copies.
 *     - For very large tables, consider a 1-D vector indexed manually
 *       (i * (W+1) + w) for cache-friendliness.
 *
 * DRY RUN:
 *     Knapsack weights={2,3,4,5}, values={3,4,5,6}, W=5
 *         dp[4][5] = 7  (take items with w=2,v=3 and w=3,v=4 -> total v=7)
 *
 *     LCS("ABCBDAB","BDCABA") -> 4
 *
 *     coinChange([1,2,5], 11)
 *         dp = [0,1,1,2,2,1,2,2,3,3,2,3]; answer = 3 (5+5+1).
 *
 * COMPLEXITY:
 *     knapsack          O(n*W) time, O(n*W) space (O(W) optimised)
 *     lcs               O(m*n) time, O(m*n) space
 *     coinChange        O(target * |coins|) time, O(target) space
 *     subsetSum         O(n * target) time, O(target) space
 *     climbStairs       O(n) time, O(1) space
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <climits>

using std::vector;
using std::string;
using std::max;
using std::min;

// ---------- 0/1 KNAPSACK ----------
int knapsack(const vector<int>& weights, const vector<int>& values, int W) {
    int n = (int)weights.size();
    vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
    for (int i = 1; i <= n; ++i) {
        int wi = weights[i - 1], vi = values[i - 1];
        for (int w = 0; w <= W; ++w) {
            dp[i][w] = dp[i - 1][w];
            if (wi <= w)
                dp[i][w] = max(dp[i][w], dp[i - 1][w - wi] + vi);
        }
    }
    return dp[n][W];
}

int knapsackOptimised(const vector<int>& weights, const vector<int>& values, int W) {
    vector<int> dp(W + 1, 0);
    for (size_t i = 0; i < weights.size(); ++i) {
        for (int w = W; w >= weights[i]; --w)               // REVERSE!
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i]);
    }
    return dp[W];
}

// ---------- LONGEST COMMON SUBSEQUENCE ----------
int lcs(const string& s1, const string& s2) {
    int m = (int)s1.size(), n = (int)s2.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    for (int i = 1; i <= m; ++i)
        for (int j = 1; j <= n; ++j)
            if (s1[i - 1] == s2[j - 1])
                dp[i][j] = dp[i - 1][j - 1] + 1;
            else
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
    return dp[m][n];
}

// ---------- COIN CHANGE (min coins) ----------
int coinChange(const vector<int>& coins, int target) {
    const int INF = target + 1;                              // sentinel
    vector<int> dp(target + 1, INF);
    dp[0] = 0;
    for (int a = 1; a <= target; ++a)
        for (int c : coins)
            if (c <= a) dp[a] = min(dp[a], dp[a - c] + 1);
    return dp[target] > target ? -1 : dp[target];
}

// ---------- SUBSET SUM ----------
bool subsetSum(const vector<int>& nums, int target) {
    vector<bool> dp(target + 1, false);
    dp[0] = true;
    for (int x : nums)
        for (int t = target; t >= x; --t)
            dp[t] = dp[t] || dp[t - x];
    return dp[target];
}

// ---------- CLIMBING STAIRS ----------
int climbStairs(int n) {
    if (n <= 2) return n;
    int prev2 = 1, prev1 = 2;
    for (int i = 3; i <= n; ++i) {
        int curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}

int main() {
    std::cout << "=== 0/1 Knapsack ===\n";
    vector<int> weights{2,3,4,5}, values{3,4,5,6};
    std::cout << "W=5  bottom-up: " << knapsack(weights, values, 5) << "\n";   // 7
    std::cout << "W=10 bottom-up: " << knapsack(weights, values, 10) << "\n";  // 13
    std::cout << "W=10 optimised: " << knapsackOptimised(weights, values, 10) << "\n";

    std::cout << "\n=== LCS ===\n";
    std::cout << "LCS(ABCBDAB,BDCABA) = " << lcs("ABCBDAB", "BDCABA") << "\n"; // 4
    std::cout << "LCS(AGGTAB,GXTXAYB) = " << lcs("AGGTAB", "GXTXAYB") << "\n"; // 4

    std::cout << "\n=== Coin Change ===\n";
    std::cout << "coins=[1,2,5], amount=11: " << coinChange({1,2,5}, 11) << "\n"; // 3
    std::cout << "coins=[2],     amount=3 : " << coinChange({2}, 3) << "\n";       // -1
    std::cout << "coins=[1],     amount=0 : " << coinChange({1}, 0) << "\n";       // 0

    std::cout << "\n=== Subset Sum ===\n";
    std::cout << std::boolalpha;
    std::cout << "{3,1,5,9,12} target=8: " << subsetSum({3,1,5,9,12}, 8) << "\n"; // true
    std::cout << "{3,1,5,9,12} target=7: " << subsetSum({3,1,5,9,12}, 7) << "\n"; // false

    std::cout << "\n=== Climbing Stairs ===\n";
    for (int i = 1; i <= 10; ++i)
        std::cout << "climbStairs(" << i << ") = " << climbStairs(i) << "\n";
}

/*
 * NOTES (C++ vs Java):
 *   - Java auto-initialises int arrays to 0; std::vector<int>(n, 0) is the
 *     C++ analogue.
 *   - INT_MAX overflow is a real risk in C++ when adding 1 — we use
 *     (target + 1) as a saturating sentinel instead.
 *   - std::vector<bool> is bit-packed (special template) — fine for our
 *     boolean DP table; for raw speed prefer std::vector<char>.
 *   - Pass big inputs by const& to avoid quadratic copying.
 *   - For very tight memory, switch to a flat 1-D buffer (vector<int>) and
 *     compute indices manually.
 */
