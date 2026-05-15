"""
WEEK 26 - PYTHON ADVANCED TOPICS
Topic: Bipartite Matching (Hopcroft-Karp)
File: bipartite_matching.py

CONCEPT:
    A *matching* in a bipartite graph G=(L u R, E) is a subset of edges with
    no shared endpoints. *Maximum* bipartite matching maximises the size of
    such a subset. Hopcroft-Karp is the asymptotically fastest classical
    algorithm: it builds a layered BFS graph and then performs DFS that
    finds *vertex-disjoint shortest augmenting paths* in a single phase.
    Each phase increases the shortest augmenting-path length by 1, so there
    are O(sqrt(V)) phases and a total of O(E*sqrt(V)) work.

KEY POINTS:
    - Equivalent to running max-flow on a unit-capacity flow graph s->L->R->t,
      where Dinic also runs in O(E*sqrt(V)).
    - Returns matching arrays: `matchL[u]` = matched right vertex (or NIL).
    - Augmenting path = path that alternates unmatched/matched edges and
      starts and ends at unmatched vertices.
    - Foundational tool for assignment, scheduling, vertex cover (Konig).

ALGORITHM / APPROACH:
    while BFS finds at least one augmenting path of length d:
        for each free left vertex u:
            DFS to extend along level-graph augmenting paths
            for each successful path: flip matchings along it
    return number of matched pairs

PYTHON-SPECIFIC NOTES:
    - Use `None` as the NIL sentinel; cleaner than -1.
    - `collections.deque` for BFS layering.
    - Recursion depth could reach O(V); bump recursion limit on huge graphs.

DRY RUN / EXAMPLE:
    Left {0,1,2,3}, Right {0,1,2,3}, edges:
        0-0, 0-1, 1-0, 1-2, 2-1, 2-3, 3-2, 3-3
    Phase 1 augmenting paths: 0->0, 1->2, 2->3 ... matching = 3
    Phase 2 finds 3->? via alternation -> matching = 4 (perfect).

COMPLEXITY:
    Time:  O(E * sqrt(V))
    Space: O(V + E)
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional


class HopcroftKarp:
    NIL = -1
    INF = float("inf")

    def __init__(self, left_size: int, right_size: int) -> None:
        self.L = left_size
        self.R = right_size
        self.adj: List[List[int]] = [[] for _ in range(left_size)]
        self.match_l: List[int] = []
        self.match_r: List[int] = []
        self.dist: List[float] = []

    def add_edge(self, u: int, v: int) -> None:
        self.adj[u].append(v)

    def _bfs(self) -> bool:
        q: deque[int] = deque()
        for u in range(self.L):
            if self.match_l[u] == self.NIL:
                self.dist[u] = 0
                q.append(u)
            else:
                self.dist[u] = self.INF
        found = False
        while q:
            u = q.popleft()
            for v in self.adj[u]:
                pair = self.match_r[v]
                if pair == self.NIL:
                    found = True
                elif self.dist[pair] == self.INF:
                    self.dist[pair] = self.dist[u] + 1
                    q.append(pair)
        return found

    def _dfs(self, u: int) -> bool:
        for v in self.adj[u]:
            pair = self.match_r[v]
            if pair == self.NIL or (self.dist[pair] == self.dist[u] + 1 and self._dfs(pair)):
                self.match_l[u] = v
                self.match_r[v] = u
                return True
        self.dist[u] = self.INF
        return False

    def max_matching(self) -> int:
        self.match_l = [self.NIL] * self.L
        self.match_r = [self.NIL] * self.R
        self.dist = [self.INF] * self.L
        matching = 0
        while self._bfs():
            for u in range(self.L):
                if self.match_l[u] == self.NIL and self._dfs(u):
                    matching += 1
        return matching

    def matched_pairs(self):
        return [(u, self.match_l[u]) for u in range(self.L) if self.match_l[u] != self.NIL]


# Simpler DFS-based Hungarian-tree augmenting-path matcher for didactic value
def kuhn_max_matching(left: int, right: int, edges) -> int:
    """O(V * E) bipartite matching using repeated DFS — classic 'Kuhn'."""
    adj: List[List[int]] = [[] for _ in range(left)]
    for u, v in edges:
        adj[u].append(v)
    match_r = [-1] * right

    def try_kuhn(u: int, used: List[bool]) -> bool:
        for v in adj[u]:
            if used[v]:
                continue
            used[v] = True
            if match_r[v] == -1 or try_kuhn(match_r[v], used):
                match_r[v] = u
                return True
        return False

    pairs = 0
    for u in range(left):
        used = [False] * right
        if try_kuhn(u, used):
            pairs += 1
    return pairs


def _demo() -> None:
    hk = HopcroftKarp(4, 4)
    for u, v in [(0, 0), (0, 1), (1, 0), (1, 2),
                 (2, 1), (2, 3), (3, 2), (3, 3)]:
        hk.add_edge(u, v)
    print(f"Hopcroft-Karp matching: {hk.max_matching()}")
    print(f"Pairs: {hk.matched_pairs()}")

    print(f"Kuhn matching:          "
          f"{kuhn_max_matching(4, 4, [(0,0),(0,1),(1,0),(1,2),(2,1),(2,3),(3,2),(3,3)])}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * Python uses `float('inf')` for the distance sentinel. Java used
#     Integer.MAX_VALUE in the same role.
#   * We expose `matched_pairs()` as a list comprehension instead of an
#     external loop — feels more Pythonic.
#   * Bonus: `kuhn_max_matching` is the textbook O(V*E) algorithm and is
#     simpler / often fast enough for small to medium inputs.
