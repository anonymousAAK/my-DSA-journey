// Reference C++ driver for tests/cases/palindrome_check.json.
// Case-insensitive, ignores non-alphanumeric (per Python reference).
#include <cctype>
#include <iostream>
#include <sstream>
#include <string>

bool isPalindrome(const std::string& s) {
    int l = 0, r = (int)s.size() - 1;
    while (l < r) {
        while (l < r && !std::isalnum((unsigned char)s[l])) ++l;
        while (l < r && !std::isalnum((unsigned char)s[r])) --r;
        if (std::tolower((unsigned char)s[l]) != std::tolower((unsigned char)s[r])) return false;
        ++l; --r;
    }
    return true;
}

int main() {
    std::string line, name, s; int expected = 0;
    bool hi = false, he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || !hi || !he) return;
        bool got = isPalindrome(s);
        if ((int)got == expected) { std::cout << "PASS palindrome_check :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL palindrome_check :: " << name << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++f; }
        name.clear(); s.clear(); hi = he = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        // STR <len> <content...>
        if (line.rfind("CASE ", 0) == 0) { name = line.substr(5); }
        else if (line.rfind("STR ", 0) == 0) {
            std::size_t sp = line.find(' ', 4);
            int len = std::stoi(line.substr(4, sp - 4));
            // content from after space
            std::size_t start = sp + 1;
            s = (start <= line.size()) ? line.substr(start) : std::string();
            if ((int)s.size() != len) {
                // pad/trim defensively
                if ((int)s.size() < len) s += std::string(len - s.size(), ' ');
                else s = s.substr(0, len);
            }
            hi = true;
        } else if (line.rfind("BOOL ", 0) == 0) { expected = std::stoi(line.substr(5)); he = true; }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
