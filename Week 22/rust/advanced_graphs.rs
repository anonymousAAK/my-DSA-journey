//! # Week 22: Advanced Graph Algorithms
//!
//! This module covers shortest path algorithms, minimum spanning trees,
//! and the Disjoint Set Union (Union-Find) data structure.
//!
//! ## Complexity Summary
//! | Algorithm      | Time                  | Space   | Notes                |
//! |---------------|-----------------------|---------|----------------------|
//! | Dijkstra      | O((V+E) log V)        | O(V+E)  | Non-negative weights |
//! | Bellman-Ford   | O(V * E)              | O(V)    | Handles negative     |
//! | Floyd-Warshall | O(V^3)                | O(V^2)  | All-pairs shortest   |
//! | Kruskal's MST | O(E log E)            | O(V)    | Uses DSU             |
//! | DSU find      | O(α(n)) ≈ O(1) amort. | O(V)    | With path compression|

use std::collections::BinaryHeap;
use std::cmp::Reverse;

// =============================================================================
// Dijkstra's Algorithm — Single-source shortest paths (non-negative weights)
// =============================================================================

/// Finds shortest paths from `src` to all other vertices using Dijkstra's
/// algorithm with a binary min-heap.
///
/// # Algorithm
/// 1. Initialize all distances to infinity, source to 0.
/// 2. Use a min-heap (priority queue) ordered by distance.
/// 3. Pop the vertex with the smallest tentative distance, relax its neighbors.
/// 4. Skip stale entries (where popped distance > known distance).
///
/// # Why Reverse?
/// Rust's `BinaryHeap` is a max-heap. We push `Reverse((dist, vertex))` to
/// turn it into a min-heap by distance.
///
/// # Complexity
/// - Time: O((V + E) log V) with binary heap
/// - Space: O(V + E)
///
/// # Parameters
/// - `adj`: adjacency list where `adj[u]` contains `(v, weight)` pairs
/// - `src`: source vertex
///
/// # Returns
/// Vector of shortest distances from `src`. `i64::MAX` means unreachable.
fn dijkstra(adj: &[Vec<(usize, i64)>], src: usize) -> Vec<i64> {
    let n = adj.len();
    let mut dist = vec![i64::MAX; n];
    dist[src] = 0;

    // Min-heap: (distance, vertex)
    let mut heap: BinaryHeap<Reverse<(i64, usize)>> = BinaryHeap::new();
    heap.push(Reverse((0, src)));

    while let Some(Reverse((d, u))) = heap.pop() {
        // Skip stale entries — we already found a shorter path to u
        if d > dist[u] {
            continue;
        }

        for &(v, weight) in &adj[u] {
            let new_dist = dist[u] + weight;
            if new_dist < dist[v] {
                dist[v] = new_dist;
                heap.push(Reverse((new_dist, v)));
            }
        }
    }

    dist
}

// =============================================================================
// Bellman-Ford — Handles negative edge weights
// =============================================================================

/// Finds shortest paths from `src` to all vertices, handling negative weights.
///
/// # Algorithm
/// 1. Initialize distances (source = 0, all others = infinity).
/// 2. Relax ALL edges V-1 times. After k iterations, shortest paths using
///    at most k edges are correct.
/// 3. One more pass: if any edge can still be relaxed, a negative cycle exists.
///
/// # Complexity
/// - Time: O(V * E)
/// - Space: O(V)
///
/// # Parameters
/// - `edges`: list of (from, to, weight) tuples
/// - `n`: number of vertices
/// - `src`: source vertex
///
/// # Returns
/// `Some(distances)` if no negative cycle reachable from `src`, else `None`.
fn bellman_ford(edges: &[(usize, usize, i64)], n: usize, src: usize) -> Option<Vec<i64>> {
    let mut dist = vec![i64::MAX; n];
    dist[src] = 0;

    // Relax all edges V-1 times
    for _ in 0..n - 1 {
        for &(u, v, w) in edges {
            if dist[u] != i64::MAX && dist[u] + w < dist[v] {
                dist[v] = dist[u] + w;
            }
        }
    }

    // Check for negative-weight cycles
    for &(u, v, w) in edges {
        if dist[u] != i64::MAX && dist[u] + w < dist[v] {
            return None; // Negative cycle detected
        }
    }

    Some(dist)
}

// =============================================================================
// Floyd-Warshall — All-pairs shortest paths
// =============================================================================

/// Computes shortest paths between ALL pairs of vertices.
///
/// # Algorithm
/// For each intermediate vertex `k`, for each pair `(i, j)`, check if the
/// path `i -> k -> j` is shorter than the current best `i -> j`.
///
/// The order of the triple loop (k outermost) is critical: after iteration k,
/// `dist[i][j]` is the shortest path using only vertices `{0..k}` as
/// intermediaries.
///
/// # Complexity
/// - Time: O(V^3)
/// - Space: O(V^2)
///
/// # Parameters
/// - `adj_matrix`: `dist[i][j]` = weight of edge i->j, or `i64::MAX` if none.
///   `dist[i][i]` should be 0.
///
/// # Returns
/// The distance matrix after computing all-pairs shortest paths.
fn floyd_warshall(adj_matrix: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let n = adj_matrix.len();
    let mut dist = adj_matrix.to_vec();

    for k in 0..n {
        for i in 0..n {
            for j in 0..n {
                if dist[i][k] != i64::MAX && dist[k][j] != i64::MAX {
                    let through_k = dist[i][k] + dist[k][j];
                    if through_k < dist[i][j] {
                        dist[i][j] = through_k;
                    }
                }
            }
        }
    }

    dist
}

// =============================================================================
// Disjoint Set Union (Union-Find)
// =============================================================================

/// Disjoint Set Union with path compression and union by rank.
///
/// # Operations
/// - `find(x)`: Returns the root representative of x's set.
///   Path compression flattens the tree so future lookups are faster.
/// - `union(x, y)`: Merges the sets containing x and y.
///   Union by rank keeps the tree shallow.
///
/// # Complexity
/// - Both operations: O(alpha(n)) amortized, where alpha is the inverse
///   Ackermann function — effectively O(1) for all practical purposes.
///
/// # Ownership
/// The DSU owns its `parent` and `rank` vectors. Since `find` modifies
/// the parent array (path compression), it requires `&mut self`.
struct DSU {
    parent: Vec<usize>,
    rank: Vec<usize>,
}

impl DSU {
    /// Creates a DSU with `n` elements, each in its own set.
    fn new(n: usize) -> Self {
        DSU {
            parent: (0..n).collect(), // Each element is its own parent
            rank: vec![0; n],
        }
    }

    /// Finds the root representative of `x` with path compression.
    ///
    /// Path compression: after finding the root, we point `x` (and all nodes
    /// on the path) directly to the root, flattening the tree.
    fn find(&mut self, x: usize) -> usize {
        if self.parent[x] != x {
            self.parent[x] = self.find(self.parent[x]); // Path compression
        }
        self.parent[x]
    }

    /// Merges the sets containing `x` and `y`. Returns `true` if they were
    /// in different sets (i.e., a merge actually happened).
    ///
    /// Union by rank: attach the shorter tree under the taller tree's root.
    fn union(&mut self, x: usize, y: usize) -> bool {
        let rx = self.find(x);
        let ry = self.find(y);

        if rx == ry {
            return false; // Already in the same set
        }

        // Attach smaller rank tree under root of higher rank tree
        match self.rank[rx].cmp(&self.rank[ry]) {
            std::cmp::Ordering::Less => self.parent[rx] = ry,
            std::cmp::Ordering::Greater => self.parent[ry] = rx,
            std::cmp::Ordering::Equal => {
                self.parent[ry] = rx;
                self.rank[rx] += 1;
            }
        }

        true
    }
}

// =============================================================================
// Kruskal's MST — Minimum Spanning Tree using DSU
// =============================================================================

/// Finds a Minimum Spanning Tree using Kruskal's algorithm.
///
/// # Algorithm
/// 1. Sort all edges by weight.
/// 2. For each edge (lightest first), if it connects two different components
///    (checked via DSU), add it to the MST.
/// 3. Stop when we have V-1 edges.
///
/// # Why Greedy Works
/// The cut property guarantees that the lightest edge crossing any cut is safe
/// to include in some MST. Kruskal's processes edges in order and only adds
/// edges that cross a cut (connect different components).
///
/// # Complexity
/// - Time: O(E log E) — dominated by sorting
/// - Space: O(V) for the DSU
///
/// # Returns
/// (total_weight, edges_in_mst) where each edge is (u, v, weight).
fn kruskal_mst(n: usize, edges: &[(usize, usize, i64)]) -> (i64, Vec<(usize, usize, i64)>) {
    let mut sorted_edges = edges.to_vec();
    sorted_edges.sort_unstable_by_key(|&(_, _, w)| w);

    let mut dsu = DSU::new(n);
    let mut mst = Vec::new();
    let mut total_weight = 0i64;

    for (u, v, w) in sorted_edges {
        if dsu.union(u, v) {
            total_weight += w;
            mst.push((u, v, w));
            if mst.len() == n - 1 {
                break; // MST is complete
            }
        }
    }

    (total_weight, mst)
}

// =============================================================================
// Main — Test cases
// =============================================================================

fn main() {
    println!("=== Week 22: Advanced Graphs ===\n");

    // --- Dijkstra ---
    println!("--- Dijkstra ---");
    // Graph: 0 --4-- 1 --1-- 3
    //        |       |       |
    //        2       2       3
    //        |       |       |
    //        2 --3-- 4 --5-- 3 (alternate path)
    let adj = vec![
        vec![(1, 4), (2, 2)],        // 0
        vec![(0, 4), (3, 1), (4, 2)], // 1
        vec![(0, 2), (4, 3)],        // 2
        vec![(1, 1), (4, 5)],        // 3
        vec![(1, 2), (2, 3), (3, 5)], // 4
    ];

    let dist = dijkstra(&adj, 0);
    println!("Shortest distances from vertex 0: {:?}", dist);
    assert_eq!(dist[0], 0);
    assert_eq!(dist[1], 4);
    assert_eq!(dist[2], 2);
    assert_eq!(dist[3], 5); // 0->1->3
    assert_eq!(dist[4], 5); // 0->2->4
    println!("PASS\n");

    // --- Bellman-Ford ---
    println!("--- Bellman-Ford ---");
    let edges = vec![
        (0, 1, 4),
        (0, 2, 2),
        (1, 3, 1),
        (1, 4, 2),
        (2, 4, 3),
        (3, 4, 5),
    ];

    match bellman_ford(&edges, 5, 0) {
        Some(dist) => {
            println!("Bellman-Ford distances from 0: {:?}", dist);
            assert_eq!(dist[0], 0);
            assert_eq!(dist[1], 4);
            assert_eq!(dist[3], 5);
        }
        None => panic!("No negative cycle expected"),
    }

    // Test with negative cycle
    let neg_cycle_edges = vec![
        (0, 1, 1),
        (1, 2, -1),
        (2, 0, -1), // Negative cycle: 0->1->2->0 has weight -1
    ];
    assert_eq!(bellman_ford(&neg_cycle_edges, 3, 0), None);
    println!("Negative cycle correctly detected");
    println!("PASS\n");

    // --- Floyd-Warshall ---
    println!("--- Floyd-Warshall ---");
    let inf = i64::MAX;
    let matrix = vec![
        vec![0,   3, inf, 7],
        vec![8,   0,   2, inf],
        vec![5, inf,   0,   1],
        vec![2, inf, inf,   0],
    ];

    let result = floyd_warshall(&matrix);
    println!("All-pairs shortest paths:");
    for (i, row) in result.iter().enumerate() {
        let formatted: Vec<String> = row.iter().map(|&d| {
            if d == inf { "INF".to_string() } else { d.to_string() }
        }).collect();
        println!("  From {}: {:?}", i, formatted);
    }
    assert_eq!(result[0][1], 3);
    assert_eq!(result[0][2], 5);
    assert_eq!(result[1][0], 5); // 1->2->3->0 = 2+1+2 = 5
    assert_eq!(result[3][1], 5); // 3->0->1 = 2+3 = 5
    println!("PASS\n");

    // --- DSU ---
    println!("--- Disjoint Set Union ---");
    let mut dsu = DSU::new(6);
    dsu.union(0, 1);
    dsu.union(2, 3);
    dsu.union(0, 2);

    assert_eq!(dsu.find(0), dsu.find(3)); // 0,1,2,3 in same set
    assert_ne!(dsu.find(0), dsu.find(4)); // 4 in different set
    println!("After union(0,1), union(2,3), union(0,2):");
    println!("  find(0) == find(3): {}", dsu.find(0) == dsu.find(3));
    println!("  find(0) == find(4): {}", dsu.find(0) == dsu.find(4));

    assert!(dsu.union(4, 5));    // Merge {4} and {5}
    assert!(!dsu.union(0, 1));   // Already same set — returns false
    println!("  union(4,5) = true (merged)");
    println!("  union(0,1) = false (already same set)");
    println!("PASS\n");

    // --- Kruskal's MST ---
    println!("--- Kruskal's MST ---");
    // Graph with 4 vertices:
    // 0--1 (weight 10), 0--2 (weight 6), 0--3 (weight 5),
    // 1--3 (weight 15), 2--3 (weight 4)
    let edges = vec![
        (0, 1, 10),
        (0, 2, 6),
        (0, 3, 5),
        (1, 3, 15),
        (2, 3, 4),
    ];

    let (total, mst_edges) = kruskal_mst(4, &edges);
    println!("MST edges: {:?}", mst_edges);
    println!("Total MST weight: {}", total);
    assert_eq!(mst_edges.len(), 3); // V - 1 edges
    assert_eq!(total, 19); // 4 + 5 + 10
    println!("PASS\n");

    println!("All Week 22 tests passed!");
}
