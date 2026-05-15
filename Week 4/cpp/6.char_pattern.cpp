/*
 * WEEK 4 - C++ PATTERN PROBLEMS
 * Topic: Consecutive Character Pattern
 * File: 6.char_pattern.cpp
 *
 * PATTERN (N=4):
 *  A
 *  BC
 *  CDE
 *  DEFG
 */

#include <iostream>

int main() {
    int n;
    if (!(std::cin >> n)) { n = 4; std::cout << "(demo n=4)\n"; }
    for (int i = 1; i <= n; ++i) {
        char start = static_cast<char>('A' + i - 1);
        for (int j = 0; j < i; ++j) {
            std::cout << static_cast<char>(start + j);
        }
        std::cout << '\n';
    }
    return 0;
}

/*
 * NOTES:
 *  - Two offsets at play: row offset and column offset.
 *  - Always cast back to char before printing (otherwise an int prints).
 */
