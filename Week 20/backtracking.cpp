/*
 * =============================================================================
 * Week 20 — Backtracking  (C++17)
 * =============================================================================
 *
 * Topics covered
 * --------------
 *   1. Permutations  (of distinct integers)
 *   2. Subsets  (power set)
 *   3. N-Queens
 *   4. Sudoku Solver
 *   5. Word Search  (2D grid)
 *   6. Generate Parentheses
 *
 * Complexity cheat-sheet
 * ----------------------
 *   permutations         O(n! * n)           |  Space O(n) stack + O(n! * n) output
 *   subsets              O(2^n * n)           |  Space O(n) stack + O(2^n * n) output
 *   n_queens             O(n!)               |  Space O(n)
 *   sudoku_solver        O(9^(empty cells))  |  Space O(81)
 *   word_search          O(m*n * 3^L)        |  Space O(L) stack
 *   generate_parens      O(4^n / sqrt(n))    |  Catalan number
 *
 * Build & run
 *   g++ -std=c++17 -O2 -o backtracking backtracking.cpp && ./backtracking
 * =============================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cassert>
#include <sstream>
#include <functional>

// ---------------------------------------------------------------------------
// Helper
// ---------------------------------------------------------------------------
template <typename T>
std::string vec_str(const std::vector<T>& v) {
    std::ostringstream oss;
    oss << "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i) oss << ", ";
        oss << v[i];
    }
    oss << "]";
    return oss.str();
}

template <typename T>
std::string vec2d_str(const std::vector<std::vector<T>>& v) {
    std::ostringstream oss;
    oss << "[\n";
    for (const auto& row : v) oss << "    " << vec_str(row) << "\n";
    oss << "  ]";
    return oss.str();
}

// ---------------------------------------------------------------------------
// 1. Permutations — generate all permutations of distinct integers
// ---------------------------------------------------------------------------
// Complexity:  Time O(n! * n)  |  Space O(n) recursion stack
std::vector<std::vector<int>> permutations(std::vector<int> nums) {
    std::vector<std::vector<int>> result;

    std::function<void(int)> backtrack = [&](int start) {
        if (start == static_cast<int>(nums.size())) {
            result.push_back(nums);
            return;
        }
        for (int i = start; i < static_cast<int>(nums.size()); ++i) {
            std::swap(nums[start], nums[i]);
            backtrack(start + 1);
            std::swap(nums[start], nums[i]);
        }
    };

    backtrack(0);
    return result;
}

// ---------------------------------------------------------------------------
// 2. Subsets — generate the power set
// ---------------------------------------------------------------------------
// Complexity:  Time O(2^n * n)  |  Space O(n) recursion stack
std::vector<std::vector<int>> subsets(const std::vector<int>& nums) {
    std::vector<std::vector<int>> result;
    std::vector<int> current;

    std::function<void(int)> backtrack = [&](int start) {
        result.push_back(current);
        for (int i = start; i < static_cast<int>(nums.size()); ++i) {
            current.push_back(nums[i]);
            backtrack(i + 1);
            current.pop_back();
        }
    };

    backtrack(0);
    return result;
}

// ---------------------------------------------------------------------------
// 3. N-Queens — place n queens on an n x n board
// ---------------------------------------------------------------------------
// Complexity:  Time O(n!)  |  Space O(n)
std::vector<std::vector<std::string>> n_queens(int n) {
    std::vector<std::vector<std::string>> solutions;
    std::vector<int> queens(n, -1);  // queens[row] = column

    std::vector<bool> cols(n, false);
    std::vector<bool> diag1(2 * n, false);  // row - col + n
    std::vector<bool> diag2(2 * n, false);  // row + col

    std::function<void(int)> solve = [&](int row) {
        if (row == n) {
            // Build board.
            std::vector<std::string> board(n, std::string(n, '.'));
            for (int r = 0; r < n; ++r) board[r][queens[r]] = 'Q';
            solutions.push_back(board);
            return;
        }
        for (int col = 0; col < n; ++col) {
            if (cols[col] || diag1[row - col + n] || diag2[row + col]) continue;

            queens[row] = col;
            cols[col] = diag1[row - col + n] = diag2[row + col] = true;
            solve(row + 1);
            cols[col] = diag1[row - col + n] = diag2[row + col] = false;
        }
    };

    solve(0);
    return solutions;
}

// ---------------------------------------------------------------------------
// 4. Sudoku Solver
// ---------------------------------------------------------------------------
// Complexity:  Time O(9^(empty cells)) worst case  |  Space O(81)
class SudokuSolver {
public:
    bool solve(std::vector<std::vector<int>>& board) {
        for (int r = 0; r < 9; ++r) {
            for (int c = 0; c < 9; ++c) {
                if (board[r][c] != 0) continue;

                for (int num = 1; num <= 9; ++num) {
                    if (is_valid(board, r, c, num)) {
                        board[r][c] = num;
                        if (solve(board)) return true;
                        board[r][c] = 0;
                    }
                }
                return false;  // no valid number => backtrack
            }
        }
        return true;  // all cells filled
    }

private:
    bool is_valid(const std::vector<std::vector<int>>& board, int row, int col, int num) {
        for (int i = 0; i < 9; ++i) {
            if (board[row][i] == num) return false;
            if (board[i][col] == num) return false;
        }
        int br = (row / 3) * 3, bc = (col / 3) * 3;
        for (int r = br; r < br + 3; ++r)
            for (int c = bc; c < bc + 3; ++c)
                if (board[r][c] == num) return false;
        return true;
    }
};

// ---------------------------------------------------------------------------
// 5. Word Search — find a word in a 2D grid
// ---------------------------------------------------------------------------
// Complexity:  Time O(m * n * 3^L)  |  Space O(L) recursion stack
bool word_search(std::vector<std::vector<char>>& board, const std::string& word) {
    int m = static_cast<int>(board.size());
    int n = static_cast<int>(board[0].size());
    constexpr int dx[] = {0, 0, 1, -1};
    constexpr int dy[] = {1, -1, 0, 0};

    std::function<bool(int, int, int)> dfs = [&](int r, int c, int idx) -> bool {
        if (idx == static_cast<int>(word.size())) return true;
        if (r < 0 || r >= m || c < 0 || c >= n) return false;
        if (board[r][c] != word[idx]) return false;

        char saved = board[r][c];
        board[r][c] = '#';  // mark visited

        for (int d = 0; d < 4; ++d) {
            if (dfs(r + dx[d], c + dy[d], idx + 1)) {
                board[r][c] = saved;
                return true;
            }
        }
        board[r][c] = saved;  // restore
        return false;
    };

    for (int r = 0; r < m; ++r)
        for (int c = 0; c < n; ++c)
            if (dfs(r, c, 0)) return true;
    return false;
}

// ---------------------------------------------------------------------------
// 6. Generate Parentheses — all valid combos of n pairs
// ---------------------------------------------------------------------------
// Complexity:  Time O(4^n / sqrt(n)) — nth Catalan number
std::vector<std::string> generate_parentheses(int n) {
    std::vector<std::string> result;
    std::string current;

    std::function<void(int, int)> backtrack = [&](int open, int close) {
        if (static_cast<int>(current.size()) == 2 * n) {
            result.push_back(current);
            return;
        }
        if (open < n) {
            current.push_back('(');
            backtrack(open + 1, close);
            current.pop_back();
        }
        if (close < open) {
            current.push_back(')');
            backtrack(open, close + 1);
            current.pop_back();
        }
    };

    backtrack(0, 0);
    return result;
}

// ---------------------------------------------------------------------------
// main — test cases
// ---------------------------------------------------------------------------
int main() {
    std::cout << "=== Week 20: Backtracking ===\n\n";

    // 1. Permutations
    {
        std::cout << "-- Permutations --\n";
        auto perms = permutations({1, 2, 3});
        assert(perms.size() == 6);
        std::cout << "  permutations({1,2,3}): " << perms.size() << " results\n";
        for (const auto& p : perms) std::cout << "    " << vec_str(p) << "\n";
        std::cout << "\n";
    }

    // 2. Subsets
    {
        std::cout << "-- Subsets --\n";
        auto subs = subsets({1, 2, 3});
        assert(subs.size() == 8);  // 2^3
        std::cout << "  subsets({1,2,3}): " << subs.size() << " results\n";
        for (const auto& s : subs) std::cout << "    " << vec_str(s) << "\n";
        std::cout << "\n";
    }

    // 3. N-Queens
    {
        std::cout << "-- N-Queens --\n";
        auto sols4 = n_queens(4);
        assert(sols4.size() == 2);
        std::cout << "  4-Queens: " << sols4.size() << " solutions\n";
        for (const auto& board : sols4) {
            for (const auto& row : board) std::cout << "    " << row << "\n";
            std::cout << "\n";
        }

        auto sols8 = n_queens(8);
        assert(sols8.size() == 92);
        std::cout << "  8-Queens: " << sols8.size() << " solutions\n\n";
    }

    // 4. Sudoku Solver
    {
        std::cout << "-- Sudoku Solver --\n";
        std::vector<std::vector<int>> board = {
            {5,3,0, 0,7,0, 0,0,0},
            {6,0,0, 1,9,5, 0,0,0},
            {0,9,8, 0,0,0, 0,6,0},

            {8,0,0, 0,6,0, 0,0,3},
            {4,0,0, 8,0,3, 0,0,1},
            {7,0,0, 0,2,0, 0,0,6},

            {0,6,0, 0,0,0, 2,8,0},
            {0,0,0, 4,1,9, 0,0,5},
            {0,0,0, 0,8,0, 0,7,9}
        };

        SudokuSolver solver;
        bool solved = solver.solve(board);
        assert(solved);
        assert(board[0][2] == 4);  // was 0
        std::cout << "  Solved:\n";
        for (const auto& row : board) {
            std::cout << "    ";
            for (int x : row) std::cout << x << " ";
            std::cout << "\n";
        }
        std::cout << "\n";
    }

    // 5. Word Search
    {
        std::cout << "-- Word Search --\n";
        std::vector<std::vector<char>> board = {
            {'A','B','C','E'},
            {'S','F','C','S'},
            {'A','D','E','E'}
        };
        assert(word_search(board, "ABCCED"));
        assert(!word_search(board, "ABCB"));
        std::cout << "  \"ABCCED\" found: true\n";
        std::cout << "  \"ABCB\" found:   false\n\n";
    }

    // 6. Generate Parentheses
    {
        std::cout << "-- Generate Parentheses --\n";
        auto parens = generate_parentheses(3);
        assert(parens.size() == 5);
        std::cout << "  n=3: " << parens.size() << " combinations\n";
        for (const auto& p : parens) std::cout << "    " << p << "\n";
    }

    std::cout << "\nAll Week 20 tests passed.\n";
    return 0;
}
