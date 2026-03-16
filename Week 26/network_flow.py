# Week 26: Network Flow & Matching
# ==================================
# Topics covered:
#   1. Ford-Fulkerson (DFS augmenting paths)      - O(E * max_flow)
#   2. Edmonds-Karp   (BFS augmenting paths)      - O(V * E^2)
#   3. Hopcroft-Karp  (bipartite matching)         - O(E * sqrt(V))
#   4. Hungarian Algorithm (min-cost assignment)   - O(N^3)

from __future__ import annotations

from collections import deque
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Flow network using adjacency list with edge triples [to, cap, rev_index]
# ---------------------------------------------------------------------------

class MaxFlowGraph:
    """Adjacency-list flow network supporting residual-graph operations."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.graph: List[List[List[int]]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        """Add directed edge u -> v with given capacity."""
        self.graph[u].append([v, cap, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    # ---- 1. Ford-Fulkerson (DFS) ----
    # Time:  O(E * max_flow)
    # Space: O(V + E)

    def _ff_dfs(self, u: int, t: int, pushed: int, visited: List[bool]) -> int:
        if u == t:
            return pushed
        visited[u] = True
        for edge in self.graph[u]:
            v, cap, rev = edge
            if not visited[v] and cap > 0:
                d = self._ff_dfs(v, t, min(pushed, cap), visited)
                if d > 0:
                    edge[1] -= d
                    self.graph[v][rev][1] += d
                    return d
        return 0

    def ford_fulkerson(self, s: int, t: int) -> int:
        """Compute max flow from s to t using DFS augmenting paths."""
        flow = 0
        while True:
            visited = [False] * self.n
            pushed = self._ff_dfs(s, t, float("inf"), visited)
            if pushed == 0:
                break
            flow += pushed
        return flow

    # ---- 2. Edmonds-Karp (BFS) ----
    # Time:  O(V * E^2)
    # Space: O(V + E)

    def _bfs(self, s: int, t: int, parent: List[Optional[Tuple[int, int]]]) -> bool:
        visited = [False] * self.n
        visited[s] = True
        queue: deque[int] = deque([s])
        while queue:
            u = queue.popleft()
            for idx, (v, cap, _rev) in enumerate(self.graph[u]):
                if not visited[v] and cap > 0:
                    visited[v] = True
                    parent[v] = (u, idx)
                    if v == t:
                        return True
                    queue.append(v)
        return False

    def edmonds_karp(self, s: int, t: int) -> int:
        """Compute max flow from s to t using BFS augmenting paths."""
        flow = 0
        parent: List[Optional[Tuple[int, int]]] = [None] * self.n
        while self._bfs(s, t, parent):
            bottleneck = float("inf")
            v = t
            while v != s:
                u, idx = parent[v]
                bottleneck = min(bottleneck, self.graph[u][idx][1])
                v = u
            v = t
            while v != s:
                u, idx = parent[v]
                self.graph[u][idx][1] -= bottleneck
                rev = self.graph[u][idx][2]
                self.graph[v][rev][1] += bottleneck
                v = u
            flow += bottleneck
            parent = [None] * self.n
        return flow


# ---------------------------------------------------------------------------
# 3. Hopcroft-Karp Bipartite Matching
#    Time:  O(E * sqrt(V))
#    Space: O(V + E)
# ---------------------------------------------------------------------------

class HopcroftKarp:
    """Maximum cardinality matching in a bipartite graph."""

    NIL = -1
    INF = float("inf")

    def __init__(self, left_size: int, right_size: int) -> None:
        self.left_size = left_size
        self.right_size = right_size
        self.adj: List[List[int]] = [[] for _ in range(left_size)]

    def add_edge(self, u: int, v: int) -> None:
        self.adj[u].append(v)

    def _bfs(self) -> bool:
        queue: deque[int] = deque()
        for u in range(self.left_size):
            if self.match_left[u] == self.NIL:
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = self.INF
        found = False
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                nxt = self.match_right[v]
                if nxt == self.NIL:
                    found = True
                elif self.dist[nxt] == self.INF:
                    self.dist[nxt] = self.dist[u] + 1
                    queue.append(nxt)
        return found

    def _dfs(self, u: int) -> bool:
        for v in self.adj[u]:
            nxt = self.match_right[v]
            if nxt == self.NIL or (
                self.dist[nxt] == self.dist[u] + 1 and self._dfs(nxt)
            ):
                self.match_left[u] = v
                self.match_right[v] = u
                return True
        self.dist[u] = self.INF
        return False

    def max_matching(self) -> int:
        """Return the size of a maximum matching."""
        self.match_left = [self.NIL] * self.left_size
        self.match_right = [self.NIL] * self.right_size
        self.dist = [0] * self.left_size
        matching = 0
        while self._bfs():
            for u in range(self.left_size):
                if self.match_left[u] == self.NIL:
                    if self._dfs(u):
                        matching += 1
        return matching

    def get_matching(self) -> List[Tuple[int, int]]:
        """Return list of matched (left, right) pairs."""
        return [
            (u, self.match_left[u])
            for u in range(self.left_size)
            if self.match_left[u] != self.NIL
        ]


# ---------------------------------------------------------------------------
# 4. Hungarian Algorithm (minimum-cost perfect assignment)
#    Time:  O(N^3)
#    Space: O(N^2)
# ---------------------------------------------------------------------------

class Hungarian:
    """Solve the N x N assignment problem in O(N^3)."""

    def __init__(self, cost: List[List[float]]) -> None:
        self.n = len(cost)
        self.cost = cost

    def solve(self) -> Tuple[float, List[int]]:
        """Returns (min_cost, assignment) where assignment[i] = col for row i."""
        n = self.n
        INF = float("inf")
        u = [0.0] * (n + 1)
        v = [0.0] * (n + 1)
        p = [0] * (n + 1)
        way = [0] * (n + 1)

        for i in range(1, n + 1):
            p[0] = i
            j0 = 0
            min_v = [INF] * (n + 1)
            used = [False] * (n + 1)

            while True:
                used[j0] = True
                i0 = p[j0]
                delta = INF
                j1 = -1
                for j in range(1, n + 1):
                    if not used[j]:
                        cur = self.cost[i0 - 1][j - 1] - u[i0] - v[j]
                        if cur < min_v[j]:
                            min_v[j] = cur
                            way[j] = j0
                        if min_v[j] < delta:
                            delta = min_v[j]
                            j1 = j
                for j in range(n + 1):
                    if used[j]:
                        u[p[j]] += delta
                        v[j] -= delta
                    else:
                        min_v[j] -= delta
                j0 = j1
                if p[j0] == 0:
                    break

            while j0:
                p[j0] = p[way[j0]]
                j0 = way[j0]

        assignment = [0] * n
        for j in range(1, n + 1):
            assignment[p[j] - 1] = j - 1
        total = sum(self.cost[i][assignment[i]] for i in range(n))
        return total, assignment


# ---------------------------------------------------------------------------
# Demo / Driver
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Week 26: Network Flow & Matching")
    print("=" * 60)

    # --- Edmonds-Karp ---
    print("\n--- Edmonds-Karp Max Flow ---")
    g = MaxFlowGraph(6)
    g.add_edge(0, 1, 16); g.add_edge(0, 2, 13)
    g.add_edge(1, 2, 4);  g.add_edge(1, 3, 12)
    g.add_edge(2, 1, 10); g.add_edge(2, 4, 14)
    g.add_edge(3, 2, 9);  g.add_edge(3, 5, 20)
    g.add_edge(4, 3, 7);  g.add_edge(4, 5, 4)
    print(f"Max flow (0 -> 5): {g.edmonds_karp(0, 5)}")  # 23

    # --- Ford-Fulkerson ---
    print("\n--- Ford-Fulkerson Max Flow ---")
    g2 = MaxFlowGraph(6)
    g2.add_edge(0, 1, 16); g2.add_edge(0, 2, 13)
    g2.add_edge(1, 2, 4);  g2.add_edge(1, 3, 12)
    g2.add_edge(2, 1, 10); g2.add_edge(2, 4, 14)
    g2.add_edge(3, 2, 9);  g2.add_edge(3, 5, 20)
    g2.add_edge(4, 3, 7);  g2.add_edge(4, 5, 4)
    print(f"Max flow (0 -> 5): {g2.ford_fulkerson(0, 5)}")  # 23

    # --- Hopcroft-Karp ---
    print("\n--- Hopcroft-Karp Bipartite Matching ---")
    hk = HopcroftKarp(4, 4)
    hk.add_edge(0, 0); hk.add_edge(0, 1)
    hk.add_edge(1, 0); hk.add_edge(1, 2)
    hk.add_edge(2, 1); hk.add_edge(2, 3)
    hk.add_edge(3, 2); hk.add_edge(3, 3)
    print(f"Maximum matching size: {hk.max_matching()}")  # 4
    print(f"Matched pairs: {hk.get_matching()}")

    # --- Hungarian ---
    print("\n--- Hungarian Algorithm (Min-Cost Assignment) ---")
    cost_matrix = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4],
    ]
    h = Hungarian(cost_matrix)
    total_cost, assignment = h.solve()
    print(f"Minimum cost: {total_cost}")  # 13
    print(f"Assignment (row -> col): {assignment}")
