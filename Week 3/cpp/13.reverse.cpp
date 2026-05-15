/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: Reverse the Digits of an Integer
 * File: 13.reverse.cpp
 *
 * PROBLEM:
 *  Read N, output reversed integer (drop trailing zeros).
 *
 * KEY POINTS:
 *  - Standard digit-extraction loop.
 *  - Cast n to long long if you might overflow (e.g. 2147483647 reversed).
 *
 * DRY RUN:
 *  N = 1234 -> 4321
 *  N = 10400 -> 401
 */

#include <iostream>
#include <cstdlib>

long long reverse_int(long long n) {
    long long sign = (n < 0) ? -1 : 1;
    n = std::llabs(n);
    long long rev = 0;
    while (n > 0) {
        rev = rev * 10 + n % 10;
        n /= 10;
    }
    return sign * rev;
}

int main() {
    long long n;
    if (!(std::cin >> n)) {
        for (long long v : {1234LL, 10400LL, 7LL, -42LL}) {
            std::cout << v << " -> " << reverse_int(v) << '\n';
        }
        return 0;
    }
    std::cout << reverse_int(n) << '\n';
    return 0;
}

/*
 * NOTES:
 *  - For 32-bit safety (LeetCode), check rev > INT_MAX/10 before each multiply.
 *  - C++ has no built-in string-reverse trick that maintains type; use std::to_string
 *    + std::reverse for the string-based variant.
 */
