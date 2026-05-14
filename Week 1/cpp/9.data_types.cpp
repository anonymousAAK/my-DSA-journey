/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Data Types in C++
 * File: 9.data_types.cpp
 *
 * CONCEPT:
 * C++ exposes a richer (and more confusing) set of fundamental types than
 * Java. Sizes are IMPLEMENTATION-DEFINED on most platforms — only minimums
 * are guaranteed by the standard. Use <cstdint> for fixed-width sizes.
 *
 * KEY POINTS:
 *  - Integer family (signed by default; can be `unsigned`):
 *      char       (>= 1 byte; usually 1)
 *      short      (>= 2 bytes)
 *      int        (>= 2; commonly 4)
 *      long       (>= 4)
 *      long long  (>= 8)
 *  - Fixed-width: int8_t, int16_t, int32_t, int64_t (and unsigned variants).
 *  - Floating-point: float (32-bit), double (64-bit), long double (>=64).
 *  - bool: true / false (typically 1 byte; not specified).
 *  - char IS an integer type — `char ch = 'A';` and `int(ch)` -> 65.
 *  - std::string is a CLASS (not a fundamental type), declared in <string>.
 *  - Use `sizeof(T)` to find the byte size on your platform.
 *
 * SYNTAX:
 *   char     c = 'A';     // 1 byte
 *   short    s = 32000;
 *   int      i = 100000;
 *   long     l = 1L;
 *   long long ll = 1LL;
 *   float    f = 1.5f;     // suffix 'f' for single precision
 *   double   d = 1.5;       // double by default
 *   bool     b = true;
 *
 * DRY RUN:
 *  sizeof(int) == 4 on most desktops
 *  sizeof(long long) == 8
 *  sizeof(double) == 8
 */

#include <iostream>
#include <cstdint>
#include <string>
#include <iomanip>

int main() {
    std::cout << std::left
              << std::setw(20) << "type" << std::setw(15) << "sizeof (bytes)" << '\n';
    std::cout << "----------------------------------------\n";
    std::cout << std::setw(20) << "char"        << sizeof(char)        << '\n';
    std::cout << std::setw(20) << "short"       << sizeof(short)       << '\n';
    std::cout << std::setw(20) << "int"         << sizeof(int)         << '\n';
    std::cout << std::setw(20) << "long"        << sizeof(long)        << '\n';
    std::cout << std::setw(20) << "long long"   << sizeof(long long)   << '\n';
    std::cout << std::setw(20) << "float"       << sizeof(float)       << '\n';
    std::cout << std::setw(20) << "double"      << sizeof(double)      << '\n';
    std::cout << std::setw(20) << "long double" << sizeof(long double) << '\n';
    std::cout << std::setw(20) << "bool"        << sizeof(bool)        << '\n';
    std::cout << std::setw(20) << "int32_t"     << sizeof(std::int32_t)<< '\n';
    std::cout << std::setw(20) << "int64_t"     << sizeof(std::int64_t)<< '\n';
    std::cout << std::setw(20) << "std::string" << sizeof(std::string) << "  (object header only)\n";

    // Default values & uninitialised behaviour
    int unset;          // garbage value
    int zero{};          // brace-init -> 0 (value-initialised)
    std::cout << "\nzero (value-initialised) = " << zero << '\n';
    std::cout << "unset (uninitialised)     = (undefined; do not use)\n";

    // Reading a single token (similar to Scanner.next())
    std::cout << "\nEnter a word: ";
    std::string word;
    if (std::cin >> word) {
        std::cout << "You entered: " << word << '\n';
    }

    return 0;
}

/*
 * NOTES:
 *  - Java's `int` is fixed at 32 bits; C++ `int` is platform-defined (>= 16 bits).
 *  - Java's `char` is 16-bit Unicode code unit; C++ `char` is 1 byte (ASCII).
 *    For wide characters use `wchar_t`, `char16_t`, `char32_t`, or `std::u8string`.
 *  - Java's `String` is reference type; C++ `std::string` is a value type.
 *  - C++ has both signed and unsigned integers; Java only signed (except `char`).
 */
