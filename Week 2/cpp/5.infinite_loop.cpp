/*
 * WEEK 2 - C++ CONTROL FLOW
 * Topic: Infinite Loop Demonstration
 * File: 5.infinite_loop.cpp
 *
 * CONCEPT:
 * In C++ the canonical infinite loops are `for(;;)` and `while (true)`.
 * Both compile to identical machine code on most compilers. We add a
 * counter-based safety break so this demo program terminates.
 *
 * KEY POINTS:
 *  - `while (true) { ... }` is the idiomatic infinite loop.
 *  - `for (;;) { ... }` is equally valid (and slightly shorter).
 *  - Use `break` to exit; `continue` to skip the rest of the iteration.
 *  - Signal handling (SIGINT) lets long-running loops respond to Ctrl-C.
 *
 * DRY RUN:
 *  x=y=5
 *  In Java: x==y forever -> infinite "Hello"s.
 *  Here we cap at 5 iterations so the program ends.
 */

#include <iostream>

int main() {
    int x = 5, y = 5, safety = 0;

    while (x == y) {
        std::cout << "Hello\n";
        ++x;
        ++y;
        if (++safety >= 5) {
            std::cout << "(safety cap reached)\n";
            break;
        }
    }

    // Canonical infinite-loop form with break
    int n = 0;
    while (true) {
        if (++n >= 3) { std::cout << "stopping at n=" << n << '\n'; break; }
    }

    return 0;
}

/*
 * NOTES:
 *  - Without `break` (and without a flag flip), the loop never ends.
 *  - C++ has no automatic detection of infinite loops -- the compiler may
 *    optimise some away if they have no observable side effects.
 *  - Always include a safety break in DEMOS of infinite-loop semantics.
 */
