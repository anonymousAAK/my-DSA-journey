// Reference C++ driver for tests/cases/rabin_karp_search.json.
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<int> rabinKarpSearch(const std::string& t, const std::string& p) {
    const long long base = 256, prime = 1000000007LL;
    int n = (int)t.size(), m = (int)p.size();
    std::vector<int> out;
    if (m == 0 || m > n) return out;
    long long h = 1;
    for (int i = 0; i < m - 1; ++i) h = (h * base) % prime;
    long long ph = 0, th = 0;
    for (int i = 0; i < m; ++i) {
        ph = (base * ph + (unsigned char)p[i]) % prime;
        th = (base * th + (unsigned char)t[i]) % prime;
    }
    for (int i = 0; i <= n - m; ++i) {
        if (ph == th && t.compare(i, m, p) == 0) out.push_back(i);
        if (i < n - m) {
            th = (base * (th - (unsigned char)t[i] * h) + (unsigned char)t[i + m]) % prime;
            if (th < 0) th += prime;
        }
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
        auto got = rabinKarpSearch(t, pat);
        if (got == expected) { std::cout << "PASS rabin_karp_search :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL rabin_karp_search :: " << name << "\n"; ++f; }
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
