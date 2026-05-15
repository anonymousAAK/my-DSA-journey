/*
 * WEEK 4 - C++ PATTERN PROBLEMS
 * Topic: Interesting Alphabet Pattern
 * File: 7.interesting_alphabet.cpp
 *
 * PATTERN (N=4):
 *  D
 *  CD
 *  BCD
 *  ABCD
 */

#include <iostream>

int main() {
    int n;
    if (!(std::cin >> n)) { n = 4; std::cout << "(demo n=4)\n"; }
    for (int i = 1; i <= n; ++i) {
        char start = static_cast<char>('A' + n - i);
        for (int j = 0; j < i; ++j) {
            std::cout << static_cast<char>(start + j);
        }
        std::cout << '\n';
    }
    return 0;
}

/*
 * NOTES:
 *  - Start letter shifts EARLIER each row; bottom row begins at 'A'.
 *  - Same column-offset pattern as char_pattern, with a different start formula.
 */
