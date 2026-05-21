// Reference C++ driver for tests/cases/kmp_search.json.
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<int> buildLps(const std::string& p) {
    int m = (int)p.size();
    std::vector<int> lps(m, 0);
    if (m == 0) return lps;
    int len = 0, i = 1;
    while (i < m) {
        if (p[i] == p[len]) { lps[i++] = ++len; }
        else if (len) len = lps[len - 1];
        else { lps[i++] = 0; }
    }
    return lps;
}
std::vector<int> kmpSearch(const std::string& t, const std::string& p) {
    std::vector<int> out;
    int n = (int)t.size(), m = (int)p.size();
    if (m == 0 || m > n) return out;
    auto lps = buildLps(p);
    int i = 0, j = 0;
    while (i < n) {
        if (t[i] == p[j]) { ++i; ++j; }
        if (j == m) { out.push_back(i - j); j = lps[j - 1]; }
        else if (i < n && t[i] != p[j]) { if (j) j = lps[j - 1]; else ++i; }
    }
    return out;
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
    std::string line, name, t, pat; std::vector<int> expected;
    int strIdx = 0; bool he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || strIdx < 2 || !he) return;
        auto got = kmpSearch(t, pat);
        if (got == expected) { std::cout << "PASS kmp_search :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL kmp_search :: " << name << "\n"; ++f; }
        name.clear(); t.clear(); pat.clear(); expected.clear(); strIdx = 0; he = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        if (line.rfind("CASE ", 0) == 0) { name = line.substr(5); strIdx = 0; }
        else if (line.rfind("STR ", 0) == 0) {
            std::string s = parseStr(line);
            if (strIdx == 0) { t = s; ++strIdx; } else { pat = s; ++strIdx; }
        } else if (line.rfind("ARR ", 0) == 0) {
            std::istringstream iss(line); std::string tag; iss >> tag;
            std::size_t n; iss >> n;
            expected.clear();
            for (std::size_t i = 0; i < n; ++i) { int v; iss >> v; expected.push_back(v); }
            he = true;
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
