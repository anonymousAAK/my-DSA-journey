/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Reading User Input with std::cin
 * File: 6.taking_input.cpp
 *
 * CONCEPT:
 * `std::cin` is the standard input stream. Use the extraction operator `>>`
 * to read whitespace-separated tokens. Internally `>>` skips leading
 * whitespace and stops at the next whitespace — analogous to Java's
 * Scanner.next()/nextInt(). For an entire line use `std::getline(std::cin, s)`.
 *
 * KEY POINTS:
 *  - `std::cin >> x;`               -> read a token, parse it as the type of `x`.
 *  - `std::cin >> a >> b;`          -> read two tokens.
 *  - `std::getline(cin, s)`         -> read a whole line into a std::string.
 *  - Mixing `>>` and `getline` requires `cin.ignore()` to drop the leftover '\n'.
 *  - Failed parses leave `cin` in a fail state — check with `if (cin)` or `cin.fail()`.
 *  - For speed, disable sync with C stdio:
 *        std::ios_base::sync_with_stdio(false);
 *        std::cin.tie(nullptr);
 *
 * SYNTAX:
 *   int a, b;        std::cin >> a >> b;
 *   std::string s;   std::getline(std::cin, s);
 *   char ch = s[0];  // first character of the line
 *
 * DRY RUN:
 *  Stdin: "10 25\nhello"
 *    a=10, b=25, c=35
 *    line="hello", ch='h'
 *
 * COMPLEXITY: O(n) where n is the input length.
 */

#include <iostream>
#include <string>
#include <limits>

int main() {
    int a = 0, b = 0;
    std::cout << "Enter two integers separated by whitespace: ";
    if (!(std::cin >> a >> b)) {
        std::cerr << "Failed to read two integers.\n";
        return 1;
    }

    int c = a + b;
    std::cout << "a + b = " << c << '\n';

    // After numeric extraction, drop the leftover newline before getline
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    std::cout << "Enter a line of text: ";
    std::string line;
    std::getline(std::cin, line);
    if (!line.empty()) {
        char ch = line[0];      // first character (a single char)
        std::cout << "First character: " << ch << '\n';
    }

    // Demonstrate reading other types
    std::cout << "Enter a double: ";
    double d;  std::cin >> d;
    std::cout << "double value = " << d << '\n';

    std::cout << "Enter a long long: ";
    long long lo; std::cin >> lo;
    std::cout << "long long value = " << lo << '\n';

    return 0;
}

/*
 * NOTES:
 *  - Java: Scanner s = new Scanner(System.in); s.nextInt(); s.nextLine();
 *    C++:  std::cin >> ...; std::getline(std::cin, s);
 *  - Both languages share the "leftover newline" pitfall when mixing token
 *    reads with line reads. Use `cin.ignore(...)` to drain the buffer.
 *  - `std::cin` ignores leading whitespace by default for `>>` extractions.
 *    To read a single character INCLUDING whitespace use `cin.get(ch)`.
 *  - Including <limits> is required for `std::numeric_limits`.
 */
