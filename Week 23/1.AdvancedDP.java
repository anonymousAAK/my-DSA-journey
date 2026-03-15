/*
 * WEEK 23 - ADVANCED DYNAMIC PROGRAMMING
 * Topic: Bitmask DP, DP on Trees, Digit DP
 *
 * =========================================
 * BITMASK DP
 * =========================================
 * Use an integer's bits to represent a SUBSET of elements.
 * Bit i = 1 means element i is in the subset; 0 means it's not.
 *
 * Useful when n ≤ 20 (2^20 ≈ 1M subsets is manageable).
 *
 * CLASSIC PROBLEM: Traveling Salesman Problem (TSP)
 * Find shortest Hamiltonian cycle visiting all n cities exactly once.
 * dp[mask][i] = shortest path visiting all cities in 'mask', ending at city i.
 * Time: O(2^n * n²), Space: O(2^n * n)
 *
 * =========================================
 * DP ON TREES
 * =========================================
 * Compute DP values for tree nodes where subproblem = subtree.
 * Standard pattern: post-order DFS.
 *
 * CLASSIC: Maximum Independent Set on a Tree
 * No two adjacent nodes can both be selected.
 * dp[node][0] = max sum if node is NOT selected
 * dp[node][1] = max sum if node IS selected
 *
 * =========================================
 * DIGIT DP
 * =========================================
 * Count numbers in range [lo, hi] satisfying some property.
 * Build number digit by digit, maintaining constraints.
 * State: (position, tight, started, ..property state..)
 * "Tight" = true means current prefix exactly matches the limit.
 *
 * CLASSIC: Count numbers in [1, N] that don't contain digit 4.
 */

import java.util.Arrays;

public class AdvancedDP {

    // =====================
    // TSP WITH BITMASK DP
    // =====================
    static int tspMinCost(int[][] dist) {
        int n = dist.length;
        int FULL = (1 << n) - 1;
        int[][] dp = new int[1 << n][n];
        for (int[] row : dp) Arrays.fill(row, Integer.MAX_VALUE / 2);
        dp[1][0] = 0; // start at city 0

        for (int mask = 1; mask <= FULL; mask++) {
            for (int u = 0; u < n; u++) {
                if ((mask & (1 << u)) == 0 || dp[mask][u] == Integer.MAX_VALUE / 2) continue;
                for (int v = 0; v < n; v++) {
                    if ((mask & (1 << v)) != 0) continue; // v already visited
                    int newMask = mask | (1 << v);
                    dp[newMask][v] = Math.min(dp[newMask][v], dp[mask][u] + dist[u][v]);
                }
            }
        }

        int ans = Integer.MAX_VALUE;
        for (int u = 1; u < n; u++) {
            if (dp[FULL][u] != Integer.MAX_VALUE / 2)
                ans = Math.min(ans, dp[FULL][u] + dist[u][0]); // return to city 0
        }
        return ans;
    }

    // =====================
    // MAXIMUM INDEPENDENT SET ON TREE
    // =====================
    static int maxIndepSet(int[] weight, int[][] children) {
        int n = weight.length;
        int[][] dp = new int[n][2]; // dp[i][0/1]
        // Post-order DFS
        dfsTree(0, weight, children, dp, new boolean[n]);
        return Math.max(dp[0][0], dp[0][1]);
    }

    static void dfsTree(int node, int[] weight, int[][] children, int[][] dp, boolean[] visited) {
        visited[node] = true;
        dp[node][1] = weight[node]; // take this node
        dp[node][0] = 0;           // don't take this node
        for (int child : children[node]) {
            if (!visited[child]) {
                dfsTree(child, weight, children, dp, visited);
                dp[node][1] += dp[child][0]; // if we take node, children can't be taken
                dp[node][0] += Math.max(dp[child][0], dp[child][1]); // if we don't take, children can go either way
            }
        }
    }

    // =====================
    // DIGIT DP — Count numbers in [1..N] with no digit '4'
    // =====================
    static int[][] digitMemo;

    static int countNoFour(int N) {
        String num = Integer.toString(N);
        int n = num.length();
        digitMemo = new int[n][2]; // [position][tight]
        for (int[] row : digitMemo) Arrays.fill(row, -1);
        return digitDP(num, 0, true, false);
    }

    // pos: current digit position
    // tight: are we still constrained by N's digits?
    // started: have we placed a non-zero digit yet?
    static int digitDP(String num, int pos, boolean tight, boolean started) {
        if (pos == num.length()) return started ? 1 : 0;
        int key = pos * 2 + (tight ? 1 : 0);
        if (!tight && started && digitMemo[pos][tight ? 1 : 0] != -1)
            return digitMemo[pos][tight ? 1 : 0];

        int limit = tight ? (num.charAt(pos) - '0') : 9;
        int count = 0;
        for (int d = 0; d <= limit; d++) {
            if (d == 4) continue; // skip digit 4
            count += digitDP(num, pos + 1, tight && (d == limit), started || (d != 0));
        }
        if (!tight && started) digitMemo[pos][0] = count;
        return count;
    }

    // Longest Increasing Subsequence (LIS) with O(n log n) patience sorting
    static int lisOptimal(int[] nums) {
        int[] tails = new int[nums.length];
        int size = 0;
        for (int x : nums) {
            // Binary search for position to place x
            int lo = 0, hi = size;
            while (lo < hi) {
                int mid = (lo + hi) / 2;
                if (tails[mid] < x) lo = mid + 1;
                else hi = mid;
            }
            tails[lo] = x;
            if (lo == size) size++;
        }
        return size;
    }

    public static void main(String[] args) {
        // TSP
        System.out.println("=== TSP with Bitmask DP ===");
        int[][] dist4 = {
            {0, 10, 15, 20},
            {10, 0, 35, 25},
            {15, 35, 0, 30},
            {20, 25, 30, 0}
        };
        System.out.println("TSP (4 cities): " + tspMinCost(dist4)); // 80

        // Max Independent Set on Tree
        System.out.println("\n=== Max Independent Set on Tree ===");
        // Tree: 0-1, 0-2, 1-3, 1-4
        // Weights: [1, 2, 3, 4, 5]
        int[] weights = {1, 2, 3, 4, 5};
        int[][] children = {{1, 2}, {3, 4}, {}, {}, {}};
        System.out.println("Max weight independent set: " + maxIndepSet(weights, children));
        // Taking {0,3,4}: 1+4+5=10 or {2,1}: 3+2=5 or {2,3,4}: 3+4+5=12
        // Correct: take {2,3,4} = 12? Let's see: 3 is child of 0, 4 is child of 1
        // {2,3,4}: 2 is child of 0, 3 is child of 1, 4 is child of 1
        // Can't take both 1 and 3,4. Can take {0 excluded, 1 included} + {2,0 excluded children}

        // Digit DP
        System.out.println("\n=== Digit DP: Count numbers without digit 4 ===");
        System.out.println("Count in [1..10]:  " + countNoFour(10));   // 9 (all but 4)
        System.out.println("Count in [1..40]:  " + countNoFour(40));
        System.out.println("Count in [1..100]: " + countNoFour(100));

        // LIS optimal
        System.out.println("\n=== LIS O(n log n) ===");
        int[][] tests = {{10,9,2,5,3,7,101,18},{0,1,0,3,2,3},{7,7,7,7,7}};
        for (int[] t : tests)
            System.out.println(Arrays.toString(t) + " → LIS = " + lisOptimal(t));
        // 4, 4, 1
    }
}
