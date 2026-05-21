// Reference C++ driver for tests/cases/linear_search.json.
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int linearSearch(const std::vector<long long>& arr, long long target) {
    for (std::size_t i = 0; i < arr.size(); ++i)
        if (arr[i] == target) return static_cast<int>(i);
    return -1;
}

int main() {
    std::string line, caseName;
    std::vector<long long> arr;
    long long target = 0, expected = 0;
    bool haveInput = false, haveExpected = false;
    int passed = 0, failed = 0;

    auto run = [&]() {
        if (caseName.empty() || !haveInput || !haveExpected) return;
        long long got = linearSearch(arr, target);
        if (got == expected) { std::cout << "PASS linear_search :: " << caseName << "\n"; ++passed; }
        else { std::cout << "FAIL linear_search :: " << caseName << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++failed; }
        caseName.clear(); arr.clear(); haveInput = haveExpected = false;
    };

    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line);
        std::string tag; iss >> tag;
        if (tag == "CASE") iss >> caseName;
        else if (tag == "INPUT") {
            arr.clear();
            std::size_t n; iss >> n;
            for (std::size_t i = 0; i < n; ++i) { long long v; iss >> v; arr.push_back(v); }
            iss >> target;
            haveInput = true;
        } else if (tag == "INT") { iss >> expected; haveExpected = true; }
    }
    run();
    std::cout << "TOTAL: " << passed << " passed, " << failed << " failed\n";
    return failed == 0 ? 0 : 1;
}
