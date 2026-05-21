// Reference C++ driver for tests/cases/n_queens_count.json.
#include <cstdlib>
#include <functional>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int nQueensCount(int n) {
    if (n <= 0) return 0;
    std::vector<int> q(n, -1);
    int count = 0;
    auto safe = [&](int row, int col) {
        for (int r = 0; r < row; ++r) {
            int c = q[r];
            if (c == col || std::abs(c - col) == std::abs(r - row)) return false;
        }
        return true;
    };
    std::function<void(int)> go = [&](int row) {
        if (row == n) { ++count; return; }
        for (int c = 0; c < n; ++c) if (safe(row, c)) { q[row] = c; go(row + 1); q[row] = -1; }
    };
    go(0);
    return count;
}

int main() {
    std::string line, name; long long n_in = 0, expected = 0;
    int phase = 0; bool he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || phase < 1 || !he) return;
        int got = nQueensCount((int)n_in);
        if (got == expected) { std::cout << "PASS n_queens_count :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL n_queens_count :: " << name << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++f; }
        name.clear(); phase = 0; he = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; phase = 0; }
        else if (tag == "INT") {
            long long v; iss >> v;
            if (phase == 0) { n_in = v; phase = 1; } else { expected = v; he = true; }
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
