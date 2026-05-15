/*
 * WEEK 10 - C++ DSA
 * Topic: Spiral & Diagonal Traversal + Sorted-Matrix Search
 * File: 2.spiral_and_diagonal_traversal.cpp
 *
 * CONCEPT:
 *     Spiral: walk the perimeter inward, shrinking four boundaries.
 *     Diagonal: alternate direction per anti-diagonal index.
 *     Sorted-matrix search: top-right corner walk in O(m + n).
 *
 * KEY POINTS:
 *     - Spiral uses four bound variables (top, bottom, left, right).
 *     - Diagonal index d ranges 0..m+n-2; even d goes up-right.
 *     - Sorted search eliminates a row or column per comparison.
 *
 * ALGORITHM / APPROACH:
 *     See per-function code; same as Java/Python.
 *
 * C++-SPECIFIC NOTES:
 *     - std::vector<int> for the linear output.
 *     - std::min for diagonal start clamping.
 *
 * DRY RUN:
 *     Spiral on 3x4 -> [1,2,3,4,8,12,11,10,9,5,6,7]
 *     Diagonal on 3x3 -> [1, 2,4, 7,5,3, 6,8, 9]
 *
 * COMPLEXITY:
 *     Spiral / Diagonal: O(m*n) time, O(m*n) for the output.
 *     Sorted-matrix search: O(m + n) time, O(1) space.
 */

#include <iostream>
#include <vector>
#include <algorithm>

using Matrix = std::vector<std::vector<int>>;

std::vector<int> spiralOrder(const Matrix& mat) {
    std::vector<int> result;
    if (mat.empty() || mat[0].empty()) return result;
    int top = 0, bottom = static_cast<int>(mat.size()) - 1;
    int left = 0, right = static_cast<int>(mat[0].size()) - 1;
    while (top <= bottom && left <= right) {
        // right along top row
        for (int i = left; i <= right; ++i) result.push_back(mat[top][i]);
        ++top;
        // down along right column
        for (int i = top; i <= bottom; ++i) result.push_back(mat[i][right]);
        --right;
        // left along bottom row
        if (top <= bottom) {
            for (int i = right; i >= left; --i) result.push_back(mat[bottom][i]);
            --bottom;
        }
        // up along left column
        if (left <= right) {
            for (int i = bottom; i >= top; --i) result.push_back(mat[i][left]);
            ++left;
        }
    }
    return result;
}

std::vector<int> diagonalOrder(const Matrix& mat) {
    int m = static_cast<int>(mat.size());
    int n = static_cast<int>(mat[0].size());
    std::vector<int> result;
    result.reserve(static_cast<std::size_t>(m) * n);
    for (int d = 0; d < m + n - 1; ++d) {
        if (d % 2 == 0) { // going up
            int r = std::min(d, m - 1);
            int c = d - r;
            while (r >= 0 && c < n) {
                result.push_back(mat[r][c]);
                --r; ++c;
            }
        } else {          // going down
            int c = std::min(d, n - 1);
            int r = d - c;
            while (c >= 0 && r < m) {
                result.push_back(mat[r][c]);
                ++r; --c;
            }
        }
    }
    return result;
}

bool searchSortedMatrix(const Matrix& mat, int target) {
    if (mat.empty() || mat[0].empty()) return false;
    int row = 0, col = static_cast<int>(mat[0].size()) - 1;
    int rows = static_cast<int>(mat.size());
    while (row < rows && col >= 0) {
        if (mat[row][col] == target) return true;
        else if (mat[row][col] > target) --col;
        else ++row;
    }
    return false;
}

void printVec(const std::vector<int>& v) {
    std::cout << "[";
    for (std::size_t i = 0; i < v.size(); ++i)
        std::cout << v[i] << (i + 1 < v.size() ? ", " : "");
    std::cout << "]";
}

int main() {
    Matrix mat = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12}
    };

    std::cout << "Matrix:\n";
    for (const auto& row : mat) { printVec(row); std::cout << "\n"; }

    std::cout << "\nSpiral order: "; printVec(spiralOrder(mat)); std::cout << "\n";

    Matrix sq = {{1,2,3},{4,5,6},{7,8,9}};
    std::cout << "\nSquare matrix:\n";
    for (const auto& row : sq) { printVec(row); std::cout << "\n"; }
    std::cout << "Spiral:   "; printVec(spiralOrder(sq));   std::cout << "\n";
    std::cout << "Diagonal: "; printVec(diagonalOrder(sq)); std::cout << "\n";

    Matrix sorted = {
        { 1,  4,  7, 11, 15},
        { 2,  5,  8, 12, 19},
        { 3,  6,  9, 16, 22},
        {10, 13, 14, 17, 24},
        {18, 21, 23, 26, 30}
    };
    std::cout << "\nSearch in sorted matrix:\n";
    std::cout << "Search 5:  " << (searchSortedMatrix(sorted,  5) ? "true" : "false") << "\n";
    std::cout << "Search 20: " << (searchSortedMatrix(sorted, 20) ? "true" : "false") << "\n";
    std::cout << "Search 1:  " << (searchSortedMatrix(sorted,  1) ? "true" : "false") << "\n";
    std::cout << "Search 30: " << (searchSortedMatrix(sorted, 30) ? "true" : "false") << "\n";

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - using Matrix = std::vector<std::vector<int>>; aliases the type.
 *     - .reserve() preallocates capacity to avoid reallocations.
 *     - std::min from <algorithm> handles diagonal start clamping.
 */
