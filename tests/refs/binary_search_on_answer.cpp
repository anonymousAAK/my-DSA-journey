// Reference C++ driver for tests/cases/binary_search_on_answer.json (Koko bananas).
#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int minEatingSpeed(const std::vector<long long>& piles, long long h) {
    long long lo = 1, hi = *std::max_element(piles.begin(), piles.end());
    auto canFinish = [&](long long speed) {
        long long hrs = 0;
        for (long long p : piles) hrs += (p + speed - 1) / speed;
        return hrs <= h;
    };
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (canFinish(mid)) hi = mid; else lo = mid + 1;
    }
    return (int)lo;
}

int main() {
    std::string line, name; std::vector<long long> piles;
    long long h = 0, expected = 0;
    int phase = 0; bool he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || phase < 2 || !he) return;
        long long got = minEatingSpeed(piles, h);
        if (got == expected) { std::cout << "PASS binary_search_on_answer :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL binary_search_on_answer :: " << name << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++f; }
        name.clear(); piles.clear(); phase = 0; he = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; phase = 0; }
        else if (tag == "ARR") {
            piles.clear(); std::size_t n; iss >> n;
            for (std::size_t i = 0; i < n; ++i) { long long v; iss >> v; piles.push_back(v); }
            phase = 1;
        } else if (tag == "INT") {
            long long v; iss >> v;
            if (phase == 1) { h = v; phase = 2; } else { expected = v; he = true; }
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
