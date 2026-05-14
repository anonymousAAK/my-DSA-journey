/*
 * WEEK 26 - C++ ADVANCED TOPICS
 * Topic: Bipartite Matching (Hopcroft-Karp + Kuhn)
 * File: bipartite_matching.cpp
 *
 * CONCEPT:
 *   Maximum bipartite matching: largest set of edges with no shared
 *   endpoints in a bipartite graph (L u R, E). Hopcroft-Karp builds a
 *   layered BFS graph and finds vertex-disjoint shortest augmenting paths
 *   per phase, achieving O(E*sqrt(V)). Kuhn's algorithm is a simpler
 *   O(V*E) DFS-based matcher useful when graphs are small.
 *
 * KEY POINTS:
 *   - Augmenting path: starts/ends at unmatched vertices and alternates
 *     unmatched/matched edges.
 *   - Hopcroft-Karp: BFS layers + DFS along level graph; phases = O(sqrt V).
 *   - Kuhn: DFS from each unmatched left vertex, attempt to augment.
 *
 * ALGORITHM / APPROACH (Hopcroft-Karp):
 *   while BFS finds at least one augmenting path of length d:
 *       for each free left vertex u:
 *           DFS(u) augments along level graph
 *
 * C++-SPECIFIC NOTES:
 *   - Use INT_MAX as INF for distance.
 *   - Sentinel NIL = -1 for unmatched vertices.
 *   - vector<vector<int>> adjacency for left -> right edges.
 *
 * DRY RUN / EXAMPLE:
 *   L=R={0,1,2,3}, edges (0-0,0-1,1-0,1-2,2-1,2-3,3-2,3-3) -> matching=4.
 *
 * COMPLEXITY:
 *   Hopcroft-Karp: O(E*sqrt(V))
 *   Kuhn:           O(V*E)
 */

#include <iostream>
#include <vector>
#include <queue>
#include <climits>
#include <algorithm>

using namespace std;

class HopcroftKarp {
public:
    static constexpr int NIL = -1;
    static constexpr int INF = INT_MAX;

    HopcroftKarp(int L, int R) : L_(L), R_(R), adj_(L) {}

    void addEdge(int u, int v) { adj_[u].push_back(v); }

    int maxMatching() {
        matchL_.assign(L_, NIL);
        matchR_.assign(R_, NIL);
        dist_.assign(L_, INF);
        int matching = 0;
        while (bfs()) {
            for (int u = 0; u < L_; ++u)
                if (matchL_[u] == NIL && dfs(u)) ++matching;
        }
        return matching;
    }

    const vector<int>& matchL() const { return matchL_; }

private:
    int L_, R_;
    vector<vector<int>> adj_;
    vector<int> matchL_, matchR_, dist_;

    bool bfs() {
        queue<int> q;
        for (int u = 0; u < L_; ++u) {
            if (matchL_[u] == NIL) { dist_[u] = 0; q.push(u); }
            else dist_[u] = INF;
        }
        bool found = false;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj_[u]) {
                int p = matchR_[v];
                if (p == NIL) found = true;
                else if (dist_[p] == INF) {
                    dist_[p] = dist_[u] + 1;
                    q.push(p);
                }
            }
        }
        return found;
    }

    bool dfs(int u) {
        for (int v : adj_[u]) {
            int p = matchR_[v];
            if (p == NIL || (dist_[p] == dist_[u] + 1 && dfs(p))) {
                matchL_[u] = v;
                matchR_[v] = u;
                return true;
            }
        }
        dist_[u] = INF;
        return false;
    }
};

// Simpler Kuhn's algorithm
class Kuhn {
public:
    Kuhn(int L, int R) : L_(L), R_(R), adj_(L), matchR_(R, -1) {}
    void addEdge(int u, int v) { adj_[u].push_back(v); }

    int maxMatching() {
        int pairs = 0;
        for (int u = 0; u < L_; ++u) {
            vector<bool> used(R_, false);
            if (tryKuhn(u, used)) ++pairs;
        }
        return pairs;
    }

private:
    int L_, R_;
    vector<vector<int>> adj_;
    vector<int> matchR_;

    bool tryKuhn(int u, vector<bool>& used) {
        for (int v : adj_[u]) {
            if (used[v]) continue;
            used[v] = true;
            if (matchR_[v] == -1 || tryKuhn(matchR_[v], used)) {
                matchR_[v] = u;
                return true;
            }
        }
        return false;
    }
};

int main() {
    HopcroftKarp hk(4, 4);
    int edges[][2] = {{0,0},{0,1},{1,0},{1,2},{2,1},{2,3},{3,2},{3,3}};
    for (auto& e : edges) hk.addEdge(e[0], e[1]);
    cout << "Hopcroft-Karp matching: " << hk.maxMatching() << "\n";
    cout << "Pairs:";
    for (int u = 0; u < 4; ++u)
        if (hk.matchL()[u] != HopcroftKarp::NIL)
            cout << " (" << u << "," << hk.matchL()[u] << ")";
    cout << "\n";

    Kuhn k(4, 4);
    for (auto& e : edges) k.addEdge(e[0], e[1]);
    cout << "Kuhn matching:          " << k.maxMatching() << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - C++ static constexpr replaces Java's `static final`.
 *   - Both Hopcroft-Karp and Kuhn live in the same translation unit so the
 *     reader can compare the simpler (Kuhn) and faster (HK) variants.
 */
