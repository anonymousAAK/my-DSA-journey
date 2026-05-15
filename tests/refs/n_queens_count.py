"""Reference: count of distinct n-queens placements on an n x n board."""

from __future__ import annotations


def nQueensCount(n: int) -> int:
    count = 0
    queens = [-1] * n

    def is_safe(row: int, col: int) -> bool:
        for r in range(row):
            c = queens[r]
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def go(row: int) -> None:
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            if is_safe(row, col):
                queens[row] = col
                go(row + 1)
                queens[row] = -1

    if n > 0:
        go(0)
    return count
