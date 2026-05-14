/*
 * WEEK 26 - C++ ADVANCED TOPICS
 * Topic: Dinic's Maximum Flow
 * File: dinic.cpp
 *
 * CONCEPT:
 *   Dinic's algorithm runs phases of (BFS-build-level-graph, DFS-blocking-
 *   flow). The level graph forces DFS to only traverse edges advancing one
 *   BFS layer at a time. With an `iter[u]` index pointer that skips dead
 *   edges, each phase costs O(V*E) and there are O(V) phases.
 *
 * KEY POINTS:
 *   - Vastly faster than Edmonds-Karp on dense graphs in practice.
 *   - On unit-capacity graphs the bound tightens to O(E*sqrt(V)) — the
 *     classical Hopcroft-Karp bound for bipartite matching.
 *   - The iter[] pointer is the key trick: never revisit dead edges.
 *
 * ALGORITHM / APPROACH:
 *   while BFS labels reach t:
 *       reset iter[]
 *       loop DFS(s, +inf) until it returns 0; accumulate
 *   return total flow
 *
 * C++-SPECIFIC NOTES:
 *   - Use long long for flow accumulator if capacities are large.
 *   - std::array<int,3> for edges keeps memory tight.
 *   - Integer iter[] vector tracks DFS pointer per vertex.
 *
 * DRY RUN / EXAMPLE:
 *   CLRS graph: Phase 1 sends 16, Phase 2 sends 7 -> total 23.
 *
 * COMPLEXITY:
 *   Time:  O(V^2 * E); O(E*sqrt(V)) on unit graphs.
 *   Space: O(V + E).
 */

#include <iostream>
#include <vector>
#include <array>
#include <queue>
#include <climits>
#include <algorithm>

using namespace std;

class Dinic {
public:
    explicit Dinic(int n) : n_(n), graph_(n), level_(n), iter_(n) {}

    void addEdge(int u, int v, int cap) {
        graph_[u].push_back({v, cap, (int)graph_[v].size()});
        graph_[v].push_back({u, 0,   (int)graph_[u].size() - 1});
    }

    long long maxFlow(int s, int t) {
        long long flow = 0;
        while (bfs(s, t)) {
            fill(iter_.begin(), iter_.end(), 0);
            int pushed;
            while ((pushed = dfs(s, t, INT_MAX)) > 0) flow += pushed;
        }
        return flow;
    }

private:
    int n_;
    vector<vector<array<int,3>>> graph_;
    vector<int> level_;
    vector<int> iter_;

    bool bfs(int s, int t) {
        fill(level_.begin(), level_.end(), -1);
        level_[s] = 0;
        queue<int> q;
        q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (auto& e : graph_[u]) {
                int v = e[0], cap = e[1];
                if (cap > 0 && level_[v] < 0) {
                    level_[v] = level_[u] + 1;
                    q.push(v);
                }
            }
        }
        return level_[t] >= 0;
    }

    int dfs(int u, int t, int pushed) {
        if (u == t) return pushed;
        for (; iter_[u] < (int)graph_[u].size(); ++iter_[u]) {
            auto& e = graph_[u][iter_[u]];
            int v = e[0], cap = e[1], rev = e[2];
            if (cap > 0 && level_[v] == level_[u] + 1) {
                int d = dfs(v, t, min(pushed, cap));
                if (d > 0) {
                    e[1] -= d;
                    graph_[v][rev][1] += d;
                    return d;
                }
            }
        }
        return 0;
    }
};

int main() {
    Dinic g(6);
    int edges[][3] = {
        {0,1,16},{0,2,13},{1,2,4},{1,3,12},
        {2,1,10},{2,4,14},{3,2,9},{3,5,20},
        {4,3,7}, {4,5,4}
    };
    for (auto& e : edges) g.addEdge(e[0], e[1], e[2]);
    cout << "Dinic max flow (0 -> 5): " << g.maxFlow(0, 5) << "\n"; // 23
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - C++ uses long long for flow accumulator to be safe on big-capacity
 *     inputs; Java's network_flow.java stays in int range for its demo.
 *   - The iter_ pointer is updated via post-increment in the for loop,
 *     making the dead-edge skip explicit.
 */
