/*
 * WEEK 24 - RESEARCH-LEVEL TOPICS
 * Topic: NP-Completeness & Approximation Algorithms
 *
 * =========================================
 * P vs NP — THE CENTRAL QUESTION OF CS
 * =========================================
 * P  = problems solvable in polynomial time O(n^k)
 * NP = problems where a solution can be VERIFIED in polynomial time
 *
 * NP-Complete: A problem X is NP-Complete if:
 * 1. X is in NP (verifiable in poly time)
 * 2. Every problem in NP can be reduced to X in poly time
 *
 * If P ≠ NP (widely believed), NP-Complete problems have no poly-time solution.
 *
 * FAMOUS NP-COMPLETE PROBLEMS:
 * - 3-SAT (Boolean satisfiability)
 * - Traveling Salesman Problem (decision version)
 * - Vertex Cover
 * - Hamiltonian Cycle
 * - Subset Sum
 * - Graph Coloring
 * - Clique
 *
 * =========================================
 * APPROXIMATION ALGORITHMS
 * =========================================
 * When exact solution is too slow (NP-Complete), find a solution
 * guaranteed to be within a factor of optimal.
 *
 * APPROXIMATION RATIO ρ: sol / OPT ≤ ρ (for minimization)
 *
 * COVERED:
 * 1. Vertex Cover: 2-approximation (take both endpoints of any matching edge)
 * 2. Set Cover: O(log n)-approximation (greedy: always pick set covering most uncovered elements)
 * 3. TSP: 2-approximation using MST (Christofides: 3/2 — not implemented here)
 *
 * =========================================
 * GREEDY SET COVER — O(log n) approximation
 * =========================================
 * Given a universe U and collection of sets S,
 * find minimum number of sets whose union covers U.
 * NP-Complete for exact solution.
 * Greedy: always pick set with most uncovered elements.
 * Approximation ratio: H(n) ≈ ln(n) where n = |U|
 */

import java.util.*;

public class NPCompletenessAndApproximation {

    // =====================
    // VERTEX COVER (2-approximation)
    // =====================
    // Problem: Find minimum set of vertices S such that every edge (u,v) has u∈S or v∈S.
    // 2-approx: For each uncovered edge, take BOTH endpoints.
    // This guarantees |our cover| ≤ 2 * |optimal cover|.
    // Proof: optimal cover must include at least one endpoint of each matched edge.
    //        We took 2 endpoints per edge in the maximal matching → ≤ 2 * OPT.
    static Set<Integer> vertexCover2Approx(int V, List<int[]> edges) {
        boolean[] covered = new boolean[V]; // is vertex covered?
        Set<Integer> cover = new HashSet<>();

        for (int[] e : edges) {
            int u = e[0], v = e[1];
            if (!covered[u] && !covered[v]) { // uncovered edge
                covered[u] = true;
                covered[v] = true;
                cover.add(u);
                cover.add(v);
            }
        }
        return cover;
    }

    // =====================
    // SET COVER GREEDY (O(log n) approximation)
    // =====================
    // Greedy: at each step, pick the set that covers the most uncovered elements.
    static List<Integer> setcoverGreedy(int universeSize, List<Set<Integer>> sets) {
        Set<Integer> uncovered = new HashSet<>();
        for (int i = 0; i < universeSize; i++) uncovered.add(i);

        List<Integer> chosen = new ArrayList<>();

        while (!uncovered.isEmpty()) {
            int bestIdx = -1, bestCount = 0;
            for (int i = 0; i < sets.size(); i++) {
                int count = 0;
                for (int x : sets.get(i)) if (uncovered.contains(x)) count++;
                if (count > bestCount) { bestCount = count; bestIdx = i; }
            }
            if (bestIdx == -1) break; // remaining elements uncoverable
            chosen.add(bestIdx);
            uncovered.removeAll(sets.get(bestIdx));
        }
        return chosen;
    }

    // =====================
    // TSP 2-APPROXIMATION (metric TSP using MST)
    // =====================
    // Assumes triangle inequality: dist(u,v) ≤ dist(u,w) + dist(w,v)
    // Algorithm:
    // 1. Build MST (O(V² for dense graphs))
    // 2. DFS preorder traversal of MST gives a Hamiltonian path
    // 3. This path has cost ≤ 2 * OPT
    //
    // Why ≤ 2 * OPT?
    // - MST weight ≤ OPT (optimal tour minus one edge is a spanning tree)
    // - DFS traversal traverses each MST edge twice → 2 * MST_weight ≤ 2 * OPT
    // - Shortcuts (triangle inequality) don't increase cost
    static int[] tsp2Approx(int[][] dist) {
        int n = dist.length;
        // Build MST using Prim's
        boolean[] inMST = new boolean[n];
        int[] parent = new int[n];
        int[] key = new int[n];
        Arrays.fill(key, Integer.MAX_VALUE);
        key[0] = 0; parent[0] = -1;
        for (int i = 0; i < n - 1; i++) {
            // Find min key vertex not in MST (naive O(n²) for simplicity)
            int u = -1;
            for (int v = 0; v < n; v++) if (!inMST[v] && (u == -1 || key[v] < key[u])) u = v;
            inMST[u] = true;
            for (int v = 0; v < n; v++)
                if (!inMST[v] && dist[u][v] < key[v]) { key[v] = dist[u][v]; parent[v] = u; }
        }

        // Build MST adjacency list
        List<List<Integer>> mst = new ArrayList<>();
        for (int i = 0; i < n; i++) mst.add(new ArrayList<>());
        for (int i = 1; i < n; i++) { mst.get(parent[i]).add(i); mst.get(i).add(parent[i]); }

        // DFS preorder to get tour
        boolean[] visited = new boolean[n];
        List<Integer> tour = new ArrayList<>();
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(0);
        while (!stack.isEmpty()) {
            int u = stack.pop();
            if (visited[u]) continue;
            visited[u] = true;
            tour.add(u);
            // Push neighbors in reverse to maintain order
            List<Integer> neighbors = mst.get(u);
            for (int i = neighbors.size() - 1; i >= 0; i--) {
                if (!visited[neighbors.get(i)]) stack.push(neighbors.get(i));
            }
        }

        // Calculate tour cost
        int totalCost = 0;
        for (int i = 0; i < n; i++) totalCost += dist[tour.get(i)][tour.get((i + 1) % n)];
        System.out.println("TSP 2-Approx tour: " + tour + ", cost: " + totalCost);

        return tour.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // Vertex Cover
        System.out.println("=== Vertex Cover (2-approximation) ===");
        //   0---1
        //   |   |
        //   2---3---4
        List<int[]> edges = List.of(new int[]{0,1}, new int[]{0,2}, new int[]{1,3}, new int[]{2,3}, new int[]{3,4});
        Set<Integer> cover = vertexCover2Approx(5, edges);
        System.out.println("2-approx vertex cover: " + cover);
        System.out.println("Cover size: " + cover.size()); // ≤ 2 * optimal

        // Set Cover
        System.out.println("\n=== Set Cover (greedy) ===");
        // Universe = {0,1,2,3,4,5,6,7,8,9}
        // Sets: {0,1,2}, {3,4,5}, {4,5,6,7}, {0,3,8}, {2,7,9}
        List<Set<Integer>> sets = new ArrayList<>();
        sets.add(new HashSet<>(Arrays.asList(0,1,2)));
        sets.add(new HashSet<>(Arrays.asList(3,4,5)));
        sets.add(new HashSet<>(Arrays.asList(4,5,6,7)));
        sets.add(new HashSet<>(Arrays.asList(0,3,8)));
        sets.add(new HashSet<>(Arrays.asList(2,7,9)));

        List<Integer> chosen = setcoverGreedy(10, sets);
        System.out.println("Chosen set indices: " + chosen);
        Set<Integer> covered = new HashSet<>();
        for (int i : chosen) covered.addAll(sets.get(i));
        System.out.println("Covered elements: " + covered);

        // TSP 2-Approximation
        System.out.println("\n=== TSP 2-Approximation (metric) ===");
        int[][] dist = {
            {0, 10, 15, 20},
            {10, 0, 35, 25},
            {15, 35, 0, 30},
            {20, 25, 30, 0}
        };
        tsp2Approx(dist);
        System.out.println("(Optimal tour cost for this instance: 80)");

        // Discuss P vs NP
        System.out.println("\n=== P vs NP Key Points ===");
        System.out.println("- P: problems solvable in poly time (sorting, shortest path, MST)");
        System.out.println("- NP: problems verifiable in poly time (TSP, vertex cover, 3-SAT)");
        System.out.println("- NP-Hard: at least as hard as NP-Complete problems");
        System.out.println("- If P=NP, all encryption would break (RSA, AES rely on hard problems)");
        System.out.println("- Most believe P≠NP (Clay Millennium Prize: $1M for proof)");
        System.out.println("- Approximation algorithms: practical solutions with quality guarantees");
    }
}
