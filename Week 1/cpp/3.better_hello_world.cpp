/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Output without/with newline (cout, '\n', std::endl)
 * File: 3.better_hello_world.cpp
 *
 * CONCEPT:
 * C++ has no pair `print` / `println`. Instead, the newline is just another
 * value you stream out. `'\n'` is a fast plain newline; `std::endl` is a
 * newline + flush of the output buffer.
 *
 * KEY POINTS:
 *  - `std::cout << "text";`               -> no newline (Java's print)
 *  - `std::cout << "text" << '\\n';`        -> newline (Java's println)
 *  - `std::cout << "text" << std::endl;`   -> newline + flush
 *  - Use `'\\n'` inside loops; reserve `std::endl` for when you need a flush.
 *  - Multiple values can be chained with `<<` operators.
 *
 * SYNTAX:
 *   cout << "abc" << "def" << '\n';
 *   cout << "no newline";
 *
 * DRY RUN:
 *  Three "Hello World" lines, then three on the same line, then a final newline.
 */

#include <iostream>

int main() {
    // println-style: three separate lines
    std::cout << "Hello World" << '\n';
    std::cout << "Hello World" << '\n';
    std::cout << "Hello World" << '\n';

    // print-style (no newline): all on the same line
    std::cout << "Hello World";
    std::cout << "Hello World";
    std::cout << "Hello World";
    std::cout << '\n';

    // std::endl flushes — useful before reading interactive input
    std::cout << "Flushed line" << std::endl;

    return 0;
}

/*
 * NOTES:
 *  - Java: `print` / `println`     | C++: stream `'\n'` or `std::endl`.
 *  - Python: `end=` parameter      | C++: include or omit `'\n'`.
 *  - `std::endl` = `'\n'` + `flush`; in tight loops prefer `'\n'`.
 *  - For "printf-style" formatting use `<cstdio>`:
 *      printf("x = %d\n", 42);
 *    or `<format>` (C++20):
 *      std::cout << std::format("x = {}\n", 42);
 */
