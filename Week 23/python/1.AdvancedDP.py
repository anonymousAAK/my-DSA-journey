"""
WEEK 23 - PYTHON ADVANCED DSA
Topic: Advanced Dynamic Programming (Bitmask, DP on Trees, Digit DP, LIS)
File: 1.AdvancedDP.py

CONCEPT:
    Three families of harder DP, plus an O(n log n) LIS.
        Bitmask DP:  state encodes a subset of n items as an integer.
        DP on Trees: post-order recursion; subproblem = subtree of node.
        Digit DP:    count numbers in [1..N] with property P, building
                     digit by digit while tracking a "tight" flag.

KEY POINTS:
    - Bitmask DP works when n <= ~20 because 2^n states are tractable.
    - For tree DP, dp[u][0/1] often distinguishes "u not taken / taken".
    - Digit DP state = (pos, tight, started, ...property-specific flags).
    - LIS via patience sorting: maintain `tails[i]` = smallest end value of
      any increasing subsequence of length i+1; size grows monotonically.

ALGORITHM / APPROACH:
    TSP (bitmask DP):
        dp[mask][i] = min cost path visiting exactly cities in mask, ending at i
        dp[1][0] = 0; for each mask, for each u in mask, for each v not in
                                 mask: dp[mask|1<<v][v] = min(..., dp[mask][u] + dist[u][v])
        answer = min over u: dp[FULL][u] + dist[u][0]

    Max Independent Set (Tree):
        post-order; dp[u][1] = w[u] + sum(dp[c][0]); dp[u][0] = sum(max(dp[c][0],dp[c][1]))

    Digit DP (count numbers 1..N without digit '4'):
        recursion on (pos, tight, started); memo on (pos, tight) when not started

    LIS in O(n log n):
        for x in nums: bisect_left(tails, x); replace tails[idx] with x;
        if idx == len(tails): tails.append(x).

PYTHON-SPECIFIC NOTES vs JAVA:
    - Use functools.lru_cache for memoised digit DP — cleaner than manual table.
    - bisect.bisect_left implements the LIS binary search.
    - Avoid recursion-depth issues by raising sys.setrecursionlimit if needed.

DRY RUN:
    TSP on 4 cities with the matrix in main(): optimal cost = 80.
    Tree weights [1,2,3,4,5], children {0:[1,2],1:[3,4]}:
        dp[2]=[0,3], dp[3]=[0,4], dp[4]=[0,5]
        dp[1] = [0+max(0,4)+max(0,5), 2+0+0] = [9, 2]
        dp[0] = [max(9,2)+max(0,3), 1 + min taken of (1) + min taken of (2)]
              = [9+3, 1 + 9_no? ] ... see code for exact reproduction
    Digit DP: count_no_four(10) = 9 (skip 4); count_no_four(40) skips 4,14,24,34,40 -> 35.
    LIS([10,9,2,5,3,7,101,18]) -> 4 (e.g., 2,3,7,101).

COMPLEXITY:
    TSP:      O(n^2 * 2^n)
    Tree DP:  O(n)
    Digit DP: O(D * 10) per state; states = O(D * states_of_extra_flags)
    LIS:      O(n log n)
"""

from __future__ import annotations
from typing import List, Tuple
from functools import lru_cache
import bisect


# ---------- TSP via Bitmask DP ----------
def tsp_min_cost(dist: List[List[int]]) -> int:
    n = len(dist)
    FULL = (1 << n) - 1
    INF = 10 ** 18
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0

    for mask in range(1, 1 << n):
        for u in range(n):
            if not (mask & (1 << u)) or dp[mask][u] == INF:
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                cand = dp[mask][u] + dist[u][v]
                if cand < dp[new_mask][v]:
                    dp[new_mask][v] = cand

    ans = INF
    for u in range(1, n):
        if dp[FULL][u] + dist[u][0] < ans:
            ans = dp[FULL][u] + dist[u][0]
    return ans


# ---------- Maximum Independent Set on Tree ----------
def max_indep_set(weight: List[int], children: List[List[int]]) -> int:
    n = len(weight)
    dp = [[0, 0] for _ in range(n)]
    visited = [False] * n

    def dfs(u: int) -> None:
        visited[u] = True
        dp[u][1] = weight[u]
        dp[u][0] = 0
        for c in children[u]:
            if not visited[c]:
                dfs(c)
                dp[u][1] += dp[c][0]
                dp[u][0] += max(dp[c][0], dp[c][1])

    dfs(0)
    return max(dp[0][0], dp[0][1])


# ---------- Digit DP: count integers in [1..N] without digit '4' ----------
def count_no_four(N: int) -> int:
    digits = list(map(int, str(N)))
    L = len(digits)

    @lru_cache(maxsize=None)
    def rec(pos: int, tight: bool, started: bool) -> int:
        if pos == L:
            return 1 if started else 0
        limit = digits[pos] if tight else 9
        total = 0
        for d in range(0, limit + 1):
            if d == 4:
                continue
            total += rec(pos + 1, tight and (d == limit), started or (d != 0))
        return total

    return rec(0, True, False)


# ---------- Longest Increasing Subsequence (O(n log n)) ----------
def lis_optimal(nums: List[int]) -> int:
    tails: List[int] = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def main() -> None:
    print("=== TSP with Bitmask DP ===")
    dist4 = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    print("TSP (4 cities):", tsp_min_cost(dist4))  # 80

    print("\n=== Max Independent Set on Tree ===")
    weights = [1, 2, 3, 4, 5]
    children = [[1, 2], [3, 4], [], [], []]
    print("Max weight independent set:", max_indep_set(weights, children))

    print("\n=== Digit DP: Count numbers without digit 4 ===")
    print("Count in [1..10]: ", count_no_four(10))
    print("Count in [1..40]: ", count_no_four(40))
    print("Count in [1..100]:", count_no_four(100))

    print("\n=== LIS O(n log n) ===")
    for t in ([10, 9, 2, 5, 3, 7, 101, 18], [0, 1, 0, 3, 2, 3], [7, 7, 7, 7, 7]):
        print(t, "-> LIS =", lis_optimal(t))


if __name__ == "__main__":
    main()
