// WEEK 26 - RUST ADVANCED TOPICS
// Topic: Dinic's Maximum Flow
// File: dinic.rs
//
// CONCEPT:
//   Dinic = phases of (BFS level graph, DFS blocking flow, iter pointer).
//   Each phase increases the s->t shortest distance by at least 1, giving
//   O(V) phases. With the iter pointer skipping dead edges, each phase
//   costs O(V*E), totalling O(V^2 * E). On unit-capacity graphs Dinic
//   matches Hopcroft-Karp at O(E*sqrt(V)).
//
// KEY POINTS:
//   - level[v] = BFS distance from source; only edges going level i ->
//     level i+1 are eligible for DFS.
//   - iter[u] = next adjacency index to try for vertex u in this phase.
//   - The blocking flow trick is a substantial constant-factor win.
//
// ALGORITHM / APPROACH:
//   while bfs(s, t):
//       reset iter[]
//       loop dfs(s, +inf) until 0 returned; flow += each push
//
// RUST-SPECIFIC NOTES:
//   - Flat edge vector + per-vertex index list (same idiom as elsewhere).
//   - Use `i64::MAX` for inf and `i64` for flow.
//
// DRY RUN / EXAMPLE:
//   CLRS graph -> max flow 23, typically in 2-3 phases.
//
// COMPLEXITY:
//   Time: O(V^2 * E)   Space: O(V + E)

use std::collections::VecDeque;

#[derive(Clone, Debug)]
struct Edge { to: usize, cap: i64, rev: usize }

pub struct Dinic {
    edges: Vec<Edge>,
    adj: Vec<Vec<usize>>,
    level: Vec<i32>,
    iter: Vec<usize>,
}

impl Dinic {
    pub fn new(n: usize) -> Self {
        Self { edges: vec![], adj: vec![Vec::new(); n], level: vec![-1; n], iter: vec![0; n] }
    }

    pub fn add_edge(&mut self, u: usize, v: usize, cap: i64) {
        let m = self.edges.len();
        self.edges.push(Edge { to: v, cap,    rev: m + 1 });
        self.edges.push(Edge { to: u, cap: 0, rev: m     });
        self.adj[u].push(m);
        self.adj[v].push(m + 1);
    }

    fn bfs(&mut self, s: usize, t: usize) -> bool {
        for x in self.level.iter_mut() { *x = -1; }
        self.level[s] = 0;
        let mut q = VecDeque::new();
        q.push_back(s);
        while let Some(u) = q.pop_front() {
            for &eid in &self.adj[u] {
                let v = self.edges[eid].to;
                if self.edges[eid].cap > 0 && self.level[v] < 0 {
                    self.level[v] = self.level[u] + 1;
                    q.push_back(v);
                }
            }
        }
        self.level[t] >= 0
    }

    fn dfs(&mut self, u: usize, t: usize, pushed: i64) -> i64 {
        if u == t { return pushed; }
        while self.iter[u] < self.adj[u].len() {
            let eid = self.adj[u][self.iter[u]];
            let v = self.edges[eid].to;
            let cap = self.edges[eid].cap;
            if cap > 0 && self.level[v] == self.level[u] + 1 {
                let d = self.dfs(v, t, pushed.min(cap));
                if d > 0 {
                    self.edges[eid].cap -= d;
                    let rev = self.edges[eid].rev;
                    self.edges[rev].cap += d;
                    return d;
                }
            }
            self.iter[u] += 1;
        }
        0
    }

    pub fn max_flow(&mut self, s: usize, t: usize) -> i64 {
        let mut flow = 0i64;
        while self.bfs(s, t) {
            for x in self.iter.iter_mut() { *x = 0; }
            loop {
                let pushed = self.dfs(s, t, i64::MAX);
                if pushed == 0 { break; }
                flow += pushed;
            }
        }
        flow
    }
}

fn main() {
    let mut g = Dinic::new(6);
    let edges = [
        (0,1,16),(0,2,13),(1,2,4),(1,3,12),
        (2,1,10),(2,4,14),(3,2,9),(3,5,20),
        (4,3,7), (4,5,4),
    ];
    for &(u, v, c) in &edges { g.add_edge(u, v, c); }
    println!("Dinic max flow (0 -> 5): {}", g.max_flow(0, 5)); // 23
}

// NOTES
// -----
// Differences from Java:
//   * Same flat-edge / per-vertex-index trick as the other Rust files to
//     navigate the borrow checker.
//   * Iteration over `self.adj[u]` indices avoids double-mutable-borrows.
//   * `i32` chosen for level (distance) and `usize` for iter pointer.
