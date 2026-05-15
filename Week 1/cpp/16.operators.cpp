/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Operators in C++ (Arithmetic, Relational, Logical, Bitwise)
 * File: 16.operators.cpp
 *
 * CONCEPT:
 * C++ exposes essentially the same operator set as Java, with a couple of
 * extras: pointer arithmetic (`*`, `->`, `&`), the scope resolution operator
 * (`::`), the comma operator, and ternary `? :`. The keywords `and`, `or`,
 * `not` exist as alternative spellings of `&&`, `||`, `!`.
 *
 * KEY POINTS:
 *  - Arithmetic: + - * / %       (no `**`; use std::pow)
 *  - Relational: == != > < >= <= -> bool
 *  - Logical:    && || !          (or `and` / `or` / `not`)
 *  - Bitwise:    & | ^ ~ << >>   (no `>>>`)
 *  - Increment/Decrement: ++ -- (prefix and postfix variants)
 *  - Assignment: = += -= *= /= %= &= |= ^= <<= >>=
 *  - Conditional: condition ? a : b
 *  - Comma: e1, e2  -> evaluates both, returns e2
 *
 * SYNTAX:
 *   bool t = (a > b) && (c < d);
 *   int  m = (a > b) ? a : b;
 *   int  q = a / b, r = a % b;
 *
 * DRY RUN:
 *  19 & 28 -> 16; 19 | 28 -> 31; 19 ^ 28 -> 15
 *  ~19 -> -20; 19 << 2 -> 76; 19 >> 2 -> 4
 *  (5 > 6) -> false; ((5>4) && (4>3)) -> true
 */

#include <iostream>
#include <bitset>

int main() {
    std::cout << "=== Arithmetic ===\n";
    std::cout << "10 + 3 = " << (10 + 3) << '\n';
    std::cout << "10 / 3 = " << (10 / 3) << "  (int truncation)\n";
    std::cout << "10 % 3 = " << (10 % 3) << '\n';
    std::cout << "10.0/3 = " << (10.0 / 3) << "  (double)\n";

    std::cout << "\n=== Relational ===\n";
    int a = 5, b = 6;
    std::cout << std::boolalpha;        // print bools as 'true'/'false'
    std::cout << "a == b: " << (a == b) << '\n';
    std::cout << "a != b: " << (a != b) << '\n';
    std::cout << "a >  b: " << (a >  b) << '\n';
    std::cout << "a <  b: " << (a <  b) << '\n';

    std::cout << "\n=== Logical ===\n";
    bool x = true, y = false;
    std::cout << "x && y: " << (x && y) << '\n';
    std::cout << "x || y: " << (x || y) << '\n';
    std::cout << "!x    : " << (!x) << '\n';
    std::cout << "x and y (alt spelling): " << (x and y) << '\n';

    std::cout << "\n=== Bitwise ===\n";
    int p = 19, q = 28;             // 19 = 10011, 28 = 11100
    std::cout << "p     = " << std::bitset<8>(p) << '\n';
    std::cout << "q     = " << std::bitset<8>(q) << '\n';
    std::cout << "p & q = " << (p & q) << "  (== " << std::bitset<8>(p & q) << ")\n";
    std::cout << "p | q = " << (p | q) << '\n';
    std::cout << "p ^ q = " << (p ^ q) << '\n';
    std::cout << "~p    = " << (~p) << '\n';
    std::cout << "p<<2  = " << (p << 2) << '\n';
    std::cout << "p>>2  = " << (p >> 2) << '\n';

    std::cout << "\n=== Conditional & comma ===\n";
    int m = (a > b) ? a : b;
    std::cout << "max(a,b) via ?: = " << m << '\n';
    int n = (a += 1, b += 2, a + b);    // evaluates left-to-right; n = a+b
    std::cout << "comma op result n = " << n << " (a now " << a << ", b now " << b << ")\n";

    return 0;
}

/*
 * NOTES:
 *  - C++ has NO `>>>` (unsigned right shift). For an unsigned shift cast to
 *    `unsigned` (or `uint32_t`) first.
 *  - `&&` / `||` short-circuit, exactly like Java and Python.
 *  - Operator overloading lets you reuse `+`, `<<`, etc. on custom types
 *    (Java forbids operator overloading except for `+` on String).
 *  - `<bitset>` is great for visualising binary values in output.
 */
