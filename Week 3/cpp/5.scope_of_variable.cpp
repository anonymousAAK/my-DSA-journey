/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: Scope of Variables
 * File: 5.scope_of_variable.cpp
 *
 * CONCEPT:
 *  C++ scopes are delimited by `{}` braces. A variable declared inside a
 *  block is destroyed when the block exits. This is the SAME as Java but
 *  the OPPOSITE of Python (which has only function-level scopes).
 *
 * KEY POINTS:
 *  - Variables declared in for-init are scoped to the for body.
 *  - Variables declared inside if/else/while are scoped to that block.
 *  - C++17 `if (auto x = f(); x > 0) { ... }` scopes x to just the if/else.
 *  - Static locals retain value across function calls.
 *  - `using namespace std;` brings std names into the current scope.
 */

#include <iostream>

void demo_for_scope() {
    for (int i = 0; i < 3; ++i) {
        int j = i * 2;
        std::cout << "  inside for: i=" << i << " j=" << j << '\n';
    }
    // i and j are OUT OF SCOPE here -- referencing them is a compile error.
}

void demo_block_scope() {
    int x = 10;
    {                           // explicit nested block
        int y = 20;
        std::cout << "inside: x=" << x << " y=" << y << '\n';
    }
    // y is gone now
    std::cout << "outside: x=" << x << '\n';
}

void demo_if_init_cpp17() {
    auto compute = []() { return 42; };
    if (int n = compute(); n > 0) {
        std::cout << "if-init n=" << n << '\n';
    }
    // n is OUT OF SCOPE here.
}

void demo_static_local() {
    static int call_count = 0;     // initialised once
    ++call_count;
    std::cout << "called " << call_count << " time(s)\n";
}

int main() {
    demo_for_scope();
    demo_block_scope();
    demo_if_init_cpp17();
    demo_static_local();
    demo_static_local();
    demo_static_local();
    return 0;
}

/*
 * NOTES:
 *  - C++ matches Java for block scoping.
 *  - Python's for/if/while DO NOT introduce scopes -- variables defined inside
 *    leak to enclosing function scope.
 *  - `static` locals are like global vars but with function-scope visibility.
 *  - Use `if (init; cond)` (C++17) to keep helper variables tightly scoped.
 */
