/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: How Integers are Stored in Memory
 * File: 13.how_integer_is_stored.cpp
 *
 * CONCEPT:
 * Like Java, C++ stores signed integers in two's-complement form on virtually
 * every modern platform (since C++20 the standard formally REQUIRES it).
 * Negative numbers reuse the same hardware addition logic as positives.
 *
 * KEY POINTS:
 *  - sizeof(int) is 4 bytes on most desktops, but the standard only guarantees >= 2.
 *  - For positive n: bit pattern == binary of n.
 *  - For negative n: bit pattern == 2^N + n (mod 2^N).
 *  - Two's complement: invert the bits of |n|, then add 1.
 *  - Bitwise operators (& | ^ ~ << >>) work directly on the underlying bits.
 *  - Use std::bitset<32> for nice binary printing.
 *
 * SYNTAX:
 *   #include <bitset>
 *   std::cout << std::bitset<32>(n) << '\n';
 *
 * DRY RUN — derive the 32-bit pattern of -4:
 *  1. +4  = 0000_0000_0000_0000_0000_0000_0000_0100
 *  2. ~4  = 1111_1111_1111_1111_1111_1111_1111_1011
 *  3. +1  = 1111_1111_1111_1111_1111_1111_1111_1100  (== -4 in two's complement)
 */

#include <iostream>
#include <bitset>
#include <cstdint>
#include <climits>

int main() {
    std::cout << "sizeof(int)  = " << sizeof(int)  << " bytes ("
              << sizeof(int) * 8 << " bits)\n";
    std::cout << "INT_MIN      = " << INT_MIN << '\n';
    std::cout << "INT_MAX      = " << INT_MAX << '\n';

    int positive = 4;
    int negative = -4;

    std::cout << "\n=== +4 ===\n";
    std::cout << "decimal: " << positive << '\n';
    std::cout << "32-bit : " << std::bitset<32>(positive) << '\n';

    std::cout << "\n=== -4 (two's complement) ===\n";
    std::cout << "decimal: " << negative << '\n';
    std::cout << "32-bit : " << std::bitset<32>(negative) << '\n';

    // Manual derivation
    std::int32_t step1 = 4;                          // +|n|
    std::int32_t step2 = ~step1;                      // ones complement
    std::int32_t step3 = step2 + 1;                   // twos complement
    std::cout << "\nstep 1) +4 binary       = " << std::bitset<32>(step1) << '\n';
    std::cout << "step 2) inverted bits   = " << std::bitset<32>(step2) << '\n';
    std::cout << "step 3) plus 1 (== -4) = " << std::bitset<32>(step3) << '\n';

    // Overflow demo (signed wraparound is technically UB; unsigned is well-defined)
    std::uint32_t u = 0xFFFFFFFFu;
    std::cout << "\nunsigned 0xFFFFFFFF + 1 = " << (u + 1) << "  (wraps to 0)\n";

    return 0;
}

/*
 * NOTES:
 *  - C++ guarantees two's complement only since C++20; earlier it was
 *    implementation-defined (in practice every mainstream compiler used 2C).
 *  - Signed overflow is UB in C++; unsigned overflow wraps modulo 2^N.
 *  - <bitset> provides cheap stringified binary printing.
 *  - For arbitrary-precision integers, consider Boost.Multiprecision.
 */
