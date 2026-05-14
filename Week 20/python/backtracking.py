"""
Week 20: Backtracking
======================
Backtracking is a systematic way to explore all possible configurations of a
search space.  It builds candidates incrementally and abandons ("backtracks")
a candidate as soon as it determines the candidate cannot lead to a valid
solution.

General template:
    def backtrack(state):
        if is_solution(state):
            record(state)
            return
        for choice in choices(state):
            make(choice)
            backtrack(state)
            undo(choice)        # <-- backtrack

Topics covered:
    1. Permutations
    2. Subsets (power set)
    3. Combinations (n choose k)
    4. N-Queens (return all solutions)
    5. Sudoku solver
    6. Word search in grid
    7. Generate valid parentheses
"""

from __future__ import annotations

from typing import List, Optional


# ---------------------------------------------------------------------------
# 1. Permutations
# ---------------------------------------------------------------------------
def permutations(nums: List[int]) -> List[List[int]]:
    """
    Generate all permutations of *nums*.

    Strategy: at each level, pick an unused element and recurse.

    Time:  O(n! * n)  — n! permutations, each taking O(n) to copy
    Space: O(n) recursion depth + O(n!) for results
    """
    result: List[List[int]] = []
    used = [False] * len(nums)
    current: List[int] = []

    def backtrack() -> None:
        if len(current) == len(nums):
            result.append(current[:])
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                current.append(nums[i])
                backtrack()
                current.pop()
                used[i] = False

    backtrack()
    return result


# ---------------------------------------------------------------------------
# 2. Subsets (Power Set)
# ---------------------------------------------------------------------------
def subsets(nums: List[int]) -> List[List[int]]:
    """
    Generate all subsets of *nums* (the power set).

    Strategy: for each element, decide to include it or not.
    Use an index to avoid duplicates.

    Time:  O(2^n * n)  — 2^n subsets, each up to O(n) to copy
    Space: O(n) recursion depth
    """
    result: List[List[int]] = []
    current: List[int] = []

    def backtrack(start: int) -> None:
        result.append(current[:])  # record every partial subset
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1)
            current.pop()

    backtrack(0)
    return result


# ---------------------------------------------------------------------------
# 3. Combinations (n choose k)
# ---------------------------------------------------------------------------
def combinations(n: int, k: int) -> List[List[int]]:
    """
    Generate all combinations of k numbers from 1..n.

    Strategy: similar to subsets but only record when we have exactly k elements.
    Prune: if remaining elements aren't enough to fill the combination, stop.

    Time:  O(C(n,k) * k)
    Space: O(k) recursion depth
    """
    result: List[List[int]] = []
    current: List[int] = []

    def backtrack(start: int) -> None:
        if len(current) == k:
            result.append(current[:])
            return
        # Pruning: need (k - len(current)) more elements, and only
        # (n - start + 1) are available.
        remaining_needed = k - len(current)
        for i in range(start, n - remaining_needed + 2):
            current.append(i)
            backtrack(i + 1)
            current.pop()

    backtrack(1)
    return result


# ---------------------------------------------------------------------------
# 4. N-Queens — return all solutions
# ---------------------------------------------------------------------------
def n_queens(n: int) -> List[List[str]]:
    """
    Place n queens on an n x n chessboard such that no two queens
    attack each other.  Return all distinct solutions.

    Each solution is a list of n strings, where 'Q' marks a queen and '.'
    marks an empty cell.

    Strategy: place queens row by row.  Track which columns and diagonals
    are under attack using sets.

    Time:  O(n!)  — upper bound; actual much less due to pruning
    Space: O(n) for the board state + O(n^2 * solutions) for results
    """
    result: List[List[str]] = []
    queens: List[int] = []  # queens[row] = column
    cols: set[int] = set()
    diag1: set[int] = set()  # row - col
    diag2: set[int] = set()  # row + col

    def backtrack(row: int) -> None:
        if row == n:
            # Build board representation
            board = []
            for r in range(n):
                line = ["."] * n
                line[queens[r]] = "Q"
                board.append("".join(line))
            result.append(board)
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue  # conflict — prune
            # Place queen
            queens.append(col)
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(row + 1)

            # Remove queen (backtrack)
            queens.pop()
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result


# ---------------------------------------------------------------------------
# 5. Sudoku Solver
# ---------------------------------------------------------------------------
def solve_sudoku(board: List[List[str]]) -> bool:
    """
    Solve a 9x9 Sudoku puzzle in-place.

    Empty cells are represented by '.'.
    Returns True if the puzzle is solvable, False otherwise.

    Strategy:
        1. Find the next empty cell.
        2. Try digits '1'-'9'.
        3. If a digit is valid (no conflict in row, column, or 3x3 box),
           place it and recurse.
        4. If recursion fails, undo and try the next digit (backtrack).

    Time:  O(9^(empty_cells)) worst case, but pruning makes it much faster.
    Space: O(empty_cells) recursion depth
    """

    def is_valid(row: int, col: int, digit: str) -> bool:
        """Check if placing *digit* at (row, col) is valid."""
        # Check row
        if digit in board[row]:
            return False
        # Check column
        for r in range(9):
            if board[r][col] == digit:
                return False
        # Check 3x3 box
        box_r, box_c = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if board[r][c] == digit:
                    return False
        return True

    def backtrack() -> bool:
        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    for digit in "123456789":
                        if is_valid(r, c, digit):
                            board[r][c] = digit
                            if backtrack():
                                return True
                            board[r][c] = "."  # undo
                    return False  # no valid digit — trigger backtrack
        return True  # all cells filled

    return backtrack()


# ---------------------------------------------------------------------------
# 6. Word Search in Grid
# ---------------------------------------------------------------------------
def word_search(board: List[List[str]], word: str) -> bool:
    """
    Determine if *word* exists in the *board* by following adjacent
    (horizontal/vertical) cells.  Each cell may be used at most once per path.

    Strategy: DFS/backtracking from every cell that matches word[0].

    Time:  O(m * n * 3^L)  where L = len(word).  From any cell we branch
           into at most 3 directions (we don't revisit the cell we came from).
    Space: O(L) recursion depth
    """
    if not board or not board[0] or not word:
        return False

    rows, cols = len(board), len(board[0])

    def backtrack(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[idx]:
            return False

        # Mark cell as visited by temporarily replacing it.
        saved = board[r][c]
        board[r][c] = "#"

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if backtrack(r + dr, c + dc, idx + 1):
                board[r][c] = saved  # restore before returning
                return True

        board[r][c] = saved  # restore (backtrack)
        return False

    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False


# ---------------------------------------------------------------------------
# 7. Generate Valid Parentheses
# ---------------------------------------------------------------------------
def generate_parentheses(n: int) -> List[str]:
    """
    Generate all combinations of *n* pairs of well-formed parentheses.

    Strategy: build the string character by character.
      - Add '(' if open_count < n.
      - Add ')' if close_count < open_count.

    Time:  O(4^n / sqrt(n))  — the n-th Catalan number
    Space: O(n) recursion depth
    """
    result: List[str] = []
    current: List[str] = []

    def backtrack(open_count: int, close_count: int) -> None:
        if open_count == n and close_count == n:
            result.append("".join(current))
            return
        if open_count < n:
            current.append("(")
            backtrack(open_count + 1, close_count)
            current.pop()
        if close_count < open_count:
            current.append(")")
            backtrack(open_count, close_count + 1)
            current.pop()

    backtrack(0, 0)
    return result


# ===========================================================================
# Test Cases
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Week 20 — Backtracking")
    print("=" * 60)

    # --- Permutations ------------------------------------------------------
    print("\n--- Permutations ---")
    perms = permutations([1, 2, 3])
    print(f"permutations([1,2,3]): {len(perms)} results")
    assert len(perms) == 6
    assert [1, 2, 3] in perms and [3, 2, 1] in perms

    # --- Subsets -----------------------------------------------------------
    print("\n--- Subsets ---")
    subs = subsets([1, 2, 3])
    print(f"subsets([1,2,3]): {subs}")
    assert len(subs) == 8  # 2^3
    assert [] in subs and [1, 2, 3] in subs

    # --- Combinations ------------------------------------------------------
    print("\n--- Combinations ---")
    combs = combinations(4, 2)
    print(f"combinations(4, 2): {combs}")
    assert len(combs) == 6  # C(4,2)
    assert [1, 2] in combs and [3, 4] in combs

    # --- N-Queens ----------------------------------------------------------
    print("\n--- N-Queens ---")
    solutions_4 = n_queens(4)
    print(f"4-Queens: {len(solutions_4)} solutions")
    assert len(solutions_4) == 2
    for sol in solutions_4:
        for row in sol:
            print(f"  {row}")
        print()

    solutions_8 = n_queens(8)
    print(f"8-Queens: {len(solutions_8)} solutions")
    assert len(solutions_8) == 92

    # --- Sudoku Solver -----------------------------------------------------
    print("\n--- Sudoku Solver ---")
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    assert solve_sudoku(board) is True
    print("Solved Sudoku:")
    for row in board:
        print(f"  {' '.join(row)}")
    # Verify no '.' remains
    assert all(cell != "." for row in board for cell in row)

    # --- Word Search -------------------------------------------------------
    print("\n--- Word Search ---")
    grid = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    assert word_search(grid, "ABCCED") is True
    assert word_search(grid, "SEE") is True
    assert word_search(grid, "ABCB") is False
    print("word_search('ABCCED') = True")
    print("word_search('SEE')    = True")
    print("word_search('ABCB')   = False")

    # --- Generate Parentheses ----------------------------------------------
    print("\n--- Generate Valid Parentheses ---")
    parens = generate_parentheses(3)
    print(f"generate_parentheses(3): {parens}")
    assert len(parens) == 5
    expected = ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert sorted(parens) == sorted(expected)

    print("\nAll tests passed!")
