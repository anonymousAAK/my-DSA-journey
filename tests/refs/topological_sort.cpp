// Reference C++ driver for tests/cases/topological_sort.json.
// Kahn's with min-heap deterministic tie-break. Returns empty + flag for cycle.
#include <iostream>
#include <queue>
#include <sstream>
#include <string>
#include <vector>

bool topoSort(int V, const std::vector<std::pair<int,int>>& edges, std::vector<int>& out) {
    std::vector<std::vector<int>> adj(V);
    std::vector<int> indeg(V, 0);
    for (auto& [u, v] : edges) { adj[u].push_back(v); ++indeg[v]; }
    std::priority_queue<int, std::vector<int>, std::greater<int>> pq;
    for (int i = 0; i < V; ++i) if (indeg[i] == 0) pq.push(i);
    out.clear();
    while (!pq.empty()) {
        int u = pq.top(); pq.pop();
        out.push_back(u);
        for (int v : adj[u]) if (--indeg[v] == 0) pq.push(v);
    }
    return (int)out.size() == V;
}

int main() {
    std::string line, name;
    int V = 0, edgesRemain = 0; bool inEdges = false;
    std::vector<std::pair<int,int>> edges;
    std::vector<int> expected; bool expectedNone = false;
    bool hi = false, he = false; int p = 0, f = 0;

    auto run = [&]() {
        if (name.empty() || !hi || !he) return;
        std::vector<int> got;
        bool ok = topoSort(V, edges, got);
        bool pass;
        if (expectedNone) pass = !ok;
        else pass = ok && got == expected;
        if (pass) { std::cout << "PASS topological_sort :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL topological_sort :: " << name << "\n"; ++f; }
        name.clear(); edges.clear(); expected.clear();
        hi = he = false; inEdges = false; expectedNone = false;
    };

    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; }
        else if (tag == "V") { iss >> V; }
        else if (tag == "EDGES") { iss >> edgesRemain; inEdges = true; edges.clear(); if (edgesRemain == 0) { hi = true; inEdges = false; } }
        else if (tag == "SRC") {}
        else if (tag == "EXPECTED_NONE") { expectedNone = true; he = true; }
        else if (tag == "ARR") {
            std::size_t n; iss >> n;
            expected.clear();
            for (std::size_t i = 0; i < n; ++i) { int v; iss >> v; expected.push_back(v); }
            he = true;
        }
        else if (inEdges) {
            // edge line: "u v"
            std::istringstream is2(line); int u, v; is2 >> u >> v;
            edges.push_back({u, v}); --edgesRemain;
            if (edgesRemain == 0) { hi = true; inEdges = false; }
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
