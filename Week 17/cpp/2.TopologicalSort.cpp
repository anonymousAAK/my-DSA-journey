/*
 * WEEK 17 - C++ DSA
 * Topic: Topological Sort (DFS + Kahn's BFS)
 * File: 2.TopologicalSort.cpp
 *
 * CONCEPT:
 *     A topological order of a DAG places every edge u -> v with u before v.
 *     Two algorithms; both O(V + E):
 *         DFS  - push vertex AFTER recursing on its successors (post-order).
 *         Kahn - repeatedly emit nodes with indegree 0.
 *     Kahn detects cycles (if result.size() < V some nodes were never freed).
 *
 * KEY POINTS:
 *     - Multiple valid topological orders may exist for the same DAG.
 *     - DFS variant uses an explicit stack of finished vertices.
 *     - Three-colour DFS (white/grey/black) detects cycles in directed graphs.
 *
 * ALGORITHM / APPROACH:
 *     Kahn:
 *         compute indegree[v] for all v
 *         queue <- {v : indegree[v]==0}
 *         while queue not empty:
 *             u = dequeue; result.push_back(u)
 *             for v in adj[u]:
 *                 if --indegree[v] == 0: queue.push(v)
 *         if result.size() != V -> cycle
 *
 * C++-SPECIFIC NOTES:
 *     - std::queue<int> for the FIFO; pop() returns void so call front() then pop().
 *     - Returning std::optional<std::vector<int>> mirrors Java's null sentinel.
 *     - Lambdas with std::function for recursive DFS.
 *
 * DRY RUN:
 *     Edges 5->2, 5->0, 4->0, 4->1, 2->3, 3->1
 *         indeg = {0:2, 1:2, 2:1, 3:1, 4:0, 5:0}
 *         queue = [4,5] -> emit 4 -> indeg{0:1,1:1}
 *                       -> emit 5 -> indeg{0:0,2:0} push 0,2
 *                       -> emit 0
 *                       -> emit 2 -> indeg{3:0} push 3
 *                       -> emit 3 -> indeg{1:0} push 1
 *                       -> emit 1
 *         result length 6 == V -> [4,5,0,2,3,1]
 *
 *     Cyclic 0->1->2->3->1: indeg{0:0,1:2,2:1,3:1}
 *         queue=[0]; emit 0 -> indeg{1:1}; queue empty.
 *         result.size()==1 < 4 -> cycle.
 *
 * COMPLEXITY: O(V + E) time, O(V) extra space.
 */

#include <iostream>
#include <vector>
#include <queue>
#include <optional>
#include <functional>

class DiGraph {
public:
    int V;
    std::vector<std::vector<int>> adj;
    explicit DiGraph(int v) : V(v), adj(v) {}
    void addEdge(int u, int v) { adj[u].push_back(v); }

    // APPROACH 1: DFS post-order
    std::vector<int> topoSortDFS() const {
        std::vector<bool> visited(V, false);
        std::vector<int> stack;                   // we'll reverse at the end
        std::function<void(int)> dfs = [&](int u) {
            visited[u] = true;
            for (int v : adj[u]) if (!visited[v]) dfs(v);
            stack.push_back(u);
        };
        for (int i = 0; i < V; ++i) if (!visited[i]) dfs(i);
        std::reverse(stack.begin(), stack.end());
        return stack;
    }

    // APPROACH 2: Kahn (BFS / indegree)
    std::optional<std::vector<int>> topoSortKahn() const {
        std::vector<int> indeg(V, 0);
        for (int u = 0; u < V; ++u)
            for (int v : adj[u]) ++indeg[v];

        std::queue<int> q;
        for (int i = 0; i < V; ++i) if (indeg[i] == 0) q.push(i);

        std::vector<int> result;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            result.push_back(u);
            for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
        }
        if ((int)result.size() != V) return std::nullopt;   // cycle
        return result;
    }

    // 3-colour cycle detection
    bool hasCycle() const {
        enum { WHITE = 0, GREY = 1, BLACK = 2 };
        std::vector<int> state(V, WHITE);
        std::function<bool(int)> dfs = [&](int u) -> bool {
            state[u] = GREY;
            for (int v : adj[u]) {
                if (state[v] == GREY) return true;
                if (state[v] == WHITE && dfs(v)) return true;
            }
            state[u] = BLACK;
            return false;
        };
        for (int i = 0; i < V; ++i)
            if (state[i] == WHITE && dfs(i)) return true;
        return false;
    }
};

template <typename T>
void printVec(const std::vector<T>& v) {
    std::cout << "[";
    for (size_t i = 0; i < v.size(); ++i) std::cout << v[i] << (i+1<v.size()?",":"");
    std::cout << "]";
}

int main() {
    DiGraph g(6);
    int edges[][2] = {{5,2},{5,0},{4,0},{4,1},{2,3},{3,1}};
    for (auto& e : edges) g.addEdge(e[0], e[1]);

    std::cout << "DFS topological sort: "; printVec(g.topoSortDFS()); std::cout << "\n";
    auto kahn = g.topoSortKahn();
    std::cout << "Kahn topological sort: ";
    if (kahn) printVec(*kahn); else std::cout << "<cycle>";
    std::cout << "\n";
    std::cout << std::boolalpha << "Has cycle: " << g.hasCycle() << "\n";

    DiGraph cyc(4);
    cyc.addEdge(0,1); cyc.addEdge(1,2); cyc.addEdge(2,3); cyc.addEdge(3,1);
    std::cout << "\nCyclic graph:\n";
    std::cout << "Has cycle: " << cyc.hasCycle() << "\n";
    auto k2 = cyc.topoSortKahn();
    std::cout << "Kahn (cycle => nullopt): "
              << (k2 ? "[returned]" : "nullopt") << "\n";

    std::cout << "\n=== Build System ===\n";
    DiGraph build(5); // 0=download,1=compile,2=test,3=package,4=deploy
    build.addEdge(0,1); build.addEdge(1,2); build.addEdge(1,3);
    build.addEdge(2,3); build.addEdge(3,4);
    auto bk = build.topoSortKahn();
    std::cout << "Build order: "; if (bk) printVec(*bk); std::cout << "\n";
}

/*
 * NOTES (C++ vs Java):
 *   - Java's `null` sentinel becomes std::nullopt with std::optional<T> for
 *     a clearer compile-time signal that the call may fail.
 *   - The DFS variant uses std::vector and a final reverse — slightly more
 *     cache-friendly than pushing into a std::stack and re-extracting.
 *   - Three-colour DFS uses a small enum; Java does the same with int constants.
 *   - Kahn requires only one pass over edges to build indegrees, then one
 *     pass over edges total inside the BFS — overall O(V+E).
 */
