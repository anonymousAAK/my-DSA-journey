/*
 * WEEK 28 - C++ ADVANCED TOPICS
 * Topic: Alpha-Beta Pruning
 * File: alpha_beta.cpp
 *
 * CONCEPT:
 *   Same minimax result, but prune branches whose value cannot affect the
 *   parent's choice. Maintain a window [alpha, beta]:
 *     - alpha = best already-guaranteed value for Max
 *     - beta  = best already-guaranteed value for Min
 *   Prune when alpha >= beta.
 *
 * KEY POINTS:
 *   - With perfect move ordering, effective branching factor sqrt(b),
 *     so depth doubles within the same time budget.
 *   - Memoising alpha-beta is tricky because the window may differ between
 *     visits; we skip memo here for clarity.
 *
 * ALGORITHM / APPROACH:
 *   ab(s, a, b, max_turn):
 *     if terminal: return utility(s)
 *     iterate moves, updating a or b and breaking on a >= b
 *
 * C++-SPECIFIC NOTES:
 *   - Pass alpha and beta by value (cheap ints).
 *   - INT_MIN/INT_MAX for initial bounds.
 *
 * DRY RUN / EXAMPLE:
 *   Empty TTT board, X to move -> value 0. Node counter shows how many
 *   states alpha-beta visits compared to pure minimax (~5-7x fewer).
 *
 * COMPLEXITY:
 *   Time O(b^d) worst; O(b^(d/2)) with good ordering. Space O(d).
 */

#include <iostream>
#include <array>
#include <climits>
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
bool isFull(const Board& b) { for (char c : b) if (c == '.') return false; return true; }
int utility(const Board& b) { char w = winner(b); return w == 'X' ? +1 : w == 'O' ? -1 : 0; }

long long nodeCount = 0;

int alphabeta(Board b, int alpha, int beta, bool maxTurn) {
    ++nodeCount;
    if (winner(b) != '.' || isFull(b)) return utility(b);
    if (maxTurn) {
        int v = INT_MIN;
        for (int i = 0; i < 9; ++i) if (b[i] == '.') {
            b[i] = 'X';
            v = max(v, alphabeta(b, alpha, beta, false));
            b[i] = '.';
            alpha = max(alpha, v);
            if (alpha >= beta) break;
        }
        return v;
    } else {
        int v = INT_MAX;
        for (int i = 0; i < 9; ++i) if (b[i] == '.') {
            b[i] = 'O';
            v = min(v, alphabeta(b, alpha, beta, true));
            b[i] = '.';
            beta = min(beta, v);
            if (alpha >= beta) break;
        }
        return v;
    }
}

int bestMove(Board b, bool maxTurn) {
    int idx = -1, bestVal = maxTurn ? INT_MIN : INT_MAX;
    for (int i = 0; i < 9; ++i) if (b[i] == '.') {
        b[i] = (maxTurn ? 'X' : 'O');
        int v = alphabeta(b, INT_MIN, INT_MAX, !maxTurn);
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
    nodeCount = 0;
    cout << "Alpha-beta value of empty TTT: "
         << alphabeta(empty, INT_MIN, INT_MAX, true) << "\n";
    cout << "Nodes explored: " << nodeCount << "\n";
    cout << "Best opening move for X: cell " << bestMove(empty, true) << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - Java's game_theory.java has no alpha-beta; we add it.
 *   - INT_MIN / INT_MAX as initial bounds; care to never max(INT_MAX, ...).
 *   - nodeCount global makes the pruning effect tangible.
 */
