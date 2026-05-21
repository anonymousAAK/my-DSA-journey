// Reference C++ driver for tests/cases/reverse_linked_list.json.
// Treats the list as an array (per fixture schema) and reverses it.
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>

struct Node { long long val; Node* next; };
std::vector<long long> reverseList(const std::vector<long long>& in) {
    Node* head = nullptr;
    for (auto it = in.rbegin(); it != in.rend(); ++it) head = new Node{*it, head};
    Node* prev = nullptr; Node* cur = head;
    while (cur) { Node* nx = cur->next; cur->next = prev; prev = cur; cur = nx; }
    std::vector<long long> out;
    while (prev) { out.push_back(prev->val); Node* nx = prev->next; delete prev; prev = nx; }
    return out;
}

int main() {
    std::string line, name; std::vector<long long> arr, expected;
    bool hi = false, he = false; int phase = 0, p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || !hi || !he) return;
        auto got = reverseList(arr);
        if (got == expected) { std::cout << "PASS reverse_linked_list :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL reverse_linked_list :: " << name << "\n"; ++f; }
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
