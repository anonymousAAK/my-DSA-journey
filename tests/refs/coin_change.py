"""Reference: minimum coin change DP (LC 322).

Returns the minimum number of coins making `amount`, or -1 if impossible.
"""

from __future__ import annotations
import math
from typing import List


def coinChange(coins: List[int], amount: int) -> int:
    INF = math.inf
    dp: List[float] = [INF] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == INF else int(dp[amount])
