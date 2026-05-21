# Week 23 — Practice Problems

Topics covered this week: advanced DP — interval DP, bitmask DP, digit DP, DP on trees/grids.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Burst Balloons | Hard | Interval DP | https://leetcode.com/problems/burst-balloons/ | Amazon, Google, Microsoft |
| 2 | Stone Game | Medium | Interval DP / minimax | https://leetcode.com/problems/stone-game/ | Amazon, Google, Common |
| 3 | Longest Increasing Path in a Matrix | Hard | DP + memo on graph | https://leetcode.com/problems/longest-increasing-path-in-a-matrix/ | Common |
| 4 | Cherry Pickup | Hard | Two-walker grid DP | https://leetcode.com/problems/cherry-pickup/ | Amazon, Google, Common |
| 5 | Cherry Pickup II | Hard | 3D DP | https://leetcode.com/problems/cherry-pickup-ii/ | Amazon, Google, Common |
| 6 | Number of Digit One | Hard | Digit DP | https://leetcode.com/problems/number-of-digit-one/ | Common |
| 7 | Find the Shortest Superstring | Hard | Bitmask TSP | https://leetcode.com/problems/find-the-shortest-superstring/ | Common |
| 8 | Minimum Cost to Cut a Stick | Hard | Interval DP | https://leetcode.com/problems/minimum-cost-to-cut-a-stick/ | Common |
| 9 | Partition Array for Maximum Sum | Medium | DP with k-window | https://leetcode.com/problems/partition-array-for-maximum-sum/ | Common |
| 10 | Palindrome Partitioning II | Hard | DP with precomputed palindromes | https://leetcode.com/problems/palindrome-partitioning-ii/ | Amazon, Google, Common |
| 11 | Number of Ways to Wear Different Hats to Each Other | Hard | Bitmask DP | https://leetcode.com/problems/number-of-ways-to-wear-different-hats-to-each-other/ | Common |
| 12 | Travelling Salesman (Shortest Path Visiting All Nodes) | Hard | Bitmask BFS/DP | https://leetcode.com/problems/shortest-path-visiting-all-nodes/ | Common |

## Stretch Problems

Bonus problems for deeper practice:

- [Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) — merge sort or BIT.
- [Profitable Schemes](https://leetcode.com/problems/profitable-schemes/) — 3D knapsack DP.
- [Distinct Subsequences II](https://leetcode.com/problems/distinct-subsequences-ii/) — DP with deduplication.

## Patterns to Master This Week

- Interval DP: iterate by length, then by left endpoint; `dp[l][r] = best over split point k`. Pitfall: choosing the "last move" vs "first move" perspective.
- Bitmask DP: `dp[mask][i]` = state of visited set ending at node i; works up to ~20 nodes. Pitfall: `1 << n` blows up — keep n small.
- Digit DP: state = (position, tight flag, accumulated info). Pitfall: forgetting the tight constraint causes overcount.
