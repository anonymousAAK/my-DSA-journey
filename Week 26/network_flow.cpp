/*
 * Week 26: Network Flow & Matching
 * ==================================
 * Topics covered:
 *   1. Ford-Fulkerson (DFS augmenting paths)      - O(E * max_flow)
 *   2. Edmonds-Karp   (BFS augmenting paths)      - O(V * E^2)
 *   3. Hopcroft-Karp  (bipartite matching)         - O(E * sqrt(V))
 *   4. Hungarian Algorithm (min-cost assignment)   - O(N^3)
 */

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <climits>
#include <utility>
using namespace std;

// ===========================================================================
// Flow network using adjacency list with edge structs
// ===========================================================================

struct Edge {
    int to, cap, rev;
};

class MaxFlowGraph {
public:
    int n;
    vector<vector<Edge>> graph;

    MaxFlowGraph(int n) : n(n), graph(n) {}

    void add_edge(int u, int v, int cap) {
        graph[u].push_back({v, cap, (int)graph[v].size()});
        graph[v].push_back({u, 0,   (int)graph[u].size() - 1});
    }

    // -------------------------------------------------------------------
    // 1. Ford-Fulkerson (DFS)
    //    Time:  O(E * max_flow)
    //    Space: O(V + E)
    // -------------------------------------------------------------------
    int ff_dfs(int u, int t, int pushed, vector<bool>& visited) {
        if (u == t) return pushed;
        visited[u] = true;
        for (auto& e : graph[u]) {
            if (!visited[e.to] && e.cap > 0) {
                int d = ff_dfs(e.to, t, min(pushed, e.cap), visited);
                if (d > 0) {
                    e.cap -= d;
                    graph[e.to][e.rev].cap += d;
                    return d;
                }
            }
        }
        return 0;
    }

    int ford_fulkerson(int s, int t) {
        int flow = 0;
        while (true) {
            vector<bool> visited(n, false);
            int pushed = ff_dfs(s, t, INT_MAX, visited);
            if (pushed == 0) break;
            flow += pushed;
        }
        return flow;
    }

    // -------------------------------------------------------------------
    // 2. Edmonds-Karp (BFS)
    //    Time:  O(V * E^2)
    //    Space: O(V + E)
    // -------------------------------------------------------------------
    int edmonds_karp(int s, int t) {
        int flow = 0;
        while (true) {
            vector<int> parent(n, -1), parent_edge(n, -1);
            parent[s] = s;
            queue<int> q;
            q.push(s);
            while (!q.empty() && parent[t] == -1) {
                int u = q.front(); q.pop();
                for (int i = 0; i < (int)graph[u].size(); i++) {
                    Edge& e = graph[u][i];
                    if (parent[e.to] == -1 && e.cap > 0) {
                        parent[e.to] = u;
                        parent_edge[e.to] = i;
                        q.push(e.to);
                    }
                }
            }
            if (parent[t] == -1) break;

            int bottleneck = INT_MAX;
            for (int v = t; v != s; v = parent[v])
                bottleneck = min(bottleneck, graph[parent[v]][parent_edge[v]].cap);
            for (int v = t; v != s; v = parent[v]) {
                Edge& e = graph[parent[v]][parent_edge[v]];
                e.cap -= bottleneck;
                graph[v][e.rev].cap += bottleneck;
            }
            flow += bottleneck;
        }
        return flow;
    }
};

// ===========================================================================
// 3. Hopcroft-Karp Bipartite Matching
//    Time:  O(E * sqrt(V))
//    Space: O(V + E)
// ===========================================================================

class HopcroftKarp {
    int left_size, right_size;
    vector<vector<int>> adj;
    vector<int> dist;

    bool bfs() {
        queue<int> q;
        for (int u = 0; u < left_size; u++) {
            if (match_left[u] == -1) { dist[u] = 0; q.push(u); }
            else                     { dist[u] = INT_MAX; }
        }
        bool found = false;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                int nxt = match_right[v];
                if (nxt == -1) {
                    found = true;
                } else if (dist[nxt] == INT_MAX) {
                    dist[nxt] = dist[u] + 1;
                    q.push(nxt);
                }
            }
        }
        return found;
    }

    bool dfs(int u) {
        for (int v : adj[u]) {
            int nxt = match_right[v];
            if (nxt == -1 || (dist[nxt] == dist[u] + 1 && dfs(nxt))) {
                match_left[u] = v;
                match_right[v] = u;
                return true;
            }
        }
        dist[u] = INT_MAX;
        return false;
    }

public:
    vector<int> match_left, match_right;

    HopcroftKarp(int l, int r) : left_size(l), right_size(r), adj(l) {}

    void add_edge(int u, int v) { adj[u].push_back(v); }

    int max_matching() {
        match_left.assign(left_size, -1);
        match_right.assign(right_size, -1);
        dist.resize(left_size);
        int matching = 0;
        while (bfs()) {
            for (int u = 0; u < left_size; u++) {
                if (match_left[u] == -1 && dfs(u)) matching++;
            }
        }
        return matching;
    }

    vector<pair<int,int>> get_matching() {
        vector<pair<int,int>> result;
        for (int u = 0; u < left_size; u++) {
            if (match_left[u] != -1) result.push_back({u, match_left[u]});
        }
        return result;
    }
};

// ===========================================================================
// 4. Hungarian Algorithm (Minimum-Cost Perfect Assignment)
//    Time:  O(N^3)
//    Space: O(N^2)
// ===========================================================================

class Hungarian {
    int n;
    vector<vector<int>> cost;

public:
    Hungarian(const vector<vector<int>>& c) : n(c.size()), cost(c) {}

    pair<int, vector<int>> solve() {
        const int INF = INT_MAX / 2;
        vector<int> u(n + 1, 0), v(n + 1, 0);
        vector<int> p(n + 1, 0), way(n + 1, 0);

        for (int i = 1; i <= n; i++) {
            p[0] = i;
            int j0 = 0;
            vector<int> minv(n + 1, INF);
            vector<bool> used(n + 1, false);

            do {
                used[j0] = true;
                int i0 = p[j0], delta = INF, j1 = -1;
                for (int j = 1; j <= n; j++) {
                    if (!used[j]) {
                        int cur = cost[i0 - 1][j - 1] - u[i0] - v[j];
                        if (cur < minv[j]) { minv[j] = cur; way[j] = j0; }
                        if (minv[j] < delta) { delta = minv[j]; j1 = j; }
                    }
                }
                for (int j = 0; j <= n; j++) {
                    if (used[j]) { u[p[j]] += delta; v[j] -= delta; }
                    else         { minv[j] -= delta; }
                }
                j0 = j1;
            } while (p[j0] != 0);

            do {
                int j1 = way[j0];
                p[j0] = p[j1];
                j0 = j1;
            } while (j0 != 0);
        }

        vector<int> assignment(n);
        for (int j = 1; j <= n; j++) assignment[p[j] - 1] = j - 1;
        int total = 0;
        for (int i = 0; i < n; i++) total += cost[i][assignment[i]];
        return {total, assignment};
    }
};

// ===========================================================================
// Demo / Driver
// ===========================================================================

int main() {
    cout << string(60, '=') << "\n";
    cout << "Week 26: Network Flow & Matching\n";
    cout << string(60, '=') << "\n";

    // --- Edmonds-Karp ---
    cout << "\n--- Edmonds-Karp Max Flow ---\n";
    {
        MaxFlowGraph g(6);
        g.add_edge(0, 1, 16); g.add_edge(0, 2, 13);
        g.add_edge(1, 2, 4);  g.add_edge(1, 3, 12);
        g.add_edge(2, 1, 10); g.add_edge(2, 4, 14);
        g.add_edge(3, 2, 9);  g.add_edge(3, 5, 20);
        g.add_edge(4, 3, 7);  g.add_edge(4, 5, 4);
        cout << "Max flow (0 -> 5): " << g.edmonds_karp(0, 5) << "\n"; // 23
    }

    // --- Ford-Fulkerson ---
    cout << "\n--- Ford-Fulkerson Max Flow ---\n";
    {
        MaxFlowGraph g(6);
        g.add_edge(0, 1, 16); g.add_edge(0, 2, 13);
        g.add_edge(1, 2, 4);  g.add_edge(1, 3, 12);
        g.add_edge(2, 1, 10); g.add_edge(2, 4, 14);
        g.add_edge(3, 2, 9);  g.add_edge(3, 5, 20);
        g.add_edge(4, 3, 7);  g.add_edge(4, 5, 4);
        cout << "Max flow (0 -> 5): " << g.ford_fulkerson(0, 5) << "\n"; // 23
    }

    // --- Hopcroft-Karp ---
    cout << "\n--- Hopcroft-Karp Bipartite Matching ---\n";
    {
        HopcroftKarp hk(4, 4);
        hk.add_edge(0, 0); hk.add_edge(0, 1);
        hk.add_edge(1, 0); hk.add_edge(1, 2);
        hk.add_edge(2, 1); hk.add_edge(2, 3);
        hk.add_edge(3, 2); hk.add_edge(3, 3);
        cout << "Maximum matching size: " << hk.max_matching() << "\n"; // 4
        cout << "Matched pairs:";
        for (auto& [u, v] : hk.get_matching()) cout << " (" << u << "," << v << ")";
        cout << "\n";
    }

    // --- Hungarian ---
    cout << "\n--- Hungarian Algorithm (Min-Cost Assignment) ---\n";
    {
        vector<vector<int>> cost_matrix = {
            {9, 2, 7, 8},
            {6, 4, 3, 7},
            {5, 8, 1, 8},
            {7, 6, 9, 4}
        };
        Hungarian h(cost_matrix);
        auto [total_cost, assignment] = h.solve();
        cout << "Minimum cost: " << total_cost << "\n"; // 13
        cout << "Assignment (row -> col):";
        for (int c : assignment) cout << " " << c;
        cout << "\n";
    }

    return 0;
}
