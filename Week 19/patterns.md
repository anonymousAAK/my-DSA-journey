# Week 19 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which greedy pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given a set of intervals `[s_i, e_i]`, find the maximum number of mutually non-overlapping intervals you can select. n ≤ 10^5.
Pattern: ______
Why: ______

### 2. Given a list of gas stations on a circular route, each with `gas[i]` available and `cost[i]` to reach the next, find the starting index from which you can complete the loop.
Pattern: ______
Why: ______

### 3. Given an array of non-negative integers where each value is the max jump length from that index, decide if you can reach the last index starting from index 0.
Pattern: ______
Why: ______

### 4. Given an array of meeting `(start, end)` intervals, find the minimum number of rooms needed so that no two overlapping meetings share a room.
Pattern: ______
Why: ______

### 5. Given a list of jobs each with deadline and profit, schedule the subset of one-unit jobs to maximize profit (one machine, integer time).
Pattern: ______
Why: ______

### 6. Distractor: Given a list of intervals with associated weights, find the maximum-weight subset of non-overlapping intervals. (Greedy?)
Pattern: ______
Why: ______

### 7. Given a string, find the lexicographically smallest result after deleting exactly k characters. n ≤ 10^5.
Pattern: ______
Why: ______

### 8. Given n coins and a target sum using only denominations `1, 5, 10, 25, 100`, find the minimum number of coins. Amount ≤ 10^6.
Pattern: ______
Why: ______

### 9. Distractor: Given arbitrary coin denominations and a target sum, find the minimum number of coins. (Same as 8?)
Pattern: ______
Why: ______

### 10. Given two strings `s` and `t`, return the minimum number of characters to append to `s` so that `t` is a subsequence of the result.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Earliest-end-time greedy. **Why**: sort by end, always pick next compatible — proven optimal by exchange argument.
2. **Pattern**: One-pass greedy with running tank. **Why**: if `sum(gas-cost) ≥ 0`, the station after the lowest cumulative deficit is the start.
3. **Pattern**: Greedy max-reach. **Why**: track furthest reachable so far; fail if `i > maxReach`.
4. **Pattern**: Sweep-line on starts/ends, or sort + min-heap of ends (Week 15). **Why**: at each start, reuse a room if earliest end ≤ start.
5. **Pattern**: Sort by profit + greedy slot assignment (or union-find). **Why**: place each job in its latest free slot ≤ deadline.
6. **Pattern**: Distractor — DP, not greedy (Week 18). **Why**: with weights, greedy by end is not optimal; needs weighted interval scheduling DP.
7. **Pattern**: Monotonic stack greedy. **Why**: pop larger characters from the stack while removals remain — builds lex-smallest result.
8. **Pattern**: Greedy from largest denomination. **Why**: canonical (US-like) coin systems satisfy the matroid property — greedy is optimal.
9. **Pattern**: Distractor — DP (Week 18 coin change). **Why**: arbitrary denominations can break greedy (e.g., {1,3,4} for 6). This is the disambiguation.
10. **Pattern**: Two-pointer greedy subsequence match. **Why**: walk both strings, advance `t` only on match; remaining suffix of `t` is the answer length.

</details>
