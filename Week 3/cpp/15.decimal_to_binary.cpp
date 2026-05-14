/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: Decimal to Binary Conversion
 * File: 15.decimal_to_binary.cpp
 *
 * PROBLEM:
 *  Convert N to a binary representation, stored as a long long whose
 *  decimal digits ARE the binary digits.
 *
 * KEY POINTS:
 *  - bit = n % 2; binary += bit * pow_of_10; pow *= 10; n /= 2.
 *  - For just printing the binary representation, use std::bitset<64>(n).
 *
 * DRY RUN:
 *  N = 12 -> 1100  (long long stores 1100)
 */

#include <iostream>
#include <bitset>

long long dec_to_bin(long long n) {
    if (n == 0) return 0;
    long long binary = 0, p = 1;
    while (n > 0) {
        int bit = n % 2;
        binary += bit * p;
        p *= 10;
        n /= 2;
    }
    return binary;
}

int main() {
    long long n;
    if (!(std::cin >> n)) {
        for (long long v : {0LL, 1LL, 2LL, 12LL, 255LL, 1024LL}) {
            std::cout << v << " -> " << dec_to_bin(v)
                      << "    [bitset: " << std::bitset<16>(v) << "]\n";
        }
        return 0;
    }
    std::cout << dec_to_bin(n) << '\n';
    return 0;
}

/*
 * NOTES:
 *  - The "store binary as decimal-formatted long" trick keeps the value an
 *    integer; great for the original Java exercise, less great for big numbers.
 *  - For real binary output, use std::bitset<N>(n).to_string() or print bits manually.
 */
