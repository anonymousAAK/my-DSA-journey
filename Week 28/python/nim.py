"""
WEEK 28 - PYTHON ADVANCED TOPICS
Topic: Nim Game
File: nim.py

CONCEPT:
    The game of Nim is the prototypical impartial combinatorial game. Two
    players alternate; on each turn, the current player removes any positive
    number of stones from exactly one of several piles. The player unable
    to move (i.e. all piles empty) loses (normal play convention).

    BOUTON'S THEOREM (1901):
        The first player wins iff the XOR of all pile sizes is non-zero.

    Intuition: think of pile sizes in binary; XOR=0 means each bit position
    contributes an even number of 1's. Any move flips at least one bit, so
    from a XOR=0 state every move leads to a non-zero state (losing for
    opponent), and from any XOR != 0 state there exists a move to XOR=0.

KEY POINTS:
    - Winning strategy: choose the pile whose top set-bit matches the high
      bit of XOR and reduce it to that pile XOR the current XOR.
    - Sprague-Grundy theory generalises Nim's XOR rule to arbitrary
      impartial games via Grundy numbers.

ALGORITHM / APPROACH:
    xor_sum = XOR of all pile sizes
    if xor_sum == 0: second player wins
    else:
        for pile in piles:
            target = pile XOR xor_sum
            if target < pile:
                winning move: reduce that pile to `target`

PYTHON-SPECIFIC NOTES:
    - Python's `^` operator is bitwise XOR.
    - `functools.reduce(operator.xor, piles)` or a simple loop both work.

DRY RUN / EXAMPLE:
    piles = [3, 4, 5]
    XOR = 3 ^ 4 ^ 5 = 0b011 ^ 0b100 ^ 0b101 = 0b010 = 2 -> first player wins.
    Winning move: find pile p with (p XOR xor_sum) < p. 3 XOR 2 = 1 < 3,
    so reduce pile 0 from 3 to 1.

COMPLEXITY:
    Time:  O(n) for both the decision and finding a winning move.
    Space: O(1).
"""

from __future__ import annotations

from functools import reduce
from operator import xor
from typing import List, Optional, Tuple


def nim_winner(piles: List[int]) -> str:
    return "First" if reduce(xor, piles, 0) != 0 else "Second"


def nim_winning_move(piles: List[int]) -> Optional[Tuple[int, int]]:
    """Return (pile_index, new_size) for a winning move, or None if losing."""
    xor_sum = reduce(xor, piles, 0)
    if xor_sum == 0:
        return None
    for i, p in enumerate(piles):
        target = p ^ xor_sum
        if target < p:
            return (i, target)
    return None  # unreachable when xor_sum != 0


def _demo() -> None:
    piles = [3, 4, 5]
    print(f"Piles {piles}: winner = {nim_winner(piles)}")
    move = nim_winning_move(piles)
    if move:
        i, new_size = move
        print(f"Winning move: reduce pile {i} from {piles[i]} to {new_size}")

    piles2 = [1, 2, 3]
    print(f"Piles {piles2}: winner = {nim_winner(piles2)}")  # XOR = 0 -> Second
    print(f"Winning move: {nim_winning_move(piles2)}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Java's nimWinner returns "First"/"Second" by XOR; we keep parity.
#   * We add `nim_winning_move` to demonstrate the constructive strategy.
#   * `reduce(xor, ...)` is the functional Pythonic way; a simple for-loop
#     is equally idiomatic.
