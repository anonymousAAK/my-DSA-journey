"""
WEEK 10 - PYTHON DSA
Topic: Matrix Basics — Traversal, Transpose, Rotation, Multiplication
File: 1.matrix_basics.py

CONCEPT:
    A matrix is a list of equal-length lists: rows of columns.
    Element at row i, column j: mat[i][j].

KEY POINTS:
    - Transpose swaps rows and columns; in-place is possible for square
      matrices; non-square needs a new matrix.
    - 90° rotation (square, in-place) = transpose then reverse each row.
    - Matrix multiplication is O(n^3) naive.

ALGORITHM / APPROACH:
    Transpose (square, in-place):
        for i in range(n):
            for j in range(i + 1, n):
                mat[i][j], mat[j][i] = mat[j][i], mat[i][j]
    Transpose (general):
        result[j][i] = mat[i][j]
    Rotate 90° CW:
        transpose + reverse each row
    Rotate 90° CCW:
        reverse each row + transpose
    Multiply A (m×k) by B (k×n):
        C[i][j] = sum_p A[i][p] * B[p][j]

PYTHON-SPECIFIC NOTES:
    - Use list comprehensions to allocate 2D arrays: [[0]*cols for _ in range(rows)].
    - NEVER do `[[0]*cols]*rows`: that aliases the same inner list!
    - zip(*mat) gives a transpose iterator: list(zip(*mat)) for general.
    - For numeric work, NumPy is the production choice.

DRY RUN:
    mat = [[1,2,3],[4,5,6],[7,8,9]]
    transpose -> [[1,4,7],[2,5,8],[3,6,9]]
    rotate 90 CW:
        transpose:        [[1,4,7],[2,5,8],[3,6,9]]
        reverse each row: [[7,4,1],[8,5,2],[9,6,3]]
    multiply [[1,2],[3,4]] x [[5,6],[7,8]]:
        [[19,22],[43,50]]

COMPLEXITY:
    Transpose      : O(rows*cols) time, O(1) in-place / O(r*c) general
    Rotation       : O(n^2) time, O(1) for in-place square
    Multiplication : O(m*n*k) time, O(m*n) space for result
"""

from typing import List

Matrix = List[List[int]]


def print_matrix(mat: Matrix) -> None:
    for row in mat:
        print(row)
    print()


def transpose_square(mat: Matrix) -> None:
    """In-place transpose for square matrices."""
    n = len(mat)
    for i in range(n):
        for j in range(i + 1, n):
            mat[i][j], mat[j][i] = mat[j][i], mat[i][j]


def transpose(mat: Matrix) -> Matrix:
    """Returns a new transposed matrix; works for non-square."""
    rows, cols = len(mat), len(mat[0])
    result: Matrix = [[0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            result[j][i] = mat[i][j]
    return result


def reverse_rows(mat: Matrix) -> None:
    for row in mat:
        l, r = 0, len(row) - 1
        while l < r:
            row[l], row[r] = row[r], row[l]
            l += 1
            r -= 1


def rotate_90_cw(mat: Matrix) -> None:
    """90° clockwise in-place for square matrix."""
    transpose_square(mat)
    reverse_rows(mat)


def rotate_90_ccw(mat: Matrix) -> None:
    """90° counter-clockwise in-place for square matrix."""
    reverse_rows(mat)
    transpose_square(mat)


def multiply(A: Matrix, B: Matrix) -> Matrix:
    """Naive O(m*n*k) matrix multiplication."""
    m, k = len(A), len(A[0])
    n = len(B[0])
    C: Matrix = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for p in range(k):
                C[i][j] += A[i][p] * B[p][j]
    return C


def main() -> None:
    mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("Original:")
    print_matrix(mat)

    mat2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    transpose_square(mat2)
    print("Transposed (square, in-place):")
    print_matrix(mat2)

    non_square = [[1, 2, 3], [4, 5, 6]]
    print("Non-square (2x3):")
    print_matrix(non_square)
    print("Transposed (3x2):")
    print_matrix(transpose(non_square))

    mat3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate_90_cw(mat3)
    print("Rotated 90° CW:")
    print_matrix(mat3)

    # Multiplication
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    print("A x B:")
    print_matrix(multiply(A, B))

    # Pythonic transpose via zip
    print("Transpose via zip (Pythonic):")
    print([list(row) for row in zip(*[[1, 2, 3], [4, 5, 6]])])


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - 2D arrays are lists of lists; pre-allocate with list comprehensions.
    - zip(*mat) does the general transpose in one expression.
    - For real numeric work use NumPy: np.transpose, np.rot90, np.matmul.
    - Tuple swap shortens in-place transpose to a single line per pair.
"""
