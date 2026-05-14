/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Arithmetic Operations & Operator Precedence
 * File: 5.arithmetic_operation.cpp
 *
 * CONCEPT:
 * C++ shares Java's arithmetic semantics for the basic five operators
 * (+ - * / %). Integer division truncates toward zero. Mixing int and
 * double promotes to double automatically.
 *
 * KEY POINTS:
 *  - + - * / % are the standard arithmetic operators
 *  - int / int  -> truncated int (10/6 == 1)
 *  - int / 0    -> undefined behaviour (CRASH or SIGFPE), unlike Python's exception
 *  - double / int -> double (the int is promoted)
 *  - parentheses override default precedence; * / % bind tighter than + -
 *  - There is NO `**` operator — use `std::pow(base, exp)` from <cmath>
 *
 * SYNTAX:
 *   int q = 10 / 6;            // 1
 *   double r = 10.0 / 6.0;     // 1.6666...
 *   int rem = 10 % 6;          // 4
 *   double p = std::pow(2,10); // 1024.0
 *
 * DRY RUN:
 *  a=3, b=10
 *  c = b/(2*a)  -> 10/6 = 1   (int division)
 *  d = b/(2.0*a)-> 10/6.0 = 1.6666...
 *
 * COMPLEXITY: O(1) per op.
 */

#include <iostream>
#include <cmath>

int main() {
    int a = 3;
    int b = 10;

    int c = b / (2 * a);             // integer division, truncates
    std::cout << "b / (2*a) = " << c << '\n';                // 1

    double d = b / (2.0 * a);        // promoted to double
    std::cout << "b / (2.0*a) = " << d << '\n';              // 1.6666...

    std::cout << "b % (2*a)  = " << b % (2 * a) << '\n';      // 4

    std::cout << "10 + 20 * 30 = " << 10 + 20 * 30 << '\n';   // 610
    std::cout << "(10+20) * 30 = " << (10 + 20) * 30 << '\n'; // 900

    // Exponentiation requires the cmath function
    std::cout << "pow(2,10) = " << std::pow(2, 10) << '\n';   // 1024

    // Integer overflow demo (32-bit signed): the value silently wraps
    int big = 2'000'000'000;          // ' is a digit-separator (C++14)
    int wrapped = big + big;          // overflow -> undefined/implementation-defined
    std::cout << "2e9 + 2e9 (32-bit int) = " << wrapped << "  <- WRAPPED\n";

    return 0;
}

/*
 * NOTES:
 *  - Java and C++ both truncate int/int toward zero.
 *  - C++ has NO arbitrary-precision int. Use long long (64 bits) or libraries
 *    like Boost.Multiprecision for big numbers.
 *  - C++ `%` follows the sign of the dividend (matches Java; differs from Python).
 *  - C++ has no built-in exponent operator — `std::pow` returns double.
 *  - Division by zero on integers is undefined behaviour (UB), not an exception.
 */
