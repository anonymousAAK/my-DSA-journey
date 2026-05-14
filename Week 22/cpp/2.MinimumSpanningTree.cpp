/*
 * WEEK 22 - C++ ADVANCED DSA
 * Topic: Minimum Spanning Tree (Kruskal + Prim) & Union-Find
 * File: 2.MinimumSpanningTree.cpp
 *
 * CONCEPT:
 *   MST = spanning tree with minimum sum of edge weights.
 *   Kruskal: sort edges by weight, add if they don't create a cycle (DSU).
 *   Prim:    grow MST greedily from one vertex via a min-heap on candidate
 *            edges crossing the current cut.
 *
 * KEY POINTS:
 *   - DSU (Union-Find) with path compression + union by rank ~ O(alpha(n)).
 *   - Sort edges using std::sort with a custom comparator.
 *   - Use std::priority_queue with std::greater for Prim's min-heap.
 *
 * ALGORITHM / APPROACH:
 *   DSU::find: recursive with path compression.
 *   DSU::unite: rank-based merge; returns false if already same set.
 *   Kruskal: iterate sorted edges, accumulate weight, stop after V-1 edges.
 *   Prim: lazy-deletion pattern, identical to Dijkstra's loop shape.
 *
 * C++-SPECIFIC NOTES vs JAVA:
 *   - `struct DSU` keeps members public; concise.
 *   - Edge type `array<int,3>` or `tuple<int,int,int>` works for sorting.
 *   - Use `auto&` on range-for to avoid unnecessary copies.
 *
 * DRY RUN:
 *   V=4 with edges (0,1,4),(0,2,3),(1,2,1),(1,3,2),(2,3,4).
 *   Sorted: (1,2,1),(1,3,2),(0,2,3),(0,1,4),(2,3,4).
 *   Kruskal picks (1,2,1),(1,3,2),(0,2,3) -> total 6.
 *
 * COMPLEXITY:
 *   DSU op: ~O(alpha(n)).
 *   Kruskal: O(E log E).
 *   Prim:    O((V+E) log V).
 */

#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <algorithm>
#include <climits>
#include <tuple>

struct DSU {
    std::vector<int> parent, rnk;
    DSU(int n) : parent(n), rnk(n, 0) { for (int i = 0; i < n; ++i) parent[i] = i; }

    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }

    bool unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        if (rnk[px] < rnk[py]) std::swap(px, py);
        parent[py] = px;
        if (rnk[px] == rnk[py]) rnk[px]++;
        return true;
    }

    bool connected(int x, int y) { return find(x) == find(y); }
};

int kruskal_mst(int V, std::vector<std::tuple<int,int,int>> edges) {
    std::sort(edges.begin(), edges.end(),
              [](auto& a, auto& b) { return std::get<2>(a) < std::get<2>(b); });
    DSU dsu(V);
    int total = 0, used = 0;
    std::cout << "Kruskal MST edges:\n";
    for (auto [u, v, w] : edges) {
        if (used == V - 1) break;
        if (dsu.unite(u, v)) {
            total += w; used++;
            std::cout << "  Edge (" << u << " - " << v << "): weight " << w << "\n";
        }
    }
    return total;
}

int prim_mst(int V, const std::vector<std::vector<std::pair<int,int>>>& adj) {
    std::vector<bool> inMST(V, false);
    std::vector<int> key(V, INT_MAX), parent(V, -1);
    key[0] = 0;
    using P = std::pair<int,int>; // (weight, vertex)
    std::priority_queue<P, std::vector<P>, std::greater<P>> pq;
    pq.push({0, 0});

    int total = 0;
    std::cout << "Prim MST edges:\n";
    while (!pq.empty()) {
        auto [w, u] = pq.top(); pq.pop();
        if (inMST[u]) continue;
        inMST[u] = true;
        total += w;
        if (parent[u] != -1)
            std::cout << "  Edge (" << parent[u] << " - " << u << "): weight " << w << "\n";
        for (auto [v, ew] : adj[u]) {
            if (!inMST[v] && ew < key[v]) {
                key[v] = ew;
                parent[v] = u;
                pq.push({ew, v});
            }
        }
    }
    return total;
}

int main() {
    int V = 4;
    std::vector<std::tuple<int,int,int>> edges = {
        {0,1,4},{0,2,3},{1,2,1},{1,3,2},{2,3,4}
    };

    std::cout << "=== Kruskal's MST ===\n";
    std::cout << "Total MST weight: " << kruskal_mst(V, edges) << "\n";

    std::vector<std::vector<std::pair<int,int>>> adj(V);
    for (auto [u, v, w] : edges) {
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    std::cout << "\n=== Prim's MST ===\n";
    std::cout << "Total MST weight: " << prim_mst(V, adj) << "\n";

    std::cout << "\n=== Union-Find Demo ===\n";
    DSU dsu(6);
    dsu.unite(0, 1); dsu.unite(2, 3); dsu.unite(4, 5);
    std::cout << std::boolalpha;
    std::cout << "0 connected to 1: " << dsu.connected(0, 1) << "\n";
    std::cout << "0 connected to 2: " << dsu.connected(0, 2) << "\n";
    dsu.unite(0, 2);
    std::cout << "0 connected to 3: " << dsu.connected(0, 3) << "\n";
    return 0;
}
