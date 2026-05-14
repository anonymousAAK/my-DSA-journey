/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: Bitwise Operators
 * File: 7.bitwise_operator.cpp
 *
 * CONCEPT:
 *  C++ provides & | ^ ~ << >> on integer types. There is NO built-in
 *  unsigned-right-shift operator (`>>>` in Java) -- emulate by casting to
 *  the unsigned type first.
 *
 * KEY POINTS:
 *  - Right shift on a SIGNED negative value is implementation-defined
 *    (typically arithmetic on x86; logical on some platforms before C++20).
 *    From C++20 it is REQUIRED to be arithmetic shift on signed types.
 *  - Cast to `unsigned int` for the equivalent of Java's `>>>`.
 *  - <bitset> can show binary representations.
 */

#include <iostream>
#include <bitset>
#include <cstdint>

int main() {
    int a = 19;        // 10011
    int b = 28;        // 11100

    std::cout << "a       = " << std::bitset<5>(a) << "  (" << a << ")\n";
    std::cout << "b       = " << std::bitset<5>(b) << "  (" << b << ")\n";
    std::cout << "a & b   = " << (a & b) << "    (" << std::bitset<5>(a & b) << ")\n";
    std::cout << "a | b   = " << (a | b) << "    (" << std::bitset<5>(a | b) << ")\n";
    std::cout << "a ^ b   = " << (a ^ b) << "    (" << std::bitset<5>(a ^ b) << ")\n";
    std::cout << "~a      = " << (~a) << "  (-(a+1))\n";
    std::cout << "a << 2  = " << (a << 2) << '\n';
    std::cout << "a >> 2  = " << (a >> 2) << '\n';

    // Java's >>> emulation:
    int n = -4;
    unsigned int un = static_cast<unsigned int>(n);
    std::cout << "(unsigned)-4 >> 28 = " << (un >> 28) << '\n';

    // Bit tricks
    int x = 0b10110;
    std::cout << "extract bit 1 of " << std::bitset<5>(x) << ": " << ((x >> 1) & 1) << '\n';
    std::cout << "set bit 0      : " << std::bitset<5>(x | (1 << 0)) << '\n';
    std::cout << "clear bit 1    : " << std::bitset<5>(x & ~(1 << 1)) << '\n';
    std::cout << "flip bit 4     : " << std::bitset<5>(x ^ (1 << 4)) << '\n';

    return 0;
}

/*
 * NOTES:
 *  - Pre-C++20, `>>` on negative SIGNED ints was implementation-defined.
 *    Since C++20 it's guaranteed arithmetic.
 *  - For Java's `>>>` use `static_cast<unsigned>(x) >> n` then cast back.
 *  - <bitset> is great for visualisation; `std::bitset<32>(n)` prints 32 bits.
 *  - For 64-bit constants use the `LL` / `ULL` suffix and `int64_t` types.
 */
