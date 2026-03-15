//! # Week 17: Graph Algorithms
//!
//! Graphs model pairwise relationships between objects. This module covers
//! fundamental graph traversals and properties using an adjacency list
//! representation.
//!
//! ## Representation
//! We use `Vec<Vec<usize>>` as an adjacency list where `adj[u]` contains
//! all vertices adjacent to vertex `u`. This is space-efficient for sparse
//! graphs: O(V + E) space vs O(V^2) for an adjacency matrix.
//!
//! ## Complexity Summary
//! | Algorithm            | Time        | Space  |
//! |---------------------|-------------|--------|
//! | BFS                 | O(V + E)    | O(V)   |
//! | DFS                 | O(V + E)    | O(V)   |
//! | Connected Components| O(V + E)    | O(V)   |
//! | Cycle Detection     | O(V + E)    | O(V)   |
//! | Bipartite Check     | O(V + E)    | O(V)   |
//! | Topological Sort    | O(V + E)    | O(V)   |

use std::collections::VecDeque;

// =============================================================================
// Graph struct — Adjacency list representation
// =============================================================================

/// An unweighted graph using adjacency list representation.
///
/// # Ownership
/// The `Graph` owns its adjacency list (`Vec<Vec<usize>>`). Each inner `Vec`
/// stores the neighbors of a vertex. The `directed` flag controls whether
/// `add_edge` adds edges in both directions.
struct Graph {
    adj: Vec<Vec<usize>>,
    num_vertices: usize,
    directed: bool,
}

impl Graph {
    /// Creates a new graph with `n` vertices and no edges.
    fn new(n: usize, directed: bool) -> Self {
        Graph {
            adj: vec![Vec::new(); n],
            num_vertices: n,
            directed,
        }
    }

    /// Adds an edge from `u` to `v`. If undirected, also adds `v` to `u`.
    fn add_edge(&mut self, u: usize, v: usize) {
        self.adj[u].push(v);
        if !self.directed {
            self.adj[v].push(u);
        }
    }

    // =========================================================================
    // BFS — Breadth-First Search
    // =========================================================================

    /// Performs BFS from `start`, returning (visit_order, distances).
    ///
    /// # Algorithm
    /// Uses a FIFO queue (VecDeque). Explores all neighbors at distance d
    /// before moving to distance d+1. This guarantees shortest paths in
    /// unweighted graphs.
    ///
    /// # Complexity
    /// - Time: O(V + E) — each vertex and edge visited once
    /// - Space: O(V) — for the queue and visited array
    ///
    /// # Returns
    /// - `visit_order`: vertices in the order they were first discovered
    /// - `distances`: distance from `start` to each vertex (-1 if unreachable)
    fn bfs(&self, start: usize) -> (Vec<usize>, Vec<i32>) {
        let mut visited = vec![false; self.num_vertices];
        let mut distances = vec![-1i32; self.num_vertices];
        let mut order = Vec::new();
        let mut queue = VecDeque::new();

        visited[start] = true;
        distances[start] = 0;
        queue.push_back(start);

        while let Some(u) = queue.pop_front() {
            order.push(u);
            for &v in &self.adj[u] {
                if !visited[v] {
                    visited[v] = true;
                    distances[v] = distances[u] + 1;
                    queue.push_back(v);
                }
            }
        }

        (order, distances)
    }

    // =========================================================================
    // DFS — Depth-First Search (recursive)
    // =========================================================================

    /// Performs DFS from `start`, returning the visit order.
    ///
    /// # Algorithm
    /// Recursively explores as deep as possible before backtracking.
    ///
    /// # Complexity
    /// - Time: O(V + E)
    /// - Space: O(V) — recursion stack in worst case (linear graph)
    ///
    /// # Ownership Note
    /// `visited` and `order` are passed as `&mut` references to the recursive
    /// helper, avoiding the need for global state.
    fn dfs(&self, start: usize) -> Vec<usize> {
        let mut visited = vec![false; self.num_vertices];
        let mut order = Vec::new();
        self.dfs_helper(start, &mut visited, &mut order);
        order
    }

    /// Recursive DFS helper.
    fn dfs_helper(&self, u: usize, visited: &mut Vec<bool>, order: &mut Vec<usize>) {
        visited[u] = true;
        order.push(u);
        for &v in &self.adj[u] {
            if !visited[v] {
                self.dfs_helper(v, visited, order);
            }
        }
    }

    // =========================================================================
    // Connected Components Count (undirected graphs)
    // =========================================================================

    /// Counts the number of connected components in an undirected graph.
    ///
    /// # Algorithm
    /// Iterate over all vertices. For each unvisited vertex, run DFS/BFS
    /// to mark all reachable vertices, then increment the component count.
    ///
    /// # Complexity
    /// - Time: O(V + E) — each vertex and edge visited once across all DFS calls
    /// - Space: O(V)
    fn connected_components(&self) -> usize {
        let mut visited = vec![false; self.num_vertices];
        let mut count = 0;

        for v in 0..self.num_vertices {
            if !visited[v] {
                self.dfs_helper(v, &mut visited, &mut Vec::new());
                count += 1;
            }
        }

        count
    }

    // =========================================================================
    // Cycle Detection (undirected graph)
    // =========================================================================

    /// Detects whether an undirected graph contains a cycle.
    ///
    /// # Algorithm
    /// DFS from each unvisited vertex. During DFS, if we encounter a visited
    /// neighbor that is NOT the parent of the current vertex, a cycle exists.
    ///
    /// # Complexity
    /// - Time: O(V + E)
    /// - Space: O(V)
    fn has_cycle(&self) -> bool {
        let mut visited = vec![false; self.num_vertices];

        for v in 0..self.num_vertices {
            if !visited[v] {
                if self.has_cycle_dfs(v, usize::MAX, &mut visited) {
                    return true;
                }
            }
        }

        false
    }

    /// DFS helper for cycle detection. `parent` is the vertex we came from
    /// (usize::MAX means no parent, i.e., the start vertex).
    fn has_cycle_dfs(&self, u: usize, parent: usize, visited: &mut Vec<bool>) -> bool {
        visited[u] = true;

        for &v in &self.adj[u] {
            if !visited[v] {
                if self.has_cycle_dfs(v, u, visited) {
                    return true;
                }
            } else if v != parent {
                // Found a visited neighbor that isn't our parent → cycle!
                return true;
            }
        }

        false
    }

    // =========================================================================
    // Bipartite Check
    // =========================================================================

    /// Checks whether the graph is bipartite (2-colorable).
    ///
    /// # Algorithm
    /// BFS-based coloring. Assign alternating colors (0 and 1) level by level.
    /// If any edge connects two vertices of the same color, the graph is not
    /// bipartite.
    ///
    /// # Key Property
    /// A graph is bipartite if and only if it contains no odd-length cycles.
    ///
    /// # Complexity
    /// - Time: O(V + E)
    /// - Space: O(V)
    fn is_bipartite(&self) -> bool {
        // -1 = uncolored, 0 or 1 = color
        let mut color = vec![-1i32; self.num_vertices];

        for start in 0..self.num_vertices {
            if color[start] != -1 {
                continue;
            }

            // BFS coloring from this component
            let mut queue = VecDeque::new();
            color[start] = 0;
            queue.push_back(start);

            while let Some(u) = queue.pop_front() {
                for &v in &self.adj[u] {
                    match color[v] {
                        -1 => {
                            color[v] = 1 - color[u]; // Alternate color
                            queue.push_back(v);
                        }
                        c if c == color[u] => {
                            return false; // Same color on both ends of an edge
                        }
                        _ => {} // Already colored with the opposite color — OK
                    }
                }
            }
        }

        true
    }

    // =========================================================================
    // Topological Sort — Kahn's Algorithm (BFS-based)
    // =========================================================================

    /// Performs topological sort on a directed acyclic graph (DAG).
    ///
    /// # Algorithm (Kahn's)
    /// 1. Compute in-degree for each vertex.
    /// 2. Enqueue all vertices with in-degree 0.
    /// 3. Repeatedly dequeue a vertex, add it to the result, and decrement
    ///    the in-degree of its neighbors. Enqueue any neighbor whose in-degree
    ///    drops to 0.
    /// 4. If the result doesn't contain all vertices, the graph has a cycle.
    ///
    /// # Complexity
    /// - Time: O(V + E)
    /// - Space: O(V)
    ///
    /// # Returns
    /// `Some(order)` if the graph is a DAG, `None` if it contains a cycle.
    fn topological_sort(&self) -> Option<Vec<usize>> {
        let mut in_degree = vec![0usize; self.num_vertices];

        // Compute in-degrees
        for u in 0..self.num_vertices {
            for &v in &self.adj[u] {
                in_degree[v] += 1;
            }
        }

        // Enqueue all vertices with in-degree 0
        let mut queue: VecDeque<usize> = VecDeque::new();
        for (v, &deg) in in_degree.iter().enumerate() {
            if deg == 0 {
                queue.push_back(v);
            }
        }

        let mut order = Vec::with_capacity(self.num_vertices);

        while let Some(u) = queue.pop_front() {
            order.push(u);
            for &v in &self.adj[u] {
                in_degree[v] -= 1;
                if in_degree[v] == 0 {
                    queue.push_back(v);
                }
            }
        }

        if order.len() == self.num_vertices {
            Some(order)
        } else {
            None // Cycle detected — not all vertices were processed
        }
    }
}

// =============================================================================
// Main — Test cases
// =============================================================================

fn main() {
    println!("=== Week 17: Graphs ===\n");

    // --- BFS ---
    println!("--- BFS ---");
    let mut g = Graph::new(6, false);
    // Create: 0-1, 0-2, 1-3, 2-4, 3-5, 4-5
    g.add_edge(0, 1);
    g.add_edge(0, 2);
    g.add_edge(1, 3);
    g.add_edge(2, 4);
    g.add_edge(3, 5);
    g.add_edge(4, 5);

    let (order, distances) = g.bfs(0);
    println!("BFS from 0: order = {:?}", order);
    println!("BFS from 0: distances = {:?}", distances);
    assert_eq!(distances[0], 0);
    assert_eq!(distances[1], 1);
    assert_eq!(distances[5], 3); // 0->1->3->5 or 0->2->4->5
    println!("PASS: BFS works correctly\n");

    // --- DFS ---
    println!("--- DFS ---");
    let dfs_order = g.dfs(0);
    println!("DFS from 0: {:?}", dfs_order);
    assert_eq!(dfs_order[0], 0);
    assert_eq!(dfs_order.len(), 6);
    println!("PASS: DFS works correctly\n");

    // --- Connected Components ---
    println!("--- Connected Components ---");
    let mut g2 = Graph::new(7, false);
    g2.add_edge(0, 1);
    g2.add_edge(1, 2);
    g2.add_edge(3, 4);
    // Vertices 5 and 6 are isolated
    let cc = g2.connected_components();
    println!("Components in 7-vertex graph with 2 edges: {}", cc);
    assert_eq!(cc, 4); // {0,1,2}, {3,4}, {5}, {6}
    println!("PASS: Connected components works correctly\n");

    // --- Cycle Detection ---
    println!("--- Cycle Detection ---");
    // Tree (no cycle): 0-1, 1-2, 1-3
    let mut tree = Graph::new(4, false);
    tree.add_edge(0, 1);
    tree.add_edge(1, 2);
    tree.add_edge(1, 3);
    assert!(!tree.has_cycle());
    println!("Tree has cycle: {}", tree.has_cycle());

    // Graph with cycle: add edge 2-3 to make a cycle
    let mut cyclic = Graph::new(4, false);
    cyclic.add_edge(0, 1);
    cyclic.add_edge(1, 2);
    cyclic.add_edge(2, 3);
    cyclic.add_edge(3, 0);
    assert!(cyclic.has_cycle());
    println!("Cyclic graph has cycle: {}", cyclic.has_cycle());
    println!("PASS: Cycle detection works correctly\n");

    // --- Bipartite Check ---
    println!("--- Bipartite Check ---");
    // Bipartite: 0-1, 1-2, 2-3, 3-0 (even cycle)
    let mut bipartite = Graph::new(4, false);
    bipartite.add_edge(0, 1);
    bipartite.add_edge(1, 2);
    bipartite.add_edge(2, 3);
    bipartite.add_edge(3, 0);
    assert!(bipartite.is_bipartite());
    println!("Even cycle is bipartite: {}", bipartite.is_bipartite());

    // Not bipartite: triangle 0-1, 1-2, 2-0 (odd cycle)
    let mut triangle = Graph::new(3, false);
    triangle.add_edge(0, 1);
    triangle.add_edge(1, 2);
    triangle.add_edge(2, 0);
    assert!(!triangle.is_bipartite());
    println!("Triangle is bipartite: {}", triangle.is_bipartite());
    println!("PASS: Bipartite check works correctly\n");

    // --- Topological Sort ---
    println!("--- Topological Sort (Kahn's) ---");
    // DAG: 5->0, 5->2, 4->0, 4->1, 2->3, 3->1
    let mut dag = Graph::new(6, true);
    dag.add_edge(5, 0);
    dag.add_edge(5, 2);
    dag.add_edge(4, 0);
    dag.add_edge(4, 1);
    dag.add_edge(2, 3);
    dag.add_edge(3, 1);

    match dag.topological_sort() {
        Some(order) => {
            println!("Topological order: {:?}", order);
            assert_eq!(order.len(), 6);
            // Verify: for every edge u->v, u appears before v in the order
            let pos: Vec<usize> = {
                let mut p = vec![0; 6];
                for (i, &v) in order.iter().enumerate() {
                    p[v] = i;
                }
                p
            };
            assert!(pos[5] < pos[0]);
            assert!(pos[5] < pos[2]);
            assert!(pos[4] < pos[0]);
            assert!(pos[4] < pos[1]);
            assert!(pos[2] < pos[3]);
            assert!(pos[3] < pos[1]);
            println!("PASS: Topological order is valid");
        }
        None => panic!("Expected a valid topological order"),
    }

    // Test cycle detection in topological sort
    let mut cyclic_dag = Graph::new(3, true);
    cyclic_dag.add_edge(0, 1);
    cyclic_dag.add_edge(1, 2);
    cyclic_dag.add_edge(2, 0);
    assert_eq!(cyclic_dag.topological_sort(), None);
    println!("Cyclic graph topological sort: None (correct)\n");

    println!("All Week 17 tests passed!");
}
