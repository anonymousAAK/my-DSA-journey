"""
Week 23: Advanced Dynamic Programming
=======================================
This module covers more sophisticated DP techniques including bitmask DP,
DP on trees, digit DP, and matrix chain multiplication.

Topics covered:
    1. Travelling Salesman Problem (TSP) with bitmask DP
    2. Maximum Independent Set on a tree (DP on trees)
    3. Digit DP: count numbers without digit 4 in [1..N]
    4. LIS in O(n log n) with bisect (revisited with path reconstruction)
    5. Matrix Chain Multiplication
"""

from __future__ import annotations

import bisect
from collections import defaultdict
from functools import lru_cache
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# 1. Travelling Salesman Problem — Bitmask DP
# ---------------------------------------------------------------------------
def tsp_bitmask(dist: List[List[float]]) -> Tuple[float, List[int]]:
    """
    Solve the Travelling Salesman Problem using bitmask DP.

    Given a distance matrix dist[i][j], find the minimum-cost tour that
    visits every city exactly once and returns to the starting city (city 0).

    State: dp[mask][i] = minimum cost to reach city i having visited
           exactly the set of cities represented by *mask*.

    Recurrence:
        dp[mask | (1 << j)][j] = min over all i in mask of
            dp[mask][i] + dist[i][j]

    Final answer:
        min over all i of dp[full_mask][i] + dist[i][0]

    Time:  O(2^n * n^2)
    Space: O(2^n * n)

    Returns (min_cost, tour) where tour is the list of cities in order.
    """
    n = len(dist)
    full = (1 << n) - 1
    INF = float("inf")

    # dp[mask][i] = min cost to reach city i with visited set = mask
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0, only city 0 visited

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            if not (mask & (1 << u)):
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue  # already visited
                new_mask = mask | (1 << v)
                new_cost = dp[mask][u] + dist[u][v]
                if new_cost < dp[new_mask][v]:
                    dp[new_mask][v] = new_cost
                    parent[new_mask][v] = u

    # Find the best last city before returning to 0
    min_cost = INF
    last_city = -1
    for u in range(n):
        total = dp[full][u] + dist[u][0]
        if total < min_cost:
            min_cost = total
            last_city = u

    # Reconstruct the tour
    tour: List[int] = []
    mask = full
    city = last_city
    while city != -1:
        tour.append(city)
        prev = parent[mask][city]
        mask ^= (1 << city)
        city = prev
    tour.reverse()
    tour.append(0)  # return to start

    return min_cost, tour


# ---------------------------------------------------------------------------
# 2. Maximum Independent Set on a Tree — DP on Trees
# ---------------------------------------------------------------------------
def max_independent_set_tree(
    n: int, edges: List[Tuple[int, int]], weights: List[int]
) -> int:
    """
    Find the maximum-weight independent set on a tree.

    An independent set is a set of vertices with no two adjacent.

    DP on tree rooted at vertex 0:
        dp[v][0] = max weight of independent set in subtree(v) when v is NOT selected
        dp[v][1] = max weight of independent set in subtree(v) when v IS selected

    Recurrence:
        dp[v][1] = weights[v] + sum(dp[child][0] for child in children(v))
        dp[v][0] = sum(max(dp[child][0], dp[child][1]) for child in children(v))

    Answer: max(dp[0][0], dp[0][1])

    Time:  O(n)
    Space: O(n)
    """
    if n == 0:
        return 0
    if n == 1:
        return max(0, weights[0])

    # Build adjacency list
    adj: Dict[int, List[int]] = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # dp[v] = (not_selected, selected)
    dp = [(0, 0)] * n

    # Iterative DFS (post-order) to avoid recursion limit for large trees.
    visited = [False] * n
    parent_map = [-1] * n
    order: List[int] = []  # post-order

    stack = [0]
    visited[0] = True
    while stack:
        node = stack.pop()
        order.append(node)
        for neighbor in adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                parent_map[neighbor] = node
                stack.append(neighbor)

    # Process in reverse post-order (leaves first).
    dp_not = [0] * n  # dp[v][0]
    dp_sel = [0] * n  # dp[v][1]

    for v in reversed(order):
        dp_sel[v] = weights[v]
        for child in adj[v]:
            if child == parent_map[v]:
                continue
            dp_sel[v] += dp_not[child]
            dp_not[v] += max(dp_not[child], dp_sel[child])

    return max(dp_not[0], dp_sel[0])


# ---------------------------------------------------------------------------
# 3. Digit DP: Count numbers in [1..N] without digit 4
# ---------------------------------------------------------------------------
def count_without_digit_4(n: int) -> int:
    """
    Count how many numbers in [1, N] do not contain the digit '4'.

    Digit DP approach:
        Process the digits of N from left to right.
        State: (position, tight, started)
            - position: current digit index
            - tight: whether previous digits exactly match N's prefix
                     (constraining the current digit's upper bound)
            - started: whether we have placed a non-zero digit yet
                       (handles leading zeros)

    Time:  O(d * 2 * 2 * 10) = O(d) where d = number of digits in N
    Space: O(d) for memoization
    """
    if n <= 0:
        return 0

    digits = [int(c) for c in str(n)]

    @lru_cache(maxsize=None)
    def dp(pos: int, tight: bool, started: bool) -> int:
        """
        Count valid numbers from position *pos* onward.
        """
        if pos == len(digits):
            return 1 if started else 0  # empty number (all zeros) doesn't count

        upper = digits[pos] if tight else 9
        count = 0

        for d in range(0, upper + 1):
            if d == 4:
                continue  # skip digit 4

            new_tight = tight and (d == upper)
            new_started = started or (d != 0)
            count += dp(pos + 1, new_tight, new_started)

        return count

    result = dp(0, True, False)
    dp.cache_clear()
    return result


# ---------------------------------------------------------------------------
# 4. LIS O(n log n) with path reconstruction
# ---------------------------------------------------------------------------
def lis_with_reconstruction(nums: List[int]) -> List[int]:
    """
    Find the actual longest increasing subsequence (not just its length)
    in O(n log n) time.

    Strategy:
        - Maintain *tails*: tails[i] = smallest tail of all increasing
          subsequences of length i+1.
        - For each num, binary-search for its position in tails.
        - Track the predecessor of each element to reconstruct the LIS.

    Time:  O(n log n)
    Space: O(n)
    """
    if not nums:
        return []

    n = len(nums)
    tails: List[int] = []         # smallest tails
    tails_idx: List[int] = []     # index in nums of each tail
    predecessor = [-1] * n        # predecessor index for reconstruction

    for i, num in enumerate(nums):
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
            tails_idx.append(i)
        else:
            tails[pos] = num
            tails_idx[pos] = i

        # Link to predecessor: the element at position pos-1 in tails
        # was the previous element in the subsequence.
        if pos > 0:
            predecessor[i] = tails_idx[pos - 1]

    # Reconstruct
    lis: List[int] = []
    idx = tails_idx[-1]
    while idx != -1:
        lis.append(nums[idx])
        idx = predecessor[idx]
    lis.reverse()
    return lis


# ---------------------------------------------------------------------------
# 5. Matrix Chain Multiplication
# ---------------------------------------------------------------------------
def matrix_chain_multiplication(dims: List[int]) -> Tuple[int, str]:
    """
    Find the optimal way to parenthesise a chain of matrix multiplications
    to minimise the total number of scalar multiplications.

    Given matrices A1 (dims[0] x dims[1]), A2 (dims[1] x dims[2]), ...,
    An (dims[n-1] x dims[n]).

    dp[i][j] = minimum cost to multiply matrices i..j.

    Recurrence:
        dp[i][j] = min over k in [i, j-1] of
            dp[i][k] + dp[k+1][j] + dims[i-1] * dims[k] * dims[j]

    Also reconstructs the optimal parenthesisation.

    Time:  O(n^3)
    Space: O(n^2)
    """
    n = len(dims) - 1  # number of matrices
    if n <= 0:
        return 0, ""

    # dp[i][j] = min cost to multiply matrices i..j (1-indexed)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    split = [[0] * (n + 1) for _ in range(n + 1)]

    # Fill table for increasing chain lengths.
    for length in range(2, n + 1):  # chain length
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k

    # Reconstruct optimal parenthesisation.
    def build_parens(i: int, j: int) -> str:
        if i == j:
            return f"A{i}"
        k = split[i][j]
        left = build_parens(i, k)
        right = build_parens(k + 1, j)
        return f"({left} x {right})"

    return dp[1][n], build_parens(1, n)


# ===========================================================================
# Test Cases
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Week 23 — Advanced DP")
    print("=" * 60)

    # --- TSP with Bitmask DP -----------------------------------------------
    print("\n--- TSP (Bitmask DP) ---")
    dist_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    cost, tour = tsp_bitmask(dist_matrix)
    print(f"Minimum TSP cost: {cost}")
    print(f"Tour: {tour}")
    assert cost == 80  # 0->1->3->2->0: 10+25+30+15 = 80

    # --- Max Independent Set on Tree ---------------------------------------
    print("\n--- Maximum Independent Set on Tree ---")
    #       0(10)
    #      / \
    #    1(5)  2(8)
    #    |
    #   3(3)
    tree_edges = [(0, 1), (0, 2), (1, 3)]
    tree_weights = [10, 5, 8, 3]
    mis = max_independent_set_tree(4, tree_edges, tree_weights)
    print(f"Max independent set weight: {mis}")
    assert mis == 13  # select vertices 0(10) and 3(3) = 13 (non-adjacent)

    # Star graph: center has weight 1, leaves have weight 10 each
    star_edges = [(0, 1), (0, 2), (0, 3)]
    star_weights = [1, 10, 10, 10]
    mis2 = max_independent_set_tree(4, star_edges, star_weights)
    print(f"Star graph MIS weight: {mis2}")
    assert mis2 == 30  # select all leaves

    # --- Digit DP: count without digit 4 -----------------------------------
    print("\n--- Digit DP: Numbers without digit 4 ---")
    assert count_without_digit_4(10) == 9     # 1-10 except 4 = 9 numbers
    # 1..50: numbers containing digit 4: {4,14,24,34,40..49} = 14 numbers
    # 50 - 14 = 36
    result_50 = count_without_digit_4(50)
    print(f"count_without_digit_4(50) = {result_50}")
    assert result_50 == 36

    result_100 = count_without_digit_4(100)
    print(f"count_without_digit_4(100) = {result_100}")
    # 1-digit: 8, 2-digit (10..99): 8*9=72 (8 choices for tens excl 0,4; 9 for units excl 4)
    # 3-digit 100: 1*0*0 -> 100 has no 4, so +1
    # total = 8 + 72 + 1 = 81
    assert result_100 == 81

    # --- LIS with reconstruction -------------------------------------------
    print("\n--- LIS O(n log n) with Reconstruction ---")
    seq = [10, 9, 2, 5, 3, 7, 101, 18]
    lis_result = lis_with_reconstruction(seq)
    print(f"LIS of {seq}: {lis_result} (length {len(lis_result)})")
    assert len(lis_result) == 4
    # Verify it's actually increasing
    for i in range(1, len(lis_result)):
        assert lis_result[i] > lis_result[i - 1]

    seq2 = [0, 1, 0, 3, 2, 3]
    lis2 = lis_with_reconstruction(seq2)
    print(f"LIS of {seq2}: {lis2} (length {len(lis2)})")
    assert len(lis2) == 4

    # --- Matrix Chain Multiplication ---------------------------------------
    print("\n--- Matrix Chain Multiplication ---")
    # Matrices: A1(30x35), A2(35x15), A3(15x5), A4(5x10), A5(10x20), A6(20x25)
    dims = [30, 35, 15, 5, 10, 20, 25]
    min_ops, parens = matrix_chain_multiplication(dims)
    print(f"Minimum multiplications: {min_ops}")
    print(f"Optimal parenthesisation: {parens}")
    assert min_ops == 15125

    # Simple case: 2 matrices
    dims2 = [10, 20, 30]
    ops2, p2 = matrix_chain_multiplication(dims2)
    assert ops2 == 6000
    print(f"2 matrices: {ops2} ops, {p2}")

    print("\nAll tests passed!")
