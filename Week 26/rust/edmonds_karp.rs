// WEEK 26 - RUST ADVANCED TOPICS
// Topic: Edmonds-Karp Maximum Flow
// File: edmonds_karp.rs
//
// CONCEPT:
//   Ford-Fulkerson with BFS for augmenting-path discovery: each path is the
//   shortest in number of edges, guaranteeing O(V * E^2) total work.
//
// KEY POINTS:
//   - BFS gives shortest-path augmentation -> bound is independent of cap.
//   - Reconstruct path via parent[] and parent_edge[] arrays.
//   - Same residual-graph trick as Ford-Fulkerson.
//
// ALGORITHM / APPROACH:
//   while BFS finds augmenting path s -> t:
//       compute bottleneck
//       update forward/reverse residuals
//       flow += bottleneck
//
// RUST-SPECIFIC NOTES:
//   - Use `VecDeque<usize>` for BFS queue.
//   - Flat edge storage to keep the borrow checker happy.
//   - `Option<usize>` could express the parent sentinel; we use `usize::MAX`
//     instead, mirroring Java's -1 idiom while keeping the type simple.
//
// DRY RUN / EXAMPLE:
//   CLRS graph -> max flow 23 in three augmenting paths.
//
// COMPLEXITY:
//   Time: O(V * E^2)   Space: O(V + E)

use std::collections::VecDeque;

#[derive(Clone, Debug)]
struct Edge { to: usize, cap: i64, rev: usize }

pub struct EdmondsKarp { edges: Vec<Edge>, adj: Vec<Vec<usize>> }

impl EdmondsKarp {
    pub fn new(n: usize) -> Self { Self { edges: vec![], adj: vec![Vec::new(); n] } }

    pub fn add_edge(&mut self, u: usize, v: usize, cap: i64) {
        let m = self.edges.len();
        self.edges.push(Edge { to: v, cap,    rev: m + 1 });
        self.edges.push(Edge { to: u, cap: 0, rev: m     });
        self.adj[u].push(m);
        self.adj[v].push(m + 1);
    }

    pub fn max_flow(&mut self, s: usize, t: usize) -> i64 {
        let n = self.adj.len();
        let none = usize::MAX;
        let mut flow = 0i64;
        loop {
            let mut parent = vec![none; n];
            let mut parent_edge = vec![none; n];
            parent[s] = s;
            let mut q = VecDeque::new();
            q.push_back(s);
            while let Some(u) = q.pop_front() {
                if parent[t] != none { break; }
                for &eid in &self.adj[u] {
                    let v = self.edges[eid].to;
                    if parent[v] == none && self.edges[eid].cap > 0 {
                        parent[v] = u;
                        parent_edge[v] = eid;
                        q.push_back(v);
                    }
                }
            }
            if parent[t] == none { return flow; }
            let mut bottleneck = i64::MAX;
            let mut v = t;
            while v != s {
                bottleneck = bottleneck.min(self.edges[parent_edge[v]].cap);
                v = parent[v];
            }
            let mut v = t;
            while v != s {
                let eid = parent_edge[v];
                let rev = self.edges[eid].rev;
                self.edges[eid].cap -= bottleneck;
                self.edges[rev].cap += bottleneck;
                v = parent[v];
            }
            flow += bottleneck;
        }
    }
}

fn main() {
    let mut g = EdmondsKarp::new(6);
    let edges = [
        (0,1,16),(0,2,13),(1,2,4),(1,3,12),
        (2,1,10),(2,4,14),(3,2,9),(3,5,20),
        (4,3,7), (4,5,4),
    ];
    for &(u, v, c) in &edges { g.add_edge(u, v, c); }
    println!("Edmonds-Karp max flow (0 -> 5): {}", g.max_flow(0, 5)); // 23
}

// NOTES
// -----
// Differences from Java:
//   * `VecDeque` replaces java.util.LinkedList/ArrayDeque.
//   * usize::MAX serves as the "no parent" sentinel in lieu of -1.
//   * The flat Vec<Edge> + per-vertex Vec<usize> idiom keeps the borrow
//     checker satisfied during in-place residual updates.
