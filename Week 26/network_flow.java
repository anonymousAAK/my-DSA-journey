/*
 * Week 26: Network Flow & Matching
 * ==================================
 * Topics covered:
 *   1. Ford-Fulkerson (DFS augmenting paths)      - O(E * max_flow)
 *   2. Edmonds-Karp   (BFS augmenting paths)      - O(V * E^2)
 *   3. Hopcroft-Karp  (bipartite matching)         - O(E * sqrt(V))
 *   4. Hungarian Algorithm (min-cost assignment)   - O(N^3)
 */

import java.util.*;

public class network_flow {

    // -----------------------------------------------------------------------
    // Edge representation for flow networks (adjacency-list with edge arrays)
    // -----------------------------------------------------------------------
    static int[] edgeTo;
    static int[] edgeCap;
    static int[] edgeRev;
    static int edgeCount;
    static List<List<Integer>> flowAdj;

    static void initGraph(int n, int maxEdges) {
        flowAdj = new ArrayList<>();
        for (int i = 0; i < n; i++) flowAdj.add(new ArrayList<>());
        edgeTo  = new int[maxEdges];
        edgeCap = new int[maxEdges];
        edgeRev = new int[maxEdges];
        edgeCount = 0;
    }

    static void addEdge(int u, int v, int cap) {
        edgeTo[edgeCount] = v;  edgeCap[edgeCount] = cap; edgeRev[edgeCount] = edgeCount + 1;
        flowAdj.get(u).add(edgeCount++);
        edgeTo[edgeCount] = u;  edgeCap[edgeCount] = 0;  edgeRev[edgeCount] = edgeCount - 1;
        flowAdj.get(v).add(edgeCount++);
    }

    // -----------------------------------------------------------------------
    // 1. Ford-Fulkerson (DFS-based)
    //    Time:  O(E * max_flow)
    //    Space: O(V + E)
    // -----------------------------------------------------------------------
    static int ffDfs(int u, int t, int pushed, boolean[] visited) {
        if (u == t) return pushed;
        visited[u] = true;
        for (int eid : flowAdj.get(u)) {
            int v = edgeTo[eid];
            if (!visited[v] && edgeCap[eid] > 0) {
                int d = ffDfs(v, t, Math.min(pushed, edgeCap[eid]), visited);
                if (d > 0) {
                    edgeCap[eid] -= d;
                    edgeCap[edgeRev[eid]] += d;
                    return d;
                }
            }
        }
        return 0;
    }

    static int fordFulkerson(int s, int t, int n) {
        int flow = 0;
        while (true) {
            boolean[] visited = new boolean[n];
            int pushed = ffDfs(s, t, Integer.MAX_VALUE, visited);
            if (pushed == 0) break;
            flow += pushed;
        }
        return flow;
    }

    // -----------------------------------------------------------------------
    // 2. Edmonds-Karp (BFS-based)
    //    Time:  O(V * E^2)
    //    Space: O(V + E)
    // -----------------------------------------------------------------------
    static int edmondsKarp(int s, int t, int n) {
        int flow = 0;
        while (true) {
            int[] parent = new int[n];
            int[] parentEdge = new int[n];
            Arrays.fill(parent, -1);
            parent[s] = s;
            Queue<Integer> queue = new LinkedList<>();
            queue.add(s);

            while (!queue.isEmpty() && parent[t] == -1) {
                int u = queue.poll();
                for (int eid : flowAdj.get(u)) {
                    int v = edgeTo[eid];
                    if (parent[v] == -1 && edgeCap[eid] > 0) {
                        parent[v] = u;
                        parentEdge[v] = eid;
                        queue.add(v);
                    }
                }
            }
            if (parent[t] == -1) break;

            int bottleneck = Integer.MAX_VALUE;
            for (int v = t; v != s; v = parent[v])
                bottleneck = Math.min(bottleneck, edgeCap[parentEdge[v]]);
            for (int v = t; v != s; v = parent[v]) {
                edgeCap[parentEdge[v]] -= bottleneck;
                edgeCap[edgeRev[parentEdge[v]]] += bottleneck;
            }
            flow += bottleneck;
        }
        return flow;
    }

    // -----------------------------------------------------------------------
    // 3. Hopcroft-Karp Bipartite Matching
    //    Time:  O(E * sqrt(V))
    //    Space: O(V + E)
    // -----------------------------------------------------------------------
    static class HopcroftKarp {
        static final int NIL = -1;
        static final int INF = Integer.MAX_VALUE;

        int leftSize, rightSize;
        List<List<Integer>> adj;
        int[] matchLeft, matchRight, dist;

        HopcroftKarp(int leftSize, int rightSize) {
            this.leftSize = leftSize;
            this.rightSize = rightSize;
            adj = new ArrayList<>();
            for (int i = 0; i < leftSize; i++) adj.add(new ArrayList<>());
        }

        void addEdge(int u, int v) { adj.get(u).add(v); }

        boolean bfs() {
            Queue<Integer> queue = new LinkedList<>();
            for (int u = 0; u < leftSize; u++) {
                if (matchLeft[u] == NIL) { dist[u] = 0; queue.add(u); }
                else                     { dist[u] = INF; }
            }
            boolean found = false;
            while (!queue.isEmpty()) {
                int u = queue.poll();
                for (int v : adj.get(u)) {
                    int next = matchRight[v];
                    if (next == NIL) {
                        found = true;
                    } else if (dist[next] == INF) {
                        dist[next] = dist[u] + 1;
                        queue.add(next);
                    }
                }
            }
            return found;
        }

        boolean dfs(int u) {
            for (int v : adj.get(u)) {
                int next = matchRight[v];
                if (next == NIL || (dist[next] == dist[u] + 1 && dfs(next))) {
                    matchLeft[u] = v;
                    matchRight[v] = u;
                    return true;
                }
            }
            dist[u] = INF;
            return false;
        }

        int maxMatching() {
            matchLeft  = new int[leftSize];
            matchRight = new int[rightSize];
            dist = new int[leftSize];
            Arrays.fill(matchLeft, NIL);
            Arrays.fill(matchRight, NIL);
            int matching = 0;
            while (bfs()) {
                for (int u = 0; u < leftSize; u++) {
                    if (matchLeft[u] == NIL && dfs(u)) matching++;
                }
            }
            return matching;
        }
    }

    // -----------------------------------------------------------------------
    // 4. Hungarian Algorithm (Minimum-Cost Perfect Assignment)
    //    Time:  O(N^3)
    //    Space: O(N^2)
    // -----------------------------------------------------------------------
    static class Hungarian {
        int n;
        int[][] cost;

        Hungarian(int[][] cost) {
            this.n = cost.length;
            this.cost = cost;
        }

        /** Returns {minCost, assignment[0], assignment[1], ...} */
        int[] solve() {
            int INF = Integer.MAX_VALUE / 2;
            int[] u = new int[n + 1];
            int[] v = new int[n + 1];
            int[] p = new int[n + 1];   // p[j] = row assigned to column j
            int[] way = new int[n + 1];

            for (int i = 1; i <= n; i++) {
                p[0] = i;
                int j0 = 0;
                int[] minv = new int[n + 1];
                boolean[] used = new boolean[n + 1];
                Arrays.fill(minv, INF);

                do {
                    used[j0] = true;
                    int i0 = p[j0], delta = INF, j1 = -1;
                    for (int j = 1; j <= n; j++) {
                        if (!used[j]) {
                            int cur = cost[i0 - 1][j - 1] - u[i0] - v[j];
                            if (cur < minv[j]) { minv[j] = cur; way[j] = j0; }
                            if (minv[j] < delta) { delta = minv[j]; j1 = j; }
                        }
                    }
                    for (int j = 0; j <= n; j++) {
                        if (used[j]) { u[p[j]] += delta; v[j] -= delta; }
                        else         { minv[j] -= delta; }
                    }
                    j0 = j1;
                } while (p[j0] != 0);

                do {
                    int j1 = way[j0];
                    p[j0] = p[j1];
                    j0 = j1;
                } while (j0 != 0);
            }

            int[] assignment = new int[n];
            for (int j = 1; j <= n; j++) assignment[p[j] - 1] = j - 1;
            int totalCost = 0;
            for (int i = 0; i < n; i++) totalCost += cost[i][assignment[i]];

            int[] result = new int[n + 1];
            result[0] = totalCost;
            System.arraycopy(assignment, 0, result, 1, n);
            return result;
        }
    }

    // -----------------------------------------------------------------------
    // Demo / Driver
    // -----------------------------------------------------------------------
    public static void main(String[] args) {
        System.out.println("=".repeat(60));
        System.out.println("Week 26: Network Flow & Matching");
        System.out.println("=".repeat(60));

        // --- Edmonds-Karp ---
        System.out.println("\n--- Edmonds-Karp Max Flow ---");
        initGraph(6, 30);
        addEdge(0, 1, 16); addEdge(0, 2, 13);
        addEdge(1, 2, 4);  addEdge(1, 3, 12);
        addEdge(2, 1, 10); addEdge(2, 4, 14);
        addEdge(3, 2, 9);  addEdge(3, 5, 20);
        addEdge(4, 3, 7);  addEdge(4, 5, 4);
        System.out.println("Max flow (0 -> 5): " + edmondsKarp(0, 5, 6)); // 23

        // --- Ford-Fulkerson ---
        System.out.println("\n--- Ford-Fulkerson Max Flow ---");
        initGraph(6, 30);
        addEdge(0, 1, 16); addEdge(0, 2, 13);
        addEdge(1, 2, 4);  addEdge(1, 3, 12);
        addEdge(2, 1, 10); addEdge(2, 4, 14);
        addEdge(3, 2, 9);  addEdge(3, 5, 20);
        addEdge(4, 3, 7);  addEdge(4, 5, 4);
        System.out.println("Max flow (0 -> 5): " + fordFulkerson(0, 5, 6)); // 23

        // --- Hopcroft-Karp ---
        System.out.println("\n--- Hopcroft-Karp Bipartite Matching ---");
        HopcroftKarp hk = new HopcroftKarp(4, 4);
        hk.addEdge(0, 0); hk.addEdge(0, 1);
        hk.addEdge(1, 0); hk.addEdge(1, 2);
        hk.addEdge(2, 1); hk.addEdge(2, 3);
        hk.addEdge(3, 2); hk.addEdge(3, 3);
        System.out.println("Maximum matching size: " + hk.maxMatching()); // 4
        System.out.print("Matched pairs:");
        for (int u = 0; u < 4; u++) {
            if (hk.matchLeft[u] != HopcroftKarp.NIL)
                System.out.print(" (" + u + "," + hk.matchLeft[u] + ")");
        }
        System.out.println();

        // --- Hungarian ---
        System.out.println("\n--- Hungarian Algorithm (Min-Cost Assignment) ---");
        int[][] costMatrix = {
            {9, 2, 7, 8},
            {6, 4, 3, 7},
            {5, 8, 1, 8},
            {7, 6, 9, 4}
        };
        Hungarian h = new Hungarian(costMatrix);
        int[] result = h.solve();
        System.out.println("Minimum cost: " + result[0]); // 13
        System.out.print("Assignment (row -> col):");
        for (int i = 1; i <= 4; i++) System.out.print(" " + result[i]);
        System.out.println();
    }
}
