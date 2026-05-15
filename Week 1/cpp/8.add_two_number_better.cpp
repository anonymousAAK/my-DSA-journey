/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Adding Two Numbers from User Input
 * File: 8.add_two_number_better.cpp
 *
 * CONCEPT:
 * Read two integers from stdin and print their sum. Showcases the simplest
 * "read -> compute -> output" pipeline in C++.
 *
 * KEY POINTS:
 *  - `std::cin >> a >> b;` reads two integer tokens.
 *  - The sum can be passed directly to cout — no temporary needed.
 *  - Returning 0 from main signals success to the OS.
 *
 * SYNTAX:
 *   int a, b; std::cin >> a >> b;
 *   std::cout << (a + b) << '\n';
 *
 * DRY RUN:
 *  Stdin: "10 25"
 *    a=10, b=25
 *    cout << (a+b) -> "35"
 *
 * COMPLEXITY: O(1)
 */

#include <iostream>

int main() {
    int a, b;
    if (!(std::cin >> a >> b)) {
        std::cerr << "Two integers expected.\n";
        return 1;
    }
    std::cout << (a + b) << '\n';
    return 0;
}

/*
 * NOTES:
 *  - Java mandates `Scanner` import + new Scanner ceremony; C++ uses cin directly.
 *  - In C++ you can read both numbers with one statement using chained `>>`.
 *  - Always validate input with `if (!(cin >> ...))` to catch malformed data.
 */
