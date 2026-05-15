/*
 * WEEK 4 - C++ PATTERN PROBLEMS
 * Topic: Square Pattern
 * File: 1.square_pattern.cpp
 *
 * PATTERN (N=4):
 *  4444
 *  4444
 *  4444
 *  4444
 *
 * CONCEPT:
 *  N x N grid where every cell is the digit N.
 *
 * COMPLEXITY: O(N^2).
 */

#include <iostream>
#include <string>

int main() {
    int n;
    if (!(std::cin >> n)) { n = 4; std::cout << "(demo n=4)\n"; }
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= n; ++j) std::cout << n;
        std::cout << '\n';
    }
    // Idiomatic: build a single line, repeat
    std::string line(n, '0' + std::min(n, 9));   // works only when n <= 9
    if (n <= 9) {
        std::cout << "--- string-repeat ---\n";
        for (int i = 0; i < n; ++i) std::cout << line << '\n';
    }
    return 0;
}

/*
 * NOTES:
 *  - std::string(n, ch) constructs an n-length string of ch.
 *  - For multi-digit N (>= 10), build the line with std::to_string(n) repeated.
 */
