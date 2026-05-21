// Reference C++ driver for tests/cases/binary_search.json.
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int binarySearch(const std::vector<long long>& a, long long target) {
    int lo = 0, hi = (int)a.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[mid] < target) lo = mid + 1; else hi = mid - 1;
    }
    return -1;
}

int main() {
    std::string line, name; std::vector<long long> arr;
    long long target = 0, expected = 0;
    int phase = 0; bool he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || phase < 2 || !he) return;
        long long got = binarySearch(arr, target);
        if (got == expected) { std::cout << "PASS binary_search :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL binary_search :: " << name << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++f; }
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
            if (phase == 1) { target = v; phase = 2; }
            else { expected = v; he = true; }
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
