/*
 * WEEK 17 - C++ DSA
 * Topic: Graph Representations + BFS / DFS
 * File: 1.GraphRepresentations.cpp
 *
 * CONCEPT:
 *     A graph is a set of vertices V and edges E. Two storage layouts:
 *         Adjacency LIST   : std::vector<std::vector<int>>  - O(V+E) space.
 *         Adjacency MATRIX : std::vector<std::vector<int>> sized V*V
 *                             - O(V^2) space, O(1) edge query.
 *     Both representations are demonstrated below.
 *
 * KEY POINTS:
 *     - BFS uses std::queue (FIFO); explores by distance; finds shortest
 *       unweighted path; O(V + E).
 *     - DFS recurses; foundation for cycle detection, components,
 *       topological sort; O(V + E).
 *     - Cycle detection (undirected): visited neighbour that isn't the
 *       parent == back edge.
 *     - Bipartite test: 2-colour BFS; conflict means odd cycle.
 *
 * ALGORITHM / APPROACH:
 *     Standard BFS / DFS templates as in the Java reference; see DRY RUN.
 *
 * C++-SPECIFIC NOTES:
 *     - std::vector<std::vector<int>> is the canonical adjacency list.
 *     - Use `std::vector<bool>` for visited flags (compact bitset).
 *     - std::queue<int> is just a thin wrapper over std::deque<int>.
 *     - Pass adjacency by `const&` to avoid copies; mark visit functions
 *       as taking the adj list by const reference.
 *     - For matrix form, prefer std::vector<std::vector<int>> initialised
 *       to V rows of V zeros.
 *
 * DRY RUN:
 *     Edges (undirected): 0-1,1-2,2-5,5-4,4-3,3-0,1-4
 *         BFS(0) -> 0,1,3,2,4,5
 *         DFS(0) -> 0,1,2,5,4,3   (recursion order may vary slightly)
 *         distances from 0: [0,1,2,1,2,2]
 *
 *     Disconnected: edges {0-1, 1-2, 3-4} with vertex 5 isolated
 *         components = 3
 *
 * COMPLEXITY:
 *     Build O(V+E); BFS/DFS O(V+E); components O(V+E);
 *     cycle / bipartite O(V+E).
 */

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <functional>

class Graph {
public:
    int V;
    std::vector<std::vector<int>> adj;

    explicit Graph(int v) : V(v), adj(v) {}

    void addEdge(int u, int v) {                  // undirected
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    void addDirectedEdge(int u, int v) { adj[u].push_back(v); }

    std::vector<int> bfs(int src) const {
        std::vector<int> order;
        std::vector<bool> visited(V, false);
        std::queue<int> q;
        visited[src] = true;
        q.push(src);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            order.push_back(u);
            for (int v : adj[u]) if (!visited[v]) {
                visited[v] = true;
                q.push(v);
            }
        }
        return order;
    }

    std::vector<int> shortestDistances(int src) const {
        std::vector<int> dist(V, -1);
        dist[src] = 0;
        std::queue<int> q; q.push(src);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
        return dist;
    }

    std::vector<int> dfs(int src) const {
        std::vector<int> order;
        std::vector<bool> visited(V, false);
        std::function<void(int)> go = [&](int u) {
            visited[u] = true;
            order.push_back(u);
            for (int v : adj[u]) if (!visited[v]) go(v);
        };
        go(src);
        return order;
    }

    int countComponents() const {
        std::vector<bool> visited(V, false);
        std::function<void(int)> go = [&](int u) {
            visited[u] = true;
            for (int v : adj[u]) if (!visited[v]) go(v);
        };
        int count = 0;
        for (int i = 0; i < V; ++i) if (!visited[i]) { go(i); ++count; }
        return count;
    }

    bool hasCycle() const {                       // undirected
        std::vector<bool> visited(V, false);
        std::function<bool(int,int)> go = [&](int u, int parent) -> bool {
            visited[u] = true;
            for (int v : adj[u]) {
                if (!visited[v]) {
                    if (go(v, u)) return true;
                } else if (v != parent) return true;
            }
            return false;
        };
        for (int i = 0; i < V; ++i)
            if (!visited[i] && go(i, -1)) return true;
        return false;
    }

    bool isBipartite() const {
        std::vector<int> color(V, 0);             // 0=uncolored, 1/-1
        for (int s = 0; s < V; ++s) {
            if (color[s] != 0) continue;
            color[s] = 1;
            std::queue<int> q; q.push(s);
            while (!q.empty()) {
                int u = q.front(); q.pop();
                for (int v : adj[u]) {
                    if (color[v] == 0) { color[v] = -color[u]; q.push(v); }
                    else if (color[v] == color[u]) return false;
                }
            }
        }
        return true;
    }
};

// MATRIX representation included to mirror Java commentary on dense graphs.
class GraphMatrix {
public:
    int V;
    std::vector<std::vector<int>> mat;
    explicit GraphMatrix(int v) : V(v), mat(v, std::vector<int>(v, 0)) {}
    void addEdge(int u, int v) { mat[u][v] = 1; mat[v][u] = 1; }
    std::vector<int> neighbours(int u) const {
        std::vector<int> out;
        for (int v = 0; v < V; ++v) if (mat[u][v]) out.push_back(v);
        return out;
    }
};

// ---------- driver ----------
template <typename T>
void printVec(const std::vector<T>& v) {
    std::cout << "[";
    for (size_t i = 0; i < v.size(); ++i) std::cout << v[i] << (i+1<v.size()?",":"");
    std::cout << "]";
}

int main() {
    Graph g(6);
    int undirected[][2] = {{0,1},{1,2},{2,5},{5,4},{4,3},{3,0},{1,4}};
    for (auto& e : undirected) g.addEdge(e[0], e[1]);

    std::cout << "BFS from 0: "; printVec(g.bfs(0)); std::cout << "\n";
    std::cout << "DFS from 0: "; printVec(g.dfs(0)); std::cout << "\n";
    std::cout << "Distances from 0: "; printVec(g.shortestDistances(0)); std::cout << "\n";
    std::cout << "Components: " << g.countComponents() << "\n";
    std::cout << std::boolalpha;
    std::cout << "Has cycle: " << g.hasCycle() << "\n";
    std::cout << "Bipartite: " << g.isBipartite() << "\n";

    Graph g2(6);
    g2.addEdge(0,1); g2.addEdge(1,2);
    g2.addEdge(3,4);
    std::cout << "\nDisconnected components: " << g2.countComponents() << "\n"; // 3
    std::cout << "BFS from 0: "; printVec(g2.bfs(0)); std::cout << "\n";

    Graph bip(5);
    for (int u : {0,1}) for (int v : {2,3,4}) bip.addEdge(u, v);
    std::cout << "\nK_{2,3} bipartite: " << bip.isBipartite() << "\n";          // true

    Graph tri(3);
    tri.addEdge(0,1); tri.addEdge(1,2); tri.addEdge(2,0);
    std::cout << "Triangle bipartite: " << tri.isBipartite() << "\n";           // false

    GraphMatrix m(4);
    m.addEdge(0,1); m.addEdge(1,2); m.addEdge(2,3);
    std::cout << "\nMatrix neighbours of 1: "; printVec(m.neighbours(1)); std::cout << "\n";
}

/*
 * NOTES (C++ vs Java):
 *   - Java auto-boxes ints into Integer for ArrayList<Integer>; C++ stores
 *     raw int in vector<int>, avoiding heap allocations and indirection.
 *   - std::vector<bool> packs bits (note: not a true container of bool).
 *     For random access you can also use std::vector<char> for simplicity.
 *   - Recursive lambdas need std::function<...> capture (no `auto` recursion
 *     in C++17 standalone). C++23 has explicit object parameter ("deducing this").
 *   - std::queue<T> defaults to std::deque<T> as its container.
 *   - std::move when transferring vectors out of a function avoids copies.
 */
