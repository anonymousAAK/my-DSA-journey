/*
 * WEEK 28 - C++ ADVANCED TOPICS
 * Topic: Minimax (Zero-Sum Game Tree Search)
 * File: minimax.cpp
 *
 * CONCEPT:
 *   For a two-player perfect-information zero-sum game, minimax assigns a
 *   value to every state representing the score the maximising player can
 *   guarantee against an optimal minimising opponent. Recurrence:
 *     v(s) = utility(s) at terminals
 *     v(s) = max v(c) at Max nodes
 *     v(s) = min v(c) at Min nodes
 *
 * KEY POINTS:
 *   - Explores every reachable terminal -> O(b^d). Use alpha-beta to prune.
 *   - Memoise hashable states for repeated subtrees.
 *
 * ALGORITHM / APPROACH:
 *   minimax(s, max_turn):
 *     if terminal: return utility(s)
 *     return (max_turn ? max : min) over moves of minimax(child, !max_turn)
 *
 * C++-SPECIFIC NOTES:
 *   - Board as std::array<char,9>; std::unordered_map for memoisation.
 *   - 'X' = Max, 'O' = Min.
 *
 * DRY RUN / EXAMPLE:
 *   Empty TTT board, X to move -> value 0 (draw with optimal play).
 *
 * COMPLEXITY:
 *   Time O(b^d) worst case; with memo bounded by |states|. Space O(d).
 */

#include <iostream>
#include <array>
#include <unordered_map>
#include <string>
#include <algorithm>

using namespace std;

using Board = array<char, 9>;
static const int LINES[8][3] = {
    {0,1,2},{3,4,5},{6,7,8},{0,3,6},{1,4,7},{2,5,8},{0,4,8},{2,4,6}
};

char winner(const Board& b) {
    for (auto& l : LINES)
        if (b[l[0]] != '.' && b[l[0]] == b[l[1]] && b[l[1]] == b[l[2]])
            return b[l[0]];
    return '.';
}

bool isFull(const Board& b) {
    for (char c : b) if (c == '.') return false;
    return true;
}

int utility(const Board& b) {
    char w = winner(b);
    if (w == 'X') return +1;
    if (w == 'O') return -1;
    return 0;
}

struct BoardHash {
    size_t operator()(const Board& b) const {
        string s(b.begin(), b.end());
        return hash<string>{}(s);
    }
};

unordered_map<Board, int, BoardHash> memo;

int minimax(Board b, bool maxTurn) {
    if (winner(b) != '.' || isFull(b)) return utility(b);
    auto it = memo.find(b);
    if (it != memo.end()) return it->second;
    int best;
    if (maxTurn) {
        best = -2;
        for (int i = 0; i < 9; ++i) if (b[i] == '.') {
            b[i] = 'X';
            best = max(best, minimax(b, false));
            b[i] = '.';
        }
    } else {
        best = +2;
        for (int i = 0; i < 9; ++i) if (b[i] == '.') {
            b[i] = 'O';
            best = min(best, minimax(b, true));
            b[i] = '.';
        }
    }
    memo[b] = best;
    return best;
}

int bestMove(Board b, bool maxTurn) {
    int idx = -1, bestVal = maxTurn ? -3 : +3;
    for (int i = 0; i < 9; ++i) if (b[i] == '.') {
        b[i] = (maxTurn ? 'X' : 'O');
        int v = minimax(b, !maxTurn);
        b[i] = '.';
        if ((maxTurn && v > bestVal) || (!maxTurn && v < bestVal)) {
            bestVal = v; idx = i;
        }
    }
    return idx;
}

int main() {
    Board empty;
    empty.fill('.');
    cout << "Minimax value of empty TTT (X to move): " << minimax(empty, true) << "\n";
    cout << "Best opening move for X: cell " << bestMove(empty, true) << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - Java's game_theory.java does not include minimax; this fills the spec.
 *   - std::unordered_map provides O(1) memoisation; Java's HashMap is the
 *     direct analogue.
 *   - std::array gives a fixed-size value-type board, perfect for hashing.
 */
