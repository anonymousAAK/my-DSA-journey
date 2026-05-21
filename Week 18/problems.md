# Week 18 — Practice Problems

Topics covered this week: dynamic programming, memoization vs tabulation, 1D/2D DP, classic recurrences.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Climbing Stairs | Easy | 1D DP | https://leetcode.com/problems/climbing-stairs/ | Amazon, Apple, Google, Adobe |
| 2 | House Robber | Medium | Linear DP | https://leetcode.com/problems/house-robber/ | Amazon, LinkedIn, Apple |
| 3 | House Robber II | Medium | Circular DP | https://leetcode.com/problems/house-robber-ii/ | Amazon, Microsoft, Apple |
| 4 | Coin Change | Medium | Unbounded knapsack | https://leetcode.com/problems/coin-change/ | Amazon, Meta, Microsoft, Google |
| 5 | Longest Increasing Subsequence | Medium | DP / patience sort | https://leetcode.com/problems/longest-increasing-subsequence/ | Amazon, Microsoft, Google, Meta |
| 6 | Edit Distance | Hard | 2D DP | https://leetcode.com/problems/edit-distance/ | Amazon, Meta, Microsoft, Google |
| 7 | Word Break | Medium | DP on strings | https://leetcode.com/problems/word-break/ | Amazon, Meta, Microsoft, Google |
| 8 | Unique Paths | Medium | Grid DP | https://leetcode.com/problems/unique-paths/ | Amazon, Apple, Google, Bloomberg |
| 9 | Longest Common Subsequence | Medium | 2D DP | https://leetcode.com/problems/longest-common-subsequence/ | Amazon, Microsoft, Google |
| 10 | Partition Equal Subset Sum | Medium | 0/1 knapsack | https://leetcode.com/problems/partition-equal-subset-sum/ | Amazon, Apple, Common |
| 11 | Maximum Product Subarray | Medium | DP with two states | https://leetcode.com/problems/maximum-product-subarray/ | Amazon, LinkedIn, Microsoft |
| 12 | Decode Ways | Medium | String DP | https://leetcode.com/problems/decode-ways/ | Common |

## Stretch Problems

Bonus problems for deeper practice:

- [Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) — multi-state DP.
- [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) — DP with wildcards.
- [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) — string DP counting.

## Patterns to Master This Week

- Memoization (top-down): recursive + cache by parameters. Pitfall: hashing complex keys; consider arrays.
- Tabulation (bottom-up): iterate states in dependency order; usually faster and stack-safe. Pitfall: initializing base row/column.
- Space-optimize 2D → rolling 1D when only previous row is needed. Pitfall: order of iteration affects correctness for 0/1 vs unbounded knapsack.
