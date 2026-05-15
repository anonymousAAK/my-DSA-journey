"""
WEEK 26 - PYTHON ADVANCED TOPICS
Topic: Minimum s-t Cut via Max-Flow / Min-Cut Theorem
File: min_cut.py

CONCEPT:
    Given a directed flow network with source `s` and sink `t`, an s-t cut is
    a partition (S, T) of the vertices with s in S and t in T. The cut's
    capacity is the sum of capacities of edges from S to T (forward only).
    The Max-Flow / Min-Cut theorem states:

        max flow value = min cut capacity.

    To extract the cut after running any max-flow algorithm, perform a BFS
    on the *residual* graph from s; vertices reachable belong to S, the rest
    to T. Cut edges are precisely the original edges (u,v) with u in S and
    v in T whose residual is now zero (i.e. saturated).

KEY POINTS:
    - Works on top of any max-flow algorithm (we use Edmonds-Karp here).
    - Distinguish ORIGINAL edges from residual reverse edges — only original
      forward edges count toward the cut capacity.
    - Useful for: image segmentation, project selection, bipartite vertex
      cover (Konig's theorem), reliability analysis.

ALGORITHM / APPROACH:
    1. Run any max-flow algorithm. Now residual graph reflects flows.
    2. BFS/DFS from `s` in residual graph treating edges with cap > 0 as
       traversable. Mark visited set S.
    3. For every original edge (u,v) with u in S and v not in S: it is a
       cut edge with original capacity contributing to min-cut value.

PYTHON-SPECIFIC NOTES:
    - We tag each edge with a flag `is_original` so we can later distinguish
      forward edges from their auto-generated reverses.
    - Returning a list[tuple[int,int,int]] of (u, v, capacity) feels Pythonic.

DRY RUN / EXAMPLE:
    Same CLRS graph (max flow 23). After saturation, BFS from 0 in residual:
        Reachable set S = {0, 2, 4} (try and confirm with the trace).
        Cut edges from S to T = {1,3,5}: (0,1)=16, (4,3)=7 ... etc.
        Sum of original capacities = 23 = max flow.

COMPLEXITY:
    Same as the underlying max-flow algorithm + O(V+E) for the cut extraction.
"""

from __future__ import annotations

from collections import deque
from typing import List, Tuple


class MinCut:
    def __init__(self, n: int) -> None:
        self.n = n
        # Edge: [to, cap, rev_index, is_original_forward, original_cap]
        self.graph: List[List[List]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        self.graph[u].append([v, cap, len(self.graph[v]), True, cap])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1, False, 0])

    # --- Edmonds-Karp embedded for self-containment ----------------------
    def _bfs(self, s: int, t: int):
        parent = [None] * self.n
        parent[s] = (-1, -1)
        q = deque([s])
        while q:
            u = q.popleft()
            for idx, edge in enumerate(self.graph[u]):
                v, cap = edge[0], edge[1]
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
            bottleneck = float("inf")
            v = t
            while v != s:
                u, eidx = parent[v]
                bottleneck = min(bottleneck, self.graph[u][eidx][1])
                v = u
            v = t
            while v != s:
                u, eidx = parent[v]
                edge = self.graph[u][eidx]
                edge[1] -= bottleneck
                self.graph[v][edge[2]][1] += bottleneck
                v = u
            flow += int(bottleneck)

    # --- Cut extraction --------------------------------------------------
    def reachable_from_source(self, s: int) -> List[bool]:
        visited = [False] * self.n
        visited[s] = True
        q = deque([s])
        while q:
            u = q.popleft()
            for v, cap, _rev, _orig, _ocap in self.graph[u]:
                if cap > 0 and not visited[v]:
                    visited[v] = True
                    q.append(v)
        return visited

    def min_cut_edges(self, s: int, t: int) -> Tuple[int, List[Tuple[int, int, int]]]:
        flow = self.max_flow(s, t)
        side = self.reachable_from_source(s)
        cut: List[Tuple[int, int, int]] = []
        for u in range(self.n):
            if not side[u]:
                continue
            for edge in self.graph[u]:
                v, _cap, _rev, is_orig, ocap = edge
                if is_orig and not side[v]:
                    cut.append((u, v, ocap))
        return flow, cut


def _demo() -> None:
    g = MinCut(6)
    edges = [
        (0, 1, 16), (0, 2, 13),
        (1, 2, 4),  (1, 3, 12),
        (2, 1, 10), (2, 4, 14),
        (3, 2, 9),  (3, 5, 20),
        (4, 3, 7),  (4, 5, 4),
    ]
    for u, v, c in edges:
        g.add_edge(u, v, c)
    flow, cut = g.min_cut_edges(0, 5)
    print(f"Max flow / Min cut value: {flow}")
    print("Cut edges (S -> T):")
    for u, v, c in cut:
        print(f"  ({u} -> {v}) capacity {c}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Java's network_flow.java focuses on max-flow and matching; min-cut
#     extraction is implicit. Here we add an explicit `min_cut_edges` helper.
#   * The tuple (u, v, original_capacity) is a more Pythonic return type
#     than a custom Edge class.
#   * We attach the original capacity to each edge so that after max-flow
#     mutates residuals we can still report the *capacity* of cut edges.
