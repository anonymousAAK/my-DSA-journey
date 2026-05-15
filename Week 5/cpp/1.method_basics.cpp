/*
 * WEEK 5 - C++ FUNCTIONS & RECURSION
 * Topic: Function Basics
 * File: 1.method_basics.cpp
 *
 * CONCEPT:
 *  C++ functions are declared with `returnType name(params) { body }`. They
 *  can be standalone or members of a class. Default arguments and overloads
 *  are supported. Pass-by-value, pass-by-reference (&), and pointer (*) all
 *  exist.
 *
 * KEY POINTS:
 *  - Default args: void greet(const std::string& name = "world");
 *  - Pass by value (copy), by reference (`int&`), by pointer (`int*`).
 *  - `const T&` is the standard idiom to pass without copying nor mutating.
 *  - Lambdas: `[](int x) { return x*x; }`.
 *
 * SYNTAX:
 *   int add(int a, int b);
 *   void try_to_change(int n);                 // pass by value
 *   void try_to_change_ref(int& n);            // pass by reference
 *
 * DRY RUN:
 *  add(5, 6) -> 11
 *  try_to_change(x) leaves outer x alone
 *  try_to_change_ref(x) updates outer x
 *
 * COMPLEXITY: O(1) per call.
 */

#include <iostream>
#include <vector>

void greet() { std::cout << "Hello from a function!\n"; }

void print_sum(int a, int b) {
    std::cout << "Sum of " << a << " and " << b << " = " << (a + b) << '\n';
}

int add(int a, int b) { return a + b; }

int multiply(int x, int y) {
    int result = x * y;        // local
    return result;
}

void try_to_change(int n) {
    n = 999;       // local copy mutated
    std::cout << "  inside try_to_change (by value): n = " << n << '\n';
}

void try_to_change_ref(int& n) {
    n = 999;       // outer is mutated
}

void mutate_vector(std::vector<int>& v) {
    v.push_back(99);
}

int main() {
    greet();
    print_sum(3, 7);
    std::cout << "add(5, 6) = " << add(5, 6) << '\n';
    std::cout << "multiply(4, 3) = " << multiply(4, 3) << '\n';

    int x = 42;
    try_to_change(x);
    std::cout << "after by-value:    x = " << x << "  (still 42)\n";
    try_to_change_ref(x);
    std::cout << "after by-reference: x = " << x << "  (mutated!)\n";

    std::vector<int> v {1, 2, 3};
    mutate_vector(v);
    std::cout << "vector after mutate: ";
    for (int n : v) std::cout << n << ' ';
    std::cout << '\n';

    return 0;
}

/*
 * NOTES:
 *  - Java passes objects by reference but ints by value.
 *  - C++ exposes the SHARP DISTINCTION via `T`, `T&`, `T*`.
 *  - Use `const T&` to avoid copies for large objects without permitting mutation.
 *  - Lambdas (C++11) make function-passing painless.
 */
