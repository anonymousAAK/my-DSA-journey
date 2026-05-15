# Week 17 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which graph pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given a directed graph with up to 10^5 nodes and 2·10^5 edges, return any topological ordering of its vertices (or detect a cycle).
Pattern: ______
Why: ______

### 2. Given an undirected graph, count the number of connected components. n ≤ 10^5.
Pattern: ______
Why: ______

### 3. Given an undirected graph, decide whether it is bipartite. n ≤ 10^5.
Pattern: ______
Why: ______

### 4. Given an unweighted directed graph and two vertices `s` and `t`, find the shortest path (in edges) from `s` to `t`.
Pattern: ______
Why: ______

### 5. Given a grid where 1 represents land and 0 water, find the size of the largest island. m·n ≤ 10^6.
Pattern: ______
Why: ______

### 6. Given a list of course prerequisites, decide whether it is possible to finish all courses. n ≤ 10^5.
Pattern: ______
Why: ______

### 7. Distractor: Given a weighted graph with non-negative edges, find the shortest path from `s` to `t`. (Is BFS enough?)
Pattern: ______
Why: ______

### 8. Given a list of dependencies between build tasks (some depend on others), schedule them across the minimum number of parallel rounds.
Pattern: ______
Why: ______

### 9. Given a graph and a starting vertex, list all vertices reachable from it.
Pattern: ______
Why: ______

### 10. Given a 2-D maze with walls and a start/end cell, find the minimum number of moves to exit. Moves are 4-directional. Grid up to 1000×1000.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Kahn's BFS (indegree) or DFS post-order reverse. **Why**: cycle iff Kahn outputs fewer than n nodes.
2. **Pattern**: BFS/DFS per unvisited node, or union-find. **Why**: launch traversal, increment component count.
3. **Pattern**: 2-coloring via BFS/DFS. **Why**: alternate colors; conflict ⇒ not bipartite.
4. **Pattern**: BFS. **Why**: unweighted ⇒ BFS layers = shortest paths.
5. **Pattern**: DFS/BFS flood fill tracking size. **Why**: per island compute component size.
6. **Pattern**: Cycle detection in directed graph (topological sort). **Why**: feasible ⇔ DAG.
7. **Pattern**: Distractor — Dijkstra (Week 22). **Why**: weighted edges break BFS's layer invariant unless weights are uniform.
8. **Pattern**: Topological sort with level/depth tracking. **Why**: rounds = longest path in DAG = max depth in Kahn's BFS.
9. **Pattern**: Plain DFS or BFS. **Why**: reachability is the simplest traversal use.
10. **Pattern**: BFS on grid (implicit graph). **Why**: unit-weight shortest path with 4 neighbours per cell.

</details>
