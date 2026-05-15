/*
 * WEEK 24 - RUST ADVANCED DSA
 * Topic: NP-Completeness & Approximation Algorithms
 * File: 2.NPCompletenessAndApproximation.rs
 *
 * CONCEPT:
 *   P:           polynomial-time solvable.
 *   NP:          polynomial-time verifiable.
 *   NP-Complete: in NP and every NP problem reduces to it (poly time).
 *   Approximation algorithms give bounded ratio guarantees vs OPT:
 *     - Vertex Cover: 2-approximation via maximal matching.
 *     - Set Cover:    O(log n) greedy.
 *     - Metric TSP:   2-approximation via MST + DFS preorder.
 *
 * KEY POINTS:
 *   - Vertex cover: take BOTH endpoints of any uncovered edge.
 *   - Set cover greedy: pick the set covering most uncovered elements.
 *   - Triangle inequality enables MST-based TSP shortcutting.
 *
 * ALGORITHM / APPROACH:
 *   Same as Java reference.
 *
 * RUST-SPECIFIC NOTES vs JAVA:
 *   - Use HashSet<usize> / BTreeSet<usize> for the cover & uncovered sets.
 *   - DFS uses a Vec<usize> as an explicit stack to avoid recursion.
 *   - The borrow checker is friendly here: read-only graph plus mutable
 *     cover/uncovered sets.
 *
 * DRY RUN:
 *   Vertex cover edges {(0,1),(0,2),(1,3),(2,3),(3,4)}:
 *     Process (0,1) -> add 0,1. (0,2): 0 covered, skip.
 *     (1,3): 1 covered, skip. (2,3) -> add 2,3. (3,4): 3 covered, skip.
 *     Cover {0,1,2,3} (size 4). OPT {0,3} (size 2).
 *
 * COMPLEXITY:
 *   Vertex cover: O(E). Set cover: ~O(|sets| * |U|) per iteration.
 *   TSP 2-approx: O(V^2) Prim + O(V) DFS.
 */

use std::collections::{BTreeSet, HashSet};

pub fn vertex_cover_2approx(v: usize, edges: &[(usize, usize)]) -> BTreeSet<usize> {
    let mut covered = vec![false; v];
    let mut cover = BTreeSet::new();
    for &(u, w) in edges {
        if !covered[u] && !covered[w] {
            covered[u] = true; covered[w] = true;
            cover.insert(u); cover.insert(w);
        }
    }
    cover
}

pub fn setcover_greedy(universe_size: usize, sets: &[HashSet<usize>]) -> Vec<usize> {
    let mut uncovered: HashSet<usize> = (0..universe_size).collect();
    let mut chosen: Vec<usize> = Vec::new();
    while !uncovered.is_empty() {
        let mut best = None;
        let mut best_cnt = 0;
        for (i, s) in sets.iter().enumerate() {
            let cnt = s.iter().filter(|x| uncovered.contains(x)).count();
            if cnt > best_cnt { best_cnt = cnt; best = Some(i); }
        }
        match best {
            Some(i) => {
                for x in &sets[i] { uncovered.remove(x); }
                chosen.push(i);
            }
            None => break,
        }
    }
    chosen
}

pub fn tsp_2approx(dist: &Vec<Vec<i32>>) -> Vec<usize> {
    let n = dist.len();
    let mut in_mst = vec![false; n];
    let mut parent = vec![usize::MAX; n];
    let mut key = vec![i32::MAX; n];
    key[0] = 0;
    for _ in 0..n - 1 {
        let mut u = usize::MAX;
        for v in 0..n {
            if !in_mst[v] && (u == usize::MAX || key[v] < key[u]) { u = v; }
        }
        in_mst[u] = true;
        for v in 0..n {
            if !in_mst[v] && dist[u][v] < key[v] { key[v] = dist[u][v]; parent[v] = u; }
        }
    }
    let mut mst: Vec<Vec<usize>> = vec![vec![]; n];
    for i in 1..n {
        mst[parent[i]].push(i);
        mst[i].push(parent[i]);
    }
    let mut visited = vec![false; n];
    let mut tour: Vec<usize> = Vec::new();
    let mut stack: Vec<usize> = vec![0];
    while let Some(u) = stack.pop() {
        if visited[u] { continue; }
        visited[u] = true;
        tour.push(u);
        for i in (0..mst[u].len()).rev() {
            let v = mst[u][i];
            if !visited[v] { stack.push(v); }
        }
    }
    let mut cost = 0i32;
    for i in 0..n { cost += dist[tour[i]][tour[(i + 1) % n]]; }
    println!("TSP 2-Approx tour: {:?}, cost: {}", tour, cost);
    tour
}

fn main() {
    println!("=== Vertex Cover (2-approximation) ===");
    let edges = vec![(0,1),(0,2),(1,3),(2,3),(3,4)];
    let cover = vertex_cover_2approx(5, &edges);
    println!("2-approx vertex cover: {:?}", cover);
    println!("Cover size: {}", cover.len());

    println!("\n=== Set Cover (greedy) ===");
    let sets: Vec<HashSet<usize>> = vec![
        [0,1,2].iter().copied().collect(),
        [3,4,5].iter().copied().collect(),
        [4,5,6,7].iter().copied().collect(),
        [0,3,8].iter().copied().collect(),
        [2,7,9].iter().copied().collect(),
    ];
    let chosen = setcover_greedy(10, &sets);
    println!("Chosen set indices: {:?}", chosen);

    println!("\n=== TSP 2-Approximation (metric) ===");
    let dist = vec![
        vec![0,10,15,20],
        vec![10,0,35,25],
        vec![15,35,0,30],
        vec![20,25,30,0],
    ];
    tsp_2approx(&dist);
    println!("(Optimal tour cost for this instance: 80)");

    println!("\n=== P vs NP Key Points ===");
    println!("- P: problems solvable in poly time (sorting, shortest path, MST)");
    println!("- NP: problems verifiable in poly time (TSP, vertex cover, 3-SAT)");
    println!("- NP-Hard: at least as hard as NP-Complete problems");
    println!("- If P=NP, all encryption would break (RSA, AES rely on hard problems)");
    println!("- Most believe P!=NP (Clay Millennium Prize: $1M for proof)");
    println!("- Approximation algorithms: practical solutions with quality guarantees");
}
