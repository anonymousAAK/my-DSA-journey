/*
 * WEEK 4 - C++ PATTERN PROBLEMS
 * Topic: Reverse Number Pattern
 * File: 4.reverse_num_pattern.cpp
 *
 * PATTERN (N=4):
 *  1
 *  21
 *  321
 *  4321
 */

#include <iostream>

int main() {
    int n;
    if (!(std::cin >> n)) { n = 4; std::cout << "(demo n=4)\n"; }
    int curRow = 1;
    while (curRow <= n) {
        int curCol = curRow;
        while (curCol >= 1) {
            std::cout << curCol;
            --curCol;
        }
        std::cout << '\n';
        ++curRow;
    }
    return 0;
}

/*
 * NOTES:
 *  - Inner counter starts at curRow and counts DOWN to 1.
 *  - Could also use a for loop: for (int j = i; j >= 1; --j) cout << j;
 */
