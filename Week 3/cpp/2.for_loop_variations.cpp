/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: For Loop Variations
 * File: 2.for_loop_variations.cpp
 *
 * CONCEPT:
 *  All three parts of `for (init; cond; update)` are optional.
 *  Multiple init/update statements separated by commas; multiple
 *  conditions joined with `&&` / `||`.
 *
 * KEY POINTS:
 *  - `for (;;) { ... }` is an infinite loop (canonical).
 *  - `for (int i=0, j=4; i<5 && j>=0; ++i, --j) { ... }` -- two counters.
 *  - `for (int i = init(); i; --i)` -- truthy condition uses the int value directly.
 *
 * DRY RUN:
 *  Two-counter loop: (0,4), (1,3), (2,2), (3,1), (4,0)
 */

#include <iostream>

int main() {
    // 1) Init removed
    int i = 0;
    for (; i < 3; ++i) std::cout << i << ' ';
    std::cout << '\n';

    // 2) Update removed (done inside body)
    for (int j = 0; j < 3; ) {
        std::cout << j << ' ';
        ++j;
    }
    std::cout << '\n';

    // 3) Condition removed -- infinite. Capped here.
    int safety = 0;
    for (int k = 0; ; ++k) {
        std::cout << k << ' ';
        if (++safety >= 3) break;
    }
    std::cout << '\n';

    // 4) Two counters with comma operator
    for (int a = 0, b = 4; a < 5 && b >= 0; ++a, --b) {
        std::cout << a << ' ' << b << '\n';
    }

    // 5) for(;;) -- canonical infinite loop
    int n = 0;
    for (;;) {
        if (++n >= 3) { std::cout << "stopped at n=" << n << '\n'; break; }
    }
    return 0;
}

/*
 * NOTES:
 *  - The comma operator `,` evaluates both expressions and yields the right one.
 *  - Multi-variable for headers can declare ONLY ONE TYPE -- so all loop vars
 *    must share a type. Use auto with structured bindings if needed.
 *  - For mixing types use a struct / pair / tuple in the init.
 */
