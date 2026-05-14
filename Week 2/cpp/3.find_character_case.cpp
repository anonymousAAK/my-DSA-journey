/*
 * WEEK 2 - C++ CONTROL FLOW
 * Topic: Character Case Detection via ASCII Values
 * File: 3.find_character_case.cpp
 *
 * PROBLEM:
 *  Output 1 for uppercase, 0 for lowercase, -1 otherwise.
 *
 * CONCEPT:
 *  Use the ASCII value of the character. Cast char to int (implicit) and
 *  test against the appropriate ranges. <cctype> offers `std::isupper`,
 *  `std::islower`, `std::isalpha` helpers.
 *
 * KEY POINTS:
 *  - 'A'-'Z' have codes 65-90; 'a'-'z' have 97-122.
 *  - `std::isupper((unsigned char) ch)` is the safe portable test.
 *  - Always cast to `unsigned char` before <cctype> functions to avoid UB
 *    when char is signed and the value is negative.
 *
 * SYNTAX:
 *   if (std::isupper((unsigned char) ch)) ...
 *
 * DRY RUN:
 *  ch='Q' -> isupper -> 1
 *  ch='q' -> islower -> 0
 *  ch='7' -> neither -> -1
 *
 * COMPLEXITY: O(1).
 */

#include <iostream>
#include <cctype>
#include <string>

int classify(char ch) {
    auto uc = static_cast<unsigned char>(ch);
    if (std::isupper(uc)) return 1;
    if (std::islower(uc)) return 0;
    return -1;
}

int main() {
    std::string s;
    if (!(std::cin >> s)) {
        // No input piped -- run the small demo.
        for (char c : {'Q', 'q', '7', '!'}) {
            std::cout << "'" << c << "' -> " << classify(c) << '\n';
        }
        return 0;
    }
    std::cout << classify(s[0]) << '\n';
    return 0;
}

/*
 * NOTES:
 *  - Java offers Character.isUpperCase / isLowerCase; C++ uses <cctype>.
 *  - char in C++ may be signed OR unsigned (implementation-defined).
 *    Casting to `unsigned char` first is the standard guard.
 *  - For locale-aware classification use <locale> or <cwctype> for wide chars.
 */
