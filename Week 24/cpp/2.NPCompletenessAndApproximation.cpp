/*
 * WEEK 24 - C++ ADVANCED DSA
 * Topic: NP-Completeness & Approximation Algorithms
 * File: 2.NPCompletenessAndApproximation.cpp
 *
 * CONCEPT:
 *   P: solvable in poly time. NP: verifiable in poly time. NP-Complete:
 *   in NP and every NP problem reduces to it. For NP-Complete optimization
 *   problems, approximation algorithms guarantee a bounded ratio vs OPT:
 *     - Vertex Cover: 2-approximation via maximal matching.
 *     - Set Cover:    O(log n) greedy.
 *     - Metric TSP:   2-approximation via MST + DFS preorder.
 *
 * KEY POINTS:
 *   - Vertex cover: take BOTH endpoints of any uncovered edge.
 *   - Set cover greedy: pick the set covering most uncovered elements.
 *   - Triangle inequality enables MST-based TSP shortcutting.
 *
 * ALGORITHM / APPROACH:
 *   See file headers in Java reference; identical control flow.
 *
 * C++-SPECIFIC NOTES vs JAVA:
 *   - std::set<int> for chosen vertices, std::unordered_set<int> would
 *     also work for O(1) lookups when sets are large.
 *   - Use std::stack<int> for iterative DFS preorder.
 *
 * DRY RUN:
 *   Vertex cover graph: edges {(0,1),(0,2),(1,3),(2,3),(3,4)}.
 *     Cover {0,1,2,3} (size 4); OPT {0,3} (size 2); ratio 2.
 *
 * COMPLEXITY:
 *   Vertex cover: O(E). Set cover: ~ O(|sets| * |U|) per iteration.
 *   TSP 2-approx: O(V^2) Prim + O(V) DFS.
 */

#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <set>
#include <stack>
#include <climits>

std::set<int> vertex_cover_2approx(int V, const std::vector<std::pair<int,int>>& edges) {
    std::vector<bool> covered(V, false);
    std::set<int> cover;
    for (auto [u, v] : edges) {
        if (!covered[u] && !covered[v]) {
            covered[u] = covered[v] = true;
            cover.insert(u); cover.insert(v);
        }
    }
    return cover;
}

std::vector<int> setcover_greedy(int universe_size, const std::vector<std::unordered_set<int>>& sets) {
    std::unordered_set<int> uncovered;
    for (int i = 0; i < universe_size; ++i) uncovered.insert(i);
    std::vector<int> chosen;
    while (!uncovered.empty()) {
        int best = -1, bestCnt = 0;
        for (int i = 0; i < (int)sets.size(); ++i) {
            int cnt = 0;
            for (int x : sets[i]) if (uncovered.count(x)) cnt++;
            if (cnt > bestCnt) { bestCnt = cnt; best = i; }
        }
        if (best == -1) break;
        chosen.push_back(best);
        for (int x : sets[best]) uncovered.erase(x);
    }
    return chosen;
}

std::vector<int> tsp_2approx(const std::vector<std::vector<int>>& dist) {
    int n = dist.size();
    std::vector<bool> inMST(n, false);
    std::vector<int> parent(n, -1), key(n, INT_MAX);
    key[0] = 0;
    for (int i = 0; i < n - 1; ++i) {
        int u = -1;
        for (int v = 0; v < n; ++v) if (!inMST[v] && (u == -1 || key[v] < key[u])) u = v;
        inMST[u] = true;
        for (int v = 0; v < n; ++v)
            if (!inMST[v] && dist[u][v] < key[v]) { key[v] = dist[u][v]; parent[v] = u; }
    }
    std::vector<std::vector<int>> mst(n);
    for (int i = 1; i < n; ++i) {
        mst[parent[i]].push_back(i);
        mst[i].push_back(parent[i]);
    }
    std::vector<bool> visited(n, false);
    std::vector<int> tour;
    std::stack<int> st;
    st.push(0);
    while (!st.empty()) {
        int u = st.top(); st.pop();
        if (visited[u]) continue;
        visited[u] = true;
        tour.push_back(u);
        for (int i = (int)mst[u].size() - 1; i >= 0; --i)
            if (!visited[mst[u][i]]) st.push(mst[u][i]);
    }
    int cost = 0;
    for (int i = 0; i < n; ++i) cost += dist[tour[i]][tour[(i + 1) % n]];
    std::cout << "TSP 2-Approx tour: [";
    for (int i = 0; i < n; ++i) std::cout << tour[i] << (i + 1 < n ? "," : "");
    std::cout << "], cost: " << cost << "\n";
    return tour;
}

int main() {
    std::cout << "=== Vertex Cover (2-approximation) ===\n";
    std::vector<std::pair<int,int>> edges = {{0,1},{0,2},{1,3},{2,3},{3,4}};
    auto cover = vertex_cover_2approx(5, edges);
    std::cout << "2-approx vertex cover: {";
    bool first = true;
    for (int v : cover) { if (!first) std::cout << ","; std::cout << v; first = false; }
    std::cout << "}\n";
    std::cout << "Cover size: " << cover.size() << "\n";

    std::cout << "\n=== Set Cover (greedy) ===\n";
    std::vector<std::unordered_set<int>> sets = {
        {0,1,2}, {3,4,5}, {4,5,6,7}, {0,3,8}, {2,7,9}
    };
    auto chosen = setcover_greedy(10, sets);
    std::cout << "Chosen set indices: [";
    for (size_t i = 0; i < chosen.size(); ++i) std::cout << chosen[i] << (i + 1 < chosen.size() ? "," : "");
    std::cout << "]\n";

    std::cout << "\n=== TSP 2-Approximation (metric) ===\n";
    std::vector<std::vector<int>> dist = {
        {0,10,15,20},{10,0,35,25},{15,35,0,30},{20,25,30,0}
    };
    tsp_2approx(dist);
    std::cout << "(Optimal tour cost for this instance: 80)\n";

    std::cout << "\n=== P vs NP Key Points ===\n";
    std::cout << "- P: problems solvable in poly time (sorting, shortest path, MST)\n";
    std::cout << "- NP: problems verifiable in poly time (TSP, vertex cover, 3-SAT)\n";
    std::cout << "- NP-Hard: at least as hard as NP-Complete problems\n";
    std::cout << "- If P=NP, all encryption would break (RSA, AES rely on hard problems)\n";
    std::cout << "- Most believe P!=NP (Clay Millennium Prize: $1M for proof)\n";
    std::cout << "- Approximation algorithms: practical solutions with quality guarantees\n";
    return 0;
}
