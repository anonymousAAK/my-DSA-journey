/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Mixing Integer and String Input + Concatenation
 * File: 11.integer_and_string.cpp
 *
 * CONCEPT:
 * Reading a string then an integer, then printing them with a space between.
 * Unlike Java, you cannot do `s + 1` to glue an int onto a string — convert
 * the int with `std::to_string(n)` first OR rely on stream operator chaining.
 *
 * KEY POINTS:
 *  - `s + std::to_string(n)`  -> string concat
 *  - `cout << s << ' ' << n` -> stream multiple values without manual concat
 *  - Use `std::to_string(...)` (C++11) for numeric-to-string conversion
 *  - `std::stoi(str)` is the inverse — parse int from string
 *
 * SYNTAX:
 *   std::string out = name + " " + std::to_string(age);
 *   std::cout << name << " " << age;
 *
 * DRY RUN:
 *  Stdin: "Alice 30"
 *    name="Alice", n=30
 *    output: "Alice 30"
 */

#include <iostream>
#include <string>

int main() {
    std::string name;
    int n;
    std::cin >> name >> n;

    // Streaming approach (most idiomatic for I/O)
    std::cout << name << " " << n << '\n';

    // Build a single std::string by concatenation
    std::string combined = name + " " + std::to_string(n);
    std::cout << combined << '\n';

    return 0;
}

/*
 * NOTES:
 *  - Java auto-converts in `name + " " + n` because `+` triggers String.valueOf(int).
 *  - C++ requires explicit `std::to_string(n)` to concat with std::string.
 *  - For high-performance string assembly, use `std::ostringstream` or `std::format`.
 */
