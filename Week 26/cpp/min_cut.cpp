/*
 * WEEK 26 - C++ ADVANCED TOPICS
 * Topic: Minimum s-t Cut via Max-Flow / Min-Cut Theorem
 * File: min_cut.cpp
 *
 * CONCEPT:
 *   max-flow value == min-cut capacity. After saturating, BFS from source
 *   in the residual graph; reachable vertices form S, the rest form T, and
 *   original forward edges crossing S->T constitute the minimum cut.
 *
 * KEY POINTS:
 *   - Distinguish original forward edges from auto-generated reverse edges
 *     (we tag with a bool flag and remember the original capacity).
 *   - Works on top of any max-flow routine (we embed Edmonds-Karp).
 *
 * ALGORITHM / APPROACH:
 *   run max-flow
 *   BFS in residual graph from s
 *   collect every original (u,v) with u in S and v not in S
 *
 * C++-SPECIFIC NOTES:
 *   - Use a struct Edge for clarity; std::vector<Edge> per vertex.
 *   - Edge stores residual cap *and* original cap so we can report cut
 *     capacity after the flow run.
 *
 * DRY RUN / EXAMPLE:
 *   CLRS graph -> max flow 23. After saturation, BFS from 0 typically
 *   reaches {0,2,4}; cut edges include (0,1)=16 and (4,3)=7 etc.; their
 *   capacities sum to 23.
 *
 * COMPLEXITY:
 *   Max-flow + O(V+E) extraction.
 */

#include <iostream>
#include <vector>
#include <queue>
#include <climits>
#include <algorithm>

using namespace std;

struct Edge {
    int to;
    int cap;            // residual
    int rev;            // index of reverse edge
    bool original;      // true for forward, false for auto-reverse
    int origCap;        // original capacity (only meaningful for original)
};

class MinCut {
public:
    explicit MinCut(int n) : n_(n), graph_(n) {}

    void addEdge(int u, int v, int cap) {
        graph_[u].push_back({v, cap, (int)graph_[v].size(), true, cap});
        graph_[v].push_back({u, 0,   (int)graph_[u].size() - 1, false, 0});
    }

    int maxFlow(int s, int t) {
        int flow = 0;
        while (true) {
            vector<int> parent(n_, -1), pe(n_, -1);
            parent[s] = s;
            queue<int> q;
            q.push(s);
            while (!q.empty() && parent[t] == -1) {
                int u = q.front(); q.pop();
                for (int i = 0; i < (int)graph_[u].size(); ++i) {
                    Edge& e = graph_[u][i];
                    if (parent[e.to] == -1 && e.cap > 0) {
                        parent[e.to] = u;
                        pe[e.to] = i;
                        q.push(e.to);
                    }
                }
            }
            if (parent[t] == -1) break;
            int b = INT_MAX;
            for (int v = t; v != s; v = parent[v])
                b = min(b, graph_[parent[v]][pe[v]].cap);
            for (int v = t; v != s; v = parent[v]) {
                Edge& e = graph_[parent[v]][pe[v]];
                e.cap -= b;
                graph_[v][e.rev].cap += b;
            }
            flow += b;
        }
        return flow;
    }

    vector<bool> reachableFromSource(int s) const {
        vector<bool> vis(n_, false);
        vis[s] = true;
        queue<int> q;
        q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (const auto& e : graph_[u])
                if (e.cap > 0 && !vis[e.to]) {
                    vis[e.to] = true;
                    q.push(e.to);
                }
        }
        return vis;
    }

    pair<int, vector<tuple<int,int,int>>> minCut(int s, int t) {
        int flow = maxFlow(s, t);
        auto side = reachableFromSource(s);
        vector<tuple<int,int,int>> cut;
        for (int u = 0; u < n_; ++u) if (side[u]) {
            for (const auto& e : graph_[u]) {
                if (e.original && !side[e.to])
                    cut.emplace_back(u, e.to, e.origCap);
            }
        }
        return {flow, cut};
    }

private:
    int n_;
    vector<vector<Edge>> graph_;
};

int main() {
    MinCut g(6);
    int edges[][3] = {
        {0,1,16},{0,2,13},{1,2,4},{1,3,12},
        {2,1,10},{2,4,14},{3,2,9},{3,5,20},
        {4,3,7}, {4,5,4}
    };
    for (auto& e : edges) g.addEdge(e[0], e[1], e[2]);
    auto [flow, cut] = g.minCut(0, 5);
    cout << "Max flow / Min cut value: " << flow << "\n";
    cout << "Cut edges:\n";
    for (auto& [u, v, c] : cut)
        cout << "  (" << u << " -> " << v << ") capacity " << c << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - Uses struct Edge (a value type) for clarity; Java code used parallel
 *     int[] arrays for performance.
 *   - C++17 structured bindings (`auto [flow, cut]`) make multi-return clean.
 *   - We tag edges with `original` and `origCap` so the cut extractor can
 *     report the capacity of each cut edge after the flow run.
 */
