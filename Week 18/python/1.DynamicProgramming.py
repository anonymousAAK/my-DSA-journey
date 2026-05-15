"""
WEEK 18 - PYTHON DSA
Topic: Dynamic Programming Fundamentals
File: 1.DynamicProgramming.py

CONCEPT:
    Dynamic Programming solves a problem by breaking it into overlapping
    subproblems, solving each subproblem ONCE, and storing the answer.
    Two preconditions:
        1. Optimal substructure: optimal answer is built from optimal sub-answers.
        2. Overlapping subproblems: the same sub-call appears many times.

    Two implementation styles:
        TOP-DOWN  (memoization) - recursion + cache. Easy to derive from the
                                  natural recurrence; we use functools.cache.
        BOTTOM-UP (tabulation)  - fill a table from smallest to largest.
                                  Usually faster (no recursion / hash overhead);
                                  often allows space optimisations.

KEY POINTS:
    - Identify the STATE (parameters that uniquely identify a subproblem).
    - Write the RECURRENCE: dp[state] in terms of smaller states.
    - Establish the BASE CASE.
    - Decide ORDER OF EVALUATION (so dependencies are solved first).
    - Optimise SPACE if only the previous row(s) are needed.

ALGORITHM / APPROACH:
    Five canonical problems are covered:
        1. 0/1 Knapsack             (2-D DP, then 1-D space-optimised)
        2. Longest Common Subseq.   (2-D DP)
        3. Coin Change (min coins)  (unbounded coin DP)
        4. Subset Sum               (boolean DP)
        5. Climbing Stairs          (Fibonacci-style)

PYTHON-SPECIFIC NOTES:
    - `@functools.cache` (Py 3.9+) auto-memoises pure recursive functions.
    - List comprehensions like `[[0]*(W+1) for _ in range(n+1)]` build 2-D tables.
    - `math.inf` is a clean sentinel for "impossible".
    - Use `tuple` (not `list`) as cache keys when needed (lists aren't hashable).
    - Type hints from `typing` (List, Sequence, Optional) keep intent clear.

DRY RUN:
    Knapsack with weights=[2,3,4,5], values=[3,4,5,6], W=5
        dp table (rows = items 0..4, cols = capacities 0..5):
                 c=0 1 2 3 4 5
            i=0:   0 0 0 0 0 0
            i=1:   0 0 3 3 3 3        (item w=2,v=3)
            i=2:   0 0 3 4 4 7        (item w=3,v=4 ; dp[1][2]+4=7 at c=5)
            i=3:   0 0 3 4 5 7        (item w=4,v=5)
            i=4:   0 0 3 4 5 7        (item w=5,v=6 doesn't beat 7)
        Answer dp[4][5] = 7.

    LCS("ABCBDAB","BDCABA")
        Builds 7x6 table; final dp[7][6] = 4.
        Possible LCS strings: "BCBA", "BDAB".

    Coin change coins=[1,2,5], target=11:
        dp[0..11] starts with 0,inf,inf,...
        dp[1]=1, dp[2]=1, dp[3]=2, dp[4]=2, dp[5]=1, dp[6]=2,
        dp[7]=2, dp[8]=3, dp[9]=3, dp[10]=2, dp[11]=3.

COMPLEXITY:
    knapsack          O(n*W) time, O(n*W) space  (O(W) optimised)
    lcs               O(m*n) time, O(m*n) space
    coin_change       O(target * |coins|) time, O(target) space
    subset_sum        O(n * target) time, O(target) space
    climb_stairs      O(n) time, O(1) space
"""

from __future__ import annotations
import functools
import math
from typing import List, Sequence


# ---------------- 0/1 KNAPSACK ----------------
def knapsack(weights: Sequence[int], values: Sequence[int], W: int) -> int:
    """Bottom-up 2-D table; dp[i][w] = best value using first i items, capacity w."""
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wi, vi = weights[i - 1], values[i - 1]
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]
            if wi <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - wi] + vi)
    return dp[n][W]


def knapsack_optimised(weights: Sequence[int], values: Sequence[int], W: int) -> int:
    """1-D rolling array. Iterate w in REVERSE to avoid using an item twice."""
    dp = [0] * (W + 1)
    for wi, vi in zip(weights, values):
        for w in range(W, wi - 1, -1):
            dp[w] = max(dp[w], dp[w - wi] + vi)
    return dp[W]


def knapsack_memo(weights: Sequence[int], values: Sequence[int], W: int) -> int:
    """Top-down memoised recursion."""
    n = len(weights)

    @functools.cache
    def best(i: int, cap: int) -> int:
        if i == n or cap == 0:
            return 0
        skip = best(i + 1, cap)
        take = best(i + 1, cap - weights[i]) + values[i] if weights[i] <= cap else 0
        return max(skip, take)

    return best(0, W)


# ---------------- LONGEST COMMON SUBSEQUENCE ----------------
def lcs(s1: str, s2: str) -> int:
    """Bottom-up tabulation."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def lcs_memo(s1: str, s2: str) -> int:
    """Top-down memoisation variant of LCS."""

    @functools.cache
    def go(i: int, j: int) -> int:
        if i == 0 or j == 0:
            return 0
        if s1[i - 1] == s2[j - 1]:
            return go(i - 1, j - 1) + 1
        return max(go(i - 1, j), go(i, j - 1))

    return go(len(s1), len(s2))


# ---------------- COIN CHANGE (min coins) ----------------
def coin_change(coins: Sequence[int], target: int) -> int:
    """Minimum coins to total `target`, or -1 if impossible."""
    INF = math.inf
    dp = [INF] * (target + 1)
    dp[0] = 0
    for a in range(1, target + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[target] == INF else int(dp[target])


def coin_change_memo(coins: Sequence[int], target: int) -> int:
    @functools.cache
    def best(remaining: int) -> int:
        if remaining == 0:
            return 0
        if remaining < 0:
            return math.inf  # type: ignore[return-value]
        result = math.inf
        for c in coins:
            sub = best(remaining - c)
            if sub + 1 < result:
                result = sub + 1
        return result

    ans = best(target)
    return -1 if ans == math.inf else int(ans)


# ---------------- SUBSET SUM ----------------
def subset_sum(nums: Sequence[int], target: int) -> bool:
    """True if some subset sums exactly to `target`."""
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for t in range(target, x - 1, -1):
            if dp[t - x]:
                dp[t] = True
    return dp[target]


# ---------------- CLIMBING STAIRS ----------------
def climb_stairs(n: int) -> int:
    """Number of ways to climb n stairs taking 1 or 2 steps at a time."""
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1


def main() -> None:
    print("=== 0/1 Knapsack ===")
    weights, values = [2, 3, 4, 5], [3, 4, 5, 6]
    print("W=5  bottom-up:", knapsack(weights, values, 5))           # 7
    print("W=10 bottom-up:", knapsack(weights, values, 10))          # 13
    print("W=10 optimised:", knapsack_optimised(weights, values, 10))
    print("W=10 memoised :", knapsack_memo(weights, values, 10))

    print("\n=== LCS ===")
    print("LCS('ABCBDAB','BDCABA') =", lcs("ABCBDAB", "BDCABA"))     # 4
    print("LCS('AGGTAB','GXTXAYB') =", lcs("AGGTAB", "GXTXAYB"))     # 4
    print("LCS memo same input    =", lcs_memo("ABCBDAB", "BDCABA"))

    print("\n=== Coin Change ===")
    print("coins=[1,2,5], amount=11:", coin_change([1, 2, 5], 11))   # 3
    print("coins=[2], amount=3      :", coin_change([2], 3))         # -1
    print("coins=[1], amount=0      :", coin_change([1], 0))         # 0
    print("memoised, 11             :", coin_change_memo([1, 2, 5], 11))

    print("\n=== Subset Sum ===")
    print("[3,1,5,9,12] target=8:", subset_sum([3, 1, 5, 9, 12], 8))  # True
    print("[3,1,5,9,12] target=7:", subset_sum([3, 1, 5, 9, 12], 7))  # False

    print("\n=== Climbing Stairs ===")
    for i in range(1, 11):
        print(f"climb_stairs({i:2d}) = {climb_stairs(i)}")


if __name__ == "__main__":
    main()


"""
NOTES (Python vs Java):
    - Java's `int[][] dp = new int[n+1][W+1]` is one line; Python needs the
      list-comprehension `[[0]*(W+1) for _ in range(n+1)]` because
      `[[0]*(W+1)]*(n+1)` would alias the same inner list.
    - Memoisation in Java requires HashMap<Pair, Integer> or a big int[][]
      sentinel array; Python's `@functools.cache` is one decorator.
    - Use `math.inf` as a clean infinity sentinel; convert back via int().
    - The 1-D space-optimised knapsack iterates `w` in reverse for the SAME
      reason as Java: avoid double-counting the current item.
    - For huge state spaces, switch from @cache to manual dict-based memo
      to control eviction.
"""
