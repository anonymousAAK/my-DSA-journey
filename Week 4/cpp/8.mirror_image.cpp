/*
 * WEEK 4 - C++ PATTERN PROBLEMS
 * Topic: Mirror Image Number Pattern (right-aligned)
 * File: 8.mirror_image.cpp
 *
 * PATTERN (N=4):
 *     1
 *    12
 *   123
 *  1234
 *
 * KEY POINTS:
 *  - Print (N - i) spaces, then digits 1..i.
 *  - Could use std::setw(N) with std::right alignment instead.
 */

#include <iostream>
#include <iomanip>
#include <sstream>

int main() {
    int n;
    if (!(std::cin >> n)) { n = 4; std::cout << "(demo n=4)\n"; }
    for (int i = 1; i <= n; ++i) {
        for (int s = 0; s < n - i; ++s) std::cout << ' ';
        for (int j = 1; j <= i; ++j) std::cout << j;
        std::cout << '\n';
    }
    std::cout << "--- setw variant ---\n";
    for (int i = 1; i <= n; ++i) {
        std::ostringstream oss;
        for (int j = 1; j <= i; ++j) oss << j;
        std::cout << std::setw(n) << oss.str() << '\n';
    }
    return 0;
}

/*
 * NOTES:
 *  - std::setw + std::right is the formal way to right-align text in cout.
 *  - For multi-digit row content, compute the row width carefully.
 */
