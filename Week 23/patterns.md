# Week 23 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which advanced-DP pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given n ≤ 20 cities with pairwise distances, find the shortest tour visiting each city exactly once and returning to start.
Pattern: ______
Why: ______

### 2. Given n ≤ 20 tasks each requiring a subset of resources, decide whether you can schedule them on two machines with equal total time.
Pattern: ______
Why: ______

### 3. Count the integers in `[L, R]` (up to 10^18) whose decimal digit sum is divisible by 7.
Pattern: ______
Why: ______

### 4. Count the integers in `[0, N]` (N up to 10^18) whose decimal representation contains no two adjacent equal digits.
Pattern: ______
Why: ______

### 5. Given a tree of n ≤ 10^5 nodes with values, choose a subset of non-adjacent nodes maximizing the sum of values.
Pattern: ______
Why: ______

### 6. Given a tree, find for every node the sum of distances to all other nodes. n ≤ 10^4.
Pattern: ______
Why: ______

### 7. Distractor: Given an array of n ≤ 10^6 integers, find the maximum subarray sum. (Bitmask DP?)
Pattern: ______
Why: ______

### 8. Given n ≤ 16 jobs and m ≤ 16 workers, each `cost[i][j]` known, find the minimum-cost assignment where every job goes to exactly one worker.
Pattern: ______
Why: ______

### 9. Given a tree with n ≤ 10^5 nodes, root it at node 1 and for each node count the size of its subtree.
Pattern: ______
Why: ______

### 10. Distractor: Given a directed graph with n ≤ 18, find any Hamiltonian path. (Backtracking only?)
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Held–Karp bitmask DP. **Why**: state `(mask, last)`; 2^n · n^2 — fits at n=20.
2. **Pattern**: Subset-sum bitmask DP / meet-in-the-middle. **Why**: enumerate subsets of tasks with running sum.
3. **Pattern**: Digit DP. **Why**: classify by position + carry-of-digit-sum mod 7 + tight flag.
4. **Pattern**: Digit DP. **Why**: state `(pos, prevDigit, tight)`.
5. **Pattern**: DP on trees ("tree rob"). **Why**: each node's answer = max(include + Σ excluded children, exclude + Σ best children).
6. **Pattern**: Tree rerooting DP. **Why**: compute subtree sums in O(n), then re-root in O(n).
7. **Pattern**: Distractor — Kadane (Week 6/18). **Why**: no bitmask needed; plain linear DP.
8. **Pattern**: Bitmask DP — assignment problem. **Why**: `dp[mask]` = best cost assigning first popcount(mask) jobs using workers in mask.
9. **Pattern**: Tree DFS post-order. **Why**: trivial DP on trees — subtree size = 1 + Σ children sizes.
10. **Pattern**: Bitmask DP (Hamiltonian existence). **Why**: 2^n · n is feasible at n=18; backtracking alone risks TLE.

</details>
