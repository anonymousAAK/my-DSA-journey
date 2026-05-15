# Week 17 — Practice Problems

Topics covered this week: graphs (adjacency list/matrix), BFS, DFS, connected components, topological sort, cycle detection.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Number of Islands | Medium | Grid DFS/BFS | https://leetcode.com/problems/number-of-islands/ |
| 2 | Max Area of Island | Medium | Grid DFS | https://leetcode.com/problems/max-area-of-island/ |
| 3 | Clone Graph | Medium | DFS + HashMap | https://leetcode.com/problems/clone-graph/ |
| 4 | Course Schedule | Medium | Topological sort | https://leetcode.com/problems/course-schedule/ |
| 5 | Course Schedule II | Medium | Topo order output | https://leetcode.com/problems/course-schedule-ii/ |
| 6 | Pacific Atlantic Water Flow | Medium | Reverse BFS | https://leetcode.com/problems/pacific-atlantic-water-flow/ |
| 7 | Word Ladder | Hard | BFS on words | https://leetcode.com/problems/word-ladder/ |
| 8 | Number of Connected Components in an Undirected Graph | Medium | Union-Find / DFS | https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/ |
| 9 | Surrounded Regions | Medium | Boundary DFS | https://leetcode.com/problems/surrounded-regions/ |
| 10 | Redundant Connection | Medium | Union-Find | https://leetcode.com/problems/redundant-connection/ |
| 11 | Graph Valid Tree | Medium | UF / DFS | https://leetcode.com/problems/graph-valid-tree/ |
| 12 | Is Graph Bipartite? | Medium | 2-coloring BFS | https://leetcode.com/problems/is-graph-bipartite/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) — topological sort from constraints.
- [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) — Hierholzer's Eulerian path.
- [Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/) — Tarjan's bridge algorithm.

## Patterns to Master This Week

- DFS via recursion vs iterative stack; mark visited at entry. Pitfall: stack overflow on deep recursion — use iterative for >10^4 depth.
- BFS for shortest path in unweighted graphs; `Queue<int[]>` for grids. Pitfall: do not re-enqueue nodes already queued.
- Topo sort = Kahn's BFS (in-degree zero) or DFS post-order reversal. Pitfall: detecting cycles when not all nodes are output.
