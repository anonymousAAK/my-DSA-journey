/*
 * =============================================================================
 * Week 23 — Advanced Dynamic Programming  (C++17)
 * =============================================================================
 *
 * Topics covered
 * --------------
 *   1. TSP — Travelling Salesman Problem (bitmask DP)
 *   2. Max independent set on a tree (tree DP)
 *   3. Digit DP — count numbers up to N with specific digit properties
 *   4. LIS O(n log n) — patience sorting with std::lower_bound
 *   5. Matrix Chain Multiplication
 *
 * Complexity cheat-sheet
 * ----------------------
 *   tsp_bitmask              O(n^2 * 2^n)   |  Space O(n * 2^n)
 *   max_independent_set      O(V + E)        |  Space O(V)
 *   digit_dp                 O(D * sum * 2)  |  Space O(D * sum * 2)
 *   lis_nlogn                O(n log n)      |  Space O(n)
 *   matrix_chain_mult        O(n^3)          |  Space O(n^2)
 *
 * Build & run
 *   g++ -std=c++17 -O2 -o advanced_dp advanced_dp.cpp && ./advanced_dp
 * =============================================================================
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>
#include <sstream>
#include <climits>
#include <cstring>
#include <functional>
#include <string>
#include <numeric>

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
// 1. TSP — bitmask DP
// ---------------------------------------------------------------------------
// dp[mask][i] = minimum cost to visit all cities in `mask`, ending at city i.
// Start and end at city 0.
// Complexity:  Time O(n^2 * 2^n)  |  Space O(n * 2^n)
int tsp_bitmask(const std::vector<std::vector<int>>& dist) {
    int n = static_cast<int>(dist.size());
    int full = (1 << n) - 1;
    std::vector<std::vector<int>> dp(1 << n, std::vector<int>(n, INT_MAX));

    dp[1][0] = 0;  // start at city 0

    for (int mask = 1; mask <= full; ++mask) {
        for (int u = 0; u < n; ++u) {
            if (dp[mask][u] == INT_MAX) continue;
            if (!(mask & (1 << u))) continue;

            for (int v = 0; v < n; ++v) {
                if (mask & (1 << v)) continue;  // already visited
                int new_mask = mask | (1 << v);
                dp[new_mask][v] = std::min(dp[new_mask][v], dp[mask][u] + dist[u][v]);
            }
        }
    }

    // Return to city 0.
    int ans = INT_MAX;
    for (int u = 1; u < n; ++u) {
        if (dp[full][u] != INT_MAX) {
            ans = std::min(ans, dp[full][u] + dist[u][0]);
        }
    }
    return ans;
}

// ---------------------------------------------------------------------------
// 2. Max Independent Set on a Tree
// ---------------------------------------------------------------------------
// dp[v][0] = max weight independent set in subtree of v, NOT including v
// dp[v][1] = max weight independent set in subtree of v, INCLUDING v
// Complexity:  Time O(V)  |  Space O(V)
int max_independent_set(const std::vector<std::vector<int>>& adj,
                        const std::vector<int>& weights) {
    int n = static_cast<int>(adj.size());
    if (n == 0) return 0;

    std::vector<std::array<int, 2>> dp(n, {0, 0});
    std::vector<bool> visited(n, false);

    std::function<void(int)> dfs = [&](int u) {
        visited[u] = true;
        dp[u][1] = weights[u];

        for (int v : adj[u]) {
            if (visited[v]) continue;
            dfs(v);
            dp[u][0] += std::max(dp[v][0], dp[v][1]);  // u not taken, v can be either
            dp[u][1] += dp[v][0];                        // u taken, v must not be taken
        }
    };

    dfs(0);  // root at 0
    return std::max(dp[0][0], dp[0][1]);
}

// ---------------------------------------------------------------------------
// 3. Digit DP — count integers in [1, N] whose digit sum equals S
// ---------------------------------------------------------------------------
// Complexity:  Time O(D * S * 2)  |  Space O(D * S * 2)
//              D = number of digits in N, S = target sum
long long digit_dp_count(const std::string& num_str, int target_sum) {
    int D = static_cast<int>(num_str.size());
    if (target_sum < 0) return 0;

    // dp[pos][sum][tight]
    // Memoize with -1 as unvisited.
    std::vector<std::vector<std::vector<long long>>> memo(
        D, std::vector<std::vector<long long>>(target_sum + 1, std::vector<long long>(2, -1)));

    std::function<long long(int, int, bool)> solve = [&](int pos, int sum, bool tight) -> long long {
        if (sum > target_sum) return 0;
        if (pos == D) return (sum == target_sum) ? 1 : 0;
        if (memo[pos][sum][tight] != -1) return memo[pos][sum][tight];

        int limit = tight ? (num_str[pos] - '0') : 9;
        long long result = 0;

        for (int d = 0; d <= limit; ++d) {
            result += solve(pos + 1, sum + d, tight && (d == limit));
        }

        return memo[pos][sum][tight] = result;
    };

    // This counts in [0, N] with digit sum = target_sum.
    // Subtract 1 if target_sum == 0 (to exclude 0 itself from [1, N]).
    long long ans = solve(0, 0, true);
    if (target_sum == 0) ans -= 1;
    return ans;
}

// ---------------------------------------------------------------------------
// 4. LIS — O(n log n) with lower_bound (patience sorting)
// ---------------------------------------------------------------------------
// tails[i] = smallest tail of all increasing subsequences of length i+1
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
// 5. Matrix Chain Multiplication
// ---------------------------------------------------------------------------
// Given dimensions p[0..n], matrix i has dimensions p[i] x p[i+1].
// Find minimum scalar multiplications needed.
// dp[i][j] = min cost to multiply matrices i..j
// Complexity:  Time O(n^3)  |  Space O(n^2)
long long matrix_chain_mult(const std::vector<int>& p) {
    int n = static_cast<int>(p.size()) - 1;  // number of matrices
    if (n <= 1) return 0;

    std::vector<std::vector<long long>> dp(n, std::vector<long long>(n, 0));

    // l = chain length
    for (int l = 2; l <= n; ++l) {
        for (int i = 0; i <= n - l; ++i) {
            int j = i + l - 1;
            dp[i][j] = LLONG_MAX;
            for (int k = i; k < j; ++k) {
                long long cost = dp[i][k] + dp[k + 1][j]
                               + (long long)p[i] * p[k + 1] * p[j + 1];
                dp[i][j] = std::min(dp[i][j], cost);
            }
        }
    }
    return dp[0][n - 1];
}

// ---------------------------------------------------------------------------
// main — test cases
// ---------------------------------------------------------------------------
int main() {
    std::cout << "=== Week 23: Advanced DP ===\n\n";

    // 1. TSP bitmask DP
    {
        std::cout << "-- TSP (bitmask DP) --\n";
        std::vector<std::vector<int>> dist = {
            {0, 10, 15, 20},
            {10,  0, 35, 25},
            {15, 35,  0, 30},
            {20, 25, 30,  0}
        };
        int ans = tsp_bitmask(dist);
        std::cout << "  min tour cost: " << ans << "\n";
        assert(ans == 80);  // 0->1(10)->3(25)->2(30)->0(15) = 80
        std::cout << "\n";
    }

    // 2. Max Independent Set on Tree
    {
        std::cout << "-- Max Independent Set (Tree DP) --\n";
        //       0(w=1)
        //      / \
        //    1(10) 2(5)
        //    /
        //  3(8)
        std::vector<std::vector<int>> adj = {
            {1, 2},   // 0's neighbors
            {0, 3},   // 1's neighbors
            {0},      // 2's neighbors
            {1}       // 3's neighbors
        };
        std::vector<int> weights = {1, 10, 5, 8};
        int mis = max_independent_set(adj, weights);
        std::cout << "  max independent set weight: " << mis << "\n";
        // Take nodes 1 and 2: 10+5=15  (can't take 0 with 1 or 2; can't take 3 with 1)
        // Or take 0, 3: 1+8=9
        // Or take 2, 3: 5+8=13
        // Best: take 1 and 2 = 15? But 1 and 2 are both children of 0, they are independent.
        assert(mis == 15);
        std::cout << "\n";
    }

    // 3. Digit DP
    {
        std::cout << "-- Digit DP --\n";
        // Count integers in [1, 100] with digit sum = 5
        // 5, 14, 23, 32, 41, 50 => 6 numbers
        long long cnt = digit_dp_count("100", 5);
        assert(cnt == 6);
        std::cout << "  numbers in [1,100] with digit sum 5: " << cnt << "\n";

        // Count in [1, 20] with digit sum = 3: 3, 12 => 2
        long long cnt2 = digit_dp_count("20", 3);
        assert(cnt2 == 2);
        std::cout << "  numbers in [1,20] with digit sum 3:  " << cnt2 << "\n\n";
    }

    // 4. LIS O(n log n)
    {
        std::cout << "-- LIS O(n log n) --\n";
        std::vector<int> nums = {10, 9, 2, 5, 3, 7, 101, 18};
        int len = lis_nlogn(nums);
        assert(len == 4);
        std::cout << "  nums=" << vec_str(nums) << "  LIS=" << len << "\n";

        std::vector<int> nums2 = {0, 1, 0, 3, 2, 3};
        int len2 = lis_nlogn(nums2);
        assert(len2 == 4);  // 0,1,2,3
        std::cout << "  nums=" << vec_str(nums2) << "  LIS=" << len2 << "\n\n";
    }

    // 5. Matrix Chain Multiplication
    {
        std::cout << "-- Matrix Chain Multiplication --\n";
        // Matrices: A1(10x30), A2(30x5), A3(5x60)
        // Optimal: (A1*A2)*A3 = 10*30*5 + 10*5*60 = 1500 + 3000 = 4500
        std::vector<int> p = {10, 30, 5, 60};
        auto cost = matrix_chain_mult(p);
        assert(cost == 4500);
        std::cout << "  dims=" << vec_str(p) << "  min cost=" << cost << "\n";

        // Matrices: A1(40x20), A2(20x30), A3(30x10), A4(10x30)
        std::vector<int> p2 = {40, 20, 30, 10, 30};
        auto cost2 = matrix_chain_mult(p2);
        assert(cost2 == 26000);
        std::cout << "  dims=" << vec_str(p2) << "  min cost=" << cost2 << "\n";
    }

    std::cout << "\nAll Week 23 tests passed.\n";
    return 0;
}
