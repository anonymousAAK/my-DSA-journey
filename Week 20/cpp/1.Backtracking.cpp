/*
 * WEEK 20 - C++ DSA
 * Topic: Backtracking — Template + Classic Problems
 * File: 1.Backtracking.cpp
 *
 * CONCEPT:
 *     Backtracking builds a candidate solution one piece at a time. After
 *     each extension, it checks whether the partial solution can still lead
 *     to a valid full answer; if not, it ABANDONS the branch and undoes
 *     the last choice.
 *
 * TEMPLATE:
 *     void backtrack(State& s) {
 *         if (isSolution(s)) { record(s); return; }
 *         for (Choice c : choices(s)) {
 *             if (isValid(c, s)) {
 *                 apply(c, s);          // choose
 *                 backtrack(s);         // explore
 *                 undo(c, s);           // backtrack
 *             }
 *         }
 *     }
 *
 * KEY POINTS:
 *     - Worst-case complexity is exponential (O(k^n) or O(n!)).
 *     - Pruning (isValid) gives the practical speed-up.
 *     - Use mutable state passed by reference; emplace_back + pop_back to
 *       grow/shrink the partial solution.
 *
 * ALGORITHM / APPROACH:
 *     Four canonical problems (matching the Java reference):
 *         1. Permutations of a list of numbers
 *         2. Subsets (power set)
 *         3. N-Queens
 *         4. Word Search in a 2-D grid
 *
 * C++-SPECIFIC NOTES:
 *     - Use std::vector<int> for the mutable state; push_back / pop_back
 *       in O(1) amortised.
 *     - Snapshot results with `result.push_back(state)` (copy) or move.
 *     - std::swap is constexpr and noexcept; perfect for permutation swap.
 *     - For word search, mutating the input char grid is fast; restore in
 *       the unwind.
 *
 * DRY RUN:
 *     permutations({1,2,3}) -> 6 vectors:
 *         [1,2,3] [1,3,2] [2,1,3] [2,3,1] [3,2,1] [3,1,2]
 *     subsets({1,2,3}) -> 8 (size 2^3).
 *     nQueens(4) -> 2 solutions.
 *     wordSearch grid="ABCE/SFCS/ADEE", "ABCCED" -> true; "ABCB" -> false.
 *
 * COMPLEXITY:
 *     permutations    O(n * n!) time
 *     subsets         O(n * 2^n) time
 *     nQueens         worst O(n!), pruned in practice
 *     wordSearch      O(m*n * 4^len(word))
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using std::vector;
using std::string;

// 1. PERMUTATIONS
void permuteHelper(vector<int>& nums, int start, vector<vector<int>>& out) {
    if (start == (int)nums.size()) { out.push_back(nums); return; }
    for (int i = start; i < (int)nums.size(); ++i) {
        std::swap(nums[start], nums[i]);     // choose
        permuteHelper(nums, start + 1, out); // explore
        std::swap(nums[start], nums[i]);     // undo
    }
}
vector<vector<int>> permutations(vector<int> nums) {
    vector<vector<int>> out;
    permuteHelper(nums, 0, out);
    return out;
}

// 2. SUBSETS
void subsetsHelper(const vector<int>& nums, int idx,
                   vector<int>& current, vector<vector<int>>& out) {
    out.push_back(current);
    for (int i = idx; i < (int)nums.size(); ++i) {
        current.push_back(nums[i]);
        subsetsHelper(nums, i + 1, current, out);
        current.pop_back();
    }
}
vector<vector<int>> subsets(const vector<int>& nums) {
    vector<vector<int>> out;
    vector<int> current;
    subsetsHelper(nums, 0, current, out);
    return out;
}

// 3. N-QUEENS
bool isSafe(const vector<int>& queens, int row, int col) {
    for (int r = 0; r < row; ++r) {
        int c = queens[r];
        if (c == col) return false;
        if (std::abs(c - col) == std::abs(r - row)) return false;
    }
    return true;
}
vector<string> buildBoard(const vector<int>& queens) {
    int n = (int)queens.size();
    vector<string> board(n, string(n, '.'));
    for (int r = 0; r < n; ++r) board[r][queens[r]] = 'Q';
    return board;
}
void nQueensHelper(vector<int>& queens, int row, int n,
                   vector<vector<string>>& out) {
    if (row == n) { out.push_back(buildBoard(queens)); return; }
    for (int col = 0; col < n; ++col) {
        if (isSafe(queens, row, col)) {
            queens[row] = col;
            nQueensHelper(queens, row + 1, n, out);
            queens[row] = -1;
        }
    }
}
vector<vector<string>> nQueens(int n) {
    vector<vector<string>> out;
    vector<int> queens(n, -1);
    nQueensHelper(queens, 0, n, out);
    return out;
}

// 4. WORD SEARCH
bool wordDFS(vector<vector<char>>& board, const string& word,
             int i, int j, int k) {
    if (k == (int)word.size()) return true;
    int m = (int)board.size(), n = (int)board[0].size();
    if (i < 0 || i >= m || j < 0 || j >= n) return false;
    if (board[i][j] != word[k]) return false;
    char tmp = board[i][j];
    board[i][j] = '#';                                   // visited
    bool found = wordDFS(board, word, i+1, j, k+1)
              || wordDFS(board, word, i-1, j, k+1)
              || wordDFS(board, word, i, j+1, k+1)
              || wordDFS(board, word, i, j-1, k+1);
    board[i][j] = tmp;                                   // restore
    return found;
}
bool wordSearch(vector<vector<char>> board, const string& word) {
    int m = (int)board.size(), n = (int)board[0].size();
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            if (wordDFS(board, word, i, j, 0)) return true;
    return false;
}

template <typename T>
void printVec(const vector<T>& v) {
    std::cout << "[";
    for (size_t i = 0; i < v.size(); ++i) std::cout << v[i] << (i+1<v.size()?",":"");
    std::cout << "]";
}

int main() {
    std::cout << "=== Permutations of [1,2,3] ===\n";
    for (auto& p : permutations({1,2,3})) { printVec(p); std::cout << "\n"; }

    std::cout << "\n=== Subsets of [1,2,3] ===\n";
    for (auto& s : subsets({1,2,3})) { printVec(s); std::cout << "\n"; }

    std::cout << "\n=== 4-Queens ===\n";
    auto sols = nQueens(4);
    std::cout << "Number of solutions: " << sols.size() << "\n";
    for (auto& sol : sols) {
        for (auto& row : sol) std::cout << row << "\n";
        std::cout << "---\n";
    }

    std::cout << "=== Word Search ===\n";
    vector<vector<char>> grid = {
        {'A','B','C','E'},
        {'S','F','C','S'},
        {'A','D','E','E'}
    };
    std::cout << std::boolalpha;
    std::cout << "Search 'ABCCED': " << wordSearch(grid, "ABCCED") << "\n"; // true
    std::cout << "Search 'SEE'   : " << wordSearch(grid, "SEE")    << "\n"; // true
    std::cout << "Search 'ABCB'  : " << wordSearch(grid, "ABCB")   << "\n"; // false
}

/*
 * NOTES (C++ vs Java):
 *   - Java's ArrayList<Integer> push/pop translates to std::vector<int>
 *     push_back/pop_back -- both amortised O(1).
 *   - std::vector<vector<char>> matches Java's char[][].
 *   - Pass `board` by value into wordSearch to keep main()'s grid pristine;
 *     internally we still mutate-restore via the DFS recursion.
 *   - std::abs<int> from <cstdlib>; for vector<int> indexing avoid using
 *     unsigned types (size_t) for arithmetic that may go negative.
 *   - C++23 lets us use auto for recursive lambdas via "deducing this", but
 *     here we use plain free functions for portability.
 */
