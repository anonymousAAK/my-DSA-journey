// Week 26: Network Flow & Matching
// ==================================
// Topics covered:
//   1. Ford-Fulkerson (DFS augmenting paths)      - O(E * max_flow)
//   2. Edmonds-Karp   (BFS augmenting paths)      - O(V * E^2)
//   3. Hopcroft-Karp  (bipartite matching)         - O(E * sqrt(V))
//   4. Hungarian Algorithm (min-cost assignment)   - O(N^3)

use std::collections::VecDeque;

// ===========================================================================
// Flow network using adjacency list
// ===========================================================================

#[derive(Clone)]
struct Edge {
    to: usize,
    cap: i64,
    rev: usize,
}

struct MaxFlowGraph {
    n: usize,
    graph: Vec<Vec<Edge>>,
}

impl MaxFlowGraph {
    fn new(n: usize) -> Self {
        MaxFlowGraph { n, graph: vec![vec![]; n] }
    }

    fn add_edge(&mut self, u: usize, v: usize, cap: i64) {
        let rev_u = self.graph[v].len();
        let rev_v = self.graph[u].len();
        self.graph[u].push(Edge { to: v, cap, rev: rev_u });
        self.graph[v].push(Edge { to: u, cap: 0, rev: rev_v });
    }

    // -------------------------------------------------------------------
    // 1. Ford-Fulkerson (DFS)
    //    Time:  O(E * max_flow)
    //    Space: O(V + E)
    // -------------------------------------------------------------------
    fn ff_dfs(&mut self, u: usize, t: usize, pushed: i64, visited: &mut Vec<bool>) -> i64 {
        if u == t { return pushed; }
        visited[u] = true;
        for i in 0..self.graph[u].len() {
            let v = self.graph[u][i].to;
            let cap = self.graph[u][i].cap;
            if !visited[v] && cap > 0 {
                let d = self.ff_dfs(v, t, pushed.min(cap), visited);
                if d > 0 {
                    let rev = self.graph[u][i].rev;
                    self.graph[u][i].cap -= d;
                    self.graph[v][rev].cap += d;
                    return d;
                }
            }
        }
        0
    }

    fn ford_fulkerson(&mut self, s: usize, t: usize) -> i64 {
        let mut flow = 0i64;
        loop {
            let mut visited = vec![false; self.n];
            let pushed = self.ff_dfs(s, t, i64::MAX, &mut visited);
            if pushed == 0 { break; }
            flow += pushed;
        }
        flow
    }

    // -------------------------------------------------------------------
    // 2. Edmonds-Karp (BFS)
    //    Time:  O(V * E^2)
    //    Space: O(V + E)
    // -------------------------------------------------------------------
    fn edmonds_karp(&mut self, s: usize, t: usize) -> i64 {
        let mut flow = 0i64;
        loop {
            // BFS to find shortest augmenting path
            let mut parent: Vec<Option<(usize, usize)>> = vec![None; self.n];
            parent[s] = Some((s, 0));
            let mut queue = VecDeque::new();
            queue.push_back(s);

            while let Some(u) = queue.pop_front() {
                if u == t { break; }
                for i in 0..self.graph[u].len() {
                    let v = self.graph[u][i].to;
                    if parent[v].is_none() && self.graph[u][i].cap > 0 {
                        parent[v] = Some((u, i));
                        queue.push_back(v);
                    }
                }
            }
            if parent[t].is_none() { break; }

            // Find bottleneck
            let mut bottleneck = i64::MAX;
            let mut v = t;
            while v != s {
                let (u, idx) = parent[v].unwrap();
                bottleneck = bottleneck.min(self.graph[u][idx].cap);
                v = u;
            }

            // Update residual graph
            v = t;
            while v != s {
                let (u, idx) = parent[v].unwrap();
                let rev = self.graph[u][idx].rev;
                self.graph[u][idx].cap -= bottleneck;
                self.graph[v][rev].cap += bottleneck;
                v = u;
            }
            flow += bottleneck;
        }
        flow
    }
}

// ===========================================================================
// 3. Hopcroft-Karp Bipartite Matching
//    Time:  O(E * sqrt(V))
//    Space: O(V + E)
// ===========================================================================

const NIL: usize = usize::MAX;

struct HopcroftKarp {
    left_size: usize,
    right_size: usize,
    adj: Vec<Vec<usize>>,
    match_left: Vec<usize>,
    match_right: Vec<usize>,
    dist: Vec<usize>,
}

impl HopcroftKarp {
    fn new(left_size: usize, right_size: usize) -> Self {
        HopcroftKarp {
            left_size,
            right_size,
            adj: vec![vec![]; left_size],
            match_left: vec![NIL; left_size],
            match_right: vec![NIL; right_size],
            dist: vec![0; left_size],
        }
    }

    fn add_edge(&mut self, u: usize, v: usize) {
        self.adj[u].push(v);
    }

    fn bfs(&mut self) -> bool {
        let mut queue = VecDeque::new();
        for u in 0..self.left_size {
            if self.match_left[u] == NIL {
                self.dist[u] = 0;
                queue.push_back(u);
            } else {
                self.dist[u] = usize::MAX;
            }
        }
        let mut found = false;
        while let Some(u) = queue.pop_front() {
            for &v in &self.adj[u] {
                let nxt = self.match_right[v];
                if nxt == NIL {
                    found = true;
                } else if self.dist[nxt] == usize::MAX {
                    self.dist[nxt] = self.dist[u] + 1;
                    queue.push_back(nxt);
                }
            }
        }
        found
    }

    fn dfs(&mut self, u: usize) -> bool {
        for i in 0..self.adj[u].len() {
            let v = self.adj[u][i];
            let nxt = self.match_right[v];
            if nxt == NIL || (self.dist[nxt] == self.dist[u] + 1 && self.dfs(nxt)) {
                self.match_left[u] = v;
                self.match_right[v] = u;
                return true;
            }
        }
        self.dist[u] = usize::MAX;
        false
    }

    fn max_matching(&mut self) -> usize {
        self.match_left = vec![NIL; self.left_size];
        self.match_right = vec![NIL; self.right_size];
        let mut matching = 0;
        while self.bfs() {
            for u in 0..self.left_size {
                if self.match_left[u] == NIL && self.dfs(u) {
                    matching += 1;
                }
            }
        }
        matching
    }

    fn get_matching(&self) -> Vec<(usize, usize)> {
        (0..self.left_size)
            .filter(|&u| self.match_left[u] != NIL)
            .map(|u| (u, self.match_left[u]))
            .collect()
    }
}

// ===========================================================================
// 4. Hungarian Algorithm (Minimum-Cost Perfect Assignment)
//    Time:  O(N^3)
//    Space: O(N^2)
// ===========================================================================

struct Hungarian {
    n: usize,
    cost: Vec<Vec<i64>>,
}

impl Hungarian {
    fn new(cost: Vec<Vec<i64>>) -> Self {
        let n = cost.len();
        Hungarian { n, cost }
    }

    fn solve(&self) -> (i64, Vec<usize>) {
        let n = self.n;
        let inf = i64::MAX / 2;

        let mut u = vec![0i64; n + 1];
        let mut v = vec![0i64; n + 1];
        let mut p = vec![0usize; n + 1];
        let mut way = vec![0usize; n + 1];

        for i in 1..=n {
            p[0] = i;
            let mut j0 = 0usize;
            let mut minv = vec![inf; n + 1];
            let mut used = vec![false; n + 1];

            loop {
                used[j0] = true;
                let i0 = p[j0];
                let mut delta = inf;
                let mut j1 = 0usize;

                for j in 1..=n {
                    if !used[j] {
                        let cur = self.cost[i0 - 1][j - 1] - u[i0] - v[j];
                        if cur < minv[j] {
                            minv[j] = cur;
                            way[j] = j0;
                        }
                        if minv[j] < delta {
                            delta = minv[j];
                            j1 = j;
                        }
                    }
                }
                for j in 0..=n {
                    if used[j] {
                        u[p[j]] += delta;
                        v[j] -= delta;
                    } else {
                        minv[j] -= delta;
                    }
                }
                j0 = j1;
                if p[j0] == 0 { break; }
            }

            loop {
                let j1 = way[j0];
                p[j0] = p[j1];
                j0 = j1;
                if j0 == 0 { break; }
            }
        }

        let mut assignment = vec![0usize; n];
        for j in 1..=n {
            assignment[p[j] - 1] = j - 1;
        }
        let total: i64 = (0..n).map(|i| self.cost[i][assignment[i]]).sum();
        (total, assignment)
    }
}

// ===========================================================================
// Demo / Driver
// ===========================================================================

fn main() {
    println!("{}", "=".repeat(60));
    println!("Week 26: Network Flow & Matching");
    println!("{}", "=".repeat(60));

    // --- Edmonds-Karp ---
    println!("\n--- Edmonds-Karp Max Flow ---");
    {
        let mut g = MaxFlowGraph::new(6);
        g.add_edge(0, 1, 16); g.add_edge(0, 2, 13);
        g.add_edge(1, 2, 4);  g.add_edge(1, 3, 12);
        g.add_edge(2, 1, 10); g.add_edge(2, 4, 14);
        g.add_edge(3, 2, 9);  g.add_edge(3, 5, 20);
        g.add_edge(4, 3, 7);  g.add_edge(4, 5, 4);
        println!("Max flow (0 -> 5): {}", g.edmonds_karp(0, 5)); // 23
    }

    // --- Ford-Fulkerson ---
    println!("\n--- Ford-Fulkerson Max Flow ---");
    {
        let mut g = MaxFlowGraph::new(6);
        g.add_edge(0, 1, 16); g.add_edge(0, 2, 13);
        g.add_edge(1, 2, 4);  g.add_edge(1, 3, 12);
        g.add_edge(2, 1, 10); g.add_edge(2, 4, 14);
        g.add_edge(3, 2, 9);  g.add_edge(3, 5, 20);
        g.add_edge(4, 3, 7);  g.add_edge(4, 5, 4);
        println!("Max flow (0 -> 5): {}", g.ford_fulkerson(0, 5)); // 23
    }

    // --- Hopcroft-Karp ---
    println!("\n--- Hopcroft-Karp Bipartite Matching ---");
    {
        let mut hk = HopcroftKarp::new(4, 4);
        hk.add_edge(0, 0); hk.add_edge(0, 1);
        hk.add_edge(1, 0); hk.add_edge(1, 2);
        hk.add_edge(2, 1); hk.add_edge(2, 3);
        hk.add_edge(3, 2); hk.add_edge(3, 3);
        println!("Maximum matching size: {}", hk.max_matching()); // 4
        print!("Matched pairs:");
        for (u, v) in hk.get_matching() {
            print!(" ({},{})", u, v);
        }
        println!();
    }

    // --- Hungarian ---
    println!("\n--- Hungarian Algorithm (Min-Cost Assignment) ---");
    {
        let cost_matrix = vec![
            vec![9, 2, 7, 8],
            vec![6, 4, 3, 7],
            vec![5, 8, 1, 8],
            vec![7, 6, 9, 4],
        ];
        let h = Hungarian::new(cost_matrix);
        let (total_cost, assignment) = h.solve();
        println!("Minimum cost: {}", total_cost); // 13
        print!("Assignment (row -> col):");
        for c in &assignment { print!(" {}", c); }
        println!();
    }
}
