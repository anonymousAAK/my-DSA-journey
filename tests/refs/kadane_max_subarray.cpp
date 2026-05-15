// Reference C++ implementation for tests/cases/kadane_max_subarray.json.
//
// Cross-language correctness harness — C++ side, kadane pilot.
//
// To keep the C++ side independent of any JSON library, the shell wrapper
// (tests/harness/harness_cpp.sh) preprocesses cases.json into a simple
// line-based format that this binary reads on stdin:
//
//     CASE <case_name>
//     INPUT <space-separated ints>
//     EXPECTED <int>
//     <blank line>
//
// Build:
//     g++ -std=c++17 -O2 tests/refs/kadane_max_subarray.cpp -o /tmp/kadane_test
//
// To extend to a new topic, copy this file, rename the function, and update
// the corresponding shell driver to emit a matching INPUT line format.

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
    std::string line;
    std::string caseName;
    std::vector<long long> input;
    long long expected = 0;
    bool haveInput = false;
    bool haveExpected = false;

    int passed = 0, failed = 0;

    auto runCase = [&]() {
        if (caseName.empty() || !haveInput || !haveExpected) return;
        long long got = maxSubarraySum(input);
        if (got == expected) {
            std::cout << "PASS kadane_max_subarray :: " << caseName << "\n";
            ++passed;
        } else {
            std::cout << "FAIL kadane_max_subarray :: " << caseName << "\n"
                      << "  expected: " << expected << "\n"
                      << "  got: " << got << "\n";
            ++failed;
        }
        caseName.clear();
        input.clear();
        haveInput = haveExpected = false;
    };

    while (std::getline(std::cin, line)) {
        if (line.empty()) {
            runCase();
            continue;
        }
        std::istringstream iss(line);
        std::string tag;
        iss >> tag;
        if (tag == "CASE") {
            iss >> caseName;
        } else if (tag == "INPUT") {
            input.clear();
            long long v;
            while (iss >> v) input.push_back(v);
            haveInput = true;
        } else if (tag == "EXPECTED") {
            iss >> expected;
            haveExpected = true;
        }
    }
    runCase();  // flush last (in case no trailing blank)

    std::cout << "TOTAL: " << passed << " passed, " << failed << " failed\n";
    return failed == 0 ? 0 : 1;
}

// TODO: to support additional topics, write a similar driver per topic with
// the function under test plus a matching INPUT-line parser. The shell
// wrapper centralises the JSON-to-line-format conversion, so each driver
// stays tiny. See tests/README.md for the extension guide.
