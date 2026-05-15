/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: How float, double, and char are Stored
 * File: 14.how_other_datatypes_are_stored.cpp
 *
 * CONCEPT:
 * C++ distinguishes float (IEEE 754 single precision, 32 bits) and double
 * (IEEE 754 double precision, 64 bits). Decimal literals default to double;
 * use the `f` suffix for float. `char` is a 1-byte integer holding an
 * ASCII (or other narrow encoding) code point — implicitly convertible to int.
 *
 * KEY POINTS:
 *  - 1.0     -> double (8 bytes)
 *  - 1.0f    -> float  (4 bytes)
 *  - 1.0L    -> long double (often 10/12/16 bytes, platform-dependent)
 *  - char ch = 'A';  static_cast<int>(ch) -> 65  (ASCII)
 *  - char + int promotes to int: 'a' + 1 == 98
 *  - For Unicode use char16_t / char32_t / wchar_t / std::u8string
 *  - <cfloat> exposes FLT_MIN/MAX, DBL_MIN/MAX, FLT_DIG, DBL_DIG, etc.
 *
 * SYNTAX:
 *   float f  = 1.5f;
 *   double d = 1.5;
 *   char  c  = 'X';            // 1 byte
 *   int   ic = c;               // 88 (implicit promotion)
 *   char  c2 = (char) 89;       // 'Y'
 *
 * DRY RUN:
 *  - char ch1=88, ch2='Y' -> "X Y"
 *  - 'a' + 1 -> 98 (int)
 *  - 'a' + 'b' -> 195
 */

#include <iostream>
#include <cfloat>
#include <climits>
#include <iomanip>

int main() {
    std::cout << std::left
              << std::setw(15) << "type" << std::setw(15) << "size (bytes)"
              << "  notes\n";
    std::cout << "----------------------------------------\n";
    std::cout << std::setw(15) << "char"        << std::setw(15) << sizeof(char)        << "  1 byte; ASCII code\n";
    std::cout << std::setw(15) << "wchar_t"     << std::setw(15) << sizeof(wchar_t)     << "  wide char (impl-defined)\n";
    std::cout << std::setw(15) << "char16_t"    << std::setw(15) << sizeof(char16_t)    << "  UTF-16 code unit\n";
    std::cout << std::setw(15) << "char32_t"    << std::setw(15) << sizeof(char32_t)    << "  UTF-32 code point\n";
    std::cout << std::setw(15) << "float"       << std::setw(15) << sizeof(float)       << "  IEEE 754 single (use 'f' suffix)\n";
    std::cout << std::setw(15) << "double"      << std::setw(15) << sizeof(double)      << "  IEEE 754 double (default for literals)\n";
    std::cout << std::setw(15) << "long double" << std::setw(15) << sizeof(long double) << "  extended precision\n";

    // Float vs double precision
    float  f = 10.4f;
    double d = 10.4;
    std::cout << std::fixed << std::setprecision(20)
              << "\nfloat  10.4f = " << f << '\n'
              << "double 10.4   = " << d << '\n';

    // Char arithmetic — exactly like Java
    char ch1 = 88;       // 'X'
    char ch2 = 'Y';
    std::cout << '\n' << ch1 << ' ' << ch2 << '\n';

    std::cout << "'a' + 1     = " << ('a' + 1) << '\n';        // 98 (int)
    std::cout << "'a' + 'b'  = " << ('a' + 'b') << '\n';       // 195
    std::cout << "static_cast<char>('a' + 1) = '"
              << static_cast<char>('a' + 1) << "'\n";          // 'b'

    return 0;
}

/*
 * NOTES:
 *  - C++'s `char` is 1 byte; Java's `char` is 2 bytes (Unicode UTF-16 code unit).
 *  - The 'f' suffix matters: `1.5` is double; `1.5f` is float.
 *  - For exact decimal arithmetic use a third-party library (no built-in equivalent
 *    of Python's `decimal.Decimal` in standard C++).
 *  - `static_cast<char>(int)` is the explicit narrowing conversion.
 */
