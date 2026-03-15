/*
 * =============================================================================
 * Week 22 — Advanced Graphs  (C++17)
 * =============================================================================
 *
 * Topics covered
 * --------------
 *   1. Dijkstra's algorithm  (priority_queue, returns distances)
 *   2. Bellman-Ford           (with negative cycle detection)
 *   3. Floyd-Warshall         (all-pairs shortest paths)
 *   4. DSU / Union-Find class (path compression + union by rank)
 *   5. Kruskal's MST          (using DSU)
 *   6. Prim's MST             (using priority_queue)
 *
 * Complexity cheat-sheet  (V = vertices, E = edges)
 * --------------------------------------------------
 *   dijkstra          O((V + E) log V)  |  Space O(V + E)
 *   bellman_ford      O(V * E)          |  Space O(V)
 *   floyd_warshall    O(V^3)            |  Space O(V^2)
 *   DSU operations    O(alpha(n)) ~ O(1) amortized
 *   kruskal_mst       O(E log E)        |  Space O(V)
 *   prim_mst          O((V + E) log V)  |  Space O(V + E)
 *
 * Build & run
 *   g++ -std=c++17 -O2 -o advanced_graphs advanced_graphs.cpp && ./advanced_graphs
 * =============================================================================
 */

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cassert>
#include <sstream>
#include <climits>
#include <numeric>
#include <tuple>
#include <optional>

// ---------------------------------------------------------------------------
// Helper
// ---------------------------------------------------------------------------
template <typename T>
std::string vec_str(const std::vector<T>& v) {
    std::ostringstream oss;
    oss << "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i) oss << ", ";
        if constexpr (std::is_same_v<T, long long>) {
            if (v[i] == LLONG_MAX) { oss << "INF"; continue; }
        }
        oss << v[i];
    }
    oss << "]";
    return oss.str();
}

using Edge = std::tuple<int, int, int>;  // (u, v, weight)
using AdjList = std::vector<std::vector<std::pair<int, int>>>;  // adj[u] = {(v, w)}

// ---------------------------------------------------------------------------
// 1. Dijkstra — single-source shortest paths (non-negative weights)
// ---------------------------------------------------------------------------
// Complexity:  Time O((V + E) log V)  |  Space O(V + E)
std::vector<long long> dijkstra(const AdjList& adj, int src) {
    int n = static_cast<int>(adj.size());
    std::vector<long long> dist(n, LLONG_MAX);
    dist[src] = 0;

    // Min-heap: (distance, vertex)
    using P = std::pair<long long, int>;
    std::priority_queue<P, std::vector<P>, std::greater<>> pq;
    pq.push({0, src});

    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;   // stale entry

        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

// ---------------------------------------------------------------------------
// 2. Bellman-Ford — handles negative weights, detects negative cycles
// ---------------------------------------------------------------------------
// Complexity:  Time O(V * E)  |  Space O(V)
// Returns nullopt if a negative cycle is reachable from src.
std::optional<std::vector<long long>> bellman_ford(int n, const std::vector<Edge>& edges, int src) {
    std::vector<long long> dist(n, LLONG_MAX);
    dist[src] = 0;

    // Relax all edges V-1 times.
    for (int i = 0; i < n - 1; ++i) {
        for (auto [u, v, w] : edges) {
            if (dist[u] != LLONG_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }

    // Check for negative cycle: if we can still relax, there is one.
    for (auto [u, v, w] : edges) {
        if (dist[u] != LLONG_MAX && dist[u] + w < dist[v]) {
            return std::nullopt;  // negative cycle detected
        }
    }
    return dist;
}

// ---------------------------------------------------------------------------
// 3. Floyd-Warshall — all-pairs shortest paths
// ---------------------------------------------------------------------------
// Complexity:  Time O(V^3)  |  Space O(V^2)
constexpr long long FW_INF = 1e18;

std::vector<std::vector<long long>> floyd_warshall(int n, const std::vector<Edge>& edges) {
    std::vector<std::vector<long long>> dist(n, std::vector<long long>(n, FW_INF));

    for (int i = 0; i < n; ++i) dist[i][i] = 0;
    for (auto [u, v, w] : edges) dist[u][v] = std::min(dist[u][v], (long long)w);

    for (int k = 0; k < n; ++k)
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                if (dist[i][k] < FW_INF && dist[k][j] < FW_INF)
                    dist[i][j] = std::min(dist[i][j], dist[i][k] + dist[k][j]);

    return dist;
}

// ---------------------------------------------------------------------------
// 4. DSU / Union-Find — path compression + union by rank
// ---------------------------------------------------------------------------
// Complexity:  Nearly O(1) amortized per operation (inverse Ackermann)
class DSU {
public:
    explicit DSU(int n) : parent_(n), rank_(n, 0) {
        std::iota(parent_.begin(), parent_.end(), 0);
    }

    int find(int x) {
        if (parent_[x] != x) parent_[x] = find(parent_[x]);  // path compression
        return parent_[x];
    }

    bool unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;

        // Union by rank.
        if (rank_[px] < rank_[py]) std::swap(px, py);
        parent_[py] = px;
        if (rank_[px] == rank_[py]) ++rank_[px];
        return true;
    }

    [[nodiscard]] bool connected(int x, int y) { return find(x) == find(y); }

private:
    std::vector<int> parent_;
    std::vector<int> rank_;
};

// ---------------------------------------------------------------------------
// 5. Kruskal's MST — sort edges, use DSU
// ---------------------------------------------------------------------------
// Complexity:  Time O(E log E)  |  Space O(V)
std::pair<long long, std::vector<Edge>> kruskal_mst(int n, std::vector<Edge> edges) {
    std::sort(edges.begin(), edges.end(),
              [](const Edge& a, const Edge& b) { return std::get<2>(a) < std::get<2>(b); });

    DSU dsu(n);
    long long total = 0;
    std::vector<Edge> mst_edges;

    for (auto& [u, v, w] : edges) {
        if (dsu.unite(u, v)) {
            total += w;
            mst_edges.emplace_back(u, v, w);
            if (static_cast<int>(mst_edges.size()) == n - 1) break;
        }
    }
    return {total, mst_edges};
}

// ---------------------------------------------------------------------------
// 6. Prim's MST — priority_queue based
// ---------------------------------------------------------------------------
// Complexity:  Time O((V + E) log V)  |  Space O(V + E)
std::pair<long long, std::vector<Edge>> prim_mst(const AdjList& adj) {
    int n = static_cast<int>(adj.size());
    std::vector<bool> in_mst(n, false);
    long long total = 0;
    std::vector<Edge> mst_edges;

    // Min-heap: (weight, vertex, parent)
    using P = std::tuple<int, int, int>;
    std::priority_queue<P, std::vector<P>, std::greater<>> pq;
    pq.push({0, 0, -1});

    while (!pq.empty() && static_cast<int>(mst_edges.size()) < n) {
        auto [w, u, parent] = pq.top(); pq.pop();
        if (in_mst[u]) continue;
        in_mst[u] = true;
        total += w;
        if (parent != -1) mst_edges.emplace_back(parent, u, w);

        for (auto [v, wt] : adj[u]) {
            if (!in_mst[v]) pq.push({wt, v, u});
        }
    }
    return {total, mst_edges};
}

// ---------------------------------------------------------------------------
// main — test cases
// ---------------------------------------------------------------------------
int main() {
    std::cout << "=== Week 22: Advanced Graphs ===\n\n";

    /*
     * Test graph (directed, weighted):
     *
     *   0 --1--> 1 --3--> 3
     *   |        |        ^
     *   4        1        |
     *   v        v        1
     *   2 --5--> 3 --2--> 4  (and edge 3->4 weight 2)
     *
     * Wait, let's use a cleaner example.
     */

    // ---- 1. Dijkstra ----
    {
        std::cout << "-- Dijkstra --\n";
        int n = 5;
        AdjList adj(n);
        adj[0] = {{1, 4}, {2, 1}};
        adj[1] = {{3, 1}};
        adj[2] = {{1, 2}, {3, 5}};
        adj[3] = {{4, 3}};
        // shortest from 0: 0->2(1), 2->1(3), 1->3(4), 3->4(7)

        auto dist = dijkstra(adj, 0);
        std::cout << "  dist from 0: " << vec_str(dist) << "\n";
        assert(dist[0] == 0 && dist[1] == 3 && dist[2] == 1 && dist[3] == 4 && dist[4] == 7);
        std::cout << "\n";
    }

    // ---- 2. Bellman-Ford ----
    {
        std::cout << "-- Bellman-Ford --\n";
        int n = 5;
        std::vector<Edge> edges = {
            {0, 1, 4}, {0, 2, 1}, {2, 1, 2}, {1, 3, 1}, {2, 3, 5}, {3, 4, 3}
        };
        auto res = bellman_ford(n, edges, 0);
        assert(res.has_value());
        std::cout << "  dist from 0: " << vec_str(*res) << "\n";
        assert((*res)[4] == 7);

        // Test negative cycle detection.
        std::vector<Edge> neg_edges = {{0, 1, 1}, {1, 2, -1}, {2, 0, -1}};
        auto neg_res = bellman_ford(3, neg_edges, 0);
        assert(!neg_res.has_value());
        std::cout << "  negative cycle detected: true\n\n";
    }

    // ---- 3. Floyd-Warshall ----
    {
        std::cout << "-- Floyd-Warshall --\n";
        int n = 4;
        std::vector<Edge> edges = {
            {0, 1, 3}, {0, 3, 7}, {1, 0, 8}, {1, 2, 2},
            {2, 0, 5}, {2, 3, 1}, {3, 0, 2}
        };
        auto dist = floyd_warshall(n, edges);
        std::cout << "  All-pairs shortest paths:\n";
        for (int i = 0; i < n; ++i) {
            std::cout << "    from " << i << ": [";
            for (int j = 0; j < n; ++j) {
                if (j) std::cout << ", ";
                std::cout << (dist[i][j] >= FW_INF ? "INF" : std::to_string(dist[i][j]));
            }
            std::cout << "]\n";
        }
        assert(dist[0][2] == 5);  // 0->1(3)->2(2) = 5
        assert(dist[2][1] == 6);  // 2->3(1)->0(2)->1(3) = 6
        std::cout << "\n";
    }

    // ---- 4. DSU ----
    {
        std::cout << "-- DSU / Union-Find --\n";
        DSU dsu(6);
        dsu.unite(0, 1);
        dsu.unite(2, 3);
        dsu.unite(0, 2);
        assert(dsu.connected(1, 3));
        assert(!dsu.connected(0, 5));
        dsu.unite(4, 5);
        dsu.unite(3, 5);
        assert(dsu.connected(0, 5));
        std::cout << "  connected(1,3)=true, connected(0,5) after unions=true\n\n";
    }

    // ---- 5 & 6. Kruskal & Prim MST ----
    {
        std::cout << "-- Kruskal's MST --\n";
        //     0
        //    / \
        //   1   4
        //  / \ / \
        // 1   2   3
        //  \ | / |
        //   3   5
        int n = 6;
        std::vector<Edge> edges = {
            {0, 1, 4}, {0, 2, 4}, {1, 2, 2},
            {1, 3, 6}, {2, 3, 8}, {2, 4, 1},
            {3, 4, 7}, {3, 5, 9}, {4, 5, 3}
        };

        auto [kw, ke] = kruskal_mst(n, edges);
        std::cout << "  Kruskal total weight: " << kw << "\n";
        std::cout << "  edges: ";
        for (auto& [u, v, w] : ke) std::cout << "(" << u << "-" << v << ":" << w << ") ";
        std::cout << "\n";
        // Edges sorted by weight: (2,4,1), (1,2,2), (4,5,3), (0,1,4), (0,2,4), (1,3,6), ...
        // Pick: 2-4(1), 1-2(2), 4-5(3), 0-1(4), 1-3(6) = 1+2+3+4+6 = 16
        assert(kw == 16);

        std::cout << "\n-- Prim's MST --\n";
        AdjList adj(n);
        for (auto& [u, v, w] : edges) {
            adj[u].emplace_back(v, w);
            adj[v].emplace_back(u, w);
        }
        auto [pw, pe] = prim_mst(adj);
        std::cout << "  Prim total weight: " << pw << "\n";
        assert(pw == kw);  // Both should give same total weight.
        std::cout << "  (Kruskal == Prim: " << std::boolalpha << (pw == kw) << ")\n";
    }

    std::cout << "\nAll Week 22 tests passed.\n";
    return 0;
}
