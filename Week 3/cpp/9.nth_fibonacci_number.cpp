/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: Nth Fibonacci Number (Iterative)
 * File: 9.nth_fibonacci_number.cpp
 *
 * PROBLEM:
 *  Read N, print F(N). F(1)=0, F(2)=1, F(n) = F(n-1)+F(n-2).
 *
 * KEY POINTS:
 *  - O(n) iterative loop with two rolling variables.
 *  - Use long long for N up to ~92; beyond that even long long overflows.
 *  - For Java's BigInteger style, use Boost.Multiprecision in C++.
 *
 * DRY RUN (n=5):
 *  a=0,b=1 -> a=1,b=1 -> a=1,b=2 -> a=2,b=3 -> a=3,b=5 -> a=5,b=8
 *  return a = 5
 *
 * COMPLEXITY: O(n) time, O(1) space.
 */

#include <iostream>

long long fib(int n) {
    long long a = 0, b = 1;
    for (int i = 0; i < n; ++i) {
        long long c = a + b;
        a = b;
        b = c;
    }
    return a;
}

int main() {
    int n;
    if (!(std::cin >> n)) {
        for (int i = 0; i < 10; ++i) std::cout << fib(i) << ' ';
        std::cout << '\n';
        std::cout << "fib(50) = " << fib(50) << '\n';
        return 0;
    }
    std::cout << fib(n) << '\n';
    return 0;
}

/*
 * NOTES:
 *  - long long is 64-bit; fib(92) overflows. Use BigInteger libraries for more.
 *  - Iterative O(n) is the standard; matrix exponentiation gives O(log n).
 *  - Memoised recursion is common but allocates more memory.
 */
