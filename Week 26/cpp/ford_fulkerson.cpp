/*
 * WEEK 26 - C++ ADVANCED TOPICS
 * Topic: Ford-Fulkerson Maximum Flow
 * File: ford_fulkerson.cpp
 *
 * CONCEPT:
 *   The Ford-Fulkerson method is a greedy framework for max-flow: keep
 *   finding s->t augmenting paths in the residual graph and pushing the
 *   bottleneck capacity. This file uses the DFS-based variant. By the
 *   max-flow / min-cut theorem the resulting flow is optimal.
 *
 * KEY POINTS:
 *   - Residual graph holds reverse edges (initial cap 0). Pushing f along
 *     (u,v) does cap[u,v] -= f and cap[v,u] += f.
 *   - O(E * max_flow): worst case grows with the flow value, not the graph
 *     density. Use Edmonds-Karp / Dinic if max_flow is huge.
 *   - Fine for unit-capacity / small-capacity graphs and competitive coding.
 *
 * ALGORITHM / APPROACH:
 *   build residual graph
 *   while DFS(s, t, INT_MAX) returns push > 0:
 *       flow += push
 *   return flow
 *
 * C++-SPECIFIC NOTES:
 *   - Use `vector<array<int,3>>` per vertex: {to, cap, rev_index}.
 *   - Mutate residual capacities through edge references — no allocations.
 *   - `INT_MAX` / `numeric_limits<int>::max()` is the natural infinity.
 *
 * DRY RUN / EXAMPLE:
 *   CLRS graph (0..5), source 0 sink 5, capacities listed in main(); the
 *   algorithm augments paths until no s->t path remains. Final flow = 23.
 *
 * COMPLEXITY:
 *   Time:  O(E * F) where F is max flow value.
 *   Space: O(V + E).
 */

#include <iostream>
#include <vector>
#include <array>
#include <climits>
#include <algorithm>

using namespace std;

class FordFulkerson {
public:
    explicit FordFulkerson(int n) : n_(n), graph_(n) {}

    void addEdge(int u, int v, int cap) {
        graph_[u].push_back({v, cap, (int)graph_[v].size()});
        graph_[v].push_back({u, 0,   (int)graph_[u].size() - 1});
    }

    int maxFlow(int s, int t) {
        int flow = 0;
        while (true) {
            vector<bool> visited(n_, false);
            int pushed = dfs(s, t, INT_MAX, visited);
            if (pushed == 0) break;
            flow += pushed;
        }
        return flow;
    }

private:
    int n_;
    vector<vector<array<int,3>>> graph_;  // each entry: {to, cap, rev}

    int dfs(int u, int t, int pushed, vector<bool>& visited) {
        if (u == t) return pushed;
        visited[u] = true;
        for (auto& e : graph_[u]) {
            int v = e[0], cap = e[1], rev = e[2];
            if (!visited[v] && cap > 0) {
                int d = dfs(v, t, min(pushed, cap), visited);
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
    FordFulkerson g(6);
    int edges[][3] = {
        {0,1,16},{0,2,13},{1,2,4},{1,3,12},
        {2,1,10},{2,4,14},{3,2,9},{3,5,20},
        {4,3,7}, {4,5,4}
    };
    for (auto& e : edges) g.addEdge(e[0], e[1], e[2]);
    cout << "Ford-Fulkerson max flow (0 -> 5): " << g.maxFlow(0, 5) << "\n";  // 23
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - C++ uses std::array<int,3> for cache-friendly edge storage (versus
 *     Java's parallel int[] arrays).
 *   - Reference (`auto& e`) iteration lets us update residual capacities
 *     in place without explicit indexing.
 *   - `INT_MAX` is the canonical infinity for ints; Java uses
 *     Integer.MAX_VALUE.
 */
