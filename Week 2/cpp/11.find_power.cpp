/*
 * WEEK 2 - C++ CONTROL FLOW
 * Topic: x^n via repeated multiplication
 * File: 11.find_power.cpp
 *
 * PROBLEM:
 *  Read x and n, print x^n. Convention 0^0 = 1.
 *
 * CONCEPT:
 *  O(n) loop accumulates x^n. Use `long long` for the result. We also
 *  showcase the O(log n) fast-power algorithm.
 *
 * KEY POINTS:
 *  - `std::pow(x, n)` returns a double; risk of precision loss for big ints.
 *  - Beware overflow: 2^63 fits in unsigned long long but not signed.
 *  - The fast-power pattern (exp by squaring) cuts to O(log n).
 *
 * DRY RUN:
 *  x=2, n=10 -> 1024
 *  x=3, n=20 -> 3486784401
 *
 * COMPLEXITY: O(n) linear; O(log n) fast.
 */

#include <iostream>

long long power_linear(long long x, int n) {
    long long ans = 1;
    for (int i = 0; i < n; ++i) ans *= x;
    return ans;
}

long long fast_pow(long long x, int n) {
    if (n == 0) return 1;
    if (n % 2 == 0) {
        long long h = fast_pow(x, n / 2);
        return h * h;
    }
    return x * fast_pow(x, n - 1);
}

int main() {
    int x, n;
    if (!(std::cin >> x >> n)) { x = 2; n = 10; std::cout << "(demo x=2 n=10)\n"; }
    std::cout << x << "^" << n << " = " << power_linear(x, n) << "  (linear)\n";
    std::cout << x << "^" << n << " = " << fast_pow(x, n)     << "  (fast)\n";
    return 0;
}

/*
 * NOTES:
 *  - For modular exponentiation, take `% mod` after every multiply to avoid overflow.
 *  - `std::pow` is fine for floating-point bases but loses precision for big ints.
 *  - Java's `Math.pow` likewise returns double; use `BigInteger.pow` for exact.
 */
