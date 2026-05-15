/*
 * WEEK 2 - C++ CONTROL FLOW
 * Topic: Multiplication Table via Loop
 * File: 8.multiplication_table.cpp
 *
 * PROBLEM:
 *  Read n, print n, 2n, ..., 10n, each on its own line.
 *
 * KEY POINTS:
 *  - Classic for/while loop with counter 1..10.
 *  - In C++ the range-based for is for containers; an indexed for is easier here.
 *
 * SYNTAX:
 *   for (int i = 1; i <= 10; ++i) std::cout << i * n << '\n';
 *
 * DRY RUN:
 *  n=4 -> 4, 8, 12, ..., 40
 */

#include <iostream>

int main() {
    int n;
    if (!(std::cin >> n)) { n = 4; std::cout << "(demo n=4)\n"; }
    for (int i = 1; i <= 10; ++i) {
        std::cout << (i * n) << '\n';
    }
    return 0;
}

/*
 * NOTES:
 *  - O(1) iterations (always 10). Beware integer overflow for large n.
 *  - In Java/Python the loop body is identical -- only the syntactic overhead
 *    around `for(...)` differs.
 */
