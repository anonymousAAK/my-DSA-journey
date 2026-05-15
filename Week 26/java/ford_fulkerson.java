/*
 * WEEK 26 - JAVA ADVANCED TOPICS
 * Topic: Ford-Fulkerson Maximum Flow
 * File: ford_fulkerson.java
 *
 * CONCEPT:
 *     The Ford-Fulkerson method is a greedy algorithm framework for computing
 *     the maximum flow in a flow network. It repeatedly finds an augmenting
 *     path from source s to sink t in the residual graph and pushes the
 *     bottleneck capacity along it. The DFS-based variant below augments
 *     along any discovered s->t path with positive residual capacity.
 *
 * KEY POINTS:
 *     - Models capacity-constrained networks (pipelines, bandwidth, supply
 *       chains).
 *     - Uses a residual graph with reverse edges of capacity 0; pushing flow
 *       along edge (u,v) decreases its residual cap and increases (v,u)'s.
 *     - Augmenting path: any s->t path with strictly positive residual
 *       capacity.
 *     - Bottleneck: minimum residual capacity along the chosen path.
 *     - Terminates when no augmenting path exists (max-flow / min-cut theorem).
 *     - With DFS, complexity is O(E * max_flow); pathological orderings can
 *       blow up on irrational capacities.
 *
 * ALGORITHM / APPROACH:
 *     initialise residual graph (forward + zero-cap reverse edges)
 *     flow <- 0
 *     repeat:
 *         pushed <- DFS(s, t, +INF)        // try to push max along any path
 *         if pushed == 0: break            // no augmenting path
 *         flow += pushed
 *     return flow
 *
 * DRY RUN / EXAMPLE:
 *     Classic CLRS graph with 6 nodes, source=0, sink=5:
 *         0->1 cap 16, 0->2 cap 13, 1->2 cap 4,  1->3 cap 12,
 *         2->1 cap 10, 2->4 cap 14, 3->2 cap 9,  3->5 cap 20,
 *         4->3 cap 7,  4->5 cap 4
 *     One DFS trace:
 *         Path 0-1-3-5    bottleneck 12 -> flow=12
 *         Path 0-2-4-5    bottleneck  4 -> flow=16
 *         Path 0-2-4-3-5  bottleneck  7 -> flow=23
 *         No more augmenting paths. Max flow = 23.
 *
 * COMPLEXITY:
 *     Time:  O(E * F) where F is the maximum flow value.
 *     Space: O(V + E) for the residual graph and DFS stack.
 */

// NOTE: snake_case filename is fine because the public class rule only
// applies to PUBLIC top-level classes. Our class FordFulkerson is
// package-private so the file may be named ford_fulkerson.java.

import java.util.ArrayList;
import java.util.List;

class FordFulkerson {

    /** Edge in the residual graph: [to, residual capacity, reverse-edge index]. */
    static class Edge {
        int to;
        int cap;
        int rev;
        Edge(int to, int cap, int rev) { this.to = to; this.cap = cap; this.rev = rev; }
    }

    private final int n;
    private final List<List<Edge>> graph;

    FordFulkerson(int n) {
        this.n = n;
        this.graph = new ArrayList<>();
        for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    }

    /** Add a directed edge u -> v with capacity `cap`; reverse edge gets cap 0. */
    void addEdge(int u, int v, int cap) {
        graph.get(u).add(new Edge(v, cap, graph.get(v).size()));
        graph.get(v).add(new Edge(u, 0, graph.get(u).size() - 1));
    }

    private int dfs(int u, int t, int pushed, boolean[] visited) {
        if (u == t) return pushed;
        visited[u] = true;
        for (Edge e : graph.get(u)) {
            if (!visited[e.to] && e.cap > 0) {
                int d = dfs(e.to, t, Math.min(pushed, e.cap), visited);
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
        while (true) {
            boolean[] visited = new boolean[n];
            int pushed = dfs(s, t, Integer.MAX_VALUE, visited);
            if (pushed == 0) return flow;
            flow += pushed;
        }
    }

    public static void main(String[] args) {
        FordFulkerson g = new FordFulkerson(6);
        int[][] edges = {
            {0, 1, 16}, {0, 2, 13},
            {1, 2, 4},  {1, 3, 12},
            {2, 1, 10}, {2, 4, 14},
            {3, 2, 9},  {3, 5, 20},
            {4, 3, 7},  {4, 5, 4}
        };
        for (int[] e : edges) g.addEdge(e[0], e[1], e[2]);
        System.out.println("Ford-Fulkerson max flow (0 -> 5): " + g.maxFlow(0, 5)); // 23
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in ford_fulkerson.py:
 *   - Java uses an explicit `Edge` class instead of [to, cap, rev] lists;
 *     fields are mutable, mirroring Python's in-place list mutation.
 *   - Integer.MAX_VALUE plays the role of math.inf for the initial pushed.
 *   - DFS recursion depth can reach |V|; Java's default stack handles up to
 *     ~10000 nodes without tuning. The companion network_flow.java keeps a
 *     parallel-array form for higher performance.
 */
