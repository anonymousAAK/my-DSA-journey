/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: continue Statement
 * File: 4.continue.cpp
 *
 * CONCEPT:
 *  `continue` skips the rest of the current iteration. In a `for` loop it
 *  jumps to the update step; in a `while` it jumps to the condition test.
 *  CAUTION: in while loops, increment your counter BEFORE `continue`.
 *
 * DRY RUN:
 *  for(i=1..5): if(i==3) continue; else print
 *  -> 1, 2, 4, 5
 */

#include <iostream>

int main() {
    // continue in for
    for (int i = 1; i <= 5; ++i) {
        if (i == 3) continue;
        std::cout << i << '\n';
    }
    std::cout << "---\n";

    // continue in while: increment FIRST
    int i = 1;
    while (i <= 5) {
        if (i == 3) {
            ++i;            // CRITICAL: advance before continue
            continue;
        }
        std::cout << i << '\n';
        ++i;
    }
    return 0;
}

/*
 * NOTES:
 *  - The for-loop counter advances automatically via the update step.
 *  - The while-loop counter does NOT -- forgetting `++i` before `continue`
 *    creates an infinite loop.
 *  - `continue` works on the innermost loop only (no labels in C++).
 */
