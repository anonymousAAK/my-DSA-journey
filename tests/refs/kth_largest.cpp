// Reference C++ driver for tests/cases/kth_largest.json. Uses a min-heap of size k.
#include <iostream>
#include <queue>
#include <sstream>
#include <string>
#include <vector>

long long kthLargest(const std::vector<long long>& a, int k) {
    std::priority_queue<long long, std::vector<long long>, std::greater<long long>> minh;
    for (long long v : a) {
        minh.push(v);
        if ((int)minh.size() > k) minh.pop();
    }
    return minh.top();
}

int main() {
    std::string line, name; std::vector<long long> arr;
    long long k = 0, expected = 0;
    int phase = 0; bool he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || phase < 2 || !he) return;
        long long got = kthLargest(arr, (int)k);
        if (got == expected) { std::cout << "PASS kth_largest :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL kth_largest :: " << name << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++f; }
        name.clear(); arr.clear(); phase = 0; he = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; phase = 0; }
        else if (tag == "ARR") {
            arr.clear(); std::size_t n; iss >> n;
            for (std::size_t i = 0; i < n; ++i) { long long v; iss >> v; arr.push_back(v); }
            phase = 1;
        } else if (tag == "INT") {
            long long v; iss >> v;
            if (phase == 1) { k = v; phase = 2; } else { expected = v; he = true; }
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
