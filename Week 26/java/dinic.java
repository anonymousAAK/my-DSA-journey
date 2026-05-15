/*
 * WEEK 26 - JAVA ADVANCED TOPICS
 * Topic: Dinic's Maximum Flow
 * File: dinic.java
 *
 * CONCEPT:
 *     Dinic's algorithm improves on Edmonds-Karp by exploiting the *level
 *     graph*: a BFS from source assigns each vertex a level equal to its
 *     shortest-path distance in the residual graph; then a *blocking flow*
 *     is sent only along edges that step from level i to level i+1. Each
 *     phase increases the minimum s-t distance by at least one, so there
 *     are O(V) phases. With an `it[]` pointer that skips dead edges, each
 *     phase runs in O(V*E), giving O(V^2 * E) overall -- and O(E*sqrt(V))
 *     on unit-capacity / bipartite graphs.
 *
 * KEY POINTS:
 *     - Two-pass per phase: BFS to build levels, DFS to send blocking flow.
 *     - `it[u]` is the per-vertex pointer that lets us avoid re-visiting
 *       dead edges within a single phase.
 *     - Massively faster than Edmonds-Karp on dense graphs in practice.
 *
 * ALGORITHM / APPROACH:
 *     while BFS-level-graph(s) reaches t:
 *         reset it[]
 *         repeat:
 *             pushed <- DFS-blocking(s, +INF)
 *             if pushed == 0: break
 *             flow += pushed
 *     return flow
 *
 * DRY RUN / EXAMPLE:
 *     Same CLRS graph (max flow 23). Dinic typically finishes in 2-3 phases:
 *         Phase 1: levels {0:0, 1:1, 2:1, 3:2, 4:2, 5:3}
 *                  Blocking flow pushes 0-1-3-5 (12) and 0-2-4-5 (4) -> 16.
 *         Phase 2: BFS uses reverse edge 4->3 to reach 5 in 4 steps.
 *                  Blocking flow pushes 0-2-4-3-5 (7) -> 23.
 *         Phase 3: BFS no longer reaches sink -> done.
 *
 * COMPLEXITY:
 *     Time:  O(V^2 * E) general; O(E * sqrt(V)) on unit-capacity graphs.
 *     Space: O(V + E).
 */

// snake_case filename is fine because class Dinic is package-private.

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;

class Dinic {

    static class Edge {
        int to, cap, rev;
        Edge(int to, int cap, int rev) { this.to = to; this.cap = cap; this.rev = rev; }
    }

    private final int n;
    private final List<List<Edge>> graph;
    private int[] level;
    private int[] it;

    Dinic(int n) {
        this.n = n;
        this.graph = new ArrayList<>();
        for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    }

    void addEdge(int u, int v, int cap) {
        graph.get(u).add(new Edge(v, cap, graph.get(v).size()));
        graph.get(v).add(new Edge(u, 0, graph.get(u).size() - 1));
    }

    private boolean bfs(int s, int t) {
        level = new int[n];
        Arrays.fill(level, -1);
        level[s] = 0;
        Deque<Integer> queue = new ArrayDeque<>();
        queue.offer(s);
        while (!queue.isEmpty()) {
            int u = queue.poll();
            for (Edge e : graph.get(u)) {
                if (e.cap > 0 && level[e.to] < 0) {
                    level[e.to] = level[u] + 1;
                    queue.offer(e.to);
                }
            }
        }
        return level[t] >= 0;
    }

    private int dfs(int u, int t, int pushed) {
        if (u == t) return pushed;
        List<Edge> adj = graph.get(u);
        for (; it[u] < adj.size(); it[u]++) {
            Edge e = adj.get(it[u]);
            if (e.cap > 0 && level[e.to] == level[u] + 1) {
                int d = dfs(e.to, t, Math.min(pushed, e.cap));
                if (d > 0) {
                    e.cap -= d;
                    graph.get(e.to).get(e.rev).cap += d;
                    return d;
                }
            }
        }
        return 0;
    }

    int maxFlow(int s, int t) {
        int flow = 0;
        while (bfs(s, t)) {
            it = new int[n];
            while (true) {
                int pushed = dfs(s, t, Integer.MAX_VALUE);
                if (pushed == 0) break;
                flow += pushed;
            }
        }
        return flow;
    }

    public static void main(String[] args) {
        Dinic g = new Dinic(6);
        int[][] edges = {
            {0, 1, 16}, {0, 2, 13},
            {1, 2, 4},  {1, 3, 12},
            {2, 1, 10}, {2, 4, 14},
            {3, 2, 9},  {3, 5, 20},
            {4, 3, 7},  {4, 5, 4}
        };
        for (int[] e : edges) g.addEdge(e[0], e[1], e[2]);
        System.out.println("Dinic max flow (0 -> 5): " + g.maxFlow(0, 5)); // 23
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in dinic.py:
 *   - it[] is a plain int[] in Java (Python uses a list of ints).
 *   - Java uses Integer.MAX_VALUE in place of float('inf'); flow is integral.
 *   - The Edge class makes the in-place mutation explicit.
 */
