/*
 * WEEK 17 - RUST DSA
 * Topic: Graph Representations + BFS / DFS
 * File: 1.GraphRepresentations.rs
 *
 * CONCEPT:
 *     A graph G = (V, E). Two storage shapes:
 *         Adjacency LIST   : Vec<Vec<usize>>          - O(V + E) space.
 *         Adjacency MATRIX : Vec<Vec<u8>> sized V*V    - O(V^2) space, O(1)
 *                                                       edge query.
 *     Both are demonstrated below.
 *
 * KEY POINTS:
 *     - BFS: VecDeque queue; explores level by level; shortest path on
 *       unweighted graphs; O(V + E).
 *     - DFS: recursion (or explicit Vec stack); foundation for cycle detection,
 *       components, topological sort; O(V + E).
 *     - Cycle in undirected graph: visited neighbour that isn't the recursion
 *       parent.
 *     - Bipartite check: 2-colour BFS; conflict implies an odd cycle.
 *
 * ALGORITHM / APPROACH:
 *     Standard textbook BFS / DFS templates as in the Java reference.
 *
 * RUST-SPECIFIC NOTES:
 *     BORROW CHECKER concerns for graph traversal:
 *       - You cannot borrow `self.adj` immutably while also mutating `visited`
 *         on `self`. Solution: keep `visited` as a local Vec<bool>, OR split
 *         the borrows by passing `&adj` and `&mut visited` separately to a
 *         private helper.
 *       - Recursion in Rust is fine; very deep graphs may overflow the stack
 *         (default ~8 MB) — use an iterative variant for V > 10^5.
 *     IDIOMS:
 *       - VecDeque<usize> is the right BFS queue (push_back / pop_front O(1)).
 *       - Vec<bool> for visited; usize for indices to interop with .len()/index.
 *       - `for &v in &adj[u]` to borrow without consuming.
 *
 * DRY RUN:
 *     Edges (undirected): 0-1,1-2,2-5,5-4,4-3,3-0,1-4
 *         BFS(0) -> [0,1,3,2,4,5]   (order depends on insertion order)
 *         DFS(0) -> [0,1,2,5,4,3]
 *         distances from 0 -> [0,1,2,1,2,2]
 *
 *     Disconnected: edges {0-1, 1-2, 3-4}, vertex 5 isolated
 *         components = 3
 *
 * COMPLEXITY:
 *     Build O(V+E); BFS/DFS O(V+E); components O(V+E);
 *     cycle / bipartite O(V+E).
 */

use std::collections::VecDeque;

pub struct Graph {
    pub v: usize,
    pub adj: Vec<Vec<usize>>,
}

impl Graph {
    pub fn new(v: usize) -> Self {
        Self { v, adj: vec![Vec::new(); v] }
    }

    pub fn add_edge(&mut self, u: usize, v: usize) {
        self.adj[u].push(v);
        self.adj[v].push(u);
    }
    pub fn add_directed_edge(&mut self, u: usize, v: usize) {
        self.adj[u].push(v);
    }

    pub fn bfs(&self, src: usize) -> Vec<usize> {
        let mut visited = vec![false; self.v];
        let mut order = Vec::new();
        let mut q: VecDeque<usize> = VecDeque::new();
        visited[src] = true;
        q.push_back(src);
        while let Some(u) = q.pop_front() {
            order.push(u);
            for &nb in &self.adj[u] {
                if !visited[nb] {
                    visited[nb] = true;
                    q.push_back(nb);
                }
            }
        }
        order
    }

    pub fn shortest_distances(&self, src: usize) -> Vec<i32> {
        let mut dist = vec![-1; self.v];
        dist[src] = 0;
        let mut q: VecDeque<usize> = VecDeque::from([src]);
        while let Some(u) = q.pop_front() {
            for &nb in &self.adj[u] {
                if dist[nb] == -1 {
                    dist[nb] = dist[u] + 1;
                    q.push_back(nb);
                }
            }
        }
        dist
    }

    pub fn dfs(&self, src: usize) -> Vec<usize> {
        let mut visited = vec![false; self.v];
        let mut order = Vec::new();
        // Pass &adj + &mut visited to avoid double-borrow on self.
        Self::dfs_helper(&self.adj, src, &mut visited, &mut order);
        order
    }
    fn dfs_helper(adj: &[Vec<usize>], u: usize,
                  visited: &mut [bool], order: &mut Vec<usize>) {
        visited[u] = true;
        order.push(u);
        for &v in &adj[u] {
            if !visited[v] {
                Self::dfs_helper(adj, v, visited, order);
            }
        }
    }

    pub fn count_components(&self) -> usize {
        let mut visited = vec![false; self.v];
        let mut count = 0;
        for i in 0..self.v {
            if !visited[i] {
                Self::component_dfs(&self.adj, i, &mut visited);
                count += 1;
            }
        }
        count
    }
    fn component_dfs(adj: &[Vec<usize>], u: usize, visited: &mut [bool]) {
        visited[u] = true;
        for &v in &adj[u] {
            if !visited[v] {
                Self::component_dfs(adj, v, visited);
            }
        }
    }

    // Cycle in UNDIRECTED graph
    pub fn has_cycle(&self) -> bool {
        let mut visited = vec![false; self.v];
        for i in 0..self.v {
            if !visited[i] && Self::cycle_dfs(&self.adj, i, None, &mut visited) {
                return true;
            }
        }
        false
    }
    fn cycle_dfs(adj: &[Vec<usize>], u: usize, parent: Option<usize>,
                 visited: &mut [bool]) -> bool {
        visited[u] = true;
        for &v in &adj[u] {
            if !visited[v] {
                if Self::cycle_dfs(adj, v, Some(u), visited) {
                    return true;
                }
            } else if Some(v) != parent {
                return true;
            }
        }
        false
    }

    pub fn is_bipartite(&self) -> bool {
        let mut color = vec![0i8; self.v];
        for start in 0..self.v {
            if color[start] != 0 { continue; }
            color[start] = 1;
            let mut q: VecDeque<usize> = VecDeque::from([start]);
            while let Some(u) = q.pop_front() {
                for &v in &self.adj[u] {
                    if color[v] == 0 {
                        color[v] = -color[u];
                        q.push_back(v);
                    } else if color[v] == color[u] {
                        return false;
                    }
                }
            }
        }
        true
    }
}

// MATRIX representation for completeness
pub struct GraphMatrix {
    pub v: usize,
    pub mat: Vec<Vec<u8>>,
}

impl GraphMatrix {
    pub fn new(v: usize) -> Self {
        Self { v, mat: vec![vec![0; v]; v] }
    }
    pub fn add_edge(&mut self, u: usize, v: usize) {
        self.mat[u][v] = 1;
        self.mat[v][u] = 1;
    }
    pub fn neighbours(&self, u: usize) -> Vec<usize> {
        (0..self.v).filter(|&v| self.mat[u][v] != 0).collect()
    }
}

fn main() {
    let mut g = Graph::new(6);
    for &(u, v) in &[(0,1),(1,2),(2,5),(5,4),(4,3),(3,0),(1,4)] {
        g.add_edge(u, v);
    }
    println!("BFS from 0: {:?}", g.bfs(0));
    println!("DFS from 0: {:?}", g.dfs(0));
    println!("Distances from 0: {:?}", g.shortest_distances(0));
    println!("Components: {}", g.count_components());
    println!("Has cycle: {}", g.has_cycle());
    println!("Bipartite: {}", g.is_bipartite());

    let mut g2 = Graph::new(6);
    g2.add_edge(0,1); g2.add_edge(1,2); g2.add_edge(3,4);
    println!("\nDisconnected components: {}", g2.count_components()); // 3
    println!("BFS from 0: {:?}", g2.bfs(0));

    let mut bip = Graph::new(5);
    for u in [0usize, 1] { for v in [2usize,3,4] { bip.add_edge(u, v); } }
    println!("\nK_{{2,3}} bipartite: {}", bip.is_bipartite());        // true

    let mut tri = Graph::new(3);
    tri.add_edge(0,1); tri.add_edge(1,2); tri.add_edge(2,0);
    println!("Triangle bipartite: {}", tri.is_bipartite());           // false

    let mut m = GraphMatrix::new(4);
    m.add_edge(0,1); m.add_edge(1,2); m.add_edge(2,3);
    println!("\nMatrix neighbours of 1: {:?}", m.neighbours(1));
}

/*
 * NOTES (Rust vs Java):
 *   - Borrow checker forbids holding `&self.adj` (immutable) and `&mut self`
 *     at the same time. Workaround: factor traversal into a free / associated
 *     fn that takes `&[Vec<usize>]` and `&mut [bool]` separately — both are
 *     fine because they're disjoint borrows.
 *   - VecDeque<T> is Rust's std queue (front/back O(1)).
 *   - Indexing uses usize; converting to/from i32 for distances requires a
 *     cast or storing as i32 from the start.
 *   - `Option<usize>` for the parent slot replaces Java's -1 sentinel.
 *   - Closures capturing `&mut` of two disjoint locals are fine; closures
 *     capturing two fields of `&mut self` are NOT — hence the helper fns.
 *   - No null; missing values are Option<T>.
 */
