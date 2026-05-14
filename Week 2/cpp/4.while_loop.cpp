/*
 * WEEK 2 - C++ CONTROL FLOW
 * Topic: While Loop Basics
 * File: 4.while_loop.cpp
 *
 * CONCEPT:
 * Unlike Python (where `=` is a statement), C++ allows assignment within an
 * expression: `(x = 5) == y` assigns 5 to x then compares with y. This is
 * the same quirky behaviour Java exhibits. The compiler usually warns:
 * "suggest parentheses around assignment used as truth value".
 *
 * KEY POINTS:
 *  - `while (cond) { ... }` — same as Java.
 *  - Assignment-in-condition is legal but discouraged.
 *  - `do { ... } while (cond);` exists (unlike Python).
 *
 * SYNTAX:
 *   while (x == y) { ... }       // common form
 *   while ((x = 5) == y) { ... } // quirky: assignment inside the test
 *   do { ... } while (cond);     // post-test loop
 *
 * DRY RUN:
 *  x=5; y=5
 *   iter 1: (x=5)==y -> (5==5) true -> "Hello"; x=6; y=6
 *   iter 2: (x=5)==y -> (5==6) false -> exit
 *  Total: one "Hello".
 */

#include <iostream>

int main() {
    int x = 5, y = 5;

    // Java-style "assignment in condition" -- compiler will likely warn.
    while ((x = 5) == y) {
        std::cout << "Hello\n";
        ++x;
        ++y;
    }

    // Clean variant
    int i = 1;
    while (i <= 3) {
        std::cout << "i = " << i << '\n';
        ++i;
    }

    // do-while runs the body at least once
    int k = 100;
    do {
        std::cout << "k = " << k << " (executes at least once)\n";
        ++k;
    } while (k < 100);

    return 0;
}

/*
 * NOTES:
 *  - C++ allows `(x = 5) == y` exactly like Java. Most lint tools flag it.
 *  - Python forbids this entirely; you'd use the walrus operator `:=`.
 *  - `do { } while (...)` is the post-test loop -- runs at least once.
 *  - C++ also has range-based for: `for (auto v : container) {...}`.
 */
