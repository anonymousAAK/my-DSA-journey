// Reference C++ driver for tests/cases/dijkstra_shortest_path.json.
// Undirected graph; unreachable -> -1.
#include <climits>
#include <iostream>
#include <queue>
#include <sstream>
#include <string>
#include <vector>

std::vector<long long> dijkstra(int V, const std::vector<std::tuple<int,int,long long>>& edges, int src) {
    std::vector<std::vector<std::pair<int,long long>>> adj(V);
    for (auto& [u, v, w] : edges) { adj[u].push_back({v, w}); adj[v].push_back({u, w}); }
    const long long INF = LLONG_MAX / 2;
    std::vector<long long> dist(V, INF);
    dist[src] = 0;
    using P = std::pair<long long, int>;
    std::priority_queue<P, std::vector<P>, std::greater<P>> pq;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto& [v, w] : adj[u]) {
            long long nd = d + w;
            if (nd < dist[v]) { dist[v] = nd; pq.push({nd, v}); }
        }
    }
    std::vector<long long> out(V);
    for (int i = 0; i < V; ++i) out[i] = (dist[i] == INF) ? -1 : dist[i];
    return out;
}

int main() {
    std::string line, name;
    int V = 0, src = 0, edgesRemain = 0; bool inEdges = false;
    std::vector<std::tuple<int,int,long long>> edges;
    std::vector<long long> expected;
    bool hi = false, he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || !hi || !he) return;
        auto got = dijkstra(V, edges, src);
        if (got == expected) { std::cout << "PASS dijkstra_shortest_path :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL dijkstra_shortest_path :: " << name << "\n"; ++f; }
        name.clear(); edges.clear(); expected.clear();
        hi = he = false; inEdges = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; }
        else if (tag == "V") { iss >> V; }
        else if (tag == "EDGES") { iss >> edgesRemain; inEdges = true; edges.clear(); if (edgesRemain == 0) inEdges = false; }
        else if (tag == "SRC") { iss >> src; hi = true; }
        else if (tag == "ARR") {
            std::size_t n; iss >> n;
            expected.clear();
            for (std::size_t i = 0; i < n; ++i) { long long v; iss >> v; expected.push_back(v); }
            he = true;
        }
        else if (inEdges) {
            std::istringstream is2(line); int u, v; long long w; is2 >> u >> v >> w;
            edges.push_back({u, v, w}); --edgesRemain;
            if (edgesRemain == 0) inEdges = false;
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
