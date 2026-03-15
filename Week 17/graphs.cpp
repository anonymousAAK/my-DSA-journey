/*
 * =============================================================================
 * Week 17 — Graphs  (C++17)
 * =============================================================================
 *
 * Topics covered
 * --------------
 *   1. Graph class  (adjacency list, weighted edges)
 *   2. BFS + shortest distances (unweighted)
 *   3. DFS — recursive & iterative
 *   4. Cycle detection — undirected & directed
 *   5. Bipartite check (BFS-based 2-coloring)
 *   6. Topological sort — DFS-based & Kahn's algorithm (BFS)
 *
 * Complexity cheat-sheet  (V = vertices, E = edges)
 * --------------------------------------------------
 *   BFS / DFS               O(V + E)  time  |  O(V) space
 *   Cycle detection          O(V + E)
 *   Bipartite check          O(V + E)
 *   Topological sort (both)  O(V + E)
 *
 * Build & run
 *   g++ -std=c++17 -O2 -o graphs graphs.cpp && ./graphs
 * =============================================================================
 */

#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <algorithm>
#include <cassert>
#include <sstream>
#include <optional>
#include <functional>

// ---------------------------------------------------------------------------
// Graph class — adjacency list with optional weights
// ---------------------------------------------------------------------------
class Graph {
public:
    explicit Graph(int n, bool directed = false)
        : adj_(n), n_(n), directed_(directed) {}

    void add_edge(int u, int v, int w = 1) {
        adj_[u].emplace_back(v, w);
        if (!directed_) adj_[v].emplace_back(u, w);
    }

    [[nodiscard]] int size() const { return n_; }
    [[nodiscard]] bool is_directed() const { return directed_; }
    [[nodiscard]] const std::vector<std::pair<int,int>>& neighbors(int u) const {
        return adj_[u];
    }

    // ----- BFS — returns shortest distances from source (unweighted) -----
    // Complexity: O(V + E) time | O(V) space
    [[nodiscard]] std::vector<int> bfs(int src) const {
        std::vector<int> dist(n_, -1);
        std::queue<int> q;
        dist[src] = 0;
        q.push(src);

        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (auto [v, w] : adj_[u]) {
                if (dist[v] == -1) {
                    dist[v] = dist[u] + 1;
                    q.push(v);
                }
            }
        }
        return dist;
    }

    // ----- DFS recursive — returns visited order -----
    // Complexity: O(V + E) time | O(V) space
    [[nodiscard]] std::vector<int> dfs_recursive(int src) const {
        std::vector<bool> visited(n_, false);
        std::vector<int> order;
        dfs_helper(src, visited, order);
        return order;
    }

    // ----- DFS iterative — returns visited order -----
    // Complexity: O(V + E) time | O(V) space
    [[nodiscard]] std::vector<int> dfs_iterative(int src) const {
        std::vector<bool> visited(n_, false);
        std::vector<int> order;
        std::stack<int> stk;
        stk.push(src);

        while (!stk.empty()) {
            int u = stk.top(); stk.pop();
            if (visited[u]) continue;
            visited[u] = true;
            order.push_back(u);
            // Push neighbors in reverse so that leftmost is visited first.
            for (auto it = adj_[u].rbegin(); it != adj_[u].rend(); ++it) {
                if (!visited[it->first]) stk.push(it->first);
            }
        }
        return order;
    }

    // ----- Cycle detection (undirected) — BFS/DFS based -----
    // Complexity: O(V + E)
    [[nodiscard]] bool has_cycle_undirected() const {
        std::vector<bool> visited(n_, false);
        for (int i = 0; i < n_; ++i) {
            if (!visited[i]) {
                if (dfs_cycle_undirected(i, -1, visited)) return true;
            }
        }
        return false;
    }

    // ----- Cycle detection (directed) — DFS coloring -----
    // Colors: 0=white(unvisited), 1=gray(in stack), 2=black(done)
    // Complexity: O(V + E)
    [[nodiscard]] bool has_cycle_directed() const {
        std::vector<int> color(n_, 0);
        for (int i = 0; i < n_; ++i) {
            if (color[i] == 0) {
                if (dfs_cycle_directed(i, color)) return true;
            }
        }
        return false;
    }

    // ----- Bipartite check — BFS 2-coloring -----
    // Complexity: O(V + E)
    [[nodiscard]] bool is_bipartite() const {
        std::vector<int> color(n_, -1);
        for (int i = 0; i < n_; ++i) {
            if (color[i] != -1) continue;
            std::queue<int> q;
            color[i] = 0;
            q.push(i);
            while (!q.empty()) {
                int u = q.front(); q.pop();
                for (auto [v, w] : adj_[u]) {
                    if (color[v] == -1) {
                        color[v] = 1 - color[u];
                        q.push(v);
                    } else if (color[v] == color[u]) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    // ----- Topological Sort (DFS-based) -----
    // Complexity: O(V + E)
    [[nodiscard]] std::optional<std::vector<int>> topo_sort_dfs() const {
        std::vector<int> color(n_, 0);
        std::vector<int> order;
        order.reserve(n_);

        for (int i = 0; i < n_; ++i) {
            if (color[i] == 0) {
                if (!topo_dfs_helper(i, color, order)) return std::nullopt; // cycle
            }
        }
        std::reverse(order.begin(), order.end());
        return order;
    }

    // ----- Topological Sort (Kahn's algorithm — BFS) -----
    // Complexity: O(V + E)
    [[nodiscard]] std::optional<std::vector<int>> topo_sort_kahn() const {
        std::vector<int> indegree(n_, 0);
        for (int u = 0; u < n_; ++u)
            for (auto [v, w] : adj_[u])
                ++indegree[v];

        std::queue<int> q;
        for (int i = 0; i < n_; ++i)
            if (indegree[i] == 0) q.push(i);

        std::vector<int> order;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            order.push_back(u);
            for (auto [v, w] : adj_[u]) {
                if (--indegree[v] == 0) q.push(v);
            }
        }

        if (static_cast<int>(order.size()) != n_) return std::nullopt; // cycle
        return order;
    }

private:
    std::vector<std::vector<std::pair<int,int>>> adj_;
    int n_;
    bool directed_;

    void dfs_helper(int u, std::vector<bool>& vis, std::vector<int>& order) const {
        vis[u] = true;
        order.push_back(u);
        for (auto [v, w] : adj_[u]) {
            if (!vis[v]) dfs_helper(v, vis, order);
        }
    }

    bool dfs_cycle_undirected(int u, int parent, std::vector<bool>& vis) const {
        vis[u] = true;
        for (auto [v, w] : adj_[u]) {
            if (!vis[v]) {
                if (dfs_cycle_undirected(v, u, vis)) return true;
            } else if (v != parent) {
                return true;
            }
        }
        return false;
    }

    bool dfs_cycle_directed(int u, std::vector<int>& color) const {
        color[u] = 1; // gray
        for (auto [v, w] : adj_[u]) {
            if (color[v] == 1) return true;           // back edge => cycle
            if (color[v] == 0 && dfs_cycle_directed(v, color)) return true;
        }
        color[u] = 2; // black
        return false;
    }

    bool topo_dfs_helper(int u, std::vector<int>& color, std::vector<int>& order) const {
        color[u] = 1;
        for (auto [v, w] : adj_[u]) {
            if (color[v] == 1) return false;
            if (color[v] == 0 && !topo_dfs_helper(v, color, order)) return false;
        }
        color[u] = 2;
        order.push_back(u);
        return true;
    }
};

// ---------------------------------------------------------------------------
// Helper
// ---------------------------------------------------------------------------
template <typename T>
std::string vec_str(const std::vector<T>& v) {
    std::ostringstream oss;
    oss << "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i) oss << ", ";
        oss << v[i];
    }
    oss << "]";
    return oss.str();
}

// ---------------------------------------------------------------------------
// main — test cases
// ---------------------------------------------------------------------------
int main() {
    std::cout << "=== Week 17: Graphs ===\n\n";

    // ---- BFS ----
    {
        std::cout << "-- BFS shortest distances --\n";
        Graph g(6, false);
        g.add_edge(0,1); g.add_edge(0,2);
        g.add_edge(1,3); g.add_edge(2,3);
        g.add_edge(3,4); g.add_edge(4,5);
        auto dist = g.bfs(0);
        std::cout << "  dist from 0: " << vec_str(dist) << "\n";
        assert(dist[0] == 0 && dist[3] == 2 && dist[5] == 4);
        std::cout << "\n";
    }

    // ---- DFS recursive & iterative ----
    {
        std::cout << "-- DFS --\n";
        Graph g(5, false);
        g.add_edge(0,1); g.add_edge(0,2);
        g.add_edge(1,3); g.add_edge(2,4);
        auto rec = g.dfs_recursive(0);
        auto iter = g.dfs_iterative(0);
        std::cout << "  recursive: " << vec_str(rec) << "\n";
        std::cout << "  iterative: " << vec_str(iter) << "\n";
        assert(rec.size() == 5 && iter.size() == 5);
        std::cout << "\n";
    }

    // ---- Cycle detection (undirected) ----
    {
        std::cout << "-- Cycle Detection (undirected) --\n";
        Graph tree(4, false);
        tree.add_edge(0,1); tree.add_edge(1,2); tree.add_edge(2,3);
        assert(!tree.has_cycle_undirected());
        std::cout << "  tree (no cycle): " << !tree.has_cycle_undirected() << "\n";

        Graph cyclic(4, false);
        cyclic.add_edge(0,1); cyclic.add_edge(1,2); cyclic.add_edge(2,3); cyclic.add_edge(3,0);
        assert(cyclic.has_cycle_undirected());
        std::cout << "  cycle present:   " << cyclic.has_cycle_undirected() << "\n\n";
    }

    // ---- Cycle detection (directed) ----
    {
        std::cout << "-- Cycle Detection (directed) --\n";
        Graph dag(4, true);
        dag.add_edge(0,1); dag.add_edge(1,2); dag.add_edge(2,3);
        assert(!dag.has_cycle_directed());
        std::cout << "  DAG (no cycle): " << !dag.has_cycle_directed() << "\n";

        Graph cyc(3, true);
        cyc.add_edge(0,1); cyc.add_edge(1,2); cyc.add_edge(2,0);
        assert(cyc.has_cycle_directed());
        std::cout << "  cycle present:  " << cyc.has_cycle_directed() << "\n\n";
    }

    // ---- Bipartite check ----
    {
        std::cout << "-- Bipartite Check --\n";
        Graph bip(4, false);
        bip.add_edge(0,1); bip.add_edge(2,3); bip.add_edge(0,3); bip.add_edge(1,2);
        assert(bip.is_bipartite());
        std::cout << "  even cycle (bipartite): " << bip.is_bipartite() << "\n";

        Graph odd(3, false);
        odd.add_edge(0,1); odd.add_edge(1,2); odd.add_edge(2,0);
        assert(!odd.is_bipartite());
        std::cout << "  triangle (not bipartite): " << !odd.is_bipartite() << "\n\n";
    }

    // ---- Topological sort ----
    {
        std::cout << "-- Topological Sort --\n";
        Graph dag(6, true);
        dag.add_edge(5,2); dag.add_edge(5,0);
        dag.add_edge(4,0); dag.add_edge(4,1);
        dag.add_edge(2,3); dag.add_edge(3,1);

        auto dfs_order = dag.topo_sort_dfs();
        assert(dfs_order.has_value());
        std::cout << "  DFS-based:   " << vec_str(*dfs_order) << "\n";

        auto kahn_order = dag.topo_sort_kahn();
        assert(kahn_order.has_value());
        std::cout << "  Kahn's BFS:  " << vec_str(*kahn_order) << "\n";

        // Verify ordering: for every edge u->v, u appears before v.
        auto valid_topo = [&](const std::vector<int>& order) {
            std::vector<int> pos(6);
            for (int i = 0; i < 6; ++i) pos[order[i]] = i;
            for (int u = 0; u < 6; ++u)
                for (auto [v,w] : dag.neighbors(u))
                    if (pos[u] >= pos[v]) return false;
            return true;
        };
        assert(valid_topo(*dfs_order));
        assert(valid_topo(*kahn_order));
        std::cout << "  (both orderings validated)\n";
    }

    std::cout << "\nAll Week 17 tests passed.\n";
    return 0;
}
