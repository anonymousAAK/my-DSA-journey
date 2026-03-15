/*
 * WEEK 17 - GRAPHS
 * Topic: Topological Sort (DFS & Kahn's BFS Algorithm)
 *
 * TOPOLOGICAL SORT: Linear ordering of vertices in a DAG such that for every
 * directed edge u→v, vertex u appears before v in the ordering.
 *
 * ONLY possible for DAGs (Directed Acyclic Graphs).
 * There can be multiple valid topological orderings.
 *
 * APPLICATIONS:
 * - Task scheduling with dependencies
 * - Course prerequisite ordering
 * - Build systems (Makefile, Gradle, Maven dependency resolution)
 * - Package manager dependency resolution
 *
 * APPROACH 1: DFS + Stack
 * - Run DFS; add node to stack AFTER all its descendants are processed.
 * - Pop stack for topological order.
 * - Time: O(V + E)
 *
 * APPROACH 2: Kahn's Algorithm (BFS / indegree)
 * - Process nodes with indegree 0 first (no dependencies).
 * - Remove their edges, add newly 0-indegree nodes to queue.
 * - If not all nodes processed: cycle detected!
 * - Time: O(V + E)
 *
 * CYCLE DETECTION: Kahn's algorithm detects cycles — if result size < V, there's a cycle.
 */

import java.util.*;

public class TopologicalSort {

    static class Graph {
        int V;
        List<List<Integer>> adj;

        Graph(int v) {
            V = v;
            adj = new ArrayList<>();
            for (int i = 0; i < v; i++) adj.add(new ArrayList<>());
        }

        void addEdge(int u, int v) { adj.get(u).add(v); } // directed

        // APPROACH 1: DFS-based topological sort
        List<Integer> topoSortDFS() {
            boolean[] visited = new boolean[V];
            Deque<Integer> stack = new ArrayDeque<>();
            for (int i = 0; i < V; i++)
                if (!visited[i]) dfsTopo(i, visited, stack);
            List<Integer> result = new ArrayList<>();
            while (!stack.isEmpty()) result.add(stack.pop());
            return result;
        }
        void dfsTopo(int u, boolean[] visited, Deque<Integer> stack) {
            visited[u] = true;
            for (int v : adj.get(u)) if (!visited[v]) dfsTopo(v, visited, stack);
            stack.push(u); // push AFTER processing all descendants
        }

        // APPROACH 2: Kahn's Algorithm (BFS)
        // Returns null if cycle detected
        List<Integer> topoSortKahn() {
            int[] indegree = new int[V];
            for (int u = 0; u < V; u++)
                for (int v : adj.get(u)) indegree[v]++;

            Queue<Integer> queue = new LinkedList<>();
            for (int i = 0; i < V; i++) if (indegree[i] == 0) queue.offer(i);

            List<Integer> result = new ArrayList<>();
            while (!queue.isEmpty()) {
                int u = queue.poll();
                result.add(u);
                for (int v : adj.get(u)) {
                    indegree[v]--;
                    if (indegree[v] == 0) queue.offer(v);
                }
            }

            if (result.size() != V) return null; // cycle detected
            return result;
        }

        // Detect cycle in directed graph (DFS with 3 states)
        // States: 0=unvisited, 1=in-stack (being processed), 2=done
        boolean hasCycle() {
            int[] state = new int[V];
            for (int i = 0; i < V; i++) if (state[i] == 0 && dfsDetectCycle(i, state)) return true;
            return false;
        }
        boolean dfsDetectCycle(int u, int[] state) {
            state[u] = 1; // mark as in-stack
            for (int v : adj.get(u)) {
                if (state[v] == 1) return true;  // back edge → cycle
                if (state[v] == 0 && dfsDetectCycle(v, state)) return true;
            }
            state[u] = 2; // fully processed
            return false;
        }
    }

    public static void main(String[] args) {
        // Example: course prerequisites
        // 5→2, 5→0, 4→0, 4→1, 2→3, 3→1
        Graph g = new Graph(6);
        g.addEdge(5, 2); g.addEdge(5, 0);
        g.addEdge(4, 0); g.addEdge(4, 1);
        g.addEdge(2, 3); g.addEdge(3, 1);

        System.out.println("DFS Topological Sort: " + g.topoSortDFS());
        // One valid output: [5, 4, 2, 3, 1, 0] (order may vary but respects constraints)

        System.out.println("Kahn's Topological Sort: " + g.topoSortKahn());
        System.out.println("Has cycle: " + g.hasCycle()); // false

        // Graph with cycle
        Graph cyclic = new Graph(4);
        cyclic.addEdge(0, 1); cyclic.addEdge(1, 2);
        cyclic.addEdge(2, 3); cyclic.addEdge(3, 1); // 3→1 creates cycle
        System.out.println("\nCyclic graph:");
        System.out.println("Has cycle: " + cyclic.hasCycle()); // true
        System.out.println("Kahn's (cycle detected → null): " + cyclic.topoSortKahn());

        // Build system example
        System.out.println("\n=== Build System Example ===");
        // Tasks: 0=download, 1=compile, 2=test, 3=package, 4=deploy
        Graph build = new Graph(5);
        build.addEdge(0, 1); // download before compile
        build.addEdge(1, 2); // compile before test
        build.addEdge(1, 3); // compile before package
        build.addEdge(2, 3); // test before package
        build.addEdge(3, 4); // package before deploy
        System.out.println("Build order: " + build.topoSortKahn());
        // Expected: 0 → 1 → 2 → 3 → 4
    }
}
