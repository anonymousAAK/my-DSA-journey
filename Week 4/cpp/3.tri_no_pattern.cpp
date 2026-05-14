/*
 * WEEK 4 - C++ PATTERN PROBLEMS
 * Topic: Triangle Number Pattern
 * File: 3.tri_no_pattern.cpp
 *
 * PATTERN (N=4):
 *  1
 *  22
 *  333
 *  4444
 */

#include <iostream>
#include <string>

int main() {
    int n;
    if (!(std::cin >> n)) { n = 4; std::cout << "(demo n=4)\n"; }
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= i; ++j) std::cout << i;
        std::cout << '\n';
    }
    return 0;
}

/*
 * NOTES:
 *  - Each row prints the OUTER counter; inner counter only controls how many.
 *  - For N >= 10, lines widen by extra digits.
 */
