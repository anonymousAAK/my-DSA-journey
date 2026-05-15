/*
 * WEEK 26 - JAVA ADVANCED TOPICS
 * Topic: Bipartite Matching (Hopcroft-Karp + Kuhn's algorithm)
 * File: bipartite_matching.java
 *
 * CONCEPT:
 *     A matching in a bipartite graph G=(L u R, E) is a subset of edges
 *     with no shared endpoints. *Maximum* bipartite matching maximises the
 *     subset's size. Hopcroft-Karp is the fastest classical algorithm: it
 *     builds a layered BFS graph then performs DFS that finds
 *     vertex-disjoint shortest augmenting paths in a single phase. Each
 *     phase increases the shortest augmenting-path length by 1, so there
 *     are O(sqrt(V)) phases and O(E*sqrt(V)) total work. We also include
 *     Kuhn's O(V*E) DFS-augment algorithm for didactic clarity.
 *
 * KEY POINTS:
 *     - Equivalent to running unit-capacity max-flow s -> L -> R -> t.
 *     - Returns matching arrays matchLeft[u] and matchRight[v]; NIL = -1.
 *     - Augmenting path = path alternating unmatched/matched edges that
 *       starts and ends at unmatched vertices.
 *     - Foundational tool for assignment, scheduling, Konig's vertex cover.
 *
 * ALGORITHM / APPROACH:
 *     Hopcroft-Karp:
 *       while BFS finds some augmenting path of length d:
 *         for each free left vertex u:
 *             DFS to extend along level-graph augmenting paths
 *             flip matchings along each successful path
 *       return number of matched pairs
 *     Kuhn:
 *       for each left vertex u:
 *           DFS with `used` marker; if it finds an augmenting path, +1.
 *
 * DRY RUN / EXAMPLE:
 *     Left {0,1,2,3}, Right {0,1,2,3}; edges
 *       0-0, 0-1, 1-0, 1-2, 2-1, 2-3, 3-2, 3-3
 *     Phase 1 augmenting paths: 0->0, 1->2, 2->3 -> matching = 3
 *     Phase 2 alternation finds path for 3 -> matching = 4 (perfect).
 *
 * COMPLEXITY:
 *     Hopcroft-Karp: O(E * sqrt(V)) time, O(V + E) space.
 *     Kuhn        : O(V * E)       time, O(V + E) space.
 */

// snake_case filename is fine because class BipartiteMatching is package-private.

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;

class BipartiteMatching {

    static final int NIL = -1;
    static final int INF = Integer.MAX_VALUE;

    // ---- Hopcroft-Karp ----------------------------------------------------
    static class HopcroftKarp {
        int leftSize, rightSize;
        List<List<Integer>> adj;
        int[] matchLeft, matchRight, dist;

        HopcroftKarp(int leftSize, int rightSize) {
            this.leftSize = leftSize;
            this.rightSize = rightSize;
            this.adj = new ArrayList<>();
            for (int i = 0; i < leftSize; i++) adj.add(new ArrayList<>());
        }

        void addEdge(int u, int v) { adj.get(u).add(v); }

        private boolean bfs() {
            Deque<Integer> queue = new ArrayDeque<>();
            for (int u = 0; u < leftSize; u++) {
                if (matchLeft[u] == NIL) { dist[u] = 0; queue.offer(u); }
                else                     { dist[u] = INF; }
            }
            boolean found = false;
            while (!queue.isEmpty()) {
                int u = queue.poll();
                for (int v : adj.get(u)) {
                    int pair = matchRight[v];
                    if (pair == NIL) {
                        found = true;
                    } else if (dist[pair] == INF) {
                        dist[pair] = dist[u] + 1;
                        queue.offer(pair);
                    }
                }
            }
            return found;
        }

        private boolean dfs(int u) {
            for (int v : adj.get(u)) {
                int pair = matchRight[v];
                if (pair == NIL || (dist[pair] == dist[u] + 1 && dfs(pair))) {
                    matchLeft[u] = v;
                    matchRight[v] = u;
                    return true;
                }
            }
            dist[u] = INF;
            return false;
        }

        int maxMatching() {
            matchLeft = new int[leftSize];
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

    // ---- Kuhn (simpler O(V*E) reference algorithm) ------------------------
    static class Kuhn {
        int leftSize, rightSize;
        List<List<Integer>> adj;
        int[] matchRight;

        Kuhn(int leftSize, int rightSize) {
            this.leftSize = leftSize;
            this.rightSize = rightSize;
            this.adj = new ArrayList<>();
            for (int i = 0; i < leftSize; i++) adj.add(new ArrayList<>());
        }

        void addEdge(int u, int v) { adj.get(u).add(v); }

        private boolean tryKuhn(int u, boolean[] used) {
            for (int v : adj.get(u)) {
                if (used[v]) continue;
                used[v] = true;
                if (matchRight[v] == -1 || tryKuhn(matchRight[v], used)) {
                    matchRight[v] = u;
                    return true;
                }
            }
            return false;
        }

        int maxMatching() {
            matchRight = new int[rightSize];
            Arrays.fill(matchRight, -1);
            int pairs = 0;
            for (int u = 0; u < leftSize; u++) {
                boolean[] used = new boolean[rightSize];
                if (tryKuhn(u, used)) pairs++;
            }
            return pairs;
        }
    }

    public static void main(String[] args) {
        int[][] edges = {
            {0, 0}, {0, 1}, {1, 0}, {1, 2},
            {2, 1}, {2, 3}, {3, 2}, {3, 3}
        };

        HopcroftKarp hk = new HopcroftKarp(4, 4);
        for (int[] e : edges) hk.addEdge(e[0], e[1]);
        System.out.println("Hopcroft-Karp matching: " + hk.maxMatching());
        System.out.print("Pairs:");
        for (int u = 0; u < 4; u++) {
            if (hk.matchLeft[u] != NIL)
                System.out.print(" (" + u + "," + hk.matchLeft[u] + ")");
        }
        System.out.println();

        Kuhn k = new Kuhn(4, 4);
        for (int[] e : edges) k.addEdge(e[0], e[1]);
        System.out.println("Kuhn matching:          " + k.maxMatching());
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in bipartite_matching.py:
 *   - Java uses Integer.MAX_VALUE as the distance sentinel; Python used
 *     float('inf').
 *   - matchedPairs() is replaced with a loop over matchLeft for output.
 *   - Bonus Kuhn class is included to mirror kuhn_max_matching in Python.
 */
