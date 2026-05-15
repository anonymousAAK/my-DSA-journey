/*
 * WEEK 26 - JAVA ADVANCED TOPICS
 * Topic: Minimum s-t Cut via Max-Flow / Min-Cut Theorem
 * File: min_cut.java
 *
 * CONCEPT:
 *     Given a directed flow network with source s and sink t, an s-t cut is
 *     a partition (S, T) of the vertices with s in S and t in T. The cut's
 *     capacity is the sum of capacities of edges from S to T (forward only).
 *     The Max-Flow / Min-Cut theorem states:
 *
 *         max flow value = min cut capacity.
 *
 *     To extract the cut after running any max-flow algorithm, BFS the
 *     residual graph from s; vertices reachable form S, the rest form T.
 *     Cut edges are the *original* forward edges (u,v) with u in S and v in
 *     T whose residual is now zero (saturated).
 *
 * KEY POINTS:
 *     - Works on top of any max-flow algorithm (we embed Edmonds-Karp).
 *     - Distinguish ORIGINAL edges from residual reverse edges; only
 *       originals count in the cut capacity.
 *     - Applications: image segmentation, project selection, bipartite
 *       vertex cover (Konig's theorem), reliability analysis.
 *
 * ALGORITHM / APPROACH:
 *     1. Run any max-flow algorithm. Residual now reflects flows.
 *     2. BFS from s in residual graph treating edges with cap > 0 as live.
 *        Mark reachable set S.
 *     3. For every original edge (u,v) with u in S and v not in S: it is a
 *        cut edge contributing its ORIGINAL capacity to the min-cut value.
 *
 * DRY RUN / EXAMPLE:
 *     Same CLRS graph (max flow 23). After saturation, BFS from 0 in
 *     residual reaches S = {0, 2, 4}. Cut edges (S -> T):
 *         (0,1) cap 16, (4,3) cap 7. Sum = 23 == max flow.
 *
 * COMPLEXITY:
 *     Same as the underlying max-flow algorithm + O(V+E) for cut extraction.
 */

// snake_case filename is fine because class MinCut is package-private.

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;

class MinCut {

    static class Edge {
        int to, cap, rev;
        boolean original;
        int originalCap;
        Edge(int to, int cap, int rev, boolean original, int originalCap) {
            this.to = to; this.cap = cap; this.rev = rev;
            this.original = original; this.originalCap = originalCap;
        }
    }

    static class CutEdge {
        final int u, v, capacity;
        CutEdge(int u, int v, int capacity) { this.u = u; this.v = v; this.capacity = capacity; }
        @Override public String toString() { return "(" + u + " -> " + v + ") cap " + capacity; }
    }

    private final int n;
    private final List<List<Edge>> graph;

    MinCut(int n) {
        this.n = n;
        this.graph = new ArrayList<>();
        for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    }

    void addEdge(int u, int v, int cap) {
        graph.get(u).add(new Edge(v, cap, graph.get(v).size(), true, cap));
        graph.get(v).add(new Edge(u, 0, graph.get(u).size() - 1, false, 0));
    }

    // --- Embedded Edmonds-Karp for self-containment ---
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

    /** BFS the residual graph from s; returns the membership of S side. */
    boolean[] reachableFromSource(int s) {
        boolean[] visited = new boolean[n];
        visited[s] = true;
        Deque<Integer> queue = new ArrayDeque<>();
        queue.offer(s);
        while (!queue.isEmpty()) {
            int u = queue.poll();
            for (Edge e : graph.get(u)) {
                if (e.cap > 0 && !visited[e.to]) {
                    visited[e.to] = true;
                    queue.offer(e.to);
                }
            }
        }
        return visited;
    }

    /** Returns total flow value and the explicit list of cut edges. */
    Object[] minCutEdges(int s, int t) {
        int flow = maxFlow(s, t);
        boolean[] side = reachableFromSource(s);
        List<CutEdge> cut = new ArrayList<>();
        for (int u = 0; u < n; u++) {
            if (!side[u]) continue;
            for (Edge e : graph.get(u)) {
                if (e.original && !side[e.to]) cut.add(new CutEdge(u, e.to, e.originalCap));
            }
        }
        return new Object[]{flow, cut};
    }

    public static void main(String[] args) {
        MinCut g = new MinCut(6);
        int[][] edges = {
            {0, 1, 16}, {0, 2, 13},
            {1, 2, 4},  {1, 3, 12},
            {2, 1, 10}, {2, 4, 14},
            {3, 2, 9},  {3, 5, 20},
            {4, 3, 7},  {4, 5, 4}
        };
        for (int[] e : edges) g.addEdge(e[0], e[1], e[2]);
        Object[] result = g.minCutEdges(0, 5);
        int flow = (int) result[0];
        @SuppressWarnings("unchecked")
        List<CutEdge> cut = (List<CutEdge>) result[1];
        System.out.println("Max flow / Min cut value: " + flow); // 23
        System.out.println("Cut edges (S -> T):");
        for (CutEdge ce : cut) System.out.println("  " + ce);
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in min_cut.py:
 *   - Java needs explicit Edge / CutEdge classes for tagged residual edges.
 *   - We return an Object[] {flow, List<CutEdge>} since Java lacks anonymous
 *     tuples; an alternative is a small record once on JDK 14+.
 *   - The original capacity is stored on the edge so we can still report it
 *     after the residual has been mutated by max-flow.
 */
