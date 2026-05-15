/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: break Statement
 * File: 3.break.cpp
 *
 * CONCEPT:
 *  `break` exits the INNERMOST enclosing loop or switch. C++ has NO labelled
 *  break -- to escape multiple nested loops, refactor into a function (use
 *  `return`) or use a flag / `goto label;` (rare and discouraged).
 *
 * KEY POINTS:
 *  - `break` works inside for/while/do-while/switch.
 *  - In nested loops, only the innermost is affected.
 *  - `goto` exists but is generally avoided; use it only if it makes the code clearer.
 */

#include <iostream>

int main() {
    // break in for
    for (int i = 1; i < 10; ++i) {
        std::cout << i << '\n';
        if (i == 5) break;
    }

    // break in while
    int i = 1;
    while (i <= 10) {
        std::cout << i << '\n';
        if (i == 5) break;
        ++i;
    }

    // Nested break only escapes inner
    for (int x = 1; x <= 3; ++x) {
        std::cout << "outer " << x << '\n';
        for (int y = 1; y <= 5; ++y) {
            std::cout << "  in (y=" << y << ")\n";
            if (y == 1) break;          // inner only
        }
    }

    // Multi-level break via goto (rare)
    for (int x = 1; x <= 3; ++x) {
        for (int y = 1; y <= 5; ++y) {
            if (x * y == 4) goto done;
        }
    }
done:
    std::cout << "found a matching pair, exiting both loops\n";
    return 0;
}

/*
 * NOTES:
 *  - Java has labelled break/continue; C++ does NOT (use goto or refactor).
 *  - Refactoring into a small function with `return` is usually cleaner than goto.
 *  - `break` inside a switch case avoids fall-through (mandatory in C++ unless intentional).
 */
