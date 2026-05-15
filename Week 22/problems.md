# Week 22 — Practice Problems

Topics covered this week: shortest paths (Dijkstra, Bellman-Ford, Floyd-Warshall), minimum spanning trees (Kruskal, Prim), Union-Find.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Network Delay Time | Medium | Dijkstra | https://leetcode.com/problems/network-delay-time/ |
| 2 | Cheapest Flights Within K Stops | Medium | Bellman-Ford / modified Dijkstra | https://leetcode.com/problems/cheapest-flights-within-k-stops/ |
| 3 | Min Cost to Connect All Points | Medium | MST (Prim/Kruskal) | https://leetcode.com/problems/min-cost-to-connect-all-points/ |
| 4 | Path with Minimum Effort | Medium | Dijkstra on grid | https://leetcode.com/problems/path-with-minimum-effort/ |
| 5 | Swim in Rising Water | Hard | Dijkstra / BS + BFS | https://leetcode.com/problems/swim-in-rising-water/ |
| 6 | Find the City With the Smallest Number of Neighbors at a Threshold Distance | Medium | Floyd-Warshall | https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/ |
| 7 | Number of Operations to Make Network Connected | Medium | Union-Find | https://leetcode.com/problems/number-of-operations-to-make-network-connected/ |
| 8 | Accounts Merge | Medium | Union-Find | https://leetcode.com/problems/accounts-merge/ |
| 9 | Path with Maximum Probability | Medium | Modified Dijkstra | https://leetcode.com/problems/path-with-maximum-probability/ |
| 10 | Connecting Cities With Minimum Cost | Medium | MST + UF | https://leetcode.com/problems/connecting-cities-with-minimum-cost/ |
| 11 | Optimize Water Distribution in a Village | Hard | MST with virtual node | https://leetcode.com/problems/optimize-water-distribution-in-a-village/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Reachable Nodes In Subdivided Graph](https://leetcode.com/problems/reachable-nodes-in-subdivided-graph/) — Dijkstra with edge weights.
- [Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/) — Tarjan's bridge algorithm.
- [Number of Restricted Paths From First to Last Node](https://leetcode.com/problems/number-of-restricted-paths-from-first-to-last-node/) — Dijkstra + DP.

## Patterns to Master This Week

- Dijkstra (PQ + relax): O((V+E) log V). Pitfall: doesn't work with negative weights — use Bellman-Ford or SPFA.
- Bellman-Ford: O(V * E), allows negative weights, detects negative cycles. Pitfall: K-stop constraint requires copying dist arrays between rounds.
- Union-Find with path compression + union by rank: near-O(α(n)) per op. Pitfall: missing compression makes naive UF slow.
