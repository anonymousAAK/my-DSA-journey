/*
 * WEEK 5 - C++ FUNCTIONS & RECURSION
 * Topic: Recursion Basics
 * File: 3.recursion_basics.cpp
 *
 * CONCEPT:
 *  Recursive functions invoke themselves with a smaller problem instance.
 *  Need a BASE CASE and a RECURSIVE CASE.
 *
 * KEY POINTS:
 *  - C++ has no built-in tail-call optimisation guarantee (some compilers do it).
 *  - Stack typically has 1-8 MB -- recursion depths into the millions can crash.
 *  - Prefer iteration for very deep problems.
 *
 * COMPLEXITY:
 *  - Linear recursion: O(n) time, O(n) stack.
 *  - Fast power: O(log n).
 */

#include <iostream>

void print_desc(int n) {
    if (n == 0) return;
    std::cout << n << ' ';
    print_desc(n - 1);
}

void print_asc(int n) {
    if (n == 0) return;
    print_asc(n - 1);
    std::cout << n << ' ';
}

long long factorial(int n) {
    if (n <= 1) return 1;
    return (long long)n * factorial(n - 1);
}

int sum_n(int n) {
    if (n == 0) return 0;
    return n + sum_n(n - 1);
}

long long power(long long base, int exp) {
    if (exp == 0) return 1;
    return base * power(base, exp - 1);
}

long long fast_power(long long base, int exp) {
    if (exp == 0) return 1;
    if (exp % 2 == 0) {
        long long h = fast_power(base, exp / 2);
        return h * h;
    }
    return base * fast_power(base, exp - 1);
}

int main() {
    std::cout << "Descending 5..1: "; print_desc(5); std::cout << '\n';
    std::cout << "Ascending  1..5: "; print_asc(5);  std::cout << '\n';

    std::cout << "5!  = " << factorial(5) << '\n';
    std::cout << "10! = " << factorial(10) << '\n';

    std::cout << "sum(10) = " << sum_n(10) << '\n';

    std::cout << "2^10 = " << power(2, 10) << '\n';
    std::cout << "2^10 (fast) = " << fast_power(2, 10) << '\n';
    std::cout << "3^20 (fast) = " << fast_power(3, 20) << '\n';

    return 0;
}

/*
 * NOTES:
 *  - long long is 64-bit; factorial(20) fits, factorial(21) overflows.
 *  - For very large factorials, use Boost.Multiprecision.
 *  - Fast exponentiation by squaring is a foundational DSA technique.
 */
