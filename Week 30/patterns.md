# Week 30 — Pattern Recognition Drills (Final Recap)

These problems span the whole curriculum. For each, identify which pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key — the hardest test of pattern recognition is when you don't know which week the problem comes from.

## Drills

### 1. Given a stream of `(timestamp, userId, eventType)` records and the question "how many distinct users in the past 5 minutes?", answer in sub-millisecond using a few KB of memory.
Pattern: ______
Why: ______

### 2. Given `n ≤ 10^5` intervals and `q ≤ 10^5` point queries, return for each point the count of intervals covering it.
Pattern: ______
Why: ______

### 3. Given an array of `n ≤ 2·10^5` integers, find the length of the longest subarray with at most two distinct values.
Pattern: ______
Why: ______

### 4. Given a list of words `w_1, …, w_n` (n ≤ 10^4) and an integer `k`, decide whether you can pick `k` words such that no two share a letter.
Pattern: ______
Why: ______

### 5. Given an `n × n` grid with some cells blocked, find the number of distinct paths from top-left to bottom-right moving only right/down. n ≤ 100.
Pattern: ______
Why: ______

### 6. Given a graph of `n ≤ 10^5` nodes with edges weighted by `0` or `1`, find the shortest path from `s` to `t`.
Pattern: ______
Why: ______

### 7. Given a stream of integers, after each insertion answer: "how many distinct values have been seen exactly once so far?"
Pattern: ______
Why: ______

### 8. Given `n ≤ 16` cities with pairwise distances, find the minimum tour visiting every city exactly once.
Pattern: ______
Why: ______

### 9. Distractor: Given a sorted array of n ≤ 10^6 integers, find a pair summing to `T`. (Several patterns fit — pick the cleanest.)
Pattern: ______
Why: ______

### 10. Given a list of `n ≤ 10^5` API endpoints and a stream of `q ≤ 10^7` calls, design an allow-list check that returns "matches the longest registered prefix" per call in under a microsecond.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: HyperLogLog over a sliding window (or sliding HLL). **Why**: probabilistic cardinality + window-expiry buckets. Week 29.
2. **Pattern**: Difference array + prefix sum (offline) — or sweep line. **Why**: convert each interval to +1 at `l`, −1 at `r+1`, prefix-sum at query points. Weeks 6/21.
3. **Pattern**: Sliding window with frequency map. **Why**: expand right; shrink left while distinct > 2. Weeks 7/13.
4. **Pattern**: Bitmask DP on letter sets. **Why**: each word → 26-bit mask; pick k pairwise-disjoint masks → bitmask DP `dp[mask] = max words usable from disjoint subsets of letters`. Week 23.
5. **Pattern**: Grid DP. **Why**: `dp[i][j] = dp[i-1][j] + dp[i][j-1]` if cell unblocked. Week 18.
6. **Pattern**: 0-1 BFS with a deque. **Why**: edges of weight 0 go to deque front, weight 1 to back — O(V+E). Weeks 13/22.
7. **Pattern**: HashMap of counts + a counter "distinct-with-count-1". **Why**: update counter as each count crosses 1. Week 16.
8. **Pattern**: Held–Karp bitmask DP (TSP). **Why**: state `(mask, last)`; 2^n · n^2 ≈ 1.7·10^7 — fine at n=16. Week 23.
9. **Pattern**: Two pointers — cleanest. **Why**: O(n) with O(1) space beats hashing (O(n) extra) and binary search (O(n log n)). Disambiguation across Weeks 6/8/16.
10. **Pattern**: Trie longest-prefix lookup. **Why**: O(L) per query (L = url length); independent of n. Week 21.

</details>
