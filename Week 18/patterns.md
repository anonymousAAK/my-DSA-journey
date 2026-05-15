# Week 18 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which DP pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. You can climb a staircase of n steps taking 1 or 2 at a time. How many distinct ways are there to reach the top? n ≤ 10^4.
Pattern: ______
Why: ______

### 2. Given n items each with weight `w_i` and value `v_i` and a knapsack capacity W, choose a subset maximizing total value subject to total weight ≤ W. Each item at most once. n, W ≤ 10^3.
Pattern: ______
Why: ______

### 3. Given an array of n ≤ 10^4 integers, find the length of the longest strictly increasing subsequence.
Pattern: ______
Why: ______

### 4. Given two strings of lengths up to 10^3, compute the minimum number of single-character insert/delete/substitute operations to transform one into the other.
Pattern: ______
Why: ______

### 5. Given coin denominations and a target amount, count the number of distinct ways to make the amount (order doesn't matter). Amount ≤ 5·10^3.
Pattern: ______
Why: ______

### 6. Given an `m × n` grid of non-negative costs, find the minimum-cost path from top-left to bottom-right, moving only right or down. m, n ≤ 10^3.
Pattern: ______
Why: ______

### 7. Distractor: Given an array, find the maximum-sum contiguous subarray. (Is this DP?)
Pattern: ______
Why: ______

### 8. Given a string of length n ≤ 500, find the length of the longest palindromic subsequence (not necessarily contiguous).
Pattern: ______
Why: ______

### 9. Given an array of house values arranged in a row, choose a non-adjacent subset maximizing total value (House Robber). n ≤ 10^5.
Pattern: ______
Why: ______

### 10. Distractor: Given a set of intervals with start, end, and weight, choose the weighted subset of non-overlapping intervals maximizing total weight. n ≤ 10^5. (Greedy or DP?)
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: 1-D DP / Fibonacci recurrence. **Why**: `ways(n) = ways(n-1) + ways(n-2)`.
2. **Pattern**: 0/1 knapsack DP. **Why**: 2-D state `(item, capacity)`; choose vs skip.
3. **Pattern**: LIS — O(n²) DP or O(n log n) patience. **Why**: at each index, length = 1 + max over predecessors with smaller value.
4. **Pattern**: Edit distance DP. **Why**: 2-D state on prefix lengths; three transitions for insert/delete/substitute.
5. **Pattern**: Unbounded knapsack (coin change ways). **Why**: outer loop over coins, inner over amount — ensures combinations not permutations.
6. **Pattern**: Grid DP. **Why**: `dp[i][j] = cost + min(dp[i-1][j], dp[i][j-1])`.
7. **Pattern**: Kadane / 1-D DP collapsed. **Why**: yes, DP — `dp[i] = max(a[i], dp[i-1]+a[i])`; recognize Kadane *is* DP.
8. **Pattern**: Interval DP on `(i, j)`. **Why**: `lps(i,j) = 2 + lps(i+1,j-1)` if matching, else max of dropping an end.
9. **Pattern**: Linear DP with two-state recurrence. **Why**: `dp[i] = max(dp[i-1], dp[i-2] + a[i])`.
10. **Pattern**: Weighted interval scheduling — DP with binary search (NOT pure greedy). **Why**: greedy by end works only when weights are equal; with weights, sort by end + `dp[i] = max(dp[i-1], w_i + dp[p(i)])`.

</details>
