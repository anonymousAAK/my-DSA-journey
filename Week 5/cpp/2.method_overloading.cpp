/*
 * WEEK 5 - C++ FUNCTIONS & RECURSION
 * Topic: Function Overloading
 * File: 2.method_overloading.cpp
 *
 * CONCEPT:
 *  C++ supports compile-time overloading by parameter list (number/types/order).
 *  The compiler picks the best match via overload resolution. Templates extend
 *  this to GENERIC parameter types.
 *
 * KEY POINTS:
 *  - Different param COUNT and/or TYPE distinguishes overloads.
 *  - Return type ALONE is NOT enough for overload resolution.
 *  - Overload resolution is at COMPILE TIME (static dispatch).
 *  - For runtime dispatch, use virtual functions (polymorphism).
 *
 * SYNTAX:
 *   int add(int, int);
 *   double add(double, double);
 *   template<typename T> T addG(T a, T b);
 *
 * DRY RUN:
 *  add(2, 3)        -> int overload
 *  add(1.5, 2.5)    -> double overload
 *  addG<int>(1, 2)  -> template instantiation
 */

#include <iostream>
#include <vector>
#include <string>

// Three overloads of add
int add(int a, int b) {
    std::cout << "add(int, int): ";
    return a + b;
}
int add(int a, int b, int c) {
    std::cout << "add(int, int, int): ";
    return a + b + c;
}
double add(double a, double b) {
    std::cout << "add(double, double): ";
    return a + b;
}

// Overloaded printer for different element types
void print_array(const std::vector<int>& v)    { std::cout << "int   : "; for (int x : v) std::cout << x << ' '; std::cout << '\n'; }
void print_array(const std::vector<double>& v) { std::cout << "double: "; for (double x : v) std::cout << x << ' '; std::cout << '\n'; }
void print_array(const std::vector<char>& v)   { std::cout << "char  : "; for (char x : v) std::cout << x << ' '; std::cout << '\n'; }

// Templated equivalent -- one definition, many instantiations
template <typename T>
T addG(T a, T b) { return a + b; }

int main() {
    std::cout << add(2, 3) << '\n';
    std::cout << add(1, 2, 3) << '\n';
    std::cout << add(1.5, 2.5) << '\n';

    print_array(std::vector<int>    {1, 2, 3});
    print_array(std::vector<double> {1.1, 2.2, 3.3});
    print_array(std::vector<char>   {'a', 'b', 'c'});

    // Templates
    std::cout << "addG<int>   = " << addG(1, 2) << '\n';
    std::cout << "addG<double>= " << addG(1.5, 2.5) << '\n';
    std::cout << "addG<string>= " << addG<std::string>("hello", "world") << '\n';

    return 0;
}

/*
 * NOTES:
 *  - C++ overloads are STATIC (compile-time); Java's are too.
 *  - Templates (C++) are roughly equivalent to Java GENERICS (with very different mechanics).
 *  - Overload resolution can be subtle; mixing implicit conversions may pick
 *    an unexpected overload -- enable warnings to catch surprises.
 */
