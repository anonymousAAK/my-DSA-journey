/*
 * WEEK 26 - C++ ADVANCED TOPICS
 * Topic: Edmonds-Karp Maximum Flow
 * File: edmonds_karp.cpp
 *
 * CONCEPT:
 *   Edmonds-Karp is Ford-Fulkerson with the BFS specialisation: each
 *   augmenting path is the *shortest* one (in number of edges) in the
 *   residual graph. This guarantees O(V * E^2) total work irrespective of
 *   capacity values.
 *
 * KEY POINTS:
 *   - BFS provides shortest paths -> at most O(V*E) phases.
 *   - Reconstruct the path with parent[] and parent_edge[] arrays.
 *   - Capacities can be arbitrarily large; runtime depends only on V, E.
 *
 * ALGORITHM / APPROACH:
 *   while BFS finds path s -> t:
 *       bottleneck = min residual along path
 *       update forward & reverse residuals
 *       flow += bottleneck
 *   return flow
 *
 * C++-SPECIFIC NOTES:
 *   - `std::queue<int>` for BFS, `std::vector<int>` for parent arrays.
 *   - Reference iteration over edges keeps mutations clean.
 *   - INT_MAX is fine since flow stays within int range here.
 *
 * DRY RUN / EXAMPLE:
 *   CLRS graph -> phases pick paths 0-1-3-5 (12), 0-2-4-5 (4),
 *   0-2-4-3-5 (7) for total flow 23.
 *
 * COMPLEXITY:
 *   Time:  O(V * E^2)
 *   Space: O(V + E)
 */

#include <iostream>
#include <vector>
#include <array>
#include <queue>
#include <climits>
#include <algorithm>

using namespace std;

class EdmondsKarp {
public:
    explicit EdmondsKarp(int n) : n_(n), graph_(n) {}

    void addEdge(int u, int v, int cap) {
        graph_[u].push_back({v, cap, (int)graph_[v].size()});
        graph_[v].push_back({u, 0,   (int)graph_[u].size() - 1});
    }

    int maxFlow(int s, int t) {
        int flow = 0;
        while (true) {
            vector<int> parent(n_, -1);
            vector<int> parentEdge(n_, -1);
            parent[s] = s;
            queue<int> q;
            q.push(s);
            while (!q.empty() && parent[t] == -1) {
                int u = q.front(); q.pop();
                for (int i = 0; i < (int)graph_[u].size(); ++i) {
                    auto& e = graph_[u][i];
                    int v = e[0], cap = e[1];
                    if (parent[v] == -1 && cap > 0) {
                        parent[v] = u;
                        parentEdge[v] = i;
                        q.push(v);
                    }
                }
            }
            if (parent[t] == -1) break;
            int bottleneck = INT_MAX;
            for (int v = t; v != s; v = parent[v])
                bottleneck = min(bottleneck, graph_[parent[v]][parentEdge[v]][1]);
            for (int v = t; v != s; v = parent[v]) {
                auto& e = graph_[parent[v]][parentEdge[v]];
                e[1] -= bottleneck;
                graph_[v][e[2]][1] += bottleneck;
            }
            flow += bottleneck;
        }
        return flow;
    }

private:
    int n_;
    vector<vector<array<int,3>>> graph_;
};

int main() {
    EdmondsKarp g(6);
    int edges[][3] = {
        {0,1,16},{0,2,13},{1,2,4},{1,3,12},
        {2,1,10},{2,4,14},{3,2,9},{3,5,20},
        {4,3,7}, {4,5,4}
    };
    for (auto& e : edges) g.addEdge(e[0], e[1], e[2]);
    cout << "Edmonds-Karp max flow (0 -> 5): " << g.maxFlow(0, 5) << "\n"; // 23
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - std::queue<int> replaces java.util.Queue.
 *   - We store parent and parent-edge in two int vectors instead of one
 *     combined structure, mirroring the Java code 1:1.
 */
