// Reference C++ driver for tests/cases/kadane_max_subarray.json.
//
// Stdin format produced by tests/harness/emit_lines.py:
//   CASE <name>
//   ARR <n> <v1> ... <vn>
//   INT <expected>
//   <blank>

#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

long long maxSubarraySum(const std::vector<long long>& arr) {
    if (arr.empty()) return 0;
    long long best = arr[0];
    long long current = arr[0];
    for (std::size_t i = 1; i < arr.size(); ++i) {
        current = std::max(arr[i], current + arr[i]);
        best = std::max(best, current);
    }
    return best;
}

int main() {
    std::string line, caseName;
    std::vector<long long> arr;
    long long expected = 0;
    bool haveInput = false, haveExpected = false;
    int passed = 0, failed = 0;

    auto run = [&]() {
        if (caseName.empty() || !haveInput || !haveExpected) return;
        long long got = maxSubarraySum(arr);
        if (got == expected) { std::cout << "PASS kadane_max_subarray :: " << caseName << "\n"; ++passed; }
        else { std::cout << "FAIL kadane_max_subarray :: " << caseName << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++failed; }
        caseName.clear(); arr.clear(); haveInput = haveExpected = false;
    };

    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line);
        std::string tag; iss >> tag;
        if (tag == "CASE") iss >> caseName;
        else if (tag == "ARR") {
            arr.clear();
            std::size_t n; iss >> n;
            for (std::size_t i = 0; i < n; ++i) { long long v; iss >> v; arr.push_back(v); }
            haveInput = true;
        } else if (tag == "INT") { iss >> expected; haveExpected = true; }
    }
    run();
    std::cout << "TOTAL: " << passed << " passed, " << failed << " failed\n";
    return failed == 0 ? 0 : 1;
}
