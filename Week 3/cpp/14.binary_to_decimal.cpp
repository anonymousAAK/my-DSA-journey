/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: Binary to Decimal Conversion
 * File: 14.binary_to_decimal.cpp
 *
 * PROBLEM:
 *  Read a base-10 integer that LOOKS LIKE binary (e.g. 1100), output its
 *  decimal value (12).
 *
 * KEY POINTS:
 *  - Peel last digit with `% 10`, multiply by power of 2, accumulate.
 *  - Built-in alternative: `std::stoi("1100", nullptr, 2)` parses base 2.
 *
 * DRY RUN:
 *  1100 -> 0*1 + 0*2 + 1*4 + 1*8 = 12
 */

#include <iostream>
#include <string>

long long bin_to_dec(long long n) {
    long long dec = 0, p = 1;
    while (n > 0) {
        int bit = n % 10;
        dec += bit * p;
        p *= 2;
        n /= 10;
    }
    return dec;
}

int main() {
    long long n;
    if (!(std::cin >> n)) {
        for (long long v : {1100LL, 1LL, 0LL, 11111111LL}) {
            std::cout << v << " (binary) -> " << bin_to_dec(v)
                      << "    [stoi: " << std::stoll(std::to_string(v), nullptr, 2) << "]\n";
        }
        return 0;
    }
    std::cout << bin_to_dec(n) << '\n';
    return 0;
}

/*
 * NOTES:
 *  - For Java's Integer.parseInt(s, 2), C++ uses std::stoi/std::stoll with a radix.
 *  - Always validate that each "digit" is 0 or 1 in production code.
 */
