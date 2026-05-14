/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: For Loop Basics
 * File: 1.for_loop.cpp
 *
 * CONCEPT:
 *  C++ inherits the C-style `for (init; cond; update) { body }`. All three
 *  parts are optional; an empty condition is treated as `true`. C++11 added
 *  the range-based for: `for (auto v : container) { ... }`.
 *
 * KEY POINTS:
 *  - `for (int i = 0; i < n; ++i)` is the canonical counted loop.
 *  - Pre-increment (++i) is preferred over postfix (i++) for non-fundamental types.
 *  - Range-based for: `for (auto x : vec)`, `for (auto& x : vec)`, `for (const auto& x : vec)`.
 *  - You can omit any of the three parts: `for (;;)` is an infinite loop.
 *
 * SYNTAX:
 *   for (int i = 0; i < n; ++i) { ... }
 *   for (auto v : container) { ... }
 *   for (auto& v : container) { v *= 2; }
 *
 * DRY RUN:
 *  for(int i=0; i<3; ++i) cout << "Inside : " << i << '\n';
 *  cout << "Done";
 *
 * COMPLEXITY: O(n).
 */

#include <iostream>
#include <vector>

int main() {
    // Classic indexed for
    for (int i = 0; i < 3; ++i) {
        std::cout << "Inside for loop : " << i << '\n';
    }
    std::cout << "Done\n";

    // Initialisation outside the for header
    int i = 1;
    for (; i <= 5; ++i) std::cout << i << ' ';
    std::cout << '\n';

    // Update inside the body
    for (int j = 1; j <= 5; ) {
        std::cout << j << ' ';
        ++j;
    }
    std::cout << '\n';

    // Range-based for over a container
    std::vector<int> v {10, 20, 30, 40};
    for (int x : v) std::cout << x << ' ';
    std::cout << '\n';

    return 0;
}

/*
 * NOTES:
 *  - C++ inherits the full C-style `for(...)`; Python's `for` is iteration-only.
 *  - Range-based for (C++11) is closest to Python's `for x in iterable`.
 *  - Always prefer pre-increment for iterators / heavy types.
 *  - Use `const auto&` in range-for to avoid copies when you don't mutate.
 */
