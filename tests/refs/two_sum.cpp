// Reference C++ driver for tests/cases/two_sum.json.
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

std::vector<int> twoSum(const std::vector<long long>& nums, long long target) {
    std::unordered_map<long long, int> seen;
    for (int i = 0; i < (int)nums.size(); ++i) {
        long long comp = target - nums[i];
        auto it = seen.find(comp);
        if (it != seen.end()) return {it->second, i};
        seen[nums[i]] = i;
    }
    return {-1, -1};
}

int main() {
    std::string line, name; std::vector<long long> nums; std::vector<int> expected;
    long long target = 0;
    int phase = 0; bool he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || phase < 2 || !he) return;
        auto got = twoSum(nums, target);
        if (got == expected) { std::cout << "PASS two_sum :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL two_sum :: " << name << "\n"; ++f; }
        name.clear(); nums.clear(); expected.clear(); phase = 0; he = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; phase = 0; }
        else if (tag == "ARR") {
            std::size_t n; iss >> n;
            if (phase == 0) {
                nums.clear();
                for (std::size_t i = 0; i < n; ++i) { long long v; iss >> v; nums.push_back(v); }
                phase = 1;
            } else {
                expected.clear();
                for (std::size_t i = 0; i < n; ++i) { int v; iss >> v; expected.push_back(v); }
                he = true;
            }
        } else if (tag == "INT") {
            iss >> target;
            phase = 2;
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
