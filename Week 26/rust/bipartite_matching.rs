// WEEK 26 - RUST ADVANCED TOPICS
// Topic: Bipartite Matching (Hopcroft-Karp + Kuhn)
// File: bipartite_matching.rs
//
// CONCEPT:
//   Maximum bipartite matching: largest set of edges with no shared
//   endpoints. Hopcroft-Karp finds vertex-disjoint shortest augmenting paths
//   per phase, achieving O(E*sqrt(V)). Kuhn's algorithm is the simpler
//   O(V*E) DFS approach.
//
// KEY POINTS:
//   - Augmenting path alternates unmatched/matched edges and starts/ends at
//     unmatched vertices.
//   - Hopcroft-Karp: BFS layers + DFS along the level graph; phases =
//     O(sqrt(V)).
//   - Kuhn: DFS from each unmatched left vertex.
//
// ALGORITHM / APPROACH (Hopcroft-Karp):
//   while bfs() finds augmenting path:
//       for each free left vertex u: dfs(u) augments along level graph
//
// RUST-SPECIFIC NOTES:
//   - Sentinel `usize::MAX` for NIL.
//   - `i32::MAX` for the BFS distance INF.
//
// DRY RUN / EXAMPLE:
//   L=R=4, edges (0-0,0-1,1-0,1-2,2-1,2-3,3-2,3-3) -> matching=4.
//
// COMPLEXITY:
//   Hopcroft-Karp: O(E*sqrt(V))
//   Kuhn:           O(V*E)

use std::collections::VecDeque;

const NIL: usize = usize::MAX;
const INF: i32 = i32::MAX;

pub struct HopcroftKarp {
    l: usize,
    r: usize,
    adj: Vec<Vec<usize>>,
    pub match_l: Vec<usize>,
    pub match_r: Vec<usize>,
    dist: Vec<i32>,
}

impl HopcroftKarp {
    pub fn new(l: usize, r: usize) -> Self {
        Self {
            l, r,
            adj: vec![Vec::new(); l],
            match_l: vec![NIL; l],
            match_r: vec![NIL; r],
            dist: vec![INF; l],
        }
    }

    pub fn add_edge(&mut self, u: usize, v: usize) { self.adj[u].push(v); }

    fn bfs(&mut self) -> bool {
        let mut q = VecDeque::new();
        for u in 0..self.l {
            if self.match_l[u] == NIL { self.dist[u] = 0; q.push_back(u); }
            else                       { self.dist[u] = INF; }
        }
        let mut found = false;
        while let Some(u) = q.pop_front() {
            for &v in &self.adj[u] {
                let p = self.match_r[v];
                if p == NIL { found = true; }
                else if self.dist[p] == INF {
                    self.dist[p] = self.dist[u] + 1;
                    q.push_back(p);
                }
            }
        }
        found
    }

    fn dfs(&mut self, u: usize) -> bool {
        // Clone the small adjacency to avoid double mutable borrows.
        let neighbours = self.adj[u].clone();
        for v in neighbours {
            let p = self.match_r[v];
            if p == NIL || (self.dist[p] == self.dist[u] + 1 && self.dfs(p)) {
                self.match_l[u] = v;
                self.match_r[v] = u;
                return true;
            }
        }
        self.dist[u] = INF;
        false
    }

    pub fn max_matching(&mut self) -> usize {
        self.match_l = vec![NIL; self.l];
        self.match_r = vec![NIL; self.r];
        self.dist    = vec![INF; self.l];
        let mut matching = 0;
        while self.bfs() {
            for u in 0..self.l {
                if self.match_l[u] == NIL && self.dfs(u) { matching += 1; }
            }
        }
        matching
    }
}

// Kuhn's simpler matcher
pub struct Kuhn { l: usize, r: usize, adj: Vec<Vec<usize>>, match_r: Vec<isize> }

impl Kuhn {
    pub fn new(l: usize, r: usize) -> Self {
        Self { l, r, adj: vec![Vec::new(); l], match_r: vec![-1; r] }
    }
    pub fn add_edge(&mut self, u: usize, v: usize) { self.adj[u].push(v); }

    fn try_kuhn(&mut self, u: usize, used: &mut [bool]) -> bool {
        let nb = self.adj[u].clone();
        for v in nb {
            if used[v] { continue; }
            used[v] = true;
            if self.match_r[v] == -1 || self.try_kuhn(self.match_r[v] as usize, used) {
                self.match_r[v] = u as isize;
                return true;
            }
        }
        false
    }

    pub fn max_matching(&mut self) -> usize {
        let mut pairs = 0;
        for u in 0..self.l {
            let mut used = vec![false; self.r];
            if self.try_kuhn(u, &mut used) { pairs += 1; }
        }
        pairs
    }
}

fn main() {
    let mut hk = HopcroftKarp::new(4, 4);
    let edges = [(0,0),(0,1),(1,0),(1,2),(2,1),(2,3),(3,2),(3,3)];
    for &(u, v) in &edges { hk.add_edge(u, v); }
    println!("Hopcroft-Karp matching: {}", hk.max_matching());
    print!("Pairs:");
    for u in 0..4 {
        if hk.match_l[u] != NIL { print!(" ({},{})", u, hk.match_l[u]); }
    }
    println!();

    let mut k = Kuhn::new(4, 4);
    for &(u, v) in &edges { k.add_edge(u, v); }
    println!("Kuhn matching:          {}", k.max_matching());
}

// NOTES
// -----
// Differences from Java:
//   * Sentinel `usize::MAX` (constant `NIL`) replaces Java's -1 for unmatched.
//   * Both algorithms live in one file so the reader can compare the two.
//   * Cloning small adjacency vectors in DFS avoids borrow-checker conflicts
//     while remaining O(deg(u)) per call.
