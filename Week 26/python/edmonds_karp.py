"""
WEEK 26 - PYTHON ADVANCED TOPICS
Topic: Edmonds-Karp Maximum Flow
File: edmonds_karp.py

CONCEPT:
    Edmonds-Karp is the BFS specialisation of Ford-Fulkerson. By always
    selecting the *shortest* augmenting path (in number of edges), it
    guarantees O(V * E^2) running time independent of edge capacities. The
    proof relies on the fact that the shortest s-t distance in the residual
    graph is non-decreasing across augmentations.

KEY POINTS:
    - Same residual-graph representation as Ford-Fulkerson.
    - BFS replaces DFS to pick a *fewest-edge* augmenting path.
    - Records `parent[v]` and `parent_edge[v]` to reconstruct the path.
    - Handles arbitrarily large integer capacities without performance loss.
    - Ideal default for textbook max-flow: well-behaved, easy to reason about.

ALGORITHM / APPROACH:
    while BFS finds path s -> t with positive residual:
        compute bottleneck along path
        update forward and reverse residuals
        flow += bottleneck
    return flow

PYTHON-SPECIFIC NOTES:
    - `collections.deque` provides O(1) popleft (Java's ArrayDeque/Queue).
    - We mutate edge entries in place — same as ford_fulkerson.py.
    - Build path-reconstruction lists with `[None] * n`; sentinel `-1` mirrors
      Java but `None` is more Pythonic for "no parent".

DRY RUN / EXAMPLE:
    Same CLRS graph as Ford-Fulkerson (max flow 23). BFS picks shortest paths:
        Iter 1: 0-1-3-5 (length 3), bottleneck = min(16,12,20)=12, flow=12
        Iter 2: 0-2-4-5 (length 3), bottleneck = min(13,14,4)=4,  flow=16
        Iter 3: 0-2-4-3-5 (length 4), bottleneck = min(9,10,7,8)=7, flow=23
        Iter 4: BFS finds no augmenting path -> done.

COMPLEXITY:
    Time:  O(V * E^2) — at most O(V*E) augmentations, each BFS is O(V+E).
    Space: O(V + E).
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional


class EdmondsKarp:
    def __init__(self, n: int) -> None:
        self.n = n
        self.graph: List[List[List[int]]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        self.graph[u].append([v, cap, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    def _bfs(self, s: int, t: int) -> Optional[List[Optional[tuple]]]:
        """Return parent-edge map or None if no augmenting path exists."""
        parent: List[Optional[tuple]] = [None] * self.n
        parent[s] = (-1, -1)
        q = deque([s])
        while q:
            u = q.popleft()
            for idx, (v, cap, _rev) in enumerate(self.graph[u]):
                if parent[v] is None and cap > 0:
                    parent[v] = (u, idx)
                    if v == t:
                        return parent
                    q.append(v)
        return None

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        while True:
            parent = self._bfs(s, t)
            if parent is None or parent[t] is None:
                return flow
            # Find bottleneck along path
            bottleneck = float("inf")
            v = t
            while v != s:
                u, eidx = parent[v]
                bottleneck = min(bottleneck, self.graph[u][eidx][1])
                v = u
            # Apply
            v = t
            while v != s:
                u, eidx = parent[v]
                edge = self.graph[u][eidx]
                edge[1] -= bottleneck
                self.graph[v][edge[2]][1] += bottleneck
                v = u
            flow += int(bottleneck)


def _demo() -> None:
    g = EdmondsKarp(6)
    edges = [
        (0, 1, 16), (0, 2, 13),
        (1, 2, 4),  (1, 3, 12),
        (2, 1, 10), (2, 4, 14),
        (3, 2, 9),  (3, 5, 20),
        (4, 3, 7),  (4, 5, 4),
    ]
    for u, v, c in edges:
        g.add_edge(u, v, c)
    print(f"Edmonds-Karp max flow (0 -> 5): {g.max_flow(0, 5)}")  # 23


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Java tracks parent and parent-edge in two separate int[] arrays. Python
#     stores them as a single tuple (parent_node, edge_index_in_parent_adj),
#     which simplifies the bookkeeping.
#   * `collections.deque` is the natural BFS queue; `popleft()` is O(1).
#   * `float('inf')` works for the bottleneck initialisation; we cast to int
#     before returning since flow values are integral.
