// Reference C++ driver for tests/cases/dutch_national_flag.json.
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

void dutchFlag(std::vector<int>& a) {
    int lo = 0, mid = 0, hi = (int)a.size() - 1;
    while (mid <= hi) {
        if (a[mid] == 0) std::swap(a[lo++], a[mid++]);
        else if (a[mid] == 2) std::swap(a[mid], a[hi--]);
        else ++mid;
    }
}

int main() {
    std::string line, name;
    std::vector<int> arr, expected;
    bool hi = false, he = false; int p = 0, f = 0;
    int phase = 0; // 0=expecting input, 1=expecting expected

    auto run = [&]() {
        if (name.empty() || !hi || !he) return;
        auto got = arr; dutchFlag(got);
        if (got == expected) { std::cout << "PASS dutch_national_flag :: " << name << "\n"; ++p; }
        else {
            std::cout << "FAIL dutch_national_flag :: " << name << "\n  expected:";
            for (int v : expected) std::cout << ' ' << v;
            std::cout << "\n  got:";
            for (int v : got) std::cout << ' ' << v;
            std::cout << "\n"; ++f;
        }
        name.clear(); arr.clear(); expected.clear(); hi = he = false; phase = 0;
    };

    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line);
        std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; phase = 0; }
        else if (tag == "ARR") {
            std::size_t n; iss >> n;
            std::vector<int> tmp(n);
            for (std::size_t i = 0; i < n; ++i) iss >> tmp[i];
            if (phase == 0) { arr = std::move(tmp); hi = true; phase = 1; }
            else { expected = std::move(tmp); he = true; }
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
