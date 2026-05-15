/*
 * WEEK 10 - C++ DSA
 * Topic: Matrix Basics
 * File: 1.matrix_basics.cpp
 *
 * CONCEPT:
 *     Use std::vector<std::vector<int>> as a 2D matrix.
 *     Operations: print, transpose (square in-place + general),
 *     row reverse, 90° CW/CCW rotation, naive matrix multiplication.
 *
 * KEY POINTS:
 *     - In-place transpose only works on square matrices.
 *     - 90° CW = transpose + reverse each row.
 *     - 90° CCW = reverse each row + transpose.
 *     - Naive matmul is O(m * n * k).
 *
 * ALGORITHM / APPROACH:
 *     See per-function code; same as Java/Python.
 *
 * C++-SPECIFIC NOTES:
 *     - std::reverse(row.begin(), row.end()) reverses a row.
 *     - Pre-size matrices: std::vector<std::vector<int>>(rows, std::vector<int>(cols)).
 *     - For numerical heavy lifting, prefer Eigen / xtensor / BLAS.
 *
 * DRY RUN:
 *     mat = {{1,2,3},{4,5,6},{7,8,9}}
 *     transpose -> {{1,4,7},{2,5,8},{3,6,9}}
 *     rotate 90 CW: {{7,4,1},{8,5,2},{9,6,3}}
 *     {{1,2},{3,4}} x {{5,6},{7,8}} = {{19,22},{43,50}}
 *
 * COMPLEXITY:
 *     Transpose      : O(rows*cols)
 *     Rotation       : O(n^2)
 *     Multiplication : O(m*n*k)
 */

#include <iostream>
#include <vector>
#include <algorithm>

using Matrix = std::vector<std::vector<int>>;

void printMatrix(const Matrix& mat) {
    for (const auto& row : mat) {
        std::cout << "[";
        for (std::size_t i = 0; i < row.size(); ++i)
            std::cout << row[i] << (i + 1 < row.size() ? ", " : "");
        std::cout << "]\n";
    }
    std::cout << "\n";
}

void transposeSquare(Matrix& mat) {
    int n = static_cast<int>(mat.size());
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            std::swap(mat[i][j], mat[j][i]);
}

Matrix transpose(const Matrix& mat) {
    int rows = static_cast<int>(mat.size());
    int cols = static_cast<int>(mat[0].size());
    Matrix result(cols, std::vector<int>(rows, 0));
    for (int i = 0; i < rows; ++i)
        for (int j = 0; j < cols; ++j)
            result[j][i] = mat[i][j];
    return result;
}

void reverseRows(Matrix& mat) {
    for (auto& row : mat)
        std::reverse(row.begin(), row.end());
}

void rotate90CW(Matrix& mat) {
    transposeSquare(mat);
    reverseRows(mat);
}

void rotate90CCW(Matrix& mat) {
    reverseRows(mat);
    transposeSquare(mat);
}

Matrix multiply(const Matrix& A, const Matrix& B) {
    int m = static_cast<int>(A.size());
    int k = static_cast<int>(A[0].size());
    int n = static_cast<int>(B[0].size());
    Matrix C(m, std::vector<int>(n, 0));
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            for (int p = 0; p < k; ++p)
                C[i][j] += A[i][p] * B[p][j];
    return C;
}

int main() {
    Matrix mat = {{1,2,3},{4,5,6},{7,8,9}};
    std::cout << "Original:\n"; printMatrix(mat);

    Matrix mat2 = mat;
    transposeSquare(mat2);
    std::cout << "Transposed (square, in-place):\n"; printMatrix(mat2);

    Matrix nonSquare = {{1,2,3},{4,5,6}};
    std::cout << "Non-square (2x3):\n"; printMatrix(nonSquare);
    std::cout << "Transposed (3x2):\n"; printMatrix(transpose(nonSquare));

    Matrix mat3 = mat;
    rotate90CW(mat3);
    std::cout << "Rotated 90° CW:\n"; printMatrix(mat3);
    // Expected: {{7,4,1},{8,5,2},{9,6,3}}

    Matrix A = {{1,2},{3,4}};
    Matrix B = {{5,6},{7,8}};
    std::cout << "A x B:\n"; printMatrix(multiply(A, B));
    // {{19,22},{43,50}}

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - std::vector<std::vector<int>> is the natural 2D container.
 *     - std::swap and std::reverse provide the primitive ops.
 *     - For production numeric work, Eigen and xtensor offer high-performance
 *       expression templates and BLAS-backed matmul.
 */
