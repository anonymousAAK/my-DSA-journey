/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Reading Mixed-Type Input
 * File: 10.multiple_input.cpp
 *
 * CONCEPT:
 * Read several values of different types (e.g., an int and a string) and
 * print them on the same line. Demonstrates chained extraction with `>>`.
 *
 * KEY POINTS:
 *  - `cin >> i >> s;` reads an int then a token-string.
 *  - Output without newline:  `cout << x;`
 *  - Output with newline:      `cout << x << '\n';`
 *  - Concatenation in C++ is done by chaining `<<`, NOT with `+` on cout.
 *
 * SYNTAX:
 *   int i; std::string s;
 *   std::cin >> i >> s;
 *   std::cout << i << s << '\n';
 *
 * DRY RUN:
 *  Stdin: "42\nhello"
 *    i=42, s="hello"
 *    cout << i << s -> "42hello"
 */

#include <iostream>
#include <string>

int main() {
    int i;
    std::string s;
    std::cin >> i >> s;

    // Print i without newline (Java: System.out.print)
    std::cout << i;
    // Then s with newline (Java: System.out.println)
    std::cout << s << '\n';

    // Same line, joined neatly
    std::cout << i << " " << s << '\n';

    return 0;
}

/*
 * NOTES:
 *  - C++ does NOT auto-convert types when concatenating with + the way Java does.
 *    But streams ALREADY know how to print every fundamental type via overloads
 *    of operator<<.
 *  - For complex formatting, prefer std::format (C++20) or printf-style.
 */
