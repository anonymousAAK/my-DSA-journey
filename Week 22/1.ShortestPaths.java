/*
 * WEEK 22 - ADVANCED GRAPH ALGORITHMS
 * Topic: Shortest Path Algorithms
 *
 * =========================================
 * DIJKSTRA'S ALGORITHM
 * =========================================
 * Single-source shortest path for graphs with NON-NEGATIVE edge weights.
 *
 * ALGORITHM:
 * - Use a min-heap (priority queue) to always process the nearest unvisited vertex.
 * - Relax edges: if dist[u] + w(u,v) < dist[v], update dist[v].
 *
 * Time: O((V + E) log V) with binary heap
 * Space: O(V + E)
 * Limitation: FAILS with negative-weight edges.
 *
 * =========================================
 * BELLMAN-FORD ALGORITHM
 * =========================================
 * Single-source shortest path. Works with NEGATIVE edge weights.
 * Detects NEGATIVE WEIGHT CYCLES.
 *
 * ALGORITHM:
 * - Relax ALL edges (V-1) times. After (V-1) iterations, distances are optimal.
 * - If any edge can still be relaxed, there's a negative weight cycle.
 *
 * Time: O(V * E)
 * Space: O(V)
 *
 * =========================================
 * FLOYD-WARSHALL
 * =========================================
 * ALL-PAIRS shortest paths. Dynamic programming.
 * dp[k][i][j] = shortest path from i to j using only vertices {0..k} as intermediates.
 * Recurrence: dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])
 *
 * Time: O(V³)
 * Space: O(V²)
 * Also detects negative cycles: if dp[i][i] < 0, negative cycle exists.
 */

import java.util.*;

public class ShortestPaths {

    static final int INF = Integer.MAX_VALUE / 2;

    // =====================
    // DIJKSTRA
    // =====================
    static int[] dijkstra(List<int[]>[] adj, int src, int V) {
        int[] dist = new int[V];
        Arrays.fill(dist, INF);
        dist[src] = 0;
        // Min-heap: [distance, vertex]
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
        pq.offer(new int[]{0, src});

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int d = curr[0], u = curr[1];
            if (d > dist[u]) continue; // outdated entry
            for (int[] edge : adj[u]) {
                int v = edge[0], w = edge[1];
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    pq.offer(new int[]{dist[v], v});
                }
            }
        }
        return dist;
    }

    // =====================
    // BELLMAN-FORD
    // =====================
    static int[] bellmanFord(int V, int[][] edges, int src) {
        int[] dist = new int[V];
        Arrays.fill(dist, INF);
        dist[src] = 0;

        // Relax all edges V-1 times
        for (int i = 0; i < V - 1; i++) {
            for (int[] e : edges) { // e = {from, to, weight}
                int u = e[0], v = e[1], w = e[2];
                if (dist[u] != INF && dist[u] + w < dist[v]) dist[v] = dist[u] + w;
            }
        }

        // Check for negative weight cycles
        for (int[] e : edges) {
            int u = e[0], v = e[1], w = e[2];
            if (dist[u] != INF && dist[u] + w < dist[v]) {
                System.out.println("Negative weight cycle detected!");
                return null;
            }
        }
        return dist;
    }

    // =====================
    // FLOYD-WARSHALL
    // =====================
    static int[][] floydWarshall(int V, int[][] graph) {
        int[][] dist = new int[V][V];
        for (int[] row : dist) Arrays.fill(row, INF);
        for (int i = 0; i < V; i++) dist[i][i] = 0;
        for (int[] e : graph) dist[e[0]][e[1]] = Math.min(dist[e[0]][e[1]], e[2]);

        for (int k = 0; k < V; k++)
            for (int i = 0; i < V; i++)
                for (int j = 0; j < V; j++)
                    if (dist[i][k] != INF && dist[k][j] != INF)
                        dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);

        // Detect negative cycles (any dist[i][i] < 0)
        for (int i = 0; i < V; i++) if (dist[i][i] < 0) { System.out.println("Negative cycle!"); return null; }
        return dist;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        // Dijkstra example
        System.out.println("=== Dijkstra ===");
        int V = 5;
        List<int[]>[] adj = new ArrayList[V];
        for (int i = 0; i < V; i++) adj[i] = new ArrayList<>();
        // Edges: [from, to, weight]
        int[][] edges = {{0,1,4},{0,2,1},{2,1,2},{1,3,1},{2,3,5},{3,4,3}};
        for (int[] e : edges) {
            adj[e[0]].add(new int[]{e[1], e[2]});
            adj[e[1]].add(new int[]{e[0], e[2]}); // undirected
        }
        int[] dist = dijkstra(adj, 0, V);
        System.out.println("Shortest distances from 0: " + Arrays.toString(dist));
        // Expected: [0, 3, 1, 4, 7]

        // Bellman-Ford (handles directed graphs with negative weights)
        System.out.println("\n=== Bellman-Ford ===");
        int[][] bfEdges = {{0,1,-1},{0,2,4},{1,2,3},{1,3,2},{1,4,2},{3,2,5},{3,1,1},{4,3,-3}};
        int[] bfDist = bellmanFord(5, bfEdges, 0);
        System.out.println("Shortest distances from 0: " + Arrays.toString(bfDist));
        // Expected: [0, -1, 2, -2, 1]

        // Floyd-Warshall (all-pairs)
        System.out.println("\n=== Floyd-Warshall ===");
        int[][] fwEdges = {{0,1,3},{0,3,7},{1,0,8},{1,2,2},{2,0,5},{2,3,1},{3,0,2}};
        int[][] allPairs = floydWarshall(4, fwEdges);
        System.out.println("All-pairs shortest paths:");
        for (int[] row : allPairs) {
            for (int d : row) System.out.printf("%4s", (d == INF ? "INF" : d));
            System.out.println();
        }
    }
}
