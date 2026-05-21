// Reference C++ driver for tests/cases/sliding_window_max.json. Monotonic deque.
#include <deque>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<long long> slidingWindowMax(const std::vector<long long>& a, int k) {
    std::vector<long long> out;
    int n = (int)a.size();
    if (n == 0 || k == 0) return out;
    std::deque<int> dq;
    for (int i = 0; i < n; ++i) {
        while (!dq.empty() && dq.front() < i - k + 1) dq.pop_front();
        while (!dq.empty() && a[dq.back()] < a[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) out.push_back(a[dq.front()]);
    }
    return out;
}

int main() {
    std::string line, name; std::vector<long long> arr, expected;
    long long k = 0; int phase = 0; bool he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || phase < 2 || !he) return;
        auto got = slidingWindowMax(arr, (int)k);
        if (got == expected) { std::cout << "PASS sliding_window_max :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL sliding_window_max :: " << name << "\n"; ++f; }
        name.clear(); arr.clear(); expected.clear(); phase = 0; he = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; phase = 0; }
        else if (tag == "ARR") {
            std::size_t n; iss >> n;
            if (phase == 0) {
                arr.clear();
                for (std::size_t i = 0; i < n; ++i) { long long v; iss >> v; arr.push_back(v); }
                phase = 1;
            } else {
                expected.clear();
                for (std::size_t i = 0; i < n; ++i) { long long v; iss >> v; expected.push_back(v); }
                he = true;
            }
        } else if (tag == "INT") { iss >> k; phase = 2; }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
