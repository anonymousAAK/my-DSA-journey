/*
 * WEEK 2 - C++ CONTROL FLOW
 * Topic: If-Else Conditional Statements
 * File: 2.if_else.cpp
 *
 * CONCEPT:
 * C++'s if/else is virtually identical to Java's. Braces are recommended
 * but optional for single statements. Conditions must convert to bool.
 *
 * KEY POINTS:
 *  - `if (cond) { ... } else if (other) { ... } else { ... }`
 *  - The condition is implicitly converted to bool (0 -> false, anything else -> true).
 *  - There is also a ternary: `cond ? a : b`.
 *  - C++17 introduced `if-init`: `if (auto x = f(); x > 0) ...`.
 *  - C++ has `switch (int/enum/char) { case ...: }` for discrete dispatch.
 *
 * SYNTAX:
 *   if (a > b) {
 *       ...
 *   } else {
 *       ...
 *   }
 *
 * DRY RUN:
 *   a=10, b=15 -> a > b is false -> "b " printed
 *   "is greater" always prints (outside the if)
 *   final: "b is greater"
 */

#include <iostream>

int main() {
    int a = 10, b = 15;

    if (a > b) {
        std::cout << "a ";
    } else {
        std::cout << "b ";
    }
    std::cout << "is greater\n";

    // Ternary expression
    std::cout << "max = " << (a > b ? a : b) << '\n';

    // if-init (C++17): scope the variable to the if-block only
    if (int diff = a - b; diff < 0) {
        std::cout << "a is " << -diff << " less than b\n";
    }

    // switch — works for ints, chars, enums (NOT strings; use if/else for strings)
    char grade = 'B';
    switch (grade) {
        case 'A':            std::cout << "Excellent\n"; break;
        case 'B': case 'C':  std::cout << "Good\n";       break;
        default:             std::cout << "Try harder\n";
    }

    return 0;
}

/*
 * NOTES:
 *  - Java and C++ have nearly identical if/else syntax; the BIG difference is
 *    C++17's `if (init; cond)` which scopes a variable to the conditional.
 *  - C++ `switch` does NOT match strings (Java 7+ does).
 *  - There is no `elif` keyword; use `else if`.
 *  - Single-statement bodies can omit braces, but doing so is error-prone.
 */
