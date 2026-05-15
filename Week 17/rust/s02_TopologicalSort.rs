/*
 * WEEK 17 - RUST DSA
 * Topic: Topological Sort (DFS post-order + Kahn's BFS)
 * File: 2.TopologicalSort.rs
 *
 * CONCEPT:
 *     A topological order of a DAG is a linear sequence in which every
 *     directed edge u -> v has u BEFORE v. Two algorithms:
 *         DFS post-order  -- push v after recursing all its successors,
 *                            then reverse the stack.
 *         Kahn (BFS)      -- repeatedly emit vertices with indegree 0.
 *     Kahn doubles as a cycle detector.
 *
 * KEY POINTS:
 *     - Multiple valid orders may exist for the same DAG.
 *     - Kahn returns Option<Vec<usize>>; None means the graph has a cycle.
 *     - 3-colour DFS detects cycles in directed graphs without producing
 *       any order.
 *
 * ALGORITHM / APPROACH:
 *     Kahn:
 *         indeg = vector of in-degrees
 *         queue = nodes with indeg == 0
 *         while queue:
 *             u = pop_front; result.push(u)
 *             for v in adj[u]: if --indeg[v] == 0: queue.push_back(v)
 *         if result.len() == V -> Some(result), else None
 *
 * RUST-SPECIFIC NOTES:
 *     BORROW CHECKER:
 *       - DFS calls itself recursively while needing &mut visited and
 *         &mut stack. Pass &[Vec<usize>] (immutable adj) and the &mut bookkeeping
 *         to a free / associated fn so the borrows don't overlap.
 *     IDIOMS:
 *       - VecDeque for the FIFO queue.
 *       - Returning Option<Vec<usize>> mirrors Java's null sentinel cleanly.
 *       - Use `enum State { White, Grey, Black }` for the colour DFS.
 *
 * DRY RUN:
 *     Edges 5->2, 5->0, 4->0, 4->1, 2->3, 3->1
 *         indeg = [2,2,1,1,0,0]
 *         queue = [4,5]
 *         emit 4 -> [-,1,-,-,-,-] (decrement indeg[0],[1])
 *         emit 5 -> indeg[2]->0 push 2; indeg[0]->0 push 0
 *         emit 2 -> indeg[3]->0 push 3
 *         emit 0
 *         emit 3 -> indeg[1]->0 push 1
 *         emit 1
 *         result = [4,5,2,0,3,1]   (length == V, valid)
 *
 *     Cycle 0->1->2->3->1: indeg=[0,2,1,1]; queue=[0]
 *         emit 0 -> indeg[1]->1; queue empty
 *         result.len() == 1 < 4 -> None.
 *
 * COMPLEXITY: O(V + E) time, O(V) extra space.
 */

use std::collections::VecDeque;

pub struct DiGraph {
    pub v: usize,
    pub adj: Vec<Vec<usize>>,
}

impl DiGraph {
    pub fn new(v: usize) -> Self {
        Self { v, adj: vec![Vec::new(); v] }
    }
    pub fn add_edge(&mut self, u: usize, v: usize) { self.adj[u].push(v); }

    // APPROACH 1: DFS post-order
    pub fn topo_sort_dfs(&self) -> Vec<usize> {
        let mut visited = vec![false; self.v];
        let mut stack: Vec<usize> = Vec::with_capacity(self.v);
        for i in 0..self.v {
            if !visited[i] {
                Self::dfs(&self.adj, i, &mut visited, &mut stack);
            }
        }
        stack.reverse();
        stack
    }
    fn dfs(adj: &[Vec<usize>], u: usize,
           visited: &mut [bool], stack: &mut Vec<usize>) {
        visited[u] = true;
        for &v in &adj[u] {
            if !visited[v] {
                Self::dfs(adj, v, visited, stack);
            }
        }
        stack.push(u);
    }

    // APPROACH 2: Kahn's algorithm; returns None on cycle
    pub fn topo_sort_kahn(&self) -> Option<Vec<usize>> {
        let mut indeg = vec![0usize; self.v];
        for u in 0..self.v {
            for &v in &self.adj[u] {
                indeg[v] += 1;
            }
        }
        let mut q: VecDeque<usize> =
            (0..self.v).filter(|&i| indeg[i] == 0).collect();

        let mut result = Vec::with_capacity(self.v);
        while let Some(u) = q.pop_front() {
            result.push(u);
            for &v in &self.adj[u] {
                indeg[v] -= 1;
                if indeg[v] == 0 { q.push_back(v); }
            }
        }
        if result.len() == self.v { Some(result) } else { None }
    }

    // 3-colour cycle detection (state codes: 0=white, 1=grey, 2=black)
    pub fn has_cycle(&self) -> bool {
        let mut state = vec![0u8; self.v];
        for i in 0..self.v {
            if state[i] == 0 && Self::cycle_dfs(&self.adj, i, &mut state) {
                return true;
            }
        }
        false
    }
    fn cycle_dfs(adj: &[Vec<usize>], u: usize, state: &mut [u8]) -> bool {
        state[u] = 1;                         // grey
        for &v in &adj[u] {
            if state[v] == 1 { return true; } // back-edge -> cycle
            if state[v] == 0 && Self::cycle_dfs(adj, v, state) { return true; }
        }
        state[u] = 2;                         // black
        false
    }
}

fn main() {
    let mut g = DiGraph::new(6);
    for &(u, v) in &[(5,2),(5,0),(4,0),(4,1),(2,3),(3,1)] {
        g.add_edge(u, v);
    }
    println!("DFS topological sort:  {:?}", g.topo_sort_dfs());
    println!("Kahn topological sort: {:?}", g.topo_sort_kahn());
    println!("Has cycle: {}", g.has_cycle());           // false

    let mut cyc = DiGraph::new(4);
    for &(u, v) in &[(0,1),(1,2),(2,3),(3,1)] { cyc.add_edge(u, v); }
    println!("\nCyclic graph:");
    println!("Has cycle: {}", cyc.has_cycle());         // true
    println!("Kahn (cycle => None): {:?}", cyc.topo_sort_kahn());

    println!("\n=== Build System ===");
    let mut build = DiGraph::new(5);                    // 0 download .. 4 deploy
    for &(u, v) in &[(0,1),(1,2),(1,3),(2,3),(3,4)] {
        build.add_edge(u, v);
    }
    println!("Build order: {:?}", build.topo_sort_kahn());
}

/*
 * NOTES (Rust vs Java):
 *   - Java's null sentinel becomes Option<T>. Pattern-match with `if let`.
 *   - Recursive DFS over Vec<Vec<usize>> needs care: we factor the recursion
 *     into a free function that takes the slice + the &mut visited/stack
 *     arrays disjointly, satisfying the borrow checker.
 *   - The 3-colour enum is a single-byte type; nicer than Java's int constants.
 *   - VecDeque is Rust's std queue; collecting from a filtered range gives us
 *     the seed queue in one expression.
 *   - Decrementing a usize that might become negative is undefined; we only
 *     decrement after confirming it's > 0 (Kahn guarantees this).
 */
