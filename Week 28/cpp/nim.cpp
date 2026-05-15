/*
 * WEEK 28 - C++ ADVANCED TOPICS
 * Topic: Nim Game
 * File: nim.cpp
 *
 * CONCEPT:
 *   Bouton's theorem: first player wins Nim iff XOR of pile sizes != 0.
 *   The constructive winning move reduces some pile p to (p XOR xor_sum)
 *   whenever that target is strictly less than p.
 *
 * KEY POINTS:
 *   - XOR captures the parity of bits across piles; the only invariant of
 *     the "P-position" set under any Nim move.
 *   - Foundational for Sprague-Grundy theory.
 *
 * ALGORITHM / APPROACH:
 *   xor_sum = XOR of piles
 *   first wins iff xor_sum != 0
 *   winning move: find pile p with (p XOR xor_sum) < p, reduce it to that.
 *
 * C++-SPECIFIC NOTES:
 *   - std::accumulate with bit_xor<int>{} works; we use a simple loop for
 *     clarity.
 *
 * DRY RUN / EXAMPLE:
 *   piles {3,4,5}: 3^4^5 = 2 != 0 -> first wins.
 *   3^2 = 1 < 3 -> reduce pile 0 from 3 to 1.
 *
 * COMPLEXITY:
 *   Time O(n)   Space O(1)
 */

#include <iostream>
#include <vector>
#include <optional>

using namespace std;

string nimWinner(const vector<int>& piles) {
    int x = 0;
    for (int p : piles) x ^= p;
    return x != 0 ? "First" : "Second";
}

optional<pair<int,int>> nimWinningMove(const vector<int>& piles) {
    int x = 0;
    for (int p : piles) x ^= p;
    if (x == 0) return nullopt;
    for (int i = 0; i < (int)piles.size(); ++i) {
        int target = piles[i] ^ x;
        if (target < piles[i]) return make_pair(i, target);
    }
    return nullopt;
}

int main() {
    vector<int> piles = {3, 4, 5};
    cout << "Piles {3,4,5}: winner = " << nimWinner(piles) << "\n";
    if (auto m = nimWinningMove(piles))
        cout << "Winning move: reduce pile " << m->first
             << " from " << piles[m->first] << " to " << m->second << "\n";

    vector<int> piles2 = {1, 2, 3};
    cout << "Piles {1,2,3}: winner = " << nimWinner(piles2) << "\n";
    cout << "Winning move exists: " << boolalpha
         << nimWinningMove(piles2).has_value() << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - We add `nimWinningMove` for the constructive aspect of Bouton's
 *     theorem; the Java file only returned "First"/"Second".
 *   - std::optional<pair<int,int>> models "no winning move".
 */
