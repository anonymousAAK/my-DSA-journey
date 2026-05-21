// Reference C++ driver for tests/cases/merge_sort.json.
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

void mergeSortRec(std::vector<long long>& a, int l, int r) {
    if (r - l <= 1) return;
    int m = (l + r) / 2;
    mergeSortRec(a, l, m); mergeSortRec(a, m, r);
    std::vector<long long> tmp(r - l);
    int i = l, j = m, k = 0;
    while (i < m && j < r) tmp[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
    while (i < m) tmp[k++] = a[i++];
    while (j < r) tmp[k++] = a[j++];
    for (int x = 0; x < (int)tmp.size(); ++x) a[l + x] = tmp[x];
}
std::vector<long long> mergeSort(std::vector<long long> a) {
    mergeSortRec(a, 0, (int)a.size()); return a;
}

int main() {
    std::string line, name; std::vector<long long> arr, expected;
    bool hi = false, he = false; int phase = 0, p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || !hi || !he) return;
        auto got = mergeSort(arr);
        if (got == expected) { std::cout << "PASS merge_sort :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL merge_sort :: " << name << "\n"; ++f; }
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
