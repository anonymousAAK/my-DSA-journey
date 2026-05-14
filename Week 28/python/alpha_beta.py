"""
WEEK 28 - PYTHON ADVANCED TOPICS
Topic: Alpha-Beta Pruning
File: alpha_beta.py

CONCEPT:
    Alpha-beta pruning is an enhancement of minimax: as we explore the game
    tree we maintain a window [alpha, beta] where alpha is the best already-
    guaranteed value for Max and beta the best for Min. When a node's value
    falls outside this window we can prune the remaining children — they
    cannot influence the parent's choice.

    Same value as minimax but with much smaller effective branching factor.
    With perfect move ordering the time complexity drops from O(b^d) to
    O(b^(d/2)) — i.e. searches twice as deep in the same time budget.

KEY POINTS:
    - alpha = lower bound on Max's value at this node.
    - beta  = upper bound on Min's value at this node.
    - When alpha >= beta: prune the rest (beta-cutoff / alpha-cutoff).
    - Move ordering is critical to realise the asymptotic speedup.

ALGORITHM / APPROACH:
    def ab(state, alpha, beta, max_turn):
        if terminal: return utility(state)
        if max_turn:
            v = -inf
            for child in moves(state):
                v = max(v, ab(child, alpha, beta, False))
                alpha = max(alpha, v)
                if alpha >= beta: break        # beta cutoff
            return v
        else:
            v = +inf
            for child in moves(state):
                v = min(v, ab(child, alpha, beta, True))
                beta = min(beta, v)
                if alpha >= beta: break        # alpha cutoff
            return v

PYTHON-SPECIFIC NOTES:
    - We share board representation with minimax.py (tuple of 9 chars).
    - lru_cache cannot easily memoise alpha-beta because the same state
      can be reached with different (alpha, beta) bounds. We omit caching
      for clarity.

DRY RUN / EXAMPLE:
    Empty TTT board, X to move -> alpha-beta returns 0 like minimax, but
    visits far fewer nodes. The "node_count" counter demonstrates the
    pruning savings vs pure minimax.

COMPLEXITY:
    Time:  O(b^d) worst case; O(b^(d/2)) with good ordering.
    Space: O(d) recursion.
"""

from __future__ import annotations

import math
from typing import Optional, Tuple, List

Board = Tuple[str, ...]

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def winner(board: Board) -> Optional[str]:
    for a, b, c in LINES:
        if board[a] != "." and board[a] == board[b] == board[c]:
            return board[a]
    return None


def utility(board: Board) -> int:
    w = winner(board)
    if w == "X": return +1
    if w == "O": return -1
    return 0


_node_count = 0  # demo counter


def alphabeta(board: Board, alpha: float, beta: float, max_turn: bool) -> int:
    global _node_count
    _node_count += 1
    w = winner(board)
    if w is not None or "." not in board:
        return utility(board)
    if max_turn:
        v = -math.inf
        for i, ch in enumerate(board):
            if ch != ".":
                continue
            child = board[:i] + ("X",) + board[i+1:]
            v = max(v, alphabeta(child, alpha, beta, False))
            alpha = max(alpha, v)
            if alpha >= beta:
                break  # beta cutoff
        return int(v)
    else:
        v = math.inf
        for i, ch in enumerate(board):
            if ch != ".":
                continue
            child = board[:i] + ("O",) + board[i+1:]
            v = min(v, alphabeta(child, alpha, beta, True))
            beta = min(beta, v)
            if alpha >= beta:
                break  # alpha cutoff
        return int(v)


def best_move(board: Board, max_turn: bool) -> int:
    best_idx, best_val = -1, -2 if max_turn else +2
    for i, ch in enumerate(board):
        if ch != ".":
            continue
        child = board[:i] + (("X" if max_turn else "O"),) + board[i+1:]
        v = alphabeta(child, -math.inf, math.inf, not max_turn)
        if max_turn and v > best_val:
            best_val, best_idx = v, i
        if not max_turn and v < best_val:
            best_val, best_idx = v, i
    return best_idx


def _demo() -> None:
    global _node_count
    empty = tuple(".") * 9
    _node_count = 0
    print(f"Alpha-beta value of empty TTT: "
          f"{alphabeta(empty, -math.inf, math.inf, True)}")
    print(f"Nodes explored: {_node_count}")
    print(f"Best opening move for X: {best_move(empty, True)}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Java's game_theory.java does not include alpha-beta. We add it to
#     satisfy the spec.
#   * Python uses math.inf for unbounded windows; integer casts ensure
#     a clean return type for non-float utility functions.
#   * A `_node_count` global makes the pruning effect visible.
