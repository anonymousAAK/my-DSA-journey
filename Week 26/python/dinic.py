"""
WEEK 26 - PYTHON ADVANCED TOPICS
Topic: Dinic's Maximum Flow
File: dinic.py

CONCEPT:
    Dinic's algorithm improves on Edmonds-Karp by exploiting the *level
    graph*: a BFS from source assigns each vertex a level equal to its
    shortest-path distance, then a series of *blocking flows* are sent only
    through edges going from level i to level i+1. Each phase increases the
    minimum s-t distance by at least one, so there are O(V) phases. With an
    `iter[]` pointer that skips dead edges, each phase runs in O(V*E),
    giving O(V^2 * E) overall — and O(E*sqrt(V)) on unit-capacity / bipartite
    graphs (Hopcroft-Karp).

KEY POINTS:
    - Two-pass per phase: BFS to build levels, DFS to send blocking flow.
    - `iter[u]` is an iterator pointer per vertex so we never revisit dead
      edges during a single DFS phase.
    - Massively faster than Edmonds-Karp on dense graphs in practice.
    - On unit-capacity graphs runs in O(E*sqrt(V)), the same bound as
      Hopcroft-Karp for bipartite matching.

ALGORITHM / APPROACH:
    while BFS-build-level-graph(s) reaches t:
        reset iter[]
        repeat:
            push <- DFS-blocking-flow(s, +inf)
            if push == 0: break
            flow += push
    return flow

PYTHON-SPECIFIC NOTES:
    - We use the [to, cap, rev_index] edge list trick so that `iter[u]` is
      simply an integer index into `graph[u]`.
    - `collections.deque` for BFS, plain lists elsewhere — no third-party
      libraries needed.
    - Recursion depth can hit O(V) so set a high recursion limit if you
      benchmark on >1000 nodes.

DRY RUN / EXAMPLE:
    Same CLRS graph (max flow = 23). Dinic typically finishes in 2-3 phases:
        Phase 1: levels {0:0, 1:1, 2:1, 3:2, 4:2, 5:3}
                 Blocking flow pushes 0-1-3-5 (12) and 0-2-4-5 (4) -> 16.
        Phase 2: BFS now uses reverse edge 4->3 to reach 5 in 4 steps.
                 Blocking flow pushes 0-2-4-3-5 (7) -> 23.
        Phase 3: BFS no longer reaches sink -> done.

COMPLEXITY:
    Time:  O(V^2 * E) general; O(E * sqrt(V)) on unit-capacity graphs.
    Space: O(V + E).
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional


class Dinic:
    def __init__(self, n: int) -> None:
        self.n = n
        self.graph: List[List[List[int]]] = [[] for _ in range(n)]
        self.level: List[int] = []
        self.it: List[int] = []

    def add_edge(self, u: int, v: int, cap: int) -> None:
        self.graph[u].append([v, cap, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    def _bfs(self, s: int, t: int) -> bool:
        self.level = [-1] * self.n
        self.level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v, cap, _ in self.graph[u]:
                if cap > 0 and self.level[v] < 0:
                    self.level[v] = self.level[u] + 1
                    q.append(v)
        return self.level[t] >= 0

    def _dfs(self, u: int, t: int, pushed: int) -> int:
        if u == t:
            return pushed
        while self.it[u] < len(self.graph[u]):
            edge = self.graph[u][self.it[u]]
            v, cap, rev = edge
            if cap > 0 and self.level[v] == self.level[u] + 1:
                d = self._dfs(v, t, min(pushed, cap))
                if d > 0:
                    edge[1] -= d
                    self.graph[v][rev][1] += d
                    return d
            self.it[u] += 1
        return 0

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        while self._bfs(s, t):
            self.it = [0] * self.n
            while True:
                pushed = self._dfs(s, t, float("inf"))
                if pushed == 0:
                    break
                flow += int(pushed)
        return flow


def _demo() -> None:
    g = Dinic(6)
    edges = [
        (0, 1, 16), (0, 2, 13),
        (1, 2, 4),  (1, 3, 12),
        (2, 1, 10), (2, 4, 14),
        (3, 2, 9),  (3, 5, 20),
        (4, 3, 7),  (4, 5, 4),
    ]
    for u, v, c in edges:
        g.add_edge(u, v, c)
    print(f"Dinic max flow (0 -> 5): {g.max_flow(0, 5)}")  # 23


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * The `iter[]` array (level-graph DFS pointer) is a plain Python list of
#     ints — no need for an int[] wrapper class.
#   * Java often uses Integer.MAX_VALUE; Python uses float('inf') for the
#     same purpose, casting to int on return.
#   * Inner edge mutation works directly because Python lists are mutable
#     references; Java uses parallel int[] arrays for cache friendliness.
