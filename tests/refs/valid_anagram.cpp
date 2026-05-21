// Reference C++ driver for tests/cases/valid_anagram.json.
#include <array>
#include <iostream>
#include <string>

bool isAnagram(const std::string& a, const std::string& b) {
    if (a.size() != b.size()) return false;
    std::array<int, 256> cnt{};
    for (unsigned char c : a) ++cnt[c];
    for (unsigned char c : b) if (--cnt[c] < 0) return false;
    return true;
}

static std::string parseStr(const std::string& line) {
    std::size_t sp = line.find(' ', 4);
    if (sp == std::string::npos) return std::string();
    int len = std::stoi(line.substr(4, sp - 4));
    std::string s = line.substr(sp + 1);
    if ((int)s.size() < len) s += std::string(len - s.size(), ' ');
    else if ((int)s.size() > len) s = s.substr(0, len);
    return s;
}

int main() {
    std::string line, name, a, b; int expected = 0;
    int strIdx = 0; bool he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || strIdx < 2 || !he) return;
        bool got = isAnagram(a, b);
        if ((int)got == expected) { std::cout << "PASS valid_anagram :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL valid_anagram :: " << name << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++f; }
        name.clear(); a.clear(); b.clear(); strIdx = 0; he = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        if (line.rfind("CASE ", 0) == 0) { name = line.substr(5); strIdx = 0; }
        else if (line.rfind("STR ", 0) == 0) {
            std::string s = parseStr(line);
            if (strIdx == 0) { a = s; ++strIdx; } else { b = s; ++strIdx; }
        } else if (line.rfind("BOOL ", 0) == 0) { expected = std::stoi(line.substr(5)); he = true; }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
