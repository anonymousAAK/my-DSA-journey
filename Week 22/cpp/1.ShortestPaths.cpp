/*
 * WEEK 22 - C++ ADVANCED DSA
 * Topic: Shortest Path Algorithms (Dijkstra, Bellman-Ford, Floyd-Warshall)
 * File: 1.ShortestPaths.cpp
 *
 * CONCEPT:
 *   Dijkstra:       single-source, non-negative weights, O((V+E) log V).
 *   Bellman-Ford:   single-source, allows negatives, detects neg-cycles, O(V*E).
 *   Floyd-Warshall: all-pairs DP, O(V^3).
 *
 * KEY POINTS:
 *   - Use std::priority_queue with std::greater for a min-heap.
 *   - Pair<int,int> = (dist, vertex) for the heap.
 *   - INF = INT_MAX/2 prevents overflow when summing weights.
 *
 * ALGORITHM / APPROACH:
 *   Dijkstra: lazy deletion (skip stale heap entries via dist[u] check).
 *   Bellman-Ford: V-1 relaxations + 1 negative-cycle check pass.
 *   Floyd-Warshall: triple nested loop with k as outermost.
 *
 * C++-SPECIFIC NOTES vs JAVA:
 *   - std::priority_queue is MAX-heap by default; use
 *     `priority_queue<T, vector<T>, greater<T>>` for min-heap.
 *   - Adjacency list: `vector<vector<pair<int,int>>>`.
 *   - `auto [d,u] = pq.top();` (C++17 structured bindings) for clarity.
 *
 * DRY RUN (Dijkstra, undirected V=5):
 *   Edges (0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5),(3,4,3).
 *   Settled order: 0(0), 2(1), 1(3), 3(4), 4(7).
 *   Final distances: [0, 3, 1, 4, 7].
 *
 * COMPLEXITY:
 *   Dijkstra:       O((V+E) log V).
 *   Bellman-Ford:   O(V*E).
 *   Floyd-Warshall: O(V^3) time, O(V^2) space.
 */

#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <climits>
#include <iomanip>

constexpr int INF = INT_MAX / 2;

std::vector<int> dijkstra(const std::vector<std::vector<std::pair<int,int>>>& adj, int src, int V) {
    std::vector<int> dist(V, INF);
    dist[src] = 0;
    using P = std::pair<int,int>; // (dist, vertex)
    std::priority_queue<P, std::vector<P>, std::greater<P>> pq;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (d + w < dist[v]) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

bool bellman_ford(int V, const std::vector<std::tuple<int,int,int>>& edges, int src, std::vector<int>& dist) {
    dist.assign(V, INF);
    dist[src] = 0;
    for (int i = 0; i < V - 1; ++i) {
        bool updated = false;
        for (auto [u, v, w] : edges) {
            if (dist[u] != INF && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                updated = true;
            }
        }
        if (!updated) break;
    }
    for (auto [u, v, w] : edges) {
        if (dist[u] != INF && dist[u] + w < dist[v]) {
            std::cout << "Negative weight cycle detected!\n";
            return false;
        }
    }
    return true;
}

std::vector<std::vector<int>> floyd_warshall(int V, const std::vector<std::tuple<int,int,int>>& edges) {
    std::vector<std::vector<int>> d(V, std::vector<int>(V, INF));
    for (int i = 0; i < V; ++i) d[i][i] = 0;
    for (auto [u, v, w] : edges) d[u][v] = std::min(d[u][v], w);
    for (int k = 0; k < V; ++k)
        for (int i = 0; i < V; ++i)
            if (d[i][k] != INF)
                for (int j = 0; j < V; ++j)
                    if (d[k][j] != INF && d[i][k] + d[k][j] < d[i][j])
                        d[i][j] = d[i][k] + d[k][j];
    for (int i = 0; i < V; ++i) if (d[i][i] < 0) { std::cout << "Negative cycle!\n"; return {}; }
    return d;
}

int main() {
    std::cout << "=== Dijkstra ===\n";
    int V = 5;
    std::vector<std::vector<std::pair<int,int>>> adj(V);
    std::vector<std::tuple<int,int,int>> edges = {
        {0,1,4},{0,2,1},{2,1,2},{1,3,1},{2,3,5},{3,4,3}
    };
    for (auto [u, v, w] : edges) {
        adj[u].push_back({v, w});
        adj[v].push_back({u, w}); // undirected
    }
    auto d = dijkstra(adj, 0, V);
    std::cout << "Shortest distances from 0: [";
    for (int i = 0; i < V; ++i) std::cout << d[i] << (i + 1 < V ? "," : "");
    std::cout << "]\n";

    std::cout << "\n=== Bellman-Ford ===\n";
    std::vector<std::tuple<int,int,int>> bf = {
        {0,1,-1},{0,2,4},{1,2,3},{1,3,2},{1,4,2},{3,2,5},{3,1,1},{4,3,-3}
    };
    std::vector<int> bfd;
    bellman_ford(5, bf, 0, bfd);
    std::cout << "Shortest distances from 0: [";
    for (size_t i = 0; i < bfd.size(); ++i) std::cout << bfd[i] << (i + 1 < bfd.size() ? "," : "");
    std::cout << "]\n";

    std::cout << "\n=== Floyd-Warshall ===\n";
    std::vector<std::tuple<int,int,int>> fw = {
        {0,1,3},{0,3,7},{1,0,8},{1,2,2},{2,0,5},{2,3,1},{3,0,2}
    };
    auto ap = floyd_warshall(4, fw);
    std::cout << "All-pairs shortest paths:\n";
    for (auto& row : ap) {
        for (int v : row) {
            if (v == INF) std::cout << std::setw(4) << "INF";
            else std::cout << std::setw(4) << v;
        }
        std::cout << "\n";
    }
    return 0;
}
