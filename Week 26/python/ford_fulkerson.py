"""
WEEK 26 - PYTHON ADVANCED TOPICS
Topic: Ford-Fulkerson Maximum Flow
File: ford_fulkerson.py

CONCEPT:
    The Ford-Fulkerson method is a greedy algorithm framework for computing
    the maximum flow in a flow network. It repeatedly finds an augmenting
    path from source `s` to sink `t` in the residual graph and pushes the
    bottleneck capacity along it. We implement the DFS-based variant.

KEY POINTS:
    - Models capacity-constrained networks (pipelines, bandwidth, supply chains).
    - Uses a *residual graph* with reverse edges of capacity 0; pushing flow
      along edge (u,v) decreases its residual cap and increases (v,u)'s.
    - Augmenting path: any s->t path with strictly positive residual capacity.
    - Bottleneck: minimum residual capacity along the chosen path.
    - Terminates when no augmenting path exists (max-flow / min-cut theorem).
    - With DFS, complexity is O(E * max_flow); pathological orderings can blow
      up on irrational capacities (rare with integers, common in textbook
      cautionary tales).

ALGORITHM / APPROACH:
    initialise residual graph with both forward and reverse edges
    flow <- 0
    repeat:
        push <- DFS(s, t, +inf)         # try to push as much as possible
        if push == 0: break             # no more augmenting paths
        flow <- flow + push
    return flow

PYTHON-SPECIFIC NOTES:
    - We model edges as small lists [to, cap, rev_index] mirroring Java's
      parallel arrays — this keeps O(1) reverse-edge lookups without classes.
    - `sys.setrecursionlimit` is bumped because the DFS recursion depth can
      reach |V|.
    - Use `math.inf` for the initial pushed value; Python ints are arbitrary
      precision so it never overflows.

DRY RUN / EXAMPLE:
    Graph (CLRS-style) with nodes 0..5, source=0, sink=5:
        0->1 cap 16, 0->2 cap 13, 1->2 cap 4, 1->3 cap 12,
        2->1 cap 10, 2->4 cap 14, 3->2 cap 9, 3->5 cap 20,
        4->3 cap 7, 4->5 cap 4
    Trace (one possible DFS order):
        Path 0-1-3-5 bottleneck 12 -> flow=12
        Path 0-2-4-5 bottleneck 4  -> flow=16
        Path 0-2-4-3-5 bottleneck 7-> flow=23
        No more augmenting paths. Max flow = 23.

COMPLEXITY:
    Time:  O(E * F) where F is the maximum flow value.
    Space: O(V + E) for residual graph and DFS stack.
"""

from __future__ import annotations

import math
import sys
from typing import List


class FordFulkerson:
    """DFS-based maximum-flow solver."""

    def __init__(self, n: int) -> None:
        self.n = n
        # graph[u] = list of edges; each edge is [to, residual_cap, rev_index]
        self.graph: List[List[List[int]]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        self.graph[u].append([v, cap, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    def _dfs(self, u: int, t: int, pushed: int, visited: List[bool]) -> int:
        if u == t:
            return pushed
        visited[u] = True
        for edge in self.graph[u]:
            v, cap, rev = edge
            if not visited[v] and cap > 0:
                d = self._dfs(v, t, min(pushed, cap), visited)
                if d > 0:
                    edge[1] -= d
                    self.graph[v][rev][1] += d
                    return d
        return 0

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        while True:
            visited = [False] * self.n
            pushed = self._dfs(s, t, math.inf, visited)
            if pushed == 0:
                return flow
            flow += int(pushed)


def _demo() -> None:
    sys.setrecursionlimit(10_000)
    g = FordFulkerson(6)
    edges = [
        (0, 1, 16), (0, 2, 13),
        (1, 2, 4),  (1, 3, 12),
        (2, 1, 10), (2, 4, 14),
        (3, 2, 9),  (3, 5, 20),
        (4, 3, 7),  (4, 5, 4),
    ]
    for u, v, c in edges:
        g.add_edge(u, v, c)
    print(f"Ford-Fulkerson max flow (0 -> 5): {g.max_flow(0, 5)}")  # 23


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from the Java implementation:
#   * Python uses a list-of-lists residual graph instead of parallel arrays.
#     Each edge mutates the inner list in place to update residual capacity,
#     which is convenient because Python lists are mutable references.
#   * `math.inf` (a float) is used for the initial pushed value — we cast
#     back to `int` before returning to avoid surprising downstream callers.
#   * Recursion depth is bumped explicitly via `sys.setrecursionlimit` since
#     Python's default of 1000 can be reached on long augmenting paths.
