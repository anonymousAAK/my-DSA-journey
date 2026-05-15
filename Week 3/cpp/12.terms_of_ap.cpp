/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: First X Terms of 3N+2 Not Divisible by 4
 * File: 12.terms_of_ap.cpp
 *
 * PROBLEM:
 *  Print the first X terms of (3N+2) that are NOT multiples of 4.
 *
 * KEY POINTS:
 *  - Walk N from 1 upward; emit `3N+2` if not divisible by 4.
 *  - Stop when X terms have been printed.
 *
 * DRY RUN:
 *  X=3 -> 5 11 14
 */

#include <iostream>

int main() {
    int x;
    if (!(std::cin >> x)) { x = 5; std::cout << "(demo x=5)\n"; }
    int count = 0, n = 1;
    while (count < x) {
        int term = 3 * n + 2;
        if (term % 4 != 0) {
            std::cout << term << ' ';
            ++count;
        }
        ++n;
    }
    std::cout << '\n';
    return 0;
}

/*
 * NOTES:
 *  - Two counters keep the loop simple: one for items emitted, one for N.
 *  - Range `for` doesn't fit naturally here because we filter at runtime.
 */
