/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: Decreasing-then-Increasing Sequence Check
 * File: 16.check_no_sequence.cpp
 *
 * PROBLEM:
 *  N integers; return true if the sequence is strictly decreasing then
 *  strictly increasing (transition allowed at most once). Equal consecutive
 *  values -> false.
 *
 * KEY POINTS:
 *  - Track current phase with a bool `is_dec`.
 *  - Equal consecutive => false immediately.
 *  - Once we transition to increasing, decreasing again => false.
 *
 * COMPLEXITY: O(n) time, O(1) space.
 */

#include <iostream>
#include <vector>

bool check(const std::vector<int>& s) {
    if (s.size() < 2) return true;
    bool is_dec = true;
    for (size_t i = 1; i < s.size(); ++i) {
        if (s[i] == s[i - 1]) return false;
        if (s[i] < s[i - 1]) {
            if (!is_dec) return false;       // already increasing -> can't decrease
        } else {
            if (is_dec) is_dec = false;       // transition once
        }
    }
    return true;
}

int main() {
    int n;
    if (!(std::cin >> n)) {
        std::cout << std::boolalpha;
        for (auto v : std::vector<std::vector<int>> {
                 {5, 3, 1, 2, 4}, {1, 2, 3, 4, 5}, {5, 4, 3, 2, 1},
                 {1, 2, 3, 2, 1}, {1, 2, 2, 3} }) {
            std::cout << "{ ";
            for (int x : v) std::cout << x << ' ';
            std::cout << "} -> " << check(v) << '\n';
        }
        return 0;
    }
    std::vector<int> s(n);
    for (auto& x : s) std::cin >> x;
    std::cout << std::boolalpha << check(s) << '\n';
    return 0;
}

/*
 * NOTES:
 *  - Linear scan with a single boolean state -- clean and fast.
 *  - For STREAMED input you don't need to store the whole sequence; just
 *    keep `prev` and `is_dec`.
 */
