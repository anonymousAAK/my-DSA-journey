/*
 * =============================================================================
 * Week 10 - Matrix Operations (C++ Edition)
 * =============================================================================
 *
 * Topics Covered:
 *   1. Transpose a matrix
 *   2. Rotate 90 degrees clockwise (in-place for square matrix)
 *   3. Matrix multiplication
 *   4. Spiral traversal
 *   5. Diagonal traversal
 *   6. Search in row-wise and column-wise sorted matrix (staircase search)
 *   7. Pascal's Triangle
 *
 * Complexity Analysis provided for every function.
 * Uses modern C++17 features where appropriate.
 * =============================================================================
 */

#include <bits/stdc++.h>
using namespace std;

using Matrix = vector<vector<int>>;

// =============================================================================
// HELPER: print matrix
// =============================================================================
void printMatrix(const Matrix& mat, const string& label = "") {
    if (!label.empty()) cout << label << ":" << endl;
    for (const auto& row : mat) {
        cout << "  [";
        for (size_t j = 0; j < row.size(); ++j) {
            cout << setw(3) << row[j] << (j + 1 < row.size() ? "," : "");
        }
        cout << " ]" << endl;
    }
}

void printVec(const vector<int>& v, const string& label = "") {
    if (!label.empty()) cout << label << ": ";
    cout << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        cout << v[i] << (i + 1 < v.size() ? ", " : "");
    }
    cout << "]" << endl;
}

// =============================================================================
// 1. TRANSPOSE
// =============================================================================
// Time: O(m * n)   Space: O(m * n) for new matrix
Matrix transpose(const Matrix& mat) {
    if (mat.empty()) return {};
    int m = mat.size(), n = mat[0].size();
    Matrix result(n, vector<int>(m));
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            result[j][i] = mat[i][j];
    return result;
}

// In-place transpose for square matrix
// Time: O(n^2)   Space: O(1)
void transposeInPlace(Matrix& mat) {
    int n = mat.size();
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            swap(mat[i][j], mat[j][i]);
}

// =============================================================================
// 2. ROTATE 90 DEGREES CLOCKWISE
// =============================================================================
// Method: Transpose + reverse each row
// Time: O(n^2)   Space: O(1) in-place for square matrix
void rotate90Clockwise(Matrix& mat) {
    transposeInPlace(mat);
    for (auto& row : mat) {
        reverse(row.begin(), row.end());
    }
}

// Rotate 90 degrees counter-clockwise: transpose + reverse each column
// (or equivalently: reverse each row, then transpose)
// Time: O(n^2)   Space: O(1)
void rotate90CounterClockwise(Matrix& mat) {
    transposeInPlace(mat);
    int n = mat.size();
    for (int j = 0; j < n; ++j) {
        for (int i = 0, k = n - 1; i < k; ++i, --k) {
            swap(mat[i][j], mat[k][j]);
        }
    }
}

// =============================================================================
// 3. MATRIX MULTIPLICATION
// =============================================================================
// A is m x p, B is p x n => result is m x n
// Time: O(m * n * p)   Space: O(m * n)
Matrix multiply(const Matrix& A, const Matrix& B) {
    int m = A.size(), p = A[0].size(), n = B[0].size();
    Matrix C(m, vector<int>(n, 0));
    for (int i = 0; i < m; ++i)
        for (int k = 0; k < p; ++k)         // loop order ikj for cache friendliness
            for (int j = 0; j < n; ++j)
                C[i][j] += A[i][k] * B[k][j];
    return C;
}

// =============================================================================
// 4. SPIRAL TRAVERSAL
// =============================================================================
// Time: O(m * n)   Space: O(m * n) for result
vector<int> spiralOrder(const Matrix& mat) {
    vector<int> result;
    if (mat.empty()) return result;

    int top = 0, bottom = mat.size() - 1;
    int left = 0, right = mat[0].size() - 1;

    while (top <= bottom && left <= right) {
        // Traverse right
        for (int j = left; j <= right; ++j)
            result.push_back(mat[top][j]);
        ++top;

        // Traverse down
        for (int i = top; i <= bottom; ++i)
            result.push_back(mat[i][right]);
        --right;

        // Traverse left
        if (top <= bottom) {
            for (int j = right; j >= left; --j)
                result.push_back(mat[bottom][j]);
            --bottom;
        }

        // Traverse up
        if (left <= right) {
            for (int i = bottom; i >= top; --i)
                result.push_back(mat[i][left]);
            ++left;
        }
    }
    return result;
}

// =============================================================================
// 5. DIAGONAL TRAVERSAL
// =============================================================================
// Traverse diagonals from top-right to bottom-left, alternating direction.
// Time: O(m * n)   Space: O(m * n) for result
vector<int> diagonalTraversal(const Matrix& mat) {
    if (mat.empty()) return {};
    int m = mat.size(), n = mat[0].size();
    vector<int> result;
    result.reserve(m * n);

    // There are (m + n - 1) diagonals
    for (int d = 0; d < m + n - 1; ++d) {
        if (d % 2 == 0) {
            // Go upward: from (min(d, m-1), d - min(d, m-1)) upward
            int r = min(d, m - 1);
            int c = d - r;
            while (r >= 0 && c < n) {
                result.push_back(mat[r][c]);
                --r;
                ++c;
            }
        } else {
            // Go downward: from (d - min(d, n-1), min(d, n-1)) downward
            int c = min(d, n - 1);
            int r = d - c;
            while (c >= 0 && r < m) {
                result.push_back(mat[r][c]);
                ++r;
                --c;
            }
        }
    }
    return result;
}

// =============================================================================
// 6. SEARCH IN SORTED MATRIX (Staircase / Step Search)
// =============================================================================
// Matrix rows are sorted left to right, columns sorted top to bottom.
// Start from top-right corner.
// Time: O(m + n)   Space: O(1)
pair<int, int> searchSortedMatrix(const Matrix& mat, int target) {
    if (mat.empty()) return {-1, -1};
    int m = mat.size(), n = mat[0].size();
    int r = 0, c = n - 1;  // start top-right

    while (r < m && c >= 0) {
        if (mat[r][c] == target) return {r, c};
        else if (mat[r][c] > target) --c;  // go left
        else ++r;                           // go down
    }
    return {-1, -1};  // not found
}

// =============================================================================
// 7. PASCAL'S TRIANGLE
// =============================================================================
// Time: O(n^2)   Space: O(n^2)
Matrix pascalsTriangle(int numRows) {
    Matrix triangle;
    for (int i = 0; i < numRows; ++i) {
        triangle.emplace_back(i + 1, 1);  // row of (i+1) ones
        for (int j = 1; j < i; ++j) {
            triangle[i][j] = triangle[i - 1][j - 1] + triangle[i - 1][j];
        }
    }
    return triangle;
}

// =============================================================================
// MAIN — Test Cases
// =============================================================================
int main() {
    cout << "========================================" << endl;
    cout << " Week 10: Matrix Operations (C++)" << endl;
    cout << "========================================" << endl;

    // --- 1. Transpose ---
    cout << "\n--- 1. Transpose ---" << endl;
    {
        Matrix mat = {{1, 2, 3}, {4, 5, 6}};
        printMatrix(mat, "Original (2x3)");
        printMatrix(transpose(mat), "Transposed (3x2)");
    }

    // --- 2. Rotate 90 ---
    cout << "\n--- 2. Rotate 90 Degrees ---" << endl;
    {
        Matrix mat = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        printMatrix(mat, "Original");
        rotate90Clockwise(mat);
        printMatrix(mat, "Clockwise 90");

        Matrix mat2 = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        rotate90CounterClockwise(mat2);
        printMatrix(mat2, "Counter-clockwise 90");
    }

    // --- 3. Matrix Multiply ---
    cout << "\n--- 3. Matrix Multiplication ---" << endl;
    {
        Matrix A = {{1, 2}, {3, 4}};
        Matrix B = {{5, 6}, {7, 8}};
        printMatrix(A, "A");
        printMatrix(B, "B");
        printMatrix(multiply(A, B), "A x B");
        // Expected: [[19,22],[43,50]]
    }

    // --- 4. Spiral Traversal ---
    cout << "\n--- 4. Spiral Traversal ---" << endl;
    {
        Matrix mat = {{1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12}};
        printMatrix(mat, "Matrix");
        printVec(spiralOrder(mat), "Spiral");
        // Expected: [1,2,3,4,8,12,11,10,9,5,6,7]
    }

    // --- 5. Diagonal Traversal ---
    cout << "\n--- 5. Diagonal Traversal ---" << endl;
    {
        Matrix mat = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        printMatrix(mat, "Matrix");
        printVec(diagonalTraversal(mat), "Diagonal");
        // Expected: [1, 2, 4, 7, 5, 3, 6, 8, 9]
    }

    // --- 6. Search in Sorted Matrix ---
    cout << "\n--- 6. Search in Sorted Matrix ---" << endl;
    {
        Matrix mat = {
            {10, 20, 30, 40},
            {15, 25, 35, 45},
            {27, 29, 37, 48},
            {32, 33, 39, 50}
        };
        printMatrix(mat, "Matrix");
        for (int target : {29, 35, 50, 100}) {
            auto [r, c] = searchSortedMatrix(mat, target);
            cout << "Search " << target << ": ";
            if (r == -1) cout << "not found" << endl;
            else cout << "found at (" << r << ", " << c << ")" << endl;
        }
    }

    // --- 7. Pascal's Triangle ---
    cout << "\n--- 7. Pascal's Triangle ---" << endl;
    {
        auto triangle = pascalsTriangle(6);
        for (size_t i = 0; i < triangle.size(); ++i) {
            // Center alignment for visual appearance
            string padding(2 * (triangle.size() - i - 1), ' ');
            cout << padding;
            for (size_t j = 0; j < triangle[i].size(); ++j) {
                cout << setw(3) << triangle[i][j] << " ";
            }
            cout << endl;
        }
    }

    cout << "\n========================================" << endl;
    cout << " All Week 10 tests complete!" << endl;
    cout << "========================================" << endl;
    return 0;
}
