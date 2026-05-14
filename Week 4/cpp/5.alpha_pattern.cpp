/*
 * WEEK 4 - C++ PATTERN PROBLEMS
 * Topic: Alpha Pattern
 * File: 5.alpha_pattern.cpp
 *
 * PATTERN (N=4):
 *  A
 *  BB
 *  CCC
 *  DDDD
 *
 * KEY POINTS:
 *  - char arithmetic in C++ is implicit: 'A' + 1 yields int 66.
 *  - Cast back with static_cast<char>(...) to print as a letter.
 */

#include <iostream>
#include <string>

int main() {
    int n;
    if (!(std::cin >> n)) { n = 4; std::cout << "(demo n=4)\n"; }
    for (int i = 1; i <= n; ++i) {
        char ch = static_cast<char>('A' + i - 1);
        for (int j = 1; j <= i; ++j) std::cout << ch;
        std::cout << '\n';
    }
    std::cout << "--- string variant ---\n";
    for (int i = 1; i <= n; ++i)
        std::cout << std::string(i, static_cast<char>('A' + i - 1)) << '\n';
    return 0;
}

/*
 * NOTES:
 *  - 'A' + i - 1 produces an int; cast to char before output.
 *  - For N > 26 you'd run off 'Z' -- consider modulo if wrapping is desired.
 */
