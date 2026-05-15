/*
 * WEEK 26 - JAVA ADVANCED TOPICS
 * Topic: Edmonds-Karp Maximum Flow
 * File: edmonds_karp.java
 *
 * CONCEPT:
 *     Edmonds-Karp is the BFS specialisation of Ford-Fulkerson. By always
 *     selecting the *shortest* augmenting path (in number of edges), it
 *     guarantees O(V * E^2) running time independent of edge capacities.
 *     The proof relies on the fact that the shortest s-t distance in the
 *     residual graph is non-decreasing across augmentations.
 *
 * KEY POINTS:
 *     - Same residual-graph representation as Ford-Fulkerson.
 *     - BFS replaces DFS so we always augment along a *fewest-edge* path.
 *     - Records parent[v] and parentEdge[v] to reconstruct the augmenting
 *       path.
 *     - Handles arbitrarily large integer capacities without performance loss.
 *     - Sensible default for max-flow on dense or capacity-skewed graphs.
 *
 * ALGORITHM / APPROACH:
 *     while BFS(s) reaches t with positive residual:
 *         compute bottleneck along the path
 *         update forward and reverse residuals
 *         flow += bottleneck
 *     return flow
 *
 * DRY RUN / EXAMPLE:
 *     Same CLRS graph (max flow 23). BFS picks shortest paths:
 *         Iter 1: 0-1-3-5    (len 3) bottleneck min(16,12,20)=12, flow=12
 *         Iter 2: 0-2-4-5    (len 3) bottleneck min(13,14, 4)= 4, flow=16
 *         Iter 3: 0-2-4-3-5  (len 4) bottleneck min( 9,10, 7, 8)=7, flow=23
 *         Iter 4: BFS finds no augmenting path -> done.
 *
 * COMPLEXITY:
 *     Time:  O(V * E^2) -- at most O(V*E) augmentations, each BFS is O(V+E).
 *     Space: O(V + E).
 */

// snake_case filename is fine; class EdmondsKarp is package-private.

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;

class EdmondsKarp {

    static class Edge {
        int to, cap, rev;
        Edge(int to, int cap, int rev) { this.to = to; this.cap = cap; this.rev = rev; }
    }

    private final int n;
    private final List<List<Edge>> graph;

    EdmondsKarp(int n) {
        this.n = n;
        this.graph = new ArrayList<>();
        for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    }

    void addEdge(int u, int v, int cap) {
        graph.get(u).add(new Edge(v, cap, graph.get(v).size()));
        graph.get(v).add(new Edge(u, 0, graph.get(u).size() - 1));
    }

    int maxFlow(int s, int t) {
        int flow = 0;
        while (true) {
            int[] parent = new int[n];
            int[] parentEdge = new int[n];
            Arrays.fill(parent, -1);
            parent[s] = s;
            Deque<Integer> queue = new ArrayDeque<>();
            queue.offer(s);
            while (!queue.isEmpty() && parent[t] == -1) {
                int u = queue.poll();
                List<Edge> adj = graph.get(u);
                for (int i = 0; i < adj.size(); i++) {
                    Edge e = adj.get(i);
                    if (parent[e.to] == -1 && e.cap > 0) {
                        parent[e.to] = u;
                        parentEdge[e.to] = i;
                        queue.offer(e.to);
                    }
                }
            }
            if (parent[t] == -1) return flow;

            int bottleneck = Integer.MAX_VALUE;
            for (int v = t; v != s; v = parent[v]) {
                Edge e = graph.get(parent[v]).get(parentEdge[v]);
                bottleneck = Math.min(bottleneck, e.cap);
            }
            for (int v = t; v != s; v = parent[v]) {
                Edge e = graph.get(parent[v]).get(parentEdge[v]);
                e.cap -= bottleneck;
                graph.get(e.to).get(e.rev).cap += bottleneck;
            }
            flow += bottleneck;
        }
    }

    public static void main(String[] args) {
        EdmondsKarp g = new EdmondsKarp(6);
        int[][] edges = {
            {0, 1, 16}, {0, 2, 13},
            {1, 2, 4},  {1, 3, 12},
            {2, 1, 10}, {2, 4, 14},
            {3, 2, 9},  {3, 5, 20},
            {4, 3, 7},  {4, 5, 4}
        };
        for (int[] e : edges) g.addEdge(e[0], e[1], e[2]);
        System.out.println("Edmonds-Karp max flow (0 -> 5): " + g.maxFlow(0, 5)); // 23
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in edmonds_karp.py:
 *   - Java tracks parent and parent-edge in two separate int[] arrays
 *     rather than a single tuple list.
 *   - ArrayDeque is the natural Java BFS queue (O(1) offer/poll).
 *   - Integer.MAX_VALUE replaces float('inf'); flows are always integral.
 */
