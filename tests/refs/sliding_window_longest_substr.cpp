// Reference C++ driver for tests/cases/sliding_window_longest_substr.json.
#include <array>
#include <iostream>
#include <string>

int longestUniqueSubstring(const std::string& s) {
    std::array<int, 256> last{}; last.fill(-1);
    int best = 0, l = 0;
    for (int i = 0; i < (int)s.size(); ++i) {
        unsigned char c = (unsigned char)s[i];
        if (last[c] >= l) l = last[c] + 1;
        last[c] = i;
        if (i - l + 1 > best) best = i - l + 1;
    }
    return best;
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
    std::string line, name, s; int expected = 0;
    bool hi = false, he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || !hi || !he) return;
        int got = longestUniqueSubstring(s);
        if (got == expected) { std::cout << "PASS sliding_window_longest_substr :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL sliding_window_longest_substr :: " << name << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++f; }
        name.clear(); s.clear(); hi = he = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        if (line.rfind("CASE ", 0) == 0) name = line.substr(5);
        else if (line.rfind("STR ", 0) == 0) { s = parseStr(line); hi = true; }
        else if (line.rfind("INT ", 0) == 0) { expected = std::stoi(line.substr(4)); he = true; }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
