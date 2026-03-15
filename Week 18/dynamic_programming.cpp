/*
 * =============================================================================
 * Week 18 — Dynamic Programming  (C++17)
 * =============================================================================
 *
 * Topics covered
 * --------------
 *   1. Climbing Stairs
 *   2. 0/1 Knapsack  (2D table + 1D space-optimized)
 *   3. Longest Common Subsequence (LCS) with reconstruction
 *   4. Longest Increasing Subsequence (LIS) — O(n^2) + O(n log n)
 *   5. Coin Change (minimum coins)
 *   6. Subset Sum (boolean)
 *   7. Edit Distance (Levenshtein)
 *
 * Complexity cheat-sheet
 * ----------------------
 *   climbing_stairs        O(n) time  |  O(1) space
 *   knapsack_2d            O(n*W)     |  O(n*W)
 *   knapsack_1d            O(n*W)     |  O(W)
 *   lcs + reconstruction   O(n*m)     |  O(n*m)
 *   lis_quadratic          O(n^2)     |  O(n)
 *   lis_nlogn              O(n log n) |  O(n)
 *   coin_change            O(n*amount)|  O(amount)
 *   subset_sum             O(n*target)|  O(target)
 *   edit_distance           O(n*m)     |  O(n*m)  (can be O(min(n,m)))
 *
 * Build & run
 *   g++ -std=c++17 -O2 -o dp dynamic_programming.cpp && ./dp
 * =============================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cassert>
#include <sstream>
#include <climits>

// ---------------------------------------------------------------------------
// Helper
// ---------------------------------------------------------------------------
template <typename T>
std::string vec_str(const std::vector<T>& v) {
    std::ostringstream oss;
    oss << "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i) oss << ", ";
        oss << v[i];
    }
    oss << "]";
    return oss.str();
}

// ---------------------------------------------------------------------------
// 1. Climbing Stairs — Fibonacci variant
// ---------------------------------------------------------------------------
// dp[i] = dp[i-1] + dp[i-2]
// Complexity:  Time O(n)  |  Space O(1)
int climbing_stairs(int n) {
    if (n <= 2) return n;
    int a = 1, b = 2;
    for (int i = 3; i <= n; ++i) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}

// ---------------------------------------------------------------------------
// 2a. 0/1 Knapsack — 2D table
// ---------------------------------------------------------------------------
// dp[i][w] = max value using first i items with capacity w
// Complexity:  Time O(n*W)  |  Space O(n*W)
int knapsack_2d(const std::vector<int>& weights, const std::vector<int>& values, int W) {
    int n = static_cast<int>(weights.size());
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(W + 1, 0));

    for (int i = 1; i <= n; ++i) {
        for (int w = 0; w <= W; ++w) {
            dp[i][w] = dp[i - 1][w];   // don't take item i
            if (weights[i - 1] <= w) {
                dp[i][w] = std::max(dp[i][w],
                                    dp[i - 1][w - weights[i - 1]] + values[i - 1]);
            }
        }
    }
    return dp[n][W];
}

// ---------------------------------------------------------------------------
// 2b. 0/1 Knapsack — 1D optimized (reverse iteration)
// ---------------------------------------------------------------------------
// Complexity:  Time O(n*W)  |  Space O(W)
int knapsack_1d(const std::vector<int>& weights, const std::vector<int>& values, int W) {
    int n = static_cast<int>(weights.size());
    std::vector<int> dp(W + 1, 0);

    for (int i = 0; i < n; ++i) {
        // Iterate backwards so each item is used at most once.
        for (int w = W; w >= weights[i]; --w) {
            dp[w] = std::max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }
    return dp[W];
}

// ---------------------------------------------------------------------------
// 3. LCS — with reconstruction
// ---------------------------------------------------------------------------
// Complexity:  Time O(n*m)  |  Space O(n*m)
std::pair<int, std::string> lcs(const std::string& a, const std::string& b) {
    int n = static_cast<int>(a.size());
    int m = static_cast<int>(b.size());
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(m + 1, 0));

    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (a[i - 1] == b[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = std::max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    // Reconstruct the subsequence.
    std::string result;
    int i = n, j = m;
    while (i > 0 && j > 0) {
        if (a[i - 1] == b[j - 1]) {
            result.push_back(a[i - 1]);
            --i; --j;
        } else if (dp[i - 1][j] > dp[i][j - 1]) {
            --i;
        } else {
            --j;
        }
    }
    std::reverse(result.begin(), result.end());
    return {dp[n][m], result};
}

// ---------------------------------------------------------------------------
// 4a. LIS — O(n^2)
// ---------------------------------------------------------------------------
// dp[i] = length of LIS ending at index i
// Complexity:  Time O(n^2)  |  Space O(n)
int lis_quadratic(const std::vector<int>& nums) {
    int n = static_cast<int>(nums.size());
    if (n == 0) return 0;
    std::vector<int> dp(n, 1);

    for (int i = 1; i < n; ++i) {
        for (int j = 0; j < i; ++j) {
            if (nums[j] < nums[i]) {
                dp[i] = std::max(dp[i], dp[j] + 1);
            }
        }
    }
    return *std::max_element(dp.begin(), dp.end());
}

// ---------------------------------------------------------------------------
// 4b. LIS — O(n log n) using patience sorting / lower_bound
// ---------------------------------------------------------------------------
// tails[i] = smallest tail element of all increasing subsequences of length i+1
// Complexity:  Time O(n log n)  |  Space O(n)
int lis_nlogn(const std::vector<int>& nums) {
    std::vector<int> tails;
    for (int x : nums) {
        auto it = std::lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) {
            tails.push_back(x);
        } else {
            *it = x;
        }
    }
    return static_cast<int>(tails.size());
}

// ---------------------------------------------------------------------------
// 5. Coin Change — minimum number of coins
// ---------------------------------------------------------------------------
// dp[i] = min coins needed to make amount i
// Complexity:  Time O(n * amount)  |  Space O(amount)
int coin_change(const std::vector<int>& coins, int amount) {
    const int INF = amount + 1;
    std::vector<int> dp(amount + 1, INF);
    dp[0] = 0;

    for (int a = 1; a <= amount; ++a) {
        for (int c : coins) {
            if (c <= a) {
                dp[a] = std::min(dp[a], dp[a - c] + 1);
            }
        }
    }
    return dp[amount] >= INF ? -1 : dp[amount];
}

// ---------------------------------------------------------------------------
// 6. Subset Sum — can we form `target` using a subset of nums?
// ---------------------------------------------------------------------------
// dp[j] = true if sum j is achievable
// Complexity:  Time O(n * target)  |  Space O(target)
bool subset_sum(const std::vector<int>& nums, int target) {
    std::vector<bool> dp(target + 1, false);
    dp[0] = true;

    for (int x : nums) {
        for (int j = target; j >= x; --j) {
            if (dp[j - x]) dp[j] = true;
        }
    }
    return dp[target];
}

// ---------------------------------------------------------------------------
// 7. Edit Distance (Levenshtein)
// ---------------------------------------------------------------------------
// dp[i][j] = min operations to convert a[0..i-1] to b[0..j-1]
// Complexity:  Time O(n*m)  |  Space O(n*m)
int edit_distance(const std::string& a, const std::string& b) {
    int n = static_cast<int>(a.size());
    int m = static_cast<int>(b.size());
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(m + 1, 0));

    for (int i = 0; i <= n; ++i) dp[i][0] = i;
    for (int j = 0; j <= m; ++j) dp[0][j] = j;

    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (a[i - 1] == b[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + std::min({dp[i - 1][j],        // delete
                                          dp[i][j - 1],        // insert
                                          dp[i - 1][j - 1]});  // replace
            }
        }
    }
    return dp[n][m];
}

// ---------------------------------------------------------------------------
// main — test cases
// ---------------------------------------------------------------------------
int main() {
    std::cout << "=== Week 18: Dynamic Programming ===\n\n";

    // 1. Climbing Stairs
    {
        std::cout << "-- Climbing Stairs --\n";
        assert(climbing_stairs(1) == 1);
        assert(climbing_stairs(2) == 2);
        assert(climbing_stairs(5) == 8);
        assert(climbing_stairs(10) == 89);
        std::cout << "  stairs(5)=" << climbing_stairs(5)
                  << "  stairs(10)=" << climbing_stairs(10) << "\n\n";
    }

    // 2. 0/1 Knapsack
    {
        std::cout << "-- 0/1 Knapsack --\n";
        std::vector<int> w = {2, 3, 4, 5};
        std::vector<int> v = {3, 4, 5, 6};
        int W = 8;
        int res2d = knapsack_2d(w, v, W);
        int res1d = knapsack_1d(w, v, W);
        assert(res2d == res1d);
        assert(res2d == 10);  // items 1+3 (w=3+5=8, v=4+6=10)
        std::cout << "  2D=" << res2d << "  1D=" << res1d << "  (capacity=" << W << ")\n\n";
    }

    // 3. LCS
    {
        std::cout << "-- Longest Common Subsequence --\n";
        auto [len, subseq] = lcs("ABCBDAB", "BDCAB");
        assert(len == 4);
        std::cout << "  LCS(\"ABCBDAB\", \"BDCAB\") = \"" << subseq
                  << "\"  length=" << len << "\n\n";
    }

    // 4. LIS
    {
        std::cout << "-- Longest Increasing Subsequence --\n";
        std::vector<int> nums = {10, 9, 2, 5, 3, 7, 101, 18};
        int r1 = lis_quadratic(nums);
        int r2 = lis_nlogn(nums);
        assert(r1 == 4 && r2 == 4);
        std::cout << "  nums=" << vec_str(nums)
                  << "\n  O(n^2)=" << r1 << "  O(n log n)=" << r2 << "\n\n";
    }

    // 5. Coin Change
    {
        std::cout << "-- Coin Change --\n";
        assert(coin_change({1, 5, 10, 25}, 30) == 2);  // 25+5
        assert(coin_change({2}, 3) == -1);
        std::cout << "  coins={1,5,10,25} amount=30 => " << coin_change({1,5,10,25}, 30) << "\n";
        std::cout << "  coins={2} amount=3 => " << coin_change({2}, 3) << "\n\n";
    }

    // 6. Subset Sum
    {
        std::cout << "-- Subset Sum --\n";
        assert(subset_sum({3, 34, 4, 12, 5, 2}, 9));    // 4+5 or 3+4+2
        assert(!subset_sum({3, 34, 4, 12, 5, 2}, 30));
        std::cout << "  {3,34,4,12,5,2} target=9  => " << std::boolalpha << subset_sum({3,34,4,12,5,2}, 9) << "\n";
        std::cout << "  {3,34,4,12,5,2} target=30 => " << subset_sum({3,34,4,12,5,2}, 30) << "\n\n";
    }

    // 7. Edit Distance
    {
        std::cout << "-- Edit Distance --\n";
        assert(edit_distance("kitten", "sitting") == 3);
        assert(edit_distance("", "abc") == 3);
        assert(edit_distance("abc", "abc") == 0);
        std::cout << "  edit_distance(\"kitten\", \"sitting\") = "
                  << edit_distance("kitten", "sitting") << "\n";
    }

    std::cout << "\nAll Week 18 tests passed.\n";
    return 0;
}
