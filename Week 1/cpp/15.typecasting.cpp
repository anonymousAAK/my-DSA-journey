/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Typecasting (Implicit and Explicit Conversions)
 * File: 15.typecasting.cpp
 *
 * CONCEPT:
 * C++ has two flavours of casts: IMPLICIT (compiler does it for you, e.g.
 * widening int -> long -> double) and EXPLICIT (you write a cast). Modern
 * C++ favours the four "named" casts:
 *   static_cast<T>(x)       - safe value-changing conversion
 *   const_cast<T>(x)         - add/remove const qualifier
 *   reinterpret_cast<T>(x)  - low-level bit reinterpretation (DANGEROUS)
 *   dynamic_cast<T>(x)       - safe downcast in polymorphic hierarchies
 *
 * KEY POINTS:
 *  - Widening (int -> long, int -> double) is implicit.
 *  - Narrowing (double -> int) requires an explicit cast; truncates toward zero.
 *  - C-style cast `(T) x` still works but is discouraged in new code.
 *  - `static_cast<long>(d)` matches Java's `(long) d`.
 *  - Brace initialisation `int n{d};` REJECTS narrowing at compile time.
 *
 * SYNTAX:
 *   long  l1 = i;                       // implicit widening
 *   long  l2 = static_cast<long>(d);    // explicit narrowing (truncates)
 *   int   n  = (int) 3.7;               // C-style cast (still legal)
 *
 * DRY RUN:
 *  i=100;       l1 = i               -> 100
 *  d=100.04;    l2 = static_cast<long>(d) -> 100  (decimal truncated)
 *  d=-100.99;   static_cast<long>(d) -> -100 (NOT -101)
 */

#include <iostream>

int main() {
    int i = 100;
    long l1 = i;                                  // implicit widening
    double d = 100.04;
    long l2 = static_cast<long>(d);              // explicit narrowing
    long l3 = (long)d;                            // C-style equivalent

    std::cout << i << '\n';
    std::cout << l1 << '\n';
    std::cout << d << '\n';
    std::cout << l2 << "  (static_cast)\n";
    std::cout << l3 << "  (C-style cast)\n";

    // Truncation (toward zero) demo
    std::cout << "static_cast<int>(-100.99) = "
              << static_cast<int>(-100.99) << "  (NOT -101)\n";

    // Narrowing rejection with braces
    // int bad{d};   // compile error: narrowing conversion from double to int

    // Implicit promotion happens during arithmetic
    int    a = 1;
    double b = 2.5;
    auto   sum = a + b;            // double, value 3.5
    std::cout << "1 + 2.5 = " << sum << " (type deduced via auto)\n";

    return 0;
}

/*
 * NOTES:
 *  - Java forbids implicit narrowing; C++ permits it via implicit conversions
 *    (with warnings). Use brace-init for safety.
 *  - The four named casts make the intent of each conversion explicit and
 *    grep-able — preferred over the bare `(T) x` C-style cast.
 *  - For converting between pointer/reference types in class hierarchies,
 *    use dynamic_cast (Java equivalent: `(SubClass) obj` with `instanceof`).
 */
