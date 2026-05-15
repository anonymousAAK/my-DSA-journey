/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Hello World - First C++ Program
 * File: 2.hello_world.cpp
 *
 * CONCEPT:
 * The smallest legal C++ program prints "Hello World" using the iostream
 * library. Unlike Java, there is NO surrounding class — `main` is a free
 * function. Every C++ program starts execution at `int main()`.
 *
 * KEY POINTS:
 *  - `#include <iostream>` brings in std::cout and std::endl.
 *  - `int main()` MUST return int. Returning 0 means "success".
 *  - `std::cout << "text"`           prints text without a newline.
 *  - `std::cout << "text" << "\\n"`   prints text followed by newline.
 *  - `std::cout << "text" << std::endl;` flushes the buffer too.
 *  - `using namespace std;` lets you drop the `std::` prefix (avoid in headers).
 *
 * SYNTAX:
 *  std::cout << value;            // chain with <<
 *  std::cout << "x = " << x;      // multiple values
 *
 * C++-SPECIFIC NOTES vs Java:
 *  - C++ uses `<<` (insertion) on streams; Java uses method calls (println).
 *  - `\n` is a single newline char; `std::endl` is newline + flush.
 *  - Statements end with `;`. Code blocks use `{}` like Java.
 *
 * DRY RUN:
 *  Run -> three lines: "Hello World" printed three times.
 *
 * COMPLEXITY: O(1)
 */

#include <iostream>

int main() {
    // The classic line
    std::cout << "Hello World" << std::endl;

    // Three separate lines, each terminated with '\n'
    std::cout << "Hello World" << '\n';
    std::cout << "Hello World" << '\n';
    std::cout << "Hello World" << '\n';

    // Multiple values in a single statement (chained <<)
    std::cout << "Hello" << ' ' << "World" << '\n';

    return 0;
}

/*
 * NOTES:
 *  - Java requires `public class Foo { public static void main(String[] args){...}}`.
 *    C++ just needs `int main()`.
 *  - `std::endl` flushes; prefer `'\n'` in tight loops for performance.
 *  - There is no automatic auto-flush on newline (unlike Python `print()` to a TTY).
 *  - For super-fast I/O on competitive problems, add at the top of main:
 *      std::ios_base::sync_with_stdio(false);
 *      std::cin.tie(nullptr);
 */
