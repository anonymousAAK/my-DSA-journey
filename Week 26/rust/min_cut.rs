// WEEK 26 - RUST ADVANCED TOPICS
// Topic: Minimum s-t Cut via Max-Flow / Min-Cut Theorem
// File: min_cut.rs
//
// CONCEPT:
//   max-flow value == min-cut capacity. To extract the cut, run any max-flow
//   then BFS from source in the residual graph; the reachable set S and its
//   complement T form the cut. Original forward edges crossing S->T are the
//   cut edges.
//
// KEY POINTS:
//   - Tag every edge with `original` to distinguish from auto-reverse pairs.
//   - Remember the original capacity so we can report cut capacities after
//     residual mutation.
//
// ALGORITHM / APPROACH:
//   run max-flow
//   BFS in residual graph from s
//   collect every original edge u in S -> v in T
//
// RUST-SPECIFIC NOTES:
//   - Use a struct Edge with fields (to, cap, rev, original, orig_cap).
//   - Returning a tuple (i64, Vec<(usize,usize,i64)>) is idiomatic.
//
// DRY RUN / EXAMPLE:
//   CLRS graph -> max flow 23. Reachable from 0 is {0,2,4}; cut edges
//   include (0,1)=16 and (4,3)=7 etc., summing to 23.
//
// COMPLEXITY:
//   max-flow time + O(V+E) extraction.

use std::collections::VecDeque;

#[derive(Clone, Debug)]
struct Edge { to: usize, cap: i64, rev: usize, original: bool, orig_cap: i64 }

pub struct MinCut { edges: Vec<Edge>, adj: Vec<Vec<usize>> }

impl MinCut {
    pub fn new(n: usize) -> Self { Self { edges: vec![], adj: vec![Vec::new(); n] } }

    pub fn add_edge(&mut self, u: usize, v: usize, cap: i64) {
        let m = self.edges.len();
        self.edges.push(Edge { to: v, cap, rev: m+1, original: true,  orig_cap: cap });
        self.edges.push(Edge { to: u, cap: 0, rev: m, original: false, orig_cap: 0 });
        self.adj[u].push(m);
        self.adj[v].push(m + 1);
    }

    fn max_flow(&mut self, s: usize, t: usize) -> i64 {
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
            let mut b = i64::MAX;
            let mut v = t;
            while v != s { b = b.min(self.edges[parent_edge[v]].cap); v = parent[v]; }
            let mut v = t;
            while v != s {
                let eid = parent_edge[v];
                let rev = self.edges[eid].rev;
                self.edges[eid].cap -= b;
                self.edges[rev].cap += b;
                v = parent[v];
            }
            flow += b;
        }
    }

    fn reachable_from(&self, s: usize) -> Vec<bool> {
        let n = self.adj.len();
        let mut vis = vec![false; n];
        vis[s] = true;
        let mut q = VecDeque::new();
        q.push_back(s);
        while let Some(u) = q.pop_front() {
            for &eid in &self.adj[u] {
                let e = &self.edges[eid];
                if e.cap > 0 && !vis[e.to] { vis[e.to] = true; q.push_back(e.to); }
            }
        }
        vis
    }

    pub fn min_cut(&mut self, s: usize, t: usize) -> (i64, Vec<(usize, usize, i64)>) {
        let flow = self.max_flow(s, t);
        let side = self.reachable_from(s);
        let mut cut = vec![];
        for u in 0..self.adj.len() {
            if !side[u] { continue; }
            for &eid in &self.adj[u] {
                let e = &self.edges[eid];
                if e.original && !side[e.to] {
                    cut.push((u, e.to, e.orig_cap));
                }
            }
        }
        (flow, cut)
    }
}

fn main() {
    let mut g = MinCut::new(6);
    let edges = [
        (0,1,16),(0,2,13),(1,2,4),(1,3,12),
        (2,1,10),(2,4,14),(3,2,9),(3,5,20),
        (4,3,7), (4,5,4),
    ];
    for &(u, v, c) in &edges { g.add_edge(u, v, c); }
    let (flow, cut) = g.min_cut(0, 5);
    println!("Max flow / Min cut value: {}", flow);
    println!("Cut edges:");
    for (u, v, c) in cut {
        println!("  ({} -> {}) capacity {}", u, v, c);
    }
}

// NOTES
// -----
// Differences from Java:
//   * Java's network_flow.java focuses on max-flow, matching, and Hungarian
//     assignment; explicit min-cut extraction is added here for completeness.
//   * Edges carry `original` and `orig_cap` so cut capacities are reportable
//     after residual updates.
