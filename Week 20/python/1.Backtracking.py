"""
WEEK 20 - PYTHON DSA
Topic: Backtracking — Template + Classic Problems
File: 1.Backtracking.py

CONCEPT:
    Backtracking incrementally builds a candidate solution. After every
    extension it checks whether the partial solution can still lead to a
    valid complete answer. If not, it ABANDONS that branch ("backtracks").

TEMPLATE:
    def backtrack(state):
        if is_solution(state):
            record(state); return
        for choice in choices(state):
            if is_valid(choice, state):
                make_choice(choice, state)   # explore
                backtrack(state)
                undo_choice(choice, state)   # backtrack

    The "undo" step distinguishes backtracking from plain DFS over a tree.

KEY POINTS:
    - Worst-case complexity is usually exponential (O(k^n) or O(n!)).
    - Pruning ("isValid") is the practical accelerator.
    - State is normally a mutable list/array — push then pop.

ALGORITHM / APPROACH:
    Four canonical problems (matching the Java reference):
        1. Permutations of a list of numbers
        2. Subsets (power set)
        3. N-Queens
        4. Word Search in grid

PYTHON-SPECIFIC NOTES:
    - Lists support efficient append/pop from the right -- the natural
      backtracking primitive.
    - Use a SHARED `current` list and snapshot it with `current[:]` or
      `list(current)` when adding to the result.
    - Recursion limit (default 1000) is plenty for these problems.
    - Yield from a generator is an alternative; we use plain accumulator
      lists for clarity.

DRY RUN:
    permutations([1,2,3])
        start=0
            swap(0,0) -> [1,2,3]; start=1
                swap(1,1) -> [1,2,3]; start=2
                    swap(2,2) -> emit [1,2,3]
                swap(1,2) -> [1,3,2]; start=2
                    swap(2,2) -> emit [1,3,2]
            (unswap back to [1,2,3])
            swap(0,1) -> [2,1,3]; ...
        eventually 6 permutations emitted.

    subsets([1,2,3])
        start=0 emit []
            include 1 -> [1] (start=1) emit [1]
                include 2 -> [1,2] emit; include 3 -> [1,2,3] emit; pop
                include 3 -> [1,3] emit; pop
            pop 1
            include 2 -> [2] emit; include 3 -> [2,3] emit; pop pop
            include 3 -> [3] emit
        Result has 8 = 2^3 subsets.

    nQueens(4) yields 2 solutions:
        .Q..      ..Q.
        ...Q      Q...
        Q...      ...Q
        ..Q.      .Q..

COMPLEXITY:
    permutations    O(n * n!) time, O(n) recursion depth
    subsets         O(n * 2^n) time, O(n) recursion depth
    nQueens         worst O(n!), pruned heavily in practice
    wordSearch      O(m*n * 4^len(word))
"""

from __future__ import annotations
from typing import List


# 1. PERMUTATIONS
def permutations(nums: List[int]) -> List[List[int]]:
    """All orderings of nums."""
    result: List[List[int]] = []

    def go(start: int) -> None:
        if start == len(nums):
            result.append(nums[:])         # snapshot
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]   # choose
            go(start + 1)                                 # explore
            nums[start], nums[i] = nums[i], nums[start]   # undo

    go(0)
    return result


# 2. SUBSETS (power set)
def subsets(nums: List[int]) -> List[List[int]]:
    """All 2^n subsets of nums."""
    result: List[List[int]] = []
    current: List[int] = []

    def go(idx: int) -> None:
        result.append(current[:])          # record current subset
        for i in range(idx, len(nums)):
            current.append(nums[i])        # include
            go(i + 1)
            current.pop()                  # backtrack

    go(0)
    return result


# 3. N-QUEENS
def n_queens(n: int) -> List[List[str]]:
    """All board configurations placing n non-attacking queens on n*n board."""
    result: List[List[str]] = []
    queens = [-1] * n                       # queens[row] = column

    def is_safe(row: int, col: int) -> bool:
        for r in range(row):
            c = queens[r]
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def build_board() -> List[str]:
        return ['.' * c + 'Q' + '.' * (n - c - 1) for c in queens]

    def go(row: int) -> None:
        if row == n:
            result.append(build_board())
            return
        for col in range(n):
            if is_safe(row, col):
                queens[row] = col
                go(row + 1)
                queens[row] = -1            # backtrack

    go(0)
    return result


# 4. WORD SEARCH IN GRID
def word_search(board: List[List[str]], word: str) -> bool:
    """Find word by traversing adjacent (no diagonal, no reuse) cells."""
    m, n = len(board), len(board[0])

    def dfs(i: int, j: int, k: int) -> bool:
        if k == len(word):
            return True
        if i < 0 or i >= m or j < 0 or j >= n:
            return False
        if board[i][j] != word[k]:
            return False
        tmp = board[i][j]
        board[i][j] = '#'                   # mark visited
        found = (dfs(i + 1, j, k + 1) or
                 dfs(i - 1, j, k + 1) or
                 dfs(i, j + 1, k + 1) or
                 dfs(i, j - 1, k + 1))
        board[i][j] = tmp                   # restore
        return found

    for i in range(m):
        for j in range(n):
            if dfs(i, j, 0):
                return True
    return False


def main() -> None:
    print("=== Permutations of [1,2,3] ===")
    for p in permutations([1, 2, 3]):
        print(p)

    print("\n=== Subsets of [1,2,3] ===")
    for s in subsets([1, 2, 3]):
        print(s)

    print("\n=== 4-Queens ===")
    sols = n_queens(4)
    print("Number of solutions:", len(sols))
    for sol in sols:
        for row in sol:
            print(row)
        print('---')

    print("\n=== Word Search ===")
    grid = [list("ABCE"), list("SFCS"), list("ADEE")]
    print("Search 'ABCCED':", word_search([r[:] for r in grid], "ABCCED"))  # True
    print("Search 'SEE'  :", word_search([r[:] for r in grid], "SEE"))      # True
    print("Search 'ABCB' :", word_search([r[:] for r in grid], "ABCB"))     # False


if __name__ == "__main__":
    main()


"""
NOTES (Python vs Java):
    - Java's char[][] mutation works for word search; Python uses list[list[str]]
      so we mutate cells likewise.
    - Snapshot mutable state with `current[:]` (slice) or `list(current)`
      before appending to results — equivalent to Java's `new ArrayList<>(current)`.
    - Tuple swap `a, b = b, a` is the natural in-place swap.
    - Recursion is idiomatic and adequate for these problem sizes; switch to
      iterative-stack only if recursion-depth becomes an issue.
    - N-queens row representation uses queens[row] = column; absolute-diff
      diagonal check is identical to the Java version.
"""
