/*
 * WEEK 2 - C++ CONTROL FLOW
 * Topic: Data Types Review
 * File: 1.data_types_review.cpp
 *
 * CONCEPT:
 * Re-examine type behaviour with arithmetic and relational operators.
 *  1. char/byte overflow vs int promotion.
 *  2. Integer-division pitfall when assigning to double.
 *  3. Modulo on int (and float via fmod).
 *  4. Relational operator returns bool.
 *
 * KEY POINTS:
 *  - C++ implicitly promotes char/short to int during arithmetic.
 *  - 6 / 4 == 1 (int division); store in a double -> 1.0 (no precision recovered).
 *  - `%` works on integers; for floats use `std::fmod`.
 *  - Relational operators return bool (true/false).
 *
 * SYNTAX:
 *   double a = 6 / 4;          // 1 (then converted to 1.0)
 *   double b = 6.0 / 4;        // 1.5 (mixed-type promotion)
 *   std::fmod(55.5, 10.0);     // 5.5
 *
 * DRY RUN:
 *   a = (double)(6/4) -> 1.0
 *   b = 6/4 -> 1
 *   c = a + b = 2.0
 *   fmod(55.5, 10) = 5.5
 *   (5 > 6) -> false
 *
 * COMPLEXITY: O(1).
 */

#include <iostream>
#include <cmath>
#include <cstdint>

int main() {
    std::cout << std::boolalpha;

    // Example 1: byte-like overflow
    // In C++ a `signed char` is similar to Java's byte. Assigning beyond [-128,127]
    // would silently wrap (implementation-defined). The compiler doesn't reject it.
    std::int8_t sb = 50;
    int product = sb * 50;        // sb is PROMOTED to int -> 2500 fits
    std::cout << "int8_t 50 * 50 = " << product
              << "  (promotion saves the day)\n";

    // Example 2: integer-division pitfall
    double a = 6 / 4;             // 1, then 1.0
    int    b = 6 / 4;             // 1
    double c = a + b;             // 2.0
    std::cout << "(double)(6/4) + (int)(6/4) = " << c << '\n';

    // Example 3: modulo on int vs fmod for floats
    double x = 55.5;
    int    y = 55;
    std::cout << "55.5 fmod 10 = " << std::fmod(x, 10.0) << '\n';   // 5.5
    std::cout << "55  %   10  = " << (y % 10)          << '\n';     // 5

    // Example 4: relational operators return bool
    int v1 = 5, v2 = 6;
    std::cout << "(5 > 6) = " << (v1 > v2) << '\n';                 // false

    return 0;
}

/*
 * NOTES:
 *  - Java auto-rejects narrow-type overflows at compile time for known
 *    constants; C++ silently wraps signed integers (UB) -- be careful.
 *  - `%` operates ONLY on integers in C++. Use `std::fmod` (from <cmath>) for floats.
 *  - `std::boolalpha` makes cout print `true`/`false` instead of 1/0.
 */
