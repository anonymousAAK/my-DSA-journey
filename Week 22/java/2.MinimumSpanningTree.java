/*
 * WEEK 22 - ADVANCED GRAPH ALGORITHMS
 * Topic: Minimum Spanning Tree (Kruskal + Prim) & Union-Find
 *
 * MINIMUM SPANNING TREE (MST):
 * A spanning tree of an undirected weighted graph with minimum total edge weight.
 * Properties: V-1 edges, connects all vertices, no cycle.
 * Applications: network design, clustering, image segmentation.
 *
 * =========================================
 * KRUSKAL'S ALGORITHM
 * =========================================
 * Greedy: Sort all edges by weight. Add edge if it doesn't form a cycle.
 * Use UNION-FIND (Disjoint Set Union) to detect cycles efficiently.
 * Time: O(E log E) for sorting
 *
 * =========================================
 * UNION-FIND (DSU — Disjoint Set Union)
 * =========================================
 * Data structure for tracking which elements belong to the same set.
 * Operations:
 * - find(x): which set does x belong to?
 * - union(x, y): merge sets containing x and y
 *
 * Optimizations:
 * 1. Union by Rank: attach smaller tree under larger
 * 2. Path Compression: flatten tree on find
 * With both: amortized O(α(n)) per operation (nearly constant!)
 *
 * =========================================
 * PRIM'S ALGORITHM
 * =========================================
 * Greedy: Start from any vertex. Repeatedly add the cheapest edge
 * that connects a new vertex to the MST.
 * Use min-heap for efficiency.
 * Time: O((V + E) log V)
 */

import java.util.*;

public class MinimumSpanningTree {

    // =====================
    // UNION-FIND (DSU)
    // =====================
    static class DSU {
        int[] parent, rank;

        DSU(int n) {
            parent = new int[n]; rank = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i; // each node is its own root
        }

        int find(int x) {
            if (parent[x] != x) parent[x] = find(parent[x]); // path compression
            return parent[x];
        }

        boolean union(int x, int y) {
            int px = find(x), py = find(y);
            if (px == py) return false; // already in same set (cycle!)
            // Union by rank
            if (rank[px] < rank[py]) { int t = px; px = py; py = t; }
            parent[py] = px;
            if (rank[px] == rank[py]) rank[px]++;
            return true;
        }

        boolean connected(int x, int y) { return find(x) == find(y); }
    }

    // =====================
    // KRUSKAL'S MST
    // =====================
    static int kruskalMST(int V, int[][] edges) {
        // Sort edges by weight
        Arrays.sort(edges, (a, b) -> a[2] - b[2]);
        DSU dsu = new DSU(V);
        int mstWeight = 0, edgeCount = 0;
        System.out.println("Kruskal MST edges:");
        for (int[] e : edges) {
            if (edgeCount == V - 1) break;
            if (dsu.union(e[0], e[1])) { // doesn't form a cycle
                mstWeight += e[2];
                edgeCount++;
                System.out.printf("  Edge (%d - %d): weight %d%n", e[0], e[1], e[2]);
            }
        }
        return mstWeight;
    }

    // =====================
    // PRIM'S MST
    // =====================
    @SuppressWarnings("unchecked")
    static int primMST(int V, List<int[]>[] adj) {
        boolean[] inMST = new boolean[V];
        int[] key = new int[V]; // minimum edge weight to include this vertex
        Arrays.fill(key, Integer.MAX_VALUE);
        key[0] = 0;

        // Min-heap: [weight, vertex]
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
        pq.offer(new int[]{0, 0});

        int mstWeight = 0;
        System.out.println("Prim MST edges:");
        int[] parent = new int[V];
        Arrays.fill(parent, -1);

        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int w = curr[0], u = curr[1];
            if (inMST[u]) continue;
            inMST[u] = true;
            mstWeight += w;
            if (parent[u] != -1) System.out.printf("  Edge (%d - %d): weight %d%n", parent[u], u, w);

            for (int[] edge : adj[u]) {
                int v = edge[0], ew = edge[1];
                if (!inMST[v] && ew < key[v]) {
                    key[v] = ew;
                    parent[v] = u;
                    pq.offer(new int[]{ew, v});
                }
            }
        }
        return mstWeight;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        // Graph:
        // 0---1 (4)
        // |   |
        // 2---3 (2)
        // Edges: (0,1,4),(0,2,3),(1,2,1),(1,3,2),(2,3,4)
        int V = 4;
        int[][] edges = {{0,1,4},{0,2,3},{1,2,1},{1,3,2},{2,3,4}};

        System.out.println("=== Kruskal's MST ===");
        int kWeight = kruskalMST(V, edges.clone());
        System.out.println("Total MST weight: " + kWeight);

        // Build adjacency list for Prim's
        List<int[]>[] adj = new ArrayList[V];
        for (int i = 0; i < V; i++) adj[i] = new ArrayList<>();
        for (int[] e : edges) {
            adj[e[0]].add(new int[]{e[1], e[2]});
            adj[e[1]].add(new int[]{e[0], e[2]});
        }

        System.out.println("\n=== Prim's MST ===");
        int pWeight = primMST(V, adj);
        System.out.println("Total MST weight: " + pWeight);

        // Union-Find demo
        System.out.println("\n=== Union-Find Demo ===");
        DSU dsu = new DSU(6);
        dsu.union(0, 1); dsu.union(2, 3); dsu.union(4, 5);
        System.out.println("0 connected to 1: " + dsu.connected(0, 1)); // true
        System.out.println("0 connected to 2: " + dsu.connected(0, 2)); // false
        dsu.union(0, 2);
        System.out.println("0 connected to 3: " + dsu.connected(0, 3)); // true (0-2-3)
    }
}
