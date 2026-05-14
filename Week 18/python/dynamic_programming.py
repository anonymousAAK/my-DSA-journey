"""
Week 18: Dynamic Programming
==============================
Dynamic programming (DP) solves problems by breaking them into overlapping
sub-problems, solving each once and caching results (memoization / tabulation).

Topics covered:
    1. Climbing stairs
    2. 0/1 Knapsack (2D table + space-optimized 1D)
    3. Longest Common Subsequence (with string reconstruction)
    4. Longest Increasing Subsequence (O(n^2) + O(n log n) with bisect)
    5. Coin change (minimum coins)
    6. Subset sum
    7. Edit distance (Levenshtein)
"""

from __future__ import annotations

import bisect
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# 1. Climbing Stairs
# ---------------------------------------------------------------------------
def climbing_stairs(n: int) -> int:
    """
    Count the number of ways to climb *n* stairs taking 1 or 2 steps at a time.

    Recurrence:  dp[i] = dp[i-1] + dp[i-2]   (same as Fibonacci)
    Base cases:  dp[0] = 1 (standing at the bottom), dp[1] = 1

    Time:  O(n)
    Space: O(1) — only two variables needed
    """
    if n <= 1:
        return 1
    prev2, prev1 = 1, 1  # dp[0], dp[1]
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1


# ---------------------------------------------------------------------------
# 2. 0/1 Knapsack
# ---------------------------------------------------------------------------
def knapsack_01_2d(weights: List[int], values: List[int], capacity: int) -> int:
    """
    0/1 Knapsack — each item can be taken at most once.

    dp[i][w] = maximum value achievable using items 0..i-1 with capacity w.

    Recurrence:
        if weights[i-1] > w:
            dp[i][w] = dp[i-1][w]          # can't include item i
        else:
            dp[i][w] = max(dp[i-1][w],     # skip item i
                           dp[i-1][w - weights[i-1]] + values[i-1])  # take item i

    Time:  O(n * capacity)
    Space: O(n * capacity)
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]  # don't take item i
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w],
                               dp[i - 1][w - weights[i - 1]] + values[i - 1])

    return dp[n][capacity]


def knapsack_01_optimized(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Space-optimized 0/1 Knapsack using a single 1D array.

    Key insight: dp[i][w] only depends on dp[i-1][...], so we can use one row.
    We iterate *w* from right to left so that we don't overwrite values we
    still need from the previous row.

    Time:  O(n * capacity)
    Space: O(capacity)
    """
    dp = [0] * (capacity + 1)

    for i in range(len(weights)):
        # Traverse capacity in reverse to avoid using the same item twice.
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]


# ---------------------------------------------------------------------------
# 3. Longest Common Subsequence (LCS) with reconstruction
# ---------------------------------------------------------------------------
def lcs(text1: str, text2: str) -> Tuple[int, str]:
    """
    Find the length and the actual longest common subsequence of *text1* and *text2*.

    dp[i][j] = LCS length for text1[:i] and text2[:j].

    Recurrence:
        if text1[i-1] == text2[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    Reconstruction: backtrack from dp[m][n] following the choices.

    Time:  O(m * n)
    Space: O(m * n)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # --- Reconstruct the LCS string ---
    lcs_chars: List[str] = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs_chars.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    lcs_str = "".join(reversed(lcs_chars))

    return dp[m][n], lcs_str


# ---------------------------------------------------------------------------
# 4. Longest Increasing Subsequence (LIS)
# ---------------------------------------------------------------------------
def lis_dp(nums: List[int]) -> int:
    """
    Classic O(n^2) DP approach.

    dp[i] = length of the LIS ending at index i.

    Recurrence:
        dp[i] = max(dp[j] + 1)  for all j < i where nums[j] < nums[i]

    Time:  O(n^2)
    Space: O(n)
    """
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n  # every element is an LIS of length 1

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def lis_bisect(nums: List[int]) -> int:
    """
    O(n log n) approach using patience sorting / binary search.

    Maintain a list *tails* where tails[i] is the smallest possible tail
    element for an increasing subsequence of length i+1.

    For each number:
        - Binary-search for the leftmost position in *tails* >= num.
        - If found, replace tails[pos] with num (we found a smaller tail).
        - If not found (num is larger than all tails), extend tails.

    The length of *tails* is the LIS length.

    Time:  O(n log n)
    Space: O(n)
    """
    tails: List[int] = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)


# ---------------------------------------------------------------------------
# 5. Coin Change — minimum coins
# ---------------------------------------------------------------------------
def coin_change(coins: List[int], amount: int) -> int:
    """
    Find the minimum number of coins needed to make *amount*.
    Return -1 if it is not possible.

    dp[a] = minimum coins to make amount a.

    Recurrence:
        dp[a] = min(dp[a - coin] + 1)  for each coin <= a

    Time:  O(amount * len(coins))
    Space: O(amount)
    """
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and dp[a - coin] + 1 < dp[a]:
                dp[a] = dp[a - coin] + 1

    return dp[amount] if dp[amount] != float("inf") else -1


# ---------------------------------------------------------------------------
# 6. Subset Sum
# ---------------------------------------------------------------------------
def subset_sum(nums: List[int], target: int) -> bool:
    """
    Determine whether any subset of *nums* sums to *target*.

    dp[j] = True if some subset of the elements considered so far sums to j.

    Recurrence (process each element, iterate j in reverse):
        dp[j] = dp[j] or dp[j - nums[i]]

    Time:  O(n * target)
    Space: O(target)
    """
    dp = [False] * (target + 1)
    dp[0] = True  # empty subset sums to 0

    for num in nums:
        # Reverse to ensure each element is used at most once (0/1 choice).
        for j in range(target, num - 1, -1):
            if dp[j - num]:
                dp[j] = True

    return dp[target]


# ---------------------------------------------------------------------------
# 7. Edit Distance (Levenshtein Distance)
# ---------------------------------------------------------------------------
def edit_distance(word1: str, word2: str) -> int:
    """
    Compute the minimum number of operations (insert, delete, replace) to
    convert *word1* into *word2*.

    dp[i][j] = edit distance between word1[:i] and word2[:j].

    Recurrence:
        if word1[i-1] == word2[j-1]:
            dp[i][j] = dp[i-1][j-1]            # characters match, no cost
        else:
            dp[i][j] = 1 + min(
                dp[i-1][j],      # delete from word1
                dp[i][j-1],      # insert into word1
                dp[i-1][j-1]     # replace
            )

    Base cases:
        dp[i][0] = i  (delete all chars from word1)
        dp[0][j] = j  (insert all chars of word2)

    Time:  O(m * n)
    Space: O(m * n)  — can be optimized to O(min(m, n)) with rolling array
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # delete
                                   dp[i][j - 1],      # insert
                                   dp[i - 1][j - 1])  # replace

    return dp[m][n]


# ===========================================================================
# Test Cases
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Week 18 — Dynamic Programming")
    print("=" * 60)

    # --- Climbing Stairs ---------------------------------------------------
    print("\n--- Climbing Stairs ---")
    assert climbing_stairs(0) == 1
    assert climbing_stairs(1) == 1
    assert climbing_stairs(2) == 2
    assert climbing_stairs(3) == 3
    assert climbing_stairs(5) == 8
    print(f"stairs(5) = {climbing_stairs(5)}")

    # --- 0/1 Knapsack -----------------------------------------------------
    print("\n--- 0/1 Knapsack ---")
    w = [1, 3, 4, 5]
    v = [1, 4, 5, 7]
    cap = 7
    assert knapsack_01_2d(w, v, cap) == 9
    assert knapsack_01_optimized(w, v, cap) == 9
    print(f"Knapsack(weights={w}, values={v}, cap={cap}) = {knapsack_01_2d(w, v, cap)}")

    # --- LCS ---------------------------------------------------------------
    print("\n--- Longest Common Subsequence ---")
    length, seq = lcs("abcde", "ace")
    assert length == 3 and seq == "ace"
    print(f'LCS("abcde", "ace") = length {length}, sequence "{seq}"')

    length2, seq2 = lcs("AGGTAB", "GXTXAYB")
    assert length2 == 4 and seq2 == "GTAB"
    print(f'LCS("AGGTAB", "GXTXAYB") = length {length2}, sequence "{seq2}"')

    # --- LIS ---------------------------------------------------------------
    print("\n--- Longest Increasing Subsequence ---")
    assert lis_dp([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert lis_bisect([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    print(f"LIS([10,9,2,5,3,7,101,18]) = {lis_bisect([10, 9, 2, 5, 3, 7, 101, 18])}")

    assert lis_dp([0, 1, 0, 3, 2, 3]) == 4
    assert lis_bisect([0, 1, 0, 3, 2, 3]) == 4

    # --- Coin Change -------------------------------------------------------
    print("\n--- Coin Change ---")
    assert coin_change([1, 5, 10, 25], 30) == 2  # 25 + 5
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0
    print(f"coin_change([1,5,10,25], 30) = {coin_change([1, 5, 10, 25], 30)}")

    # --- Subset Sum --------------------------------------------------------
    print("\n--- Subset Sum ---")
    assert subset_sum([3, 34, 4, 12, 5, 2], 9) is True   # 4+5
    assert subset_sum([3, 34, 4, 12, 5, 2], 30) is False
    print(f"subset_sum([3,34,4,12,5,2], 9) = {subset_sum([3, 34, 4, 12, 5, 2], 9)}")

    # --- Edit Distance -----------------------------------------------------
    print("\n--- Edit Distance ---")
    assert edit_distance("horse", "ros") == 3
    assert edit_distance("intention", "execution") == 5
    assert edit_distance("", "abc") == 3
    assert edit_distance("abc", "abc") == 0
    print(f'edit_distance("horse", "ros") = {edit_distance("horse", "ros")}')
    print(f'edit_distance("intention", "execution") = {edit_distance("intention", "execution")}')

    print("\nAll tests passed!")
