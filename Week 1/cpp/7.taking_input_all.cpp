/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Reading All Common Input Types
 * File: 7.taking_input_all.cpp
 *
 * CONCEPT:
 * Java's `Scanner` exposes one method per type (nextInt, nextDouble, etc.).
 * C++ relies on operator `>>` to pick the right parse based on the
 * destination variable's type. The end result is the same.
 *
 * KEY POINTS:
 *  - `>>` is overloaded for char, int, long, long long, float, double, string, ...
 *  - `cin >> w`   where w is a std::string reads ONE whitespace-delimited token.
 *  - `getline(cin, s)` reads a full line.
 *  - For a "single char" use `cin >> ch` (skips whitespace) or `cin.get(ch)`.
 *  - Always check that the extraction succeeded: `if (!(cin >> x)) ...`.
 *
 * SYNTAX:
 *   int i;          cin >> i;
 *   long long lo;   cin >> lo;
 *   double  d;      cin >> d;
 *   std::string w;  cin >> w;          // one token
 *   std::getline(cin, line);            // one line
 *
 * DRY RUN:
 *  Stdin: "10 5 hello 3.14 12345678901234567890"
 *    a=10, b=5, c=15
 *    word="hello", ch='h'
 *    d=3.14, lo=very big number
 */

#include <iostream>
#include <string>
#include <limits>

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int a, b;
    std::cin >> a >> b;            // nextInt, nextInt
    int c = a + b;
    std::cout << "a + b = " << c << '\n';

    std::string word;
    std::cin >> word;              // next() — one token
    char ch = word.empty() ? '?' : word[0];
    std::cout << "First char of '" << word << "' = '" << ch << "'\n";

    double d;
    std::cin >> d;                 // nextDouble
    std::cout << "double = " << d << '\n';

    long long lo;
    std::cin >> lo;                // nextLong
    std::cout << "long long = " << lo << '\n';

    return 0;
}

/*
 * NOTES:
 *  - C++ requires <string> for std::string and <limits> for buffer draining.
 *  - On failed parse, `cin` enters a fail state and subsequent reads silently fail
 *    until you call `cin.clear()` and discard the bad input.
 *  - For very fast input, disable C-stdio sync (shown above) — this is the C++
 *    equivalent of Python's `sys.stdin.readline()` trick.
 *  - C++ has fixed-width long long (64 bits); Python int / Java BigInteger are
 *    arbitrary precision.
 */
