// Reference C++ driver for tests/cases/spiral_traversal.json.
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<long long> spiralOrder(const std::vector<std::vector<long long>>& m) {
    std::vector<long long> out;
    if (m.empty() || m[0].empty()) return out;
    int top = 0, bot = (int)m.size() - 1, lo = 0, hi = (int)m[0].size() - 1;
    while (top <= bot && lo <= hi) {
        for (int c = lo; c <= hi; ++c) out.push_back(m[top][c]);
        ++top;
        for (int r = top; r <= bot; ++r) out.push_back(m[r][hi]);
        --hi;
        if (top <= bot) {
            for (int c = hi; c >= lo; --c) out.push_back(m[bot][c]);
            --bot;
        }
        if (lo <= hi) {
            for (int r = bot; r >= top; --r) out.push_back(m[r][lo]);
            ++lo;
        }
    }
    return out;
}

int main() {
    std::string line, name;
    std::vector<std::vector<long long>> mat;
    std::vector<long long> expected;
    bool hm = false, he = false; int p = 0, f = 0;
    int rows = 0, cols = 0, rowsRead = 0;
    bool inMat = false;
    auto run = [&]() {
        if (name.empty() || !hm || !he) return;
        auto got = spiralOrder(mat);
        if (got == expected) { std::cout << "PASS spiral_traversal :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL spiral_traversal :: " << name << "\n"; ++f; }
        name.clear(); mat.clear(); expected.clear(); hm = he = false; inMat = false; rowsRead = 0;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; }
        else if (tag == "MAT") {
            iss >> rows >> cols;
            mat.clear(); inMat = true; rowsRead = 0;
        } else if (tag == "ARR") {
            std::size_t n; iss >> n;
            expected.clear();
            for (std::size_t i = 0; i < n; ++i) { long long v; iss >> v; expected.push_back(v); }
            he = true;
        } else if (inMat) {
            // numeric row line
            std::istringstream is2(line);
            std::vector<long long> row;
            long long v;
            while (is2 >> v) row.push_back(v);
            mat.push_back(row);
            ++rowsRead;
            if (rowsRead == rows) { hm = true; inMat = false; }
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
