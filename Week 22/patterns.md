# Week 22 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which shortest-path/MST pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given a directed weighted graph (non-negative weights) with n ≤ 10^4 nodes and m ≤ 5·10^4 edges, find the shortest path from `s` to every other vertex.
Pattern: ______
Why: ______

### 2. Given a directed graph that may contain negative edge weights (no negative cycles), find shortest distances from `s`. n ≤ 500.
Pattern: ______
Why: ______

### 3. Given a directed weighted graph with up to 400 nodes, find shortest distances between *every pair* of nodes.
Pattern: ______
Why: ______

### 4. Given an undirected weighted graph, build a minimum spanning tree. n ≤ 10^5, m ≤ 2·10^5.
Pattern: ______
Why: ______

### 5. Given a directed weighted graph, find the cheapest flight from src to dst with at most k stops. n ≤ 100, m ≤ 10^4.
Pattern: ______
Why: ______

### 6. Distractor: Given an undirected unweighted graph, find the shortest path from `s` to `t`. (Dijkstra?)
Pattern: ______
Why: ______

### 7. Given a network of n routers and edge latencies, find the time it takes for a signal from node `k` to reach every node, or report unreachable.
Pattern: ______
Why: ______

### 8. Given a graph and edge probabilities of success, find the path from `s` to `t` that maximizes the product of edge probabilities.
Pattern: ______
Why: ______

### 9. Given a connected weighted undirected graph, detect whether it contains a negative-weight cycle. n ≤ 500.
Pattern: ______
Why: ______

### 10. Distractor: Given a weighted undirected graph, find the *maximum* spanning tree. (New algorithm?)
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Dijkstra with priority queue. **Why**: non-negative weights, single source — O((n+m) log n).
2. **Pattern**: Bellman–Ford. **Why**: handles negative edges; n·m relaxations.
3. **Pattern**: Floyd–Warshall. **Why**: all-pairs, O(n^3) feasible at n=400.
4. **Pattern**: Kruskal (sort edges + union-find) or Prim. **Why**: classic MST construction.
5. **Pattern**: Modified Dijkstra with state `(node, stops)` or Bellman-Ford with k relaxations. **Why**: hop limit prevents standard Dijkstra; relax exactly k+1 times.
6. **Pattern**: Distractor — BFS (Week 17). **Why**: unweighted ⇒ BFS suffices; Dijkstra is over-engineering.
7. **Pattern**: Dijkstra from source `k`; report max distance. **Why**: classic single-source shortest path; "network delay time".
8. **Pattern**: Dijkstra with max-heap on probability (or log-transform to additive). **Why**: product max ↔ sum of `-log(p)` min ⇒ Dijkstra.
9. **Pattern**: Bellman–Ford with one extra relaxation pass. **Why**: any successful relaxation in pass n indicates a negative cycle.
10. **Pattern**: Kruskal with descending sort (or negate weights). **Why**: greedy argument is symmetric — pick heaviest non-cycling edges.

</details>
