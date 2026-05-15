/*
 * WEEK 7 - C++ DSA
 * Topic: String Basics
 * File: 1.string_basics.cpp
 *
 * CONCEPT:
 *     std::string is a mutable, contiguous container of char.
 *     Common operations: size, indexing, substr, find, replace,
 *     stream concatenation with std::ostringstream / std::string +=.
 *
 * KEY POINTS:
 *     - std::string is mutable, unlike Java String — append in place is O(1)
 *       amortised.
 *     - std::string::find returns std::string::npos when not found.
 *     - For repeated building, std::ostringstream / push_back / += all work;
 *       += is O(1) amortised because std::string maintains a capacity buffer.
 *
 * ALGORITHM / APPROACH:
 *     Showcase: size(), [i], substr(start, length), find(c), find(s),
 *     replace, transform (std::transform + std::tolower), split.
 *
 * C++-SPECIFIC NOTES:
 *     - No built-in split; show a manual one using std::stringstream.
 *     - std::transform with ::tolower converts a string in place.
 *     - To reverse, use std::reverse on the iterator pair.
 *
 * DRY RUN:
 *     s = "Hello, World!"
 *     s.size() = 13
 *     s[7] = 'W'
 *     s.substr(7, 5) = "World"
 *     s.find('o') = 4
 *
 * COMPLEXITY:
 *     Most operations O(n) in the size of their argument; subscript is O(1).
 */

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>
#include <cctype>

std::vector<std::string> split(const std::string& s, char delim) {
    std::vector<std::string> out;
    std::string token;
    std::stringstream ss(s);
    while (std::getline(ss, token, delim)) out.push_back(token);
    return out;
}

std::string toLower(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c) { return std::tolower(c); });
    return s;
}

std::string toUpper(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c) { return std::toupper(c); });
    return s;
}

int main() {
    std::string s = "Hello, World!";
    std::cout << "String: " << s << "\n";
    std::cout << "size: " << s.size() << "\n";
    std::cout << "s[7]: " << s[7] << "\n";
    std::cout << "substr(7, 5): " << s.substr(7, 5) << "\n";
    std::cout << "find('o'): " << s.find('o') << "\n";
    std::cout << "rfind('o'): " << s.rfind('o') << "\n";
    std::cout << "find(\"World\"): " << s.find("World") << "\n";
    std::cout << "toLower: " << toLower(s) << "\n";
    std::cout << "toUpper: " << toUpper(s) << "\n";

    // Replace all 'l' with 'r'
    std::string r = s;
    std::replace(r.begin(), r.end(), 'l', 'r');
    std::cout << "replace 'l' -> 'r': " << r << "\n";

    // --- Comparison ---
    std::string a = "apple", b = "apple";
    std::cout << "\n\"apple\" == \"apple\": " << (a == b) << "\n";  // 1 (content)
    std::cout << "compare(\"apple\",\"banana\"): "
              << std::string("apple").compare("banana") << "\n";     // negative

    // --- Iterate ---
    std::cout << "\nChars: ";
    for (char c : s) std::cout << c;
    std::cout << "\n";

    // --- Split ---
    std::string csv = "one,two,three,four";
    std::cout << "\nSplit by ',':\n";
    for (const auto& p : split(csv, ',')) std::cout << "  " << p << "\n";

    // --- Build with += (amortised O(1)) ---
    std::string built;
    for (int i = 1; i <= 5; ++i) {
        built += std::to_string(i);
        if (i < 5) built += "-";
    }
    std::cout << "\nBuilt: " << built << "\n";

    // --- Reverse ---
    std::string rev = "hello";
    std::reverse(rev.begin(), rev.end());
    std::cout << "Reversed 'hello': " << rev << "\n";

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - std::string is mutable; += is O(1) amortised — no StringBuilder needed.
 *     - std::string::find returns npos (size_t max) when missing.
 *     - There is no built-in split — use stringstream + getline.
 *     - char operations use <cctype> with unsigned-char casts to avoid UB.
 */
