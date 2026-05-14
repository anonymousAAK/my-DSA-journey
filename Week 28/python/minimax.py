"""
WEEK 28 - PYTHON ADVANCED TOPICS
Topic: Minimax (Zero-Sum Game Tree Search)
File: minimax.py

CONCEPT:
    For a two-player, perfect-information, zero-sum game, minimax assigns a
    value v(s) to every state s representing the score the *maximising*
    player can guarantee against an optimally-playing *minimising* opponent.
    The recurrence:

        v(s) = utility(s)                              if s is terminal
             = max over moves of v(child(s))           if Max to move
             = min over moves of v(child(s))           if Min to move

    The depth-first traversal of the full game tree computes v(root).

KEY POINTS:
    - Evaluates every reachable leaf in the worst case -> O(b^d) where b is
      branching factor, d is depth. Use alpha-beta for pruning.
    - Memoisation (transposition table) helps for repeated subtrees.
    - For non-finite games introduce a depth limit + heuristic evaluator.

ALGORITHM / APPROACH:
    def minimax(state, max_turn):
        if terminal(state): return utility(state)
        if max_turn: return max(minimax(child, False) for child in moves(state))
        else:        return min(minimax(child, True)  for child in moves(state))

PYTHON-SPECIFIC NOTES:
    - Tic-tac-toe board stored as a tuple of 9 characters; tuples are
      hashable, so we can memoise with @lru_cache.
    - 'X' is Max (+1), 'O' is Min (-1).

DRY RUN / EXAMPLE:
    Empty TTT board, X to move -> minimax returns 0 (game is a draw with
    optimal play). Best move from the centre is to grab the centre cell
    (or any corner).

COMPLEXITY:
    Time:  O(b^d) without pruning; here d <= 9 for TTT -> ~360k positions.
    Space: O(d) recursion; O(|states|) when memoised.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Optional, Tuple

Board = Tuple[str, ...]

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # cols
    (0, 4, 8), (2, 4, 6),              # diagonals
]


def winner(board: Board) -> Optional[str]:
    for a, b, c in LINES:
        if board[a] != "." and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board: Board) -> bool:
    return "." not in board


def utility(board: Board) -> int:
    w = winner(board)
    if w == "X": return +1
    if w == "O": return -1
    return 0


@lru_cache(maxsize=None)
def minimax(board: Board, max_turn: bool) -> int:
    if winner(board) is not None or is_full(board):
        return utility(board)
    if max_turn:
        best = -2
        for i, ch in enumerate(board):
            if ch == ".":
                child = board[:i] + ("X",) + board[i+1:]
                best = max(best, minimax(child, False))
        return best
    else:
        best = +2
        for i, ch in enumerate(board):
            if ch == ".":
                child = board[:i] + ("O",) + board[i+1:]
                best = min(best, minimax(child, True))
        return best


def best_move(board: Board, max_turn: bool) -> int:
    """Returns the index of the optimal move (0..8) for the side to move."""
    best_idx, best_val = -1, -3 if max_turn else +3
    for i, ch in enumerate(board):
        if ch != ".":
            continue
        child = board[:i] + (("X" if max_turn else "O"),) + board[i+1:]
        v = minimax(child, not max_turn)
        if max_turn and v > best_val:
            best_val, best_idx = v, i
        if not max_turn and v < best_val:
            best_val, best_idx = v, i
    return best_idx


def _demo() -> None:
    empty = tuple(".") * 9
    print(f"Minimax value of empty TTT board (X to move): {minimax(empty, True)}")
    print(f"Best opening move for X: cell index {best_move(empty, True)}")

    # X plays centre, then X forces draw against any O response.
    board: Board = ("X", ".", ".", ".", ".", ".", ".", ".", ".")
    print(f"After X corner, minimax value: {minimax(board, False)}")  # should be 0


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java (which covered different game-theory topics):
#   * Java's game_theory.java focuses on Nim, Grundy, Pascal, Catalan, and
#     matrix exponentiation. This file completes the spec by adding
#     minimax — a foundational adversarial search algorithm.
#   * @lru_cache provides automatic memoisation by hashing the tuple board.
#   * Tuples (immutable) ensure cacheability.
