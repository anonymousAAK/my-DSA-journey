"""
WEEK 28 - PYTHON ADVANCED TOPICS
Topic: Sprague-Grundy Theorem and Grundy Numbers
File: sprague_grundy.py

CONCEPT:
    The Sprague-Grundy theorem generalises Bouton's rule for Nim: every
    impartial game (no draws, no chance, both players have the same legal
    moves from any position) is equivalent to a single Nim pile whose size
    equals the position's Grundy number. The Grundy number g(s) is:

        g(s) = mex { g(s') : s' is a position reachable from s in one move }

    where `mex` is the minimum excludant — the smallest non-negative integer
    not present in the set.

    For a sum of independent games, the overall Grundy value is the XOR of
    the components, so the position is losing for the player to move iff
    the XOR is 0.

KEY POINTS:
    - Used to analyse any impartial game (subtraction games, Nim variants,
      green-Hackenbush trees, Wythoff's game, ...).
    - Memoisation crucial: many recursions revisit the same state.
    - `mex(S)` runs in O(|S|) by counting from 0.

ALGORITHM / APPROACH:
    def grundy(state):
        if no moves: return 0
        reachable = { grundy(child) for child in moves(state) }
        return mex(reachable)

PYTHON-SPECIFIC NOTES:
    - `set` data structure for the reachable Grundy values.
    - `functools.lru_cache` memoises by state.
    - `mex` is a small helper.

DRY RUN / EXAMPLE:
    Subtraction game: from a pile of n stones, the player may remove
    1, 3 or 4 stones. Compute Grundy(n):

        g(0) = 0
        g(1) = mex{g(0)}       = mex{0} = 1
        g(2) = mex{g(1)}       = mex{1} = 0
        g(3) = mex{g(2),g(0)}  = mex{0} = 1
        g(4) = mex{g(3),g(1),g(0)} = mex{1,1,0} = 2
        g(5) = mex{g(4),g(2),g(1)} = mex{2,0,1} = 3
        g(6) = mex{g(5),g(3),g(2)} = mex{3,1,0} = 2
        ...
        g(10) = 1.

COMPLEXITY:
    Time:  O(n * |moves|) for a subtraction game on a single pile up to n.
    Space: O(n).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Iterable, List


def mex(values: Iterable[int]) -> int:
    s = set(values)
    m = 0
    while m in s:
        m += 1
    return m


def grundy_subtraction(n: int, moves: List[int]) -> int:
    """Grundy number of a one-pile subtraction game."""
    g = [0] * (n + 1)
    for i in range(1, n + 1):
        reachable = {g[i - m] for m in moves if i - m >= 0}
        g[i] = mex(reachable)
    return g[n]


def first_player_wins(positions: List[int], moves: List[int]) -> bool:
    """Multi-pile subtraction game: XOR Grundy values."""
    xor_sum = 0
    if not positions:
        return False
    max_pos = max(positions)
    # Precompute g[0..max_pos]
    g = [0] * (max_pos + 1)
    for i in range(1, max_pos + 1):
        reachable = {g[i - m] for m in moves if i - m >= 0}
        g[i] = mex(reachable)
    for p in positions:
        xor_sum ^= g[p]
    return xor_sum != 0


@lru_cache(maxsize=None)
def grundy_general(state: int, moves_tuple) -> int:
    """Generic single-pile grundy via recursion + memoisation."""
    moves = list(moves_tuple)
    reachable = {grundy_general(state - m, moves_tuple) for m in moves if state - m >= 0}
    return mex(reachable)


def _demo() -> None:
    moves = [1, 3, 4]
    print("Grundy table for subtraction moves {1,3,4}:")
    for i in range(11):
        print(f"  g({i}) = {grundy_subtraction(i, moves)}")
    print(f"\ngrundy(10) = {grundy_subtraction(10, moves)}")
    print(f"Two piles [10, 6]: first player wins? "
          f"{first_player_wins([10, 6], moves)}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Java's grundy() returns a single value; we add a multi-pile XOR
#     wrapper plus a per-state lru_cache version.
#   * `mex` is implemented as a tiny helper instead of inline like Java's.
#   * `lru_cache(maxsize=None)` provides cheap memoisation; we pass moves
#     as a hashable tuple.
