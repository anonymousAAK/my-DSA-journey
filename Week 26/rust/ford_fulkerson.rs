// WEEK 26 - RUST ADVANCED TOPICS
// Topic: Ford-Fulkerson Maximum Flow
// File: ford_fulkerson.rs
//
// CONCEPT:
//   Greedy max-flow: keep finding augmenting paths from source to sink in the
//   residual graph and pushing the bottleneck capacity. With DFS as the path
//   finder we get the classical Ford-Fulkerson algorithm.
//
// KEY POINTS:
//   - Maintain a residual graph: each forward edge (u,v) has a paired reverse
//     edge (v,u) with initial capacity 0. Pushing f along (u,v) decreases
//     forward capacity and increases the reverse one.
//   - DFS-driven; runtime O(E * max_flow) so prefer Edmonds-Karp / Dinic on
//     graphs with large flow values.
//
// ALGORITHM / APPROACH:
//   loop {
//       let pushed = dfs(s, t, INT_MAX);
//       if pushed == 0 { break; }
//       flow += pushed;
//   }
//
// RUST-SPECIFIC NOTES:
//   - Use a `Vec<Edge>` flat list and per-vertex `Vec<usize>` adjacency
//     containing edge indices. This sidesteps the borrow checker complaining
//     about simultaneous mutable references to nested vectors.
//   - `i64` for capacity / flow keeps headroom for big inputs.
//
// DRY RUN / EXAMPLE:
//   CLRS graph with V=6, source 0, sink 5 -> max flow = 23.
//
// COMPLEXITY:
//   Time:  O(E * max_flow)
//   Space: O(V + E)

#[derive(Clone, Debug)]
struct Edge {
    to: usize,
    cap: i64,
    rev: usize, // index in `edges` of the paired reverse edge
}

pub struct FordFulkerson {
    edges: Vec<Edge>,
    adj: Vec<Vec<usize>>, // adj[v] = indices into `edges`
}

impl FordFulkerson {
    pub fn new(n: usize) -> Self {
        Self { edges: Vec::new(), adj: vec![Vec::new(); n] }
    }

    pub fn add_edge(&mut self, u: usize, v: usize, cap: i64) {
        let m = self.edges.len();
        self.edges.push(Edge { to: v, cap,        rev: m + 1 });
        self.edges.push(Edge { to: u, cap: 0,     rev: m     });
        self.adj[u].push(m);
        self.adj[v].push(m + 1);
    }

    fn dfs(&mut self, u: usize, t: usize, pushed: i64, visited: &mut [bool]) -> i64 {
        if u == t { return pushed; }
        visited[u] = true;
        // Borrow split: clone the small Vec<usize> adjacency so we can mutate
        // self.edges freely during the recursion.
        let edges_idx = self.adj[u].clone();
        for &eid in &edges_idx {
            let (v, cap) = (self.edges[eid].to, self.edges[eid].cap);
            if !visited[v] && cap > 0 {
                let d = self.dfs(v, t, pushed.min(cap), visited);
                if d > 0 {
                    self.edges[eid].cap -= d;
                    let rev = self.edges[eid].rev;
                    self.edges[rev].cap += d;
                    return d;
                }
            }
        }
        0
    }

    pub fn max_flow(&mut self, s: usize, t: usize) -> i64 {
        let n = self.adj.len();
        let mut flow = 0i64;
        loop {
            let mut visited = vec![false; n];
            let pushed = self.dfs(s, t, i64::MAX, &mut visited);
            if pushed == 0 { return flow; }
            flow += pushed;
        }
    }
}

fn main() {
    let mut g = FordFulkerson::new(6);
    let edges = [
        (0,1,16),(0,2,13),(1,2,4),(1,3,12),
        (2,1,10),(2,4,14),(3,2,9),(3,5,20),
        (4,3,7), (4,5,4),
    ];
    for &(u, v, c) in &edges { g.add_edge(u, v, c); }
    println!("Ford-Fulkerson max flow (0 -> 5): {}", g.max_flow(0, 5)); // 23
}

// NOTES
// -----
// Differences from Java:
//   * Rust's borrow checker forbids holding two mutable refs into nested
//     vectors. We solve it by storing edges in a flat `Vec<Edge>` and
//     per-vertex `Vec<usize>` of indices.
//   * Cloning the small adjacency list inside DFS avoids `&mut self` /
//     `&self` aliasing while keeping the algorithm linear in edges visited.
//   * `i64::MAX` plays the role of Java's Integer.MAX_VALUE.
