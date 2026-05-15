/*
 * WEEK 22 - RUST ADVANCED DSA
 * Topic: Minimum Spanning Tree (Kruskal + Prim) & Union-Find
 * File: 2.MinimumSpanningTree.rs
 *
 * CONCEPT:
 *   MST: spanning tree (V-1 edges, all vertices reached, no cycle) with
 *   minimum total weight. Two greedy algorithms:
 *     - Kruskal: sort edges, add if no cycle (DSU).
 *     - Prim:    grow MST greedily from one vertex via min-heap.
 *
 * KEY POINTS:
 *   - DSU with path compression + union by rank ~ O(alpha(n)).
 *   - BinaryHeap is max-heap; use Reverse for min-heap behaviour.
 *   - Prim is structurally identical to Dijkstra except we sum edge
 *     weights and only relax when ew < key[v].
 *
 * ALGORITHM / APPROACH:
 *   DSU.find: iterative with path compression to avoid recursion limits.
 *   DSU.union: rank-based; returns false if already same set.
 *   Kruskal: sort edges, accumulate while in different sets.
 *   Prim: lazy-deletion pattern from Dijkstra.
 *
 * RUST-SPECIFIC NOTES vs JAVA:
 *   - DSU's find needs &mut self for path compression.
 *   - Borrow checker note: when reading adjacency list during Prim, we
 *     hold a shared borrow of `&adj` and mutate `key`/`in_mst` via index
 *     access — no aliasing conflict.
 *   - Sorting edges: `Vec<(usize,usize,i64)>` and sort_by_key on weight.
 *
 * DRY RUN:
 *   V=4, edges (0,1,4),(0,2,3),(1,2,1),(1,3,2),(2,3,4).
 *   Sorted by weight: (1,2,1),(1,3,2),(0,2,3),(0,1,4),(2,3,4).
 *   Kruskal picks (1,2,1) [union], (1,3,2) [union], (0,2,3) [union].
 *   Total = 6. Done after V-1=3 edges.
 *
 * COMPLEXITY:
 *   DSU op: ~O(alpha(n)).
 *   Kruskal: O(E log E).
 *   Prim:    O((V+E) log V).
 */

use std::cmp::Reverse;
use std::collections::BinaryHeap;

pub struct DSU {
    parent: Vec<usize>,
    rank: Vec<u32>,
}

impl DSU {
    pub fn new(n: usize) -> Self {
        DSU { parent: (0..n).collect(), rank: vec![0; n] }
    }

    pub fn find(&mut self, x: usize) -> usize {
        let mut root = x;
        while self.parent[root] != root {
            root = self.parent[root];
        }
        let mut cur = x;
        while self.parent[cur] != root {
            let nxt = self.parent[cur];
            self.parent[cur] = root;
            cur = nxt;
        }
        root
    }

    pub fn union(&mut self, x: usize, y: usize) -> bool {
        let mut px = self.find(x);
        let mut py = self.find(y);
        if px == py { return false; }
        if self.rank[px] < self.rank[py] { std::mem::swap(&mut px, &mut py); }
        self.parent[py] = px;
        if self.rank[px] == self.rank[py] { self.rank[px] += 1; }
        true
    }

    pub fn connected(&mut self, x: usize, y: usize) -> bool {
        self.find(x) == self.find(y)
    }
}

pub fn kruskal_mst(v: usize, mut edges: Vec<(usize, usize, i64)>) -> i64 {
    edges.sort_by_key(|e| e.2);
    let mut dsu = DSU::new(v);
    let mut total = 0i64;
    let mut used = 0usize;
    println!("Kruskal MST edges:");
    for (u, w_v, w) in edges {
        if used == v - 1 { break; }
        if dsu.union(u, w_v) {
            total += w;
            used += 1;
            println!("  Edge ({} - {}): weight {}", u, w_v, w);
        }
    }
    total
}

pub fn prim_mst(v: usize, adj: &Vec<Vec<(usize, i64)>>) -> i64 {
    let mut in_mst = vec![false; v];
    let mut key = vec![i64::MAX; v];
    let mut parent = vec![usize::MAX; v];
    key[0] = 0;
    let mut pq: BinaryHeap<Reverse<(i64, usize)>> = BinaryHeap::new();
    pq.push(Reverse((0, 0)));
    let mut total = 0i64;
    println!("Prim MST edges:");
    while let Some(Reverse((w, u))) = pq.pop() {
        if in_mst[u] { continue; }
        in_mst[u] = true;
        total += w;
        if parent[u] != usize::MAX {
            println!("  Edge ({} - {}): weight {}", parent[u], u, w);
        }
        for &(vtx, ew) in &adj[u] {
            if !in_mst[vtx] && ew < key[vtx] {
                key[vtx] = ew;
                parent[vtx] = u;
                pq.push(Reverse((ew, vtx)));
            }
        }
    }
    total
}

fn main() {
    let v = 4;
    let edges: Vec<(usize, usize, i64)> = vec![(0,1,4),(0,2,3),(1,2,1),(1,3,2),(2,3,4)];

    println!("=== Kruskal's MST ===");
    println!("Total MST weight: {}", kruskal_mst(v, edges.clone()));

    let mut adj: Vec<Vec<(usize, i64)>> = vec![vec![]; v];
    for &(u, w_v, w) in &edges {
        adj[u].push((w_v, w));
        adj[w_v].push((u, w));
    }
    println!("\n=== Prim's MST ===");
    println!("Total MST weight: {}", prim_mst(v, &adj));

    println!("\n=== Union-Find Demo ===");
    let mut dsu = DSU::new(6);
    dsu.union(0, 1); dsu.union(2, 3); dsu.union(4, 5);
    println!("0 connected to 1: {}", dsu.connected(0, 1));
    println!("0 connected to 2: {}", dsu.connected(0, 2));
    dsu.union(0, 2);
    println!("0 connected to 3: {}", dsu.connected(0, 3));
}
