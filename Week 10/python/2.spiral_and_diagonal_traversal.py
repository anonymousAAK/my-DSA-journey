"""
WEEK 10 - PYTHON DSA
Topic: Spiral & Diagonal Traversal + Sorted-Matrix Search
File: 2.spiral_and_diagonal_traversal.py

CONCEPT:
    Spiral traversal walks the perimeter inward: right -> down -> left -> up,
    shrinking boundaries each lap.
    Diagonal (anti-diagonal zigzag) traversal alternates direction on each
    diagonal index.
    Row/column-sorted-matrix search starts at the top-right and moves
    left/down to eliminate a row or column per step.

KEY POINTS:
    - Spiral: maintain four boundaries (top, bottom, left, right).
    - Diagonal: iterate d from 0 to m+n-2; even d goes up-right, odd goes down-left.
    - Sorted-matrix search: O(m + n) instead of O(m*n) brute force.

ALGORITHM / APPROACH:
    Spiral:
        while top <= bottom and left <= right:
            traverse top row    [left..right];  top++
            traverse right col  [top..bottom];  right--
            if top <= bottom: traverse bottom row [right..left]; bottom--
            if left <= right: traverse left col   [bottom..top]; left++

    Diagonal:
        for d in 0..m+n-2:
            if d even: start (min(d,m-1), d - min(d,m-1)); walk r--, c++
            else:      start (d - min(d,n-1), min(d,n-1)); walk r++, c--

    Sorted-matrix search:
        start at top-right; if equal -> found; if > target -> col--; else row++

PYTHON-SPECIFIC NOTES:
    - Tuple unpacking and ranges (range(start, stop, -1)) keep traversal concise.
    - any() / all() not directly used here, but lists naturally hold the result.

DRY RUN:
    Spiral on:
        1 2 3 4
        5 6 7 8
        9 10 11 12
    => [1,2,3,4,8,12,11,10,9,5,6,7]

    Diagonal zigzag on:
        1 2 3
        4 5 6
        7 8 9
    => [1, 2,4, 7,5,3, 6,8, 9]

COMPLEXITY:
    Spiral / Diagonal: O(m*n) time, O(m*n) for output.
    Sorted search    : O(m + n) time, O(1) space.
"""

from typing import List

Matrix = List[List[int]]


def spiral_order(mat: Matrix) -> List[int]:
    result: List[int] = []
    if not mat or not mat[0]:
        return result
    top, bottom = 0, len(mat) - 1
    left, right = 0, len(mat[0]) - 1
    while top <= bottom and left <= right:
        # right along top row
        for i in range(left, right + 1):
            result.append(mat[top][i])
        top += 1
        # down along right column
        for i in range(top, bottom + 1):
            result.append(mat[i][right])
        right -= 1
        # left along bottom row
        if top <= bottom:
            for i in range(right, left - 1, -1):
                result.append(mat[bottom][i])
            bottom -= 1
        # up along left column
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(mat[i][left])
            left += 1
    return result


def diagonal_order(mat: Matrix) -> List[int]:
    """Anti-diagonal zigzag traversal."""
    m, n = len(mat), len(mat[0])
    result: List[int] = []
    for d in range(m + n - 1):
        if d % 2 == 0:  # going up
            r = min(d, m - 1)
            c = d - r
            while r >= 0 and c < n:
                result.append(mat[r][c])
                r -= 1
                c += 1
        else:  # going down
            c = min(d, n - 1)
            r = d - c
            while c >= 0 and r < m:
                result.append(mat[r][c])
                r += 1
                c -= 1
    return result


def search_sorted_matrix(mat: Matrix, target: int) -> bool:
    """Row- and column-sorted matrix search starting from top-right."""
    if not mat or not mat[0]:
        return False
    row, col = 0, len(mat[0]) - 1
    while row < len(mat) and col >= 0:
        if mat[row][col] == target:
            return True
        elif mat[row][col] > target:
            col -= 1
        else:
            row += 1
    return False


def main() -> None:
    mat = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]
    print("Matrix:")
    for row in mat:
        print(row)
    print(f"\nSpiral order: {spiral_order(mat)}")
    # Expected: [1,2,3,4,8,12,11,10,9,5,6,7]

    sq = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("\nSquare matrix:")
    for row in sq:
        print(row)
    print(f"Spiral:   {spiral_order(sq)}")
    print(f"Diagonal: {diagonal_order(sq)}")
    # Expected diagonal: [1,2,4,7,5,3,6,8,9]

    sorted_mat = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30],
    ]
    print("\nSearch in sorted matrix:")
    print(f"Search 5:  {search_sorted_matrix(sorted_mat, 5)}")   # True
    print(f"Search 20: {search_sorted_matrix(sorted_mat, 20)}")  # False
    print(f"Search 1:  {search_sorted_matrix(sorted_mat, 1)}")   # True
    print(f"Search 30: {search_sorted_matrix(sorted_mat, 30)}")  # True


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - range(start, stop, -1) handles descending loops cleanly.
    - List append + list literals replace Java ArrayList/Arrays.
    - The four-boundary spiral idiom is identical across languages.
"""
