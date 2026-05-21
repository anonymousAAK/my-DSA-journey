// Reference C++ driver for tests/cases/kruskal_mst_weight.json. Union-find.
#include <algorithm>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

struct DSU {
    std::vector<int> p, r;
    DSU(int n) : p(n), r(n, 0) { std::iota(p.begin(), p.end(), 0); }
    int find(int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; }
    bool unite(int a, int b) {
        a = find(a); b = find(b); if (a == b) return false;
        if (r[a] < r[b]) std::swap(a, b);
        p[b] = a; if (r[a] == r[b]) ++r[a]; return true;
    }
};

long long kruskal(int V, std::vector<std::tuple<int,int,long long>> edges) {
    std::sort(edges.begin(), edges.end(), [](auto& a, auto& b) { return std::get<2>(a) < std::get<2>(b); });
    DSU d(V); long long total = 0; int used = 0;
    for (auto& [u, v, w] : edges) if (d.unite(u, v)) { total += w; if (++used == V - 1) break; }
    return total;
}

int main() {
    std::string line, name;
    int V = 0, edgesRemain = 0; bool inEdges = false;
    std::vector<std::tuple<int,int,long long>> edges;
    long long expected = 0;
    bool hi = false, he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || !hi || !he) return;
        long long got = kruskal(V, edges);
        if (got == expected) { std::cout << "PASS kruskal_mst_weight :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL kruskal_mst_weight :: " << name << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++f; }
        name.clear(); edges.clear(); hi = he = false; inEdges = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; }
        else if (tag == "V") { iss >> V; }
        else if (tag == "EDGES") { iss >> edgesRemain; inEdges = true; edges.clear(); if (edgesRemain == 0) { hi = true; inEdges = false; } }
        else if (tag == "INT") { iss >> expected; he = true; }
        else if (inEdges) {
            std::istringstream is2(line); int u, v; long long w; is2 >> u >> v >> w;
            edges.push_back({u, v, w}); --edgesRemain;
            if (edgesRemain == 0) { hi = true; inEdges = false; }
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
