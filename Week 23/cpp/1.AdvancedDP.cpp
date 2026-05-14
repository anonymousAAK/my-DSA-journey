/*
 * WEEK 23 - C++ ADVANCED DSA
 * Topic: Advanced Dynamic Programming (Bitmask, Tree, Digit DP, LIS)
 * File: 1.AdvancedDP.cpp
 *
 * CONCEPT:
 *   Bitmask DP encodes a subset as an integer (n <= ~20).
 *   DP on Trees uses post-order recursion.
 *   Digit DP iterates over digit positions with a "tight" flag.
 *   LIS via patience sorting reaches O(n log n).
 *
 * KEY POINTS:
 *   - For TSP, dp[mask][i] = min cost path covering 'mask' ending at i.
 *   - For tree max-indep-set, dp[u][0/1] track "u not taken" / "u taken".
 *   - Digit DP memoises (pos, tight) when "started"; otherwise recompute.
 *   - LIS uses std::lower_bound on a tails vector.
 *
 * ALGORITHM / APPROACH:
 *   See sibling files; identical recurrences.
 *
 * C++-SPECIFIC NOTES vs JAVA:
 *   - Use INT_MAX/2 sentinel; or explicit large constant.
 *   - std::vector<std::vector<int>> for the dp table.
 *   - Use std::lower_bound for LIS binary search.
 *   - Recursion is fine; switch to iterative DFS for very deep trees.
 *
 * DRY RUN:
 *   TSP for 4-city symmetric matrix in main(): optimal = 80
 *   (route 0 -> 1 -> 3 -> 2 -> 0).
 *   count_no_four(10) -> 9 (skip 4).
 *   LIS([10,9,2,5,3,7,101,18]) -> 4.
 *
 * COMPLEXITY:
 *   TSP:      O(n^2 * 2^n) time, O(n * 2^n) space.
 *   Tree DP:  O(n).
 *   Digit DP: O(D * 10) per state.
 *   LIS:      O(n log n).
 */

#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <algorithm>
#include <climits>
#include <string>
#include <array>

constexpr int INF_HALF = INT_MAX / 2;

int tsp_min_cost(const std::vector<std::vector<int>>& dist) {
    int n = dist.size();
    int FULL = (1 << n) - 1;
    std::vector<std::vector<int>> dp(1 << n, std::vector<int>(n, INF_HALF));
    dp[1][0] = 0;
    for (int mask = 1; mask <= FULL; ++mask) {
        for (int u = 0; u < n; ++u) {
            if (!(mask & (1 << u)) || dp[mask][u] == INF_HALF) continue;
            for (int v = 0; v < n; ++v) {
                if (mask & (1 << v)) continue;
                int nm = mask | (1 << v);
                if (dp[mask][u] + dist[u][v] < dp[nm][v])
                    dp[nm][v] = dp[mask][u] + dist[u][v];
            }
        }
    }
    int ans = INT_MAX;
    for (int u = 1; u < n; ++u)
        if (dp[FULL][u] != INF_HALF)
            ans = std::min(ans, dp[FULL][u] + dist[u][0]);
    return ans;
}

void dfs_tree(int u, const std::vector<int>& weight,
              const std::vector<std::vector<int>>& children,
              std::vector<std::array<int,2>>& dp,
              std::vector<bool>& visited) {
    visited[u] = true;
    dp[u][1] = weight[u];
    dp[u][0] = 0;
    for (int c : children[u]) {
        if (!visited[c]) {
            dfs_tree(c, weight, children, dp, visited);
            dp[u][1] += dp[c][0];
            dp[u][0] += std::max(dp[c][0], dp[c][1]);
        }
    }
}

int max_indep_set(const std::vector<int>& weight, const std::vector<std::vector<int>>& children) {
    int n = weight.size();
    std::vector<std::array<int,2>> dp(n, {0, 0});
    std::vector<bool> visited(n, false);
    dfs_tree(0, weight, children, dp, visited);
    return std::max(dp[0][0], dp[0][1]);
}

// Digit DP: count numbers in [1..N] without digit '4'
static std::vector<std::vector<int>> digitMemo;
static std::string g_num;

int digit_dp(int pos, int tight, int started) {
    int n = (int)g_num.size();
    if (pos == n) return started ? 1 : 0;
    if (!tight && started && digitMemo[pos][0] != -1) return digitMemo[pos][0];
    int limit = tight ? (g_num[pos] - '0') : 9;
    int count = 0;
    for (int d = 0; d <= limit; ++d) {
        if (d == 4) continue;
        count += digit_dp(pos + 1, tight && (d == limit), started || (d != 0));
    }
    if (!tight && started) digitMemo[pos][0] = count;
    return count;
}

int count_no_four(int N) {
    g_num = std::to_string(N);
    digitMemo.assign(g_num.size(), std::vector<int>(2, -1));
    return digit_dp(0, 1, 0);
}

// LIS in O(n log n) via patience sorting
int lis_optimal(const std::vector<int>& nums) {
    std::vector<int> tails;
    for (int x : nums) {
        auto it = std::lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    return (int)tails.size();
}

int main() {
    std::cout << "=== TSP with Bitmask DP ===\n";
    std::vector<std::vector<int>> dist4 = {
        {0,10,15,20},{10,0,35,25},{15,35,0,30},{20,25,30,0}
    };
    std::cout << "TSP (4 cities): " << tsp_min_cost(dist4) << "\n";

    std::cout << "\n=== Max Independent Set on Tree ===\n";
    std::vector<int> weights = {1, 2, 3, 4, 5};
    std::vector<std::vector<int>> children = {{1,2},{3,4},{},{},{}};
    std::cout << "Max weight independent set: " << max_indep_set(weights, children) << "\n";

    std::cout << "\n=== Digit DP: Count numbers without digit 4 ===\n";
    std::cout << "Count in [1..10]:  " << count_no_four(10)  << "\n";
    std::cout << "Count in [1..40]:  " << count_no_four(40)  << "\n";
    std::cout << "Count in [1..100]: " << count_no_four(100) << "\n";

    std::cout << "\n=== LIS O(n log n) ===\n";
    std::vector<std::vector<int>> tests = {
        {10,9,2,5,3,7,101,18}, {0,1,0,3,2,3}, {7,7,7,7,7}
    };
    for (auto& t : tests) {
        std::cout << "[ ";
        for (int v : t) std::cout << v << " ";
        std::cout << "] -> LIS = " << lis_optimal(t) << "\n";
    }
    return 0;
}
