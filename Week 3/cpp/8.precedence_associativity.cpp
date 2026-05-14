/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: Operator Precedence and Associativity
 * File: 8.precedence_associativity.cpp
 *
 * CONCEPT:
 *  Precedence determines which operator is evaluated first when multiple
 *  operators appear without parentheses. Associativity decides ties between
 *  operators of EQUAL precedence.
 *
 * KEY POINTS:
 *  - High to low (selected): postfix ++/-- > unary +/-/!/~ > * / % > + - >
 *    << >> > < <= > >= > == != > & > ^ > | > && > || > ?: > = += etc. > ,
 *  - Most binary operators are LEFT-TO-RIGHT.
 *  - Assignments and ternary `?:` are RIGHT-TO-LEFT.
 *  - C++ does NOT support chained comparisons (a > b > c parses as
 *    `(a > b) > c`, comparing a bool with c).
 *  - Operand evaluation order for most operators is UNSEQUENCED in C++ (UB
 *    if the operands have side effects on the same variable).
 */

#include <iostream>

static int x = 0;

int F1() { x = 5;  return x; }
int F2() { x = 10; return x; }

int main() {
    // Precedence basics
    std::cout << "10 + 20 * 30  = " << (10 + 20 * 30) << '\n';   // 610
    std::cout << "(10+20) * 30  = " << ((10 + 20) * 30) << '\n'; // 900

    // Right-associative assignment
    int a, b, c;
    a = b = c = 42;     // c=42, then b=42, then a=42
    std::cout << "a=" << a << " b=" << b << " c=" << c << '\n';

    // Operand evaluation ORDER for + is UNSEQUENCED in C++ (since C++17 it
    // is INDETERMINATELY SEQUENCED for some operators -- still no guarantee).
    int p = F1() + F2();
    std::cout << "F1() + F2() = " << p << "; final x = " << x << '\n';
    // The output for `final x` is implementation-dependent.

    // No chained comparisons
    // bool ok = 1 < 5 < 10;     // parses as (1 < 5) < 10 -> true < 10 -> 1 < 10 -> true (misleading!)
    bool correct = (1 < 5) && (5 < 10);
    std::cout << "1 < 5 && 5 < 10 = " << std::boolalpha << correct << '\n';

    return 0;
}

/*
 * NOTES:
 *  - C++ has WAY more operators than Java; the precedence table is dense.
 *  - When in doubt, ADD PARENTHESES; readability beats cleverness.
 *  - Avoid relying on operand evaluation order; never modify the same variable
 *    twice in one expression.
 *  - C++ has no chained comparisons; Python does.
 */
