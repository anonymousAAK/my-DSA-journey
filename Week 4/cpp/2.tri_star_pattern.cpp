/*
 * WEEK 4 - C++ PATTERN PROBLEMS
 * Topic: Triangular Star Pattern
 * File: 2.tri_star_pattern.cpp
 *
 * PATTERN (N=4):
 *  *
 *  **
 *  ***
 *  ****
 *
 * COMPLEXITY: O(N^2).
 */

#include <iostream>
#include <string>

int main() {
    int n;
    if (!(std::cin >> n)) { n = 4; std::cout << "(demo n=4)\n"; }
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= i; ++j) std::cout << '*';
        std::cout << '\n';
    }
    std::cout << "--- string variant ---\n";
    for (int i = 1; i <= n; ++i) std::cout << std::string(i, '*') << '\n';
    return 0;
}

/*
 * NOTES:
 *  - std::string(i, '*') creates an i-character string filled with '*'.
 *  - Builds the line in one allocation -- much faster for huge N.
 */
