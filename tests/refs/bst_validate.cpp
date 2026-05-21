// Reference C++ driver for tests/cases/bst_validate.json.
// Tree comes in level-order with NULL sentinels.
#include <climits>
#include <iostream>
#include <optional>
#include <queue>
#include <sstream>
#include <string>
#include <vector>

struct Node { long long val; Node* L = nullptr; Node* R = nullptr; };

Node* build(const std::vector<std::optional<long long>>& v) {
    if (v.empty() || !v[0].has_value()) return nullptr;
    Node* root = new Node{*v[0]};
    std::queue<Node*> q; q.push(root);
    std::size_t i = 1;
    while (!q.empty() && i < v.size()) {
        Node* node = q.front(); q.pop();
        if (i < v.size()) {
            if (v[i].has_value()) { node->L = new Node{*v[i]}; q.push(node->L); }
            ++i;
        }
        if (i < v.size()) {
            if (v[i].has_value()) { node->R = new Node{*v[i]}; q.push(node->R); }
            ++i;
        }
    }
    return root;
}

bool check(Node* n, long long lo, long long hi, bool loInf, bool hiInf) {
    if (!n) return true;
    if (!loInf && !(lo < n->val)) return false;
    if (!hiInf && !(n->val < hi)) return false;
    return check(n->L, lo, n->val, loInf, false) && check(n->R, n->val, hi, false, hiInf);
}

bool isValidBST(const std::vector<std::optional<long long>>& v) {
    Node* r = build(v);
    return check(r, 0, 0, true, true);
}

int main() {
    std::string line, name;
    std::vector<std::optional<long long>> vals;
    int treeLen = 0, treeRead = 0; bool inTree = false;
    int expected = 0; bool hi = false, he = false;
    int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || !hi || !he) return;
        bool got = isValidBST(vals);
        if ((int)got == expected) { std::cout << "PASS bst_validate :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL bst_validate :: " << name << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++f; }
        name.clear(); vals.clear(); hi = he = false; inTree = false; treeRead = 0;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; }
        else if (tag == "TREE") {
            iss >> treeLen; vals.clear(); inTree = true; treeRead = 0;
            if (treeLen == 0) { hi = true; inTree = false; }
        }
        else if (tag == "NULL" && inTree) {
            vals.push_back(std::nullopt); ++treeRead;
            if (treeRead == treeLen) { hi = true; inTree = false; }
        }
        else if (tag == "VAL" && inTree) {
            long long v; iss >> v; vals.push_back(v); ++treeRead;
            if (treeRead == treeLen) { hi = true; inTree = false; }
        }
        else if (tag == "BOOL") { iss >> expected; he = true; }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
