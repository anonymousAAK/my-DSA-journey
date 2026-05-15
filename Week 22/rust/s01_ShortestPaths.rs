/*
 * WEEK 22 - RUST ADVANCED DSA
 * Topic: Shortest Path Algorithms (Dijkstra, Bellman-Ford, Floyd-Warshall)
 * File: 1.ShortestPaths.rs
 *
 * CONCEPT:
 *   Dijkstra:       single-source non-negative weights, O((V+E) log V).
 *   Bellman-Ford:   single-source allowing negatives, detects neg-cycles, O(V*E).
 *   Floyd-Warshall: all-pairs shortest paths via DP, O(V^3).
 *
 * KEY POINTS:
 *   - std::collections::BinaryHeap is a MAX-heap; wrap entries in
 *     `Reverse(...)` for min-heap behaviour.
 *   - Use i64 with INF = i64::MAX / 4 to avoid overflow on additions.
 *   - Adjacency list as Vec<Vec<(usize, i64)>>.
 *
 * ALGORITHM / APPROACH:
 *   See file header in Java reference; identical recurrences.
 *
 * RUST-SPECIFIC NOTES vs JAVA:
 *   - Borrow checker tradeoffs:
 *       * Reading neighbours requires only `&adj`, so we borrow it shared
 *         and mutate `dist` inside the loop without conflict.
 *       * For graph mutation (e.g., decrease-key), we'd need RefCell or
 *         indexed-only access; here Dijkstra uses lazy-deletion so we
 *         just push duplicates and check `if d > dist[u]`.
 *   - Pattern-match on `Reverse((d, u))` directly in `while let Some(...)`.
 *
 * DRY RUN (Dijkstra, undirected V=5):
 *   Edges (0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5),(3,4,3).
 *   Settle: 0(0), 2(1), 1(3), 3(4), 4(7).
 *   Final dist = [0, 3, 1, 4, 7].
 *
 * COMPLEXITY:
 *   Dijkstra:       O((V+E) log V).
 *   Bellman-Ford:   O(V*E).
 *   Floyd-Warshall: O(V^3).
 */

use std::cmp::Reverse;
use std::collections::BinaryHeap;

const INF: i64 = i64::MAX / 4;

pub fn dijkstra(adj: &Vec<Vec<(usize, i64)>>, src: usize) -> Vec<i64> {
    let v = adj.len();
    let mut dist = vec![INF; v];
    dist[src] = 0;
    let mut pq: BinaryHeap<Reverse<(i64, usize)>> = BinaryHeap::new();
    pq.push(Reverse((0, src)));
    while let Some(Reverse((d, u))) = pq.pop() {
        if d > dist[u] { continue; }
        for &(vtx, w) in &adj[u] {
            let nd = d + w;
            if nd < dist[vtx] {
                dist[vtx] = nd;
                pq.push(Reverse((nd, vtx)));
            }
        }
    }
    dist
}

pub fn bellman_ford(v: usize, edges: &[(usize, usize, i64)], src: usize) -> Option<Vec<i64>> {
    let mut dist = vec![INF; v];
    dist[src] = 0;
    for _ in 0..v - 1 {
        let mut updated = false;
        for &(u, w_v, w) in edges {
            if dist[u] != INF && dist[u] + w < dist[w_v] {
                dist[w_v] = dist[u] + w;
                updated = true;
            }
        }
        if !updated { break; }
    }
    for &(u, w_v, w) in edges {
        if dist[u] != INF && dist[u] + w < dist[w_v] {
            println!("Negative weight cycle detected!");
            return None;
        }
    }
    Some(dist)
}

pub fn floyd_warshall(v: usize, edges: &[(usize, usize, i64)]) -> Option<Vec<Vec<i64>>> {
    let mut d = vec![vec![INF; v]; v];
    for i in 0..v { d[i][i] = 0; }
    for &(u, w_v, w) in edges {
        if w < d[u][w_v] { d[u][w_v] = w; }
    }
    for k in 0..v {
        for i in 0..v {
            if d[i][k] == INF { continue; }
            for j in 0..v {
                if d[k][j] != INF && d[i][k] + d[k][j] < d[i][j] {
                    d[i][j] = d[i][k] + d[k][j];
                }
            }
        }
    }
    for i in 0..v { if d[i][i] < 0 { println!("Negative cycle!"); return None; } }
    Some(d)
}

fn main() {
    println!("=== Dijkstra ===");
    let v = 5;
    let mut adj: Vec<Vec<(usize, i64)>> = vec![vec![]; v];
    let edges = [(0,1,4i64),(0,2,1),(2,1,2),(1,3,1),(2,3,5),(3,4,3)];
    for &(u, w_v, w) in &edges {
        adj[u].push((w_v, w));
        adj[w_v].push((u, w)); // undirected
    }
    let d = dijkstra(&adj, 0);
    println!("Shortest distances from 0: {:?}", d);

    println!("\n=== Bellman-Ford ===");
    let bf: Vec<(usize, usize, i64)> = vec![
        (0,1,-1),(0,2,4),(1,2,3),(1,3,2),(1,4,2),(3,2,5),(3,1,1),(4,3,-3)
    ];
    println!("Shortest distances from 0: {:?}", bellman_ford(5, &bf, 0));

    println!("\n=== Floyd-Warshall ===");
    let fw: Vec<(usize, usize, i64)> = vec![
        (0,1,3),(0,3,7),(1,0,8),(1,2,2),(2,0,5),(2,3,1),(3,0,2)
    ];
    let ap = floyd_warshall(4, &fw).unwrap();
    println!("All-pairs shortest paths:");
    for row in &ap {
        for &x in row {
            if x >= INF / 2 { print!("{:>4}", "INF"); }
            else { print!("{:>4}", x); }
        }
        println!();
    }
}
