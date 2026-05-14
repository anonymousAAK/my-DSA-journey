/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Variables and Addition
 * File: 4.add_two_numbers.cpp
 *
 * CONCEPT:
 * Variables in C++ are STATICALLY TYPED — you must declare a type at the
 * point of declaration. Local variables are NOT default-initialised; reading
 * an uninitialised variable is undefined behaviour.
 *
 * KEY POINTS:
 *  - Syntax: `type name [= value];`
 *  - C++11+ supports `auto x = expr;` (type deduced from the initialiser)
 *  - Names: letters, digits, _; cannot start with a digit; case-sensitive
 *  - Local vars on the stack get garbage values until you initialise them
 *  - Constants: `const int N = 10;` or `constexpr int N = 10;`
 *
 * SYNTAX:
 *   int a = 10;
 *   int b{25};            // brace initialisation (preferred, prevents narrowing)
 *   auto c = a + b;       // type deduced as int
 *
 * DRY RUN:
 *  a = 10; b = 25;
 *  c = a + b -> 35
 *  cout << c -> "35"
 *
 * COMPLEXITY: O(1) time and space.
 */

#include <iostream>

int main() {
    int a = 10;            // declaration + initialisation
    int b{25};              // brace-init (C++11), prevents narrowing
    int c = a + b;          // c = 35

    std::cout << c << '\n';

    // auto deduces the type from the right-hand side
    auto sum = a + b;       // int
    std::cout << "auto sum = " << sum << '\n';

    // const & constexpr — replace `final` from Java
    const int kFixed = 100;
    constexpr int kCompileTime = 5 * 5; // computed at compile time
    std::cout << "kFixed=" << kFixed
              << " kCompileTime=" << kCompileTime << '\n';

    // Declaration without initialisation: do NOT read before you write to it
    int unset;              // undefined value
    unset = 7;               // safe now
    std::cout << "unset (after assign) = " << unset << '\n';

    return 0;
}

/*
 * NOTES:
 *  - Java's local primitives MUST be initialised before use (compile error if not).
 *    C++ allows the declaration but reading an uninitialised value is
 *    undefined behaviour (a runtime hazard).
 *  - C++ has many integer widths: short, int, long, long long, plus the
 *    `int8_t` ... `int64_t` types from <cstdint>.
 *  - `auto` lets the compiler infer types — useful with iterators and templates.
 */
