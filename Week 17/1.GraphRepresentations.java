/*
 * WEEK 17 - GRAPHS: FUNDAMENTALS & TRAVERSALS
 * Topic: Graph Representations, BFS, DFS
 *
 * GRAPH: A set of vertices (V) connected by edges (E).
 * - Undirected vs Directed (digraph)
 * - Weighted vs Unweighted
 * - Cyclic vs Acyclic (DAG = Directed Acyclic Graph)
 *
 * REPRESENTATIONS:
 * 1. Adjacency Matrix: int[V][V], mat[u][v]=1 if edge u-v exists
 *    Space: O(V²)
 *    Check edge: O(1)
 *    Iterate neighbors: O(V)
 *    Good for dense graphs.
 *
 * 2. Adjacency List: List<List<Integer>>, adj[u] = list of neighbors
 *    Space: O(V + E)
 *    Iterate neighbors: O(degree)
 *    Good for sparse graphs (most real-world graphs).
 *
 * TRAVERSALS:
 * BFS (Breadth-First Search): explore level by level using a queue.
 *   - Finds shortest path in unweighted graph
 *   - Time: O(V + E)
 *
 * DFS (Depth-First Search): explore as deep as possible using stack/recursion.
 *   - Cycle detection, topological sort, connected components
 *   - Time: O(V + E)
 *
 * COVERED:
 * 1. Graph construction
 * 2. BFS and shortest path
 * 3. DFS
 * 4. Connected components
 * 5. Cycle detection in undirected graph
 * 6. Bipartite check
 */

import java.util.*;

public class GraphRepresentations {

    static class Graph {
        int V;
        List<List<Integer>> adj;

        Graph(int v) {
            V = v;
            adj = new ArrayList<>();
            for (int i = 0; i < v; i++) adj.add(new ArrayList<>());
        }

        void addEdge(int u, int v) { // undirected
            adj.get(u).add(v);
            adj.get(v).add(u);
        }

        void addDirectedEdge(int u, int v) {
            adj.get(u).add(v);
        }

        // BFS from source — returns visited order
        List<Integer> bfs(int src) {
            List<Integer> result = new ArrayList<>();
            boolean[] visited = new boolean[V];
            Queue<Integer> queue = new LinkedList<>();
            visited[src] = true;
            queue.offer(src);
            while (!queue.isEmpty()) {
                int u = queue.poll();
                result.add(u);
                for (int neighbor : adj.get(u)) {
                    if (!visited[neighbor]) {
                        visited[neighbor] = true;
                        queue.offer(neighbor);
                    }
                }
            }
            return result;
        }

        // BFS shortest distances from source (-1 = not reachable)
        int[] shortestDistances(int src) {
            int[] dist = new int[V];
            Arrays.fill(dist, -1);
            dist[src] = 0;
            Queue<Integer> queue = new LinkedList<>();
            queue.offer(src);
            while (!queue.isEmpty()) {
                int u = queue.poll();
                for (int v : adj.get(u)) {
                    if (dist[v] == -1) {
                        dist[v] = dist[u] + 1;
                        queue.offer(v);
                    }
                }
            }
            return dist;
        }

        // DFS from source (recursive)
        List<Integer> dfs(int src) {
            List<Integer> result = new ArrayList<>();
            boolean[] visited = new boolean[V];
            dfsHelper(src, visited, result);
            return result;
        }
        void dfsHelper(int u, boolean[] visited, List<Integer> result) {
            visited[u] = true;
            result.add(u);
            for (int v : adj.get(u)) if (!visited[v]) dfsHelper(v, visited, result);
        }

        // Count connected components
        int countComponents() {
            boolean[] visited = new boolean[V];
            int count = 0;
            for (int i = 0; i < V; i++) {
                if (!visited[i]) {
                    dfsForComponent(i, visited);
                    count++;
                }
            }
            return count;
        }
        void dfsForComponent(int u, boolean[] visited) {
            visited[u] = true;
            for (int v : adj.get(u)) if (!visited[v]) dfsForComponent(v, visited);
        }

        // Cycle detection in undirected graph (DFS)
        boolean hasCycle() {
            boolean[] visited = new boolean[V];
            for (int i = 0; i < V; i++)
                if (!visited[i] && hasCycleDFS(i, visited, -1)) return true;
            return false;
        }
        boolean hasCycleDFS(int u, boolean[] visited, int parent) {
            visited[u] = true;
            for (int v : adj.get(u)) {
                if (!visited[v]) {
                    if (hasCycleDFS(v, visited, u)) return true;
                } else if (v != parent) {
                    return true; // back edge found → cycle
                }
            }
            return false;
        }

        // Bipartite check (2-colorable): can vertices be colored with 2 colors
        // such that no two adjacent vertices have the same color?
        // Uses BFS. If a graph has an odd-length cycle, it's NOT bipartite.
        boolean isBipartite() {
            int[] color = new int[V]; // 0=uncolored, 1=red, -1=blue
            for (int i = 0; i < V; i++) {
                if (color[i] == 0) {
                    Queue<Integer> queue = new LinkedList<>();
                    queue.offer(i);
                    color[i] = 1;
                    while (!queue.isEmpty()) {
                        int u = queue.poll();
                        for (int v : adj.get(u)) {
                            if (color[v] == 0) { color[v] = -color[u]; queue.offer(v); }
                            else if (color[v] == color[u]) return false;
                        }
                    }
                }
            }
            return true;
        }
    }

    public static void main(String[] args) {
        //  0 -- 1 -- 2
        //  |         |
        //  3 -- 4 -- 5
        Graph g = new Graph(6);
        g.addEdge(0, 1); g.addEdge(1, 2); g.addEdge(2, 5);
        g.addEdge(5, 4); g.addEdge(4, 3); g.addEdge(3, 0);
        g.addEdge(1, 4); // extra edge

        System.out.println("BFS from 0: " + g.bfs(0));
        System.out.println("DFS from 0: " + g.dfs(0));

        int[] dist = g.shortestDistances(0);
        System.out.println("Distances from 0: " + Arrays.toString(dist));

        System.out.println("Components: " + g.countComponents()); // 1
        System.out.println("Has cycle: " + g.hasCycle());         // true
        System.out.println("Bipartite: " + g.isBipartite());      // depends on structure

        // Disconnected graph
        Graph g2 = new Graph(6);
        g2.addEdge(0, 1); g2.addEdge(1, 2);
        g2.addEdge(3, 4);
        // node 5 is isolated
        System.out.println("\nDisconnected graph components: " + g2.countComponents()); // 3
        System.out.println("BFS from 0: " + g2.bfs(0));

        // Bipartite graph (e.g., complete bipartite K_{2,3})
        Graph bipartite = new Graph(5);
        bipartite.addEdge(0, 2); bipartite.addEdge(0, 3); bipartite.addEdge(0, 4);
        bipartite.addEdge(1, 2); bipartite.addEdge(1, 3); bipartite.addEdge(1, 4);
        System.out.println("\nK_{2,3} bipartite: " + bipartite.isBipartite()); // true

        // Non-bipartite (triangle)
        Graph triangle = new Graph(3);
        triangle.addEdge(0, 1); triangle.addEdge(1, 2); triangle.addEdge(2, 0);
        System.out.println("Triangle bipartite: " + triangle.isBipartite()); // false
    }
}
