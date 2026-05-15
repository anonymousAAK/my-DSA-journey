# Week 26 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which flow/matching pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given a flow network with source `s`, sink `t`, and integer edge capacities, find the maximum s–t flow. n ≤ 500, m ≤ 10^4.
Pattern: ______
Why: ______

### 2. Given a bipartite graph with up to 500 nodes on each side, find a maximum cardinality matching.
Pattern: ______
Why: ______

### 3. Given a set of jobs and machines with compatibility relations, assign each job to a compatible machine maximizing the number of assigned jobs.
Pattern: ______
Why: ______

### 4. Given a flow network with capacities and costs per unit, find the minimum-cost maximum flow.
Pattern: ______
Why: ______

### 5. Given an undirected graph, find the minimum number of edges whose removal disconnects `s` from `t`.
Pattern: ______
Why: ______

### 6. Distractor: Given a DAG, find the longest path. (Network flow?)
Pattern: ______
Why: ______

### 7. Given a bipartite graph with weights on left vertices, find a max-weight independent set on the left.
Pattern: ______
Why: ______

### 8. Given a directed graph and a vertex capacity (each vertex can carry at most `c_v` units), find the max flow from `s` to `t`.
Pattern: ______
Why: ______

### 9. Given an n × n grid of integers, decide if you can route k disjoint paths from k left-edge cells to k right-edge cells without sharing cells.
Pattern: ______
Why: ______

### 10. Distractor: Given a bipartite graph with weighted edges, find a maximum-weight matching. (Same as drill 2?)
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Dinic's algorithm (or Edmonds–Karp). **Why**: classic max flow; Dinic is O(V^2 E) — fine at given size.
2. **Pattern**: Hopcroft–Karp (or max flow with unit caps). **Why**: bipartite matching reduces to max flow; HK is O(E·√V).
3. **Pattern**: Bipartite matching. **Why**: jobs vs machines = two-side graph; compatibility = edges.
4. **Pattern**: Min-cost max flow (SSP with Bellman–Ford / Johnson). **Why**: each augmenting path is the cheapest.
5. **Pattern**: Max-flow / min-cut. **Why**: by max-flow min-cut theorem — unit-capacity max flow = min edge cut.
6. **Pattern**: Distractor — DP on DAG (topo order). **Why**: longest path in DAG is in P via topo + relaxation; no flow needed.
7. **Pattern**: Min cut on bipartite weighted graph (project selection / König). **Why**: max independent set on bipartite = n − min vertex cover = n − max matching (König).
8. **Pattern**: Vertex-split trick + max flow. **Why**: split v into v_in, v_out with capacity c_v; standard reduction.
9. **Pattern**: Vertex-disjoint paths via vertex-split + max flow. **Why**: unit-capacity vertex flow = max vertex-disjoint paths.
10. **Pattern**: Distractor — Hungarian algorithm (assignment) or min-cost max flow. **Why**: weighted bipartite matching is NOT plain Hopcroft–Karp.

</details>
