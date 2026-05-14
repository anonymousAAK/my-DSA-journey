"""
Week 10 — 2D Arrays / Matrices
================================
Topics covered:
  - Transpose: in-place (square matrix) + general (any m x n)
  - Rotate 90 degrees clockwise
  - Matrix multiplication
  - Spiral traversal
  - Diagonal traversal
  - Search in a row-and-column sorted matrix (staircase search)
  - Pascal's triangle

Each function includes time/space complexity analysis in its docstring.
"""

from __future__ import annotations

from typing import List

# Type alias for readability
Matrix = List[List[int]]


# ---------------------------------------------------------------------------
# Transpose
# ---------------------------------------------------------------------------

def transpose_square_inplace(matrix: Matrix) -> Matrix:
    """Transpose a square (n x n) matrix in-place by swapping matrix[i][j]
    with matrix[j][i] for i < j.

    Time:  O(n^2)
    Space: O(1)
    """
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    return matrix


def transpose_general(matrix: Matrix) -> Matrix:
    """Transpose an m x n matrix, returning a new n x m matrix.

    Time:  O(m * n)
    Space: O(m * n)
    """
    if not matrix or not matrix[0]:
        return []
    rows, cols = len(matrix), len(matrix[0])
    return [[matrix[r][c] for r in range(rows)] for c in range(cols)]


# ---------------------------------------------------------------------------
# Rotate 90° Clockwise
# ---------------------------------------------------------------------------

def rotate_90_clockwise(matrix: Matrix) -> Matrix:
    """Rotate an n x n matrix 90 degrees clockwise in-place.

    Algorithm: transpose, then reverse each row.

    Time:  O(n^2)
    Space: O(1)  — done in-place
    """
    n = len(matrix)
    # Step 1: transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Step 2: reverse each row
    for row in matrix:
        row.reverse()
    return matrix


# ---------------------------------------------------------------------------
# Matrix Multiplication
# ---------------------------------------------------------------------------

def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    """Multiply matrix *a* (m x n) by matrix *b* (n x p) → (m x p).

    Time:  O(m * n * p)
    Space: O(m * p)  — the result matrix
    """
    m, n, p = len(a), len(a[0]), len(b[0])
    assert len(b) == n, "Inner dimensions must match"

    result = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            result[i][j] = sum(a[i][k] * b[k][j] for k in range(n))
    return result


# ---------------------------------------------------------------------------
# Spiral Traversal
# ---------------------------------------------------------------------------

def spiral_traversal(matrix: Matrix) -> List[int]:
    """Return elements of *matrix* in spiral (clockwise) order.

    Time:  O(m * n)
    Space: O(1)  — excluding the output list
    """
    if not matrix or not matrix[0]:
        return []

    result: list[int] = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Traverse right
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1

        # Traverse down
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1

        # Traverse left
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1

        # Traverse up
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1

    return result


# ---------------------------------------------------------------------------
# Diagonal Traversal
# ---------------------------------------------------------------------------

def diagonal_traversal(matrix: Matrix) -> List[int]:
    """Traverse the matrix diagonally (top-right to bottom-left), alternating
    direction on each diagonal — as in LeetCode 498.

    Time:  O(m * n)
    Space: O(1)  — excluding the output list
    """
    if not matrix or not matrix[0]:
        return []

    m, n = len(matrix), len(matrix[0])
    result: list[int] = []
    # There are m + n - 1 diagonals, indexed by (row + col).
    for d in range(m + n - 1):
        if d % 2 == 0:
            # Even diagonal: go upward (row decreases, col increases)
            r = min(d, m - 1)
            c = d - r
            while r >= 0 and c < n:
                result.append(matrix[r][c])
                r -= 1
                c += 1
        else:
            # Odd diagonal: go downward (row increases, col decreases)
            c = min(d, n - 1)
            r = d - c
            while c >= 0 and r < m:
                result.append(matrix[r][c])
                r += 1
                c -= 1
    return result


# ---------------------------------------------------------------------------
# Search in Row-and-Column Sorted Matrix (Staircase Search)
# ---------------------------------------------------------------------------

def search_sorted_matrix(matrix: Matrix, target: int) -> tuple[int, int] | None:
    """Search for *target* in a matrix where each row and each column is
    sorted in ascending order.

    Start from the top-right corner:
      - If current == target → found
      - If current > target  → move left  (eliminate column)
      - If current < target  → move down  (eliminate row)

    Time:  O(m + n)
    Space: O(1)
    """
    if not matrix or not matrix[0]:
        return None

    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1

    while row < m and col >= 0:
        val = matrix[row][col]
        if val == target:
            return (row, col)
        elif val > target:
            col -= 1
        else:
            row += 1

    return None


# ---------------------------------------------------------------------------
# Pascal's Triangle
# ---------------------------------------------------------------------------

def pascals_triangle(num_rows: int) -> List[List[int]]:
    """Generate the first *num_rows* rows of Pascal's triangle.

    Each element is the sum of the two elements directly above it.

    Time:  O(n^2)  — total number of elements
    Space: O(n^2)  — storing all rows
    """
    if num_rows <= 0:
        return []

    triangle: list[list[int]] = [[1]]
    for i in range(1, num_rows):
        prev = triangle[-1]
        # Each row starts and ends with 1; interior elements are sums
        row = [1] + [prev[j] + prev[j + 1] for j in range(len(prev) - 1)] + [1]
        triangle.append(row)
    return triangle


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ---- Transpose ----
    sq = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    transpose_square_inplace(sq)
    assert sq == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

    rect = [[1, 2, 3], [4, 5, 6]]
    assert transpose_general(rect) == [[1, 4], [2, 5], [3, 6]]
    print("[PASS] Transpose — square in-place & general")

    # ---- Rotate 90° ----
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate_90_clockwise(m)
    assert m == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    print("[PASS] Rotate 90° clockwise")

    # ---- Matrix Multiplication ----
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    assert matrix_multiply(a, b) == [[19, 22], [43, 50]]

    # Non-square: (2x3) * (3x2)
    a2 = [[1, 2, 3], [4, 5, 6]]
    b2 = [[7, 8], [9, 10], [11, 12]]
    assert matrix_multiply(a2, b2) == [[58, 64], [139, 154]]
    print("[PASS] Matrix multiplication")

    # ---- Spiral ----
    assert spiral_traversal([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]

    assert spiral_traversal([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    print("[PASS] Spiral traversal")

    # ---- Diagonal ----
    assert diagonal_traversal([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]) == [1, 2, 4, 7, 5, 3, 6, 8, 9]
    print("[PASS] Diagonal traversal")

    # ---- Staircase Search ----
    sorted_m = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30],
    ]
    assert search_sorted_matrix(sorted_m, 5) == (1, 1)
    assert search_sorted_matrix(sorted_m, 20) is None
    assert search_sorted_matrix(sorted_m, 18) == (4, 0)
    print("[PASS] Search in row-and-column sorted matrix")

    # ---- Pascal's Triangle ----
    pt = pascals_triangle(5)
    assert pt == [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
    ]
    assert pascals_triangle(0) == []
    print("[PASS] Pascal's triangle")

    print("\nAll Week 10 tests passed!")
