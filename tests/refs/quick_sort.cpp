// Reference C++ driver for tests/cases/quick_sort.json.
#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

void quickSortRec(std::vector<long long>& a, int l, int r) {
    if (l >= r) return;
    long long pivot = a[(l + r) / 2];
    int i = l, j = r;
    while (i <= j) {
        while (a[i] < pivot) ++i;
        while (a[j] > pivot) --j;
        if (i <= j) { std::swap(a[i], a[j]); ++i; --j; }
    }
    quickSortRec(a, l, j); quickSortRec(a, i, r);
}
std::vector<long long> quickSort(std::vector<long long> a) {
    if (!a.empty()) quickSortRec(a, 0, (int)a.size() - 1);
    return a;
}

int main() {
    std::string line, name; std::vector<long long> arr, expected;
    bool hi = false, he = false; int phase = 0, p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || !hi || !he) return;
        auto got = quickSort(arr);
        if (got == expected) { std::cout << "PASS quick_sort :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL quick_sort :: " << name << "\n"; ++f; }
        name.clear(); arr.clear(); expected.clear(); hi = he = false; phase = 0;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; phase = 0; }
        else if (tag == "ARR") {
            std::size_t n; iss >> n;
            std::vector<long long> tmp(n);
            for (std::size_t i = 0; i < n; ++i) iss >> tmp[i];
            if (phase == 0) { arr = std::move(tmp); hi = true; phase = 1; }
            else { expected = std::move(tmp); he = true; }
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
