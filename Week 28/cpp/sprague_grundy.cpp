/*
 * WEEK 28 - C++ ADVANCED TOPICS
 * Topic: Sprague-Grundy Theorem
 * File: sprague_grundy.cpp
 *
 * CONCEPT:
 *   Every impartial game position s has a Grundy number g(s) defined as
 *     g(s) = mex { g(s') : s' reachable from s in one move }
 *   For a sum of independent impartial games, the overall Grundy value is
 *   the XOR of the components, and the position is losing iff that XOR is
 *   zero.
 *
 * KEY POINTS:
 *   - Generalises Bouton's theorem for Nim.
 *   - DP table over single-pile positions; multi-pile via XOR.
 *   - mex(S) = smallest non-negative integer not in S.
 *
 * ALGORITHM / APPROACH:
 *   for n in 0..max:
 *     compute set of reachable g-values for each allowed move
 *     g[n] = mex(set)
 *   for multi-pile: XOR g[piles[i]]
 *
 * C++-SPECIFIC NOTES:
 *   - std::unordered_set<int> for the "reachable" set.
 *   - mex implemented by counting from 0 upward.
 *
 * DRY RUN / EXAMPLE:
 *   moves {1,3,4}: g(10) = 1. Two piles [10,6] -> XOR(g(10), g(6)) =
 *   XOR(1, 2) = 3 != 0 -> first wins.
 *
 * COMPLEXITY:
 *   Time O(n * |moves|)   Space O(n)
 */

#include <iostream>
#include <vector>
#include <unordered_set>
#include <algorithm>

using namespace std;

int mex(const unordered_set<int>& s) {
    int m = 0;
    while (s.count(m)) ++m;
    return m;
}

int grundySubtraction(int n, const vector<int>& moves) {
    vector<int> g(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        unordered_set<int> reachable;
        for (int m : moves) if (i - m >= 0) reachable.insert(g[i - m]);
        g[i] = mex(reachable);
    }
    return g[n];
}

bool firstPlayerWins(const vector<int>& piles, const vector<int>& moves) {
    if (piles.empty()) return false;
    int maxPos = *max_element(piles.begin(), piles.end());
    vector<int> g(maxPos + 1, 0);
    for (int i = 1; i <= maxPos; ++i) {
        unordered_set<int> reachable;
        for (int m : moves) if (i - m >= 0) reachable.insert(g[i - m]);
        g[i] = mex(reachable);
    }
    int x = 0;
    for (int p : piles) x ^= g[p];
    return x != 0;
}

int main() {
    vector<int> moves = {1, 3, 4};
    cout << "Grundy table for moves {1,3,4}:\n";
    for (int i = 0; i <= 10; ++i)
        cout << "  g(" << i << ") = " << grundySubtraction(i, moves) << "\n";
    cout << "grundy(10) = " << grundySubtraction(10, moves) << "\n";
    cout << "Two piles {10, 6}: first wins? " << boolalpha
         << firstPlayerWins({10, 6}, moves) << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - We extend the single-pile grundy() with a multi-pile XOR wrapper.
 *   - std::unordered_set replaces Java's HashSet for the reachable set.
 */
