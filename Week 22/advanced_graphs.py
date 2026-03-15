"""
Week 22: Advanced Graphs
=========================
This module covers shortest-path algorithms, minimum spanning trees, and
the Disjoint Set Union (Union-Find) data structure.

Topics covered:
    1. Dijkstra's algorithm (using heapq, with path reconstruction)
    2. Bellman-Ford (with negative cycle detection)
    3. Floyd-Warshall (all-pairs shortest paths, with path reconstruction)
    4. DSU / Union-Find (path compression + union by rank)
    5. Kruskal's MST
    6. Prim's MST
"""

from __future__ import annotations

import heapq
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple


# Type aliases for clarity
INF = float("inf")
AdjList = Dict[int, List[Tuple[int, float]]]  # vertex -> [(neighbor, weight)]


# ---------------------------------------------------------------------------
# Helper: build weighted adjacency list
# ---------------------------------------------------------------------------
def build_adj_list(
    edges: List[Tuple[int, int, float]], directed: bool = False
) -> Tuple[AdjList, Set[int]]:
    """
    Build an adjacency list from a list of (u, v, weight) edges.
    Returns (adj, vertices).
    """
    adj: AdjList = defaultdict(list)
    vertices: Set[int] = set()
    for u, v, w in edges:
        adj[u].append((v, w))
        vertices.update([u, v])
        if not directed:
            adj[v].append((u, w))
    return adj, vertices


# ---------------------------------------------------------------------------
# 1. Dijkstra's Algorithm
# ---------------------------------------------------------------------------
def dijkstra(
    adj: AdjList, source: int, vertices: Set[int]
) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """
    Dijkstra's single-source shortest path algorithm for non-negative weights.

    Uses a min-heap (priority queue) to greedily process the nearest unvisited
    vertex.

    Returns:
        dist   — dict mapping each vertex to its shortest distance from source
        parent — dict for path reconstruction (parent[v] = predecessor of v)

    Time:  O((V + E) log V) with a binary heap
    Space: O(V + E)
    """
    dist: Dict[int, float] = {v: INF for v in vertices}
    parent: Dict[int, Optional[int]] = {v: None for v in vertices}
    dist[source] = 0.0

    # Min-heap: (distance, vertex)
    heap: List[Tuple[float, int]] = [(0.0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # stale entry — we already found a shorter path to u

        for v, w in adj[u]:
            new_dist = dist[u] + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                parent[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, parent


def reconstruct_path(parent: Dict[int, Optional[int]], target: int) -> List[int]:
    """
    Reconstruct the shortest path from source to *target* using the parent map.

    Time: O(path_length)
    """
    path: List[int] = []
    node: Optional[int] = target
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


# ---------------------------------------------------------------------------
# 2. Bellman-Ford Algorithm
# ---------------------------------------------------------------------------
def bellman_ford(
    edges: List[Tuple[int, int, float]], source: int, vertices: Set[int]
) -> Tuple[Optional[Dict[int, float]], Dict[int, Optional[int]]]:
    """
    Bellman-Ford single-source shortest path algorithm.

    Unlike Dijkstra, handles *negative* edge weights.
    Detects negative-weight cycles.

    Algorithm:
        1. Initialise dist[source] = 0, all others = INF.
        2. Relax all edges V-1 times.
        3. One more pass: if any edge can still be relaxed, a negative
           cycle exists.

    Returns:
        dist   — shortest distances, or None if a negative cycle is reachable
        parent — predecessor map for path reconstruction

    Time:  O(V * E)
    Space: O(V)
    """
    dist: Dict[int, float] = {v: INF for v in vertices}
    parent: Dict[int, Optional[int]] = {v: None for v in vertices}
    dist[source] = 0.0

    n = len(vertices)

    # Relax all edges V-1 times.
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
        if not updated:
            break  # early termination — no changes in this pass

    # Check for negative-weight cycles.
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None, parent  # negative cycle detected

    return dist, parent


# ---------------------------------------------------------------------------
# 3. Floyd-Warshall (all-pairs shortest paths)
# ---------------------------------------------------------------------------
def floyd_warshall(
    n: int, edges: List[Tuple[int, int, float]]
) -> Tuple[List[List[float]], List[List[Optional[int]]]]:
    """
    Floyd-Warshall all-pairs shortest path algorithm.

    Vertices are numbered 0..n-1.

    Algorithm:
        For each intermediate vertex k, for each pair (i, j):
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    Also maintains a *next* matrix for path reconstruction.

    Returns:
        dist — n x n matrix of shortest distances
        nxt  — n x n matrix where nxt[i][j] = next vertex on the shortest
               path from i to j (None if no path)

    Time:  O(V^3)
    Space: O(V^2)
    """
    dist = [[INF] * n for _ in range(n)]
    nxt: List[List[Optional[int]]] = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0.0

    for u, v, w in edges:
        dist[u][v] = w
        nxt[u][v] = v

    # Main triple loop
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]

    return dist, nxt


def reconstruct_path_fw(
    nxt: List[List[Optional[int]]], u: int, v: int
) -> Optional[List[int]]:
    """
    Reconstruct the shortest path from u to v using the Floyd-Warshall
    *next* matrix.

    Returns None if no path exists.
    Time: O(path_length)
    """
    if nxt[u][v] is None:
        return None
    path = [u]
    while u != v:
        u = nxt[u][v]
        if u is None:
            return None
        path.append(u)
    return path


# ---------------------------------------------------------------------------
# 4. Disjoint Set Union (Union-Find)
# ---------------------------------------------------------------------------
class UnionFind:
    """
    Disjoint Set Union (DSU) with path compression and union by rank.

    Operations:
        find(x)      — O(alpha(n)) amortized  (nearly O(1))
        union(x, y)  — O(alpha(n)) amortized
        connected(x, y) — O(alpha(n)) amortized

    alpha is the inverse Ackermann function, which grows incredibly slowly
    and is effectively constant for all practical input sizes.

    Space: O(n)
    """

    def __init__(self, n: int) -> None:
        """Create n disjoint singleton sets {0}, {1}, ..., {n-1}."""
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # number of disjoint sets

    def find(self, x: int) -> int:
        """
        Find the representative (root) of the set containing *x*.
        Uses path compression: every node on the path to the root is made
        to point directly at the root, flattening the tree.
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Merge the sets containing *x* and *y*.
        Uses union by rank: attach the shorter tree under the taller one.
        Returns True if a merge happened, False if x and y were already
        in the same set.
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # already in the same set

        # Union by rank
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        self.count -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """Check if *x* and *y* are in the same set."""
        return self.find(x) == self.find(y)


# ---------------------------------------------------------------------------
# 5. Kruskal's MST
# ---------------------------------------------------------------------------
def kruskal_mst(
    n: int, edges: List[Tuple[int, int, float]]
) -> Tuple[float, List[Tuple[int, int, float]]]:
    """
    Kruskal's algorithm for Minimum Spanning Tree.

    Algorithm:
        1. Sort all edges by weight.
        2. Greedily add each edge if it doesn't form a cycle (checked via
           Union-Find).
        3. Stop after n-1 edges (MST is complete).

    Time:  O(E log E)  — dominated by sorting
    Space: O(V + E)
    """
    sorted_edges = sorted(edges, key=lambda e: e[2])
    uf = UnionFind(n)
    mst_weight = 0.0
    mst_edges: List[Tuple[int, int, float]] = []

    for u, v, w in sorted_edges:
        if uf.union(u, v):
            mst_weight += w
            mst_edges.append((u, v, w))
            if len(mst_edges) == n - 1:
                break

    return mst_weight, mst_edges


# ---------------------------------------------------------------------------
# 6. Prim's MST
# ---------------------------------------------------------------------------
def prim_mst(
    adj: AdjList, start: int, n: int
) -> Tuple[float, List[Tuple[int, int, float]]]:
    """
    Prim's algorithm for Minimum Spanning Tree using a min-heap.

    Algorithm:
        1. Start from *start* vertex.
        2. Maintain a min-heap of (weight, from_vertex, to_vertex) for
           edges crossing the cut (visited / unvisited).
        3. Greedily pick the lightest crossing edge whose endpoint is
           unvisited.

    Time:  O((V + E) log V)
    Space: O(V + E)
    """
    visited = [False] * n
    mst_weight = 0.0
    mst_edges: List[Tuple[int, int, float]] = []

    # Heap: (weight, from_vertex, to_vertex)
    heap: List[Tuple[float, int, int]] = [(0.0, -1, start)]

    while heap and len(mst_edges) < n - 1:
        w, frm, to = heapq.heappop(heap)
        if visited[to]:
            continue
        visited[to] = True
        if frm != -1:
            mst_weight += w
            mst_edges.append((frm, to, w))

        for neighbor, weight in adj[to]:
            if not visited[neighbor]:
                heapq.heappush(heap, (weight, to, neighbor))

    return mst_weight, mst_edges


# ===========================================================================
# Test Cases
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Week 22 — Advanced Graphs")
    print("=" * 60)

    # --- Dijkstra ----------------------------------------------------------
    print("\n--- Dijkstra ---")
    edges_d = [
        (0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1),
        (2, 3, 5), (3, 4, 3),
    ]
    adj_d, verts_d = build_adj_list(edges_d, directed=True)
    dist, parent = dijkstra(adj_d, 0, verts_d)
    print(f"Distances from 0: {dist}")
    assert dist[0] == 0 and dist[1] == 3 and dist[3] == 4 and dist[4] == 7

    path = reconstruct_path(parent, 4)
    print(f"Shortest path 0 -> 4: {path}")
    assert path == [0, 2, 1, 3, 4]

    # --- Bellman-Ford ------------------------------------------------------
    print("\n--- Bellman-Ford ---")
    edges_bf = [
        (0, 1, -1), (0, 2, 4), (1, 2, 3),
        (1, 3, 2), (1, 4, 2), (3, 2, 5),
        (3, 1, 1), (4, 3, -3),
    ]
    verts_bf = {0, 1, 2, 3, 4}
    dist_bf, parent_bf = bellman_ford(edges_bf, 0, verts_bf)
    assert dist_bf is not None
    print(f"Distances from 0: {dist_bf}")
    assert dist_bf[0] == 0 and dist_bf[1] == -1 and dist_bf[4] == 1

    # Negative cycle test
    edges_neg = [(0, 1, 1), (1, 2, -1), (2, 0, -1)]
    verts_neg = {0, 1, 2}
    dist_neg, _ = bellman_ford(edges_neg, 0, verts_neg)
    assert dist_neg is None
    print("Negative cycle detected correctly.")

    # --- Floyd-Warshall ----------------------------------------------------
    print("\n--- Floyd-Warshall ---")
    edges_fw = [
        (0, 1, 3), (0, 2, 8), (0, 4, -4),
        (1, 3, 1), (1, 4, 7),
        (2, 1, 4),
        (3, 0, 2), (3, 2, -5),
        (4, 3, 6),
    ]
    dist_fw, nxt_fw = floyd_warshall(5, edges_fw)
    print("Floyd-Warshall distance matrix:")
    for row in dist_fw:
        print(f"  {row}")
    assert dist_fw[0][3] == 2   # 0->4->3 = -4+6 = 2
    assert dist_fw[3][1] == -1  # 3->2->1 = -5+4 = -1

    path_fw = reconstruct_path_fw(nxt_fw, 0, 2)
    print(f"Path 0 -> 2: {path_fw}")

    # --- Union-Find --------------------------------------------------------
    print("\n--- Union-Find ---")
    uf = UnionFind(6)
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(0, 3)
    assert uf.connected(0, 2) is True
    assert uf.connected(0, 4) is False
    assert uf.count == 3  # {0,1,2,3}, {4}, {5}
    print(f"Components: {uf.count}, connected(0,2)={uf.connected(0,2)}")

    # --- Kruskal's MST -----------------------------------------------------
    print("\n--- Kruskal's MST ---")
    #   0 --1-- 1
    #   |      /|
    #   4    3  2
    #   |  /    |
    #   3 --5-- 2
    mst_edges_input = [
        (0, 1, 1), (0, 3, 4), (1, 2, 2), (1, 3, 3),
        (2, 3, 5), (2, 4, 6), (3, 4, 7),
    ]
    total, mst = kruskal_mst(5, mst_edges_input)
    print(f"MST weight: {total}, edges: {mst}")
    assert total == 12  # 1 + 2 + 3 + 6

    # --- Prim's MST --------------------------------------------------------
    print("\n--- Prim's MST ---")
    adj_p, verts_p = build_adj_list(mst_edges_input, directed=False)
    total_p, mst_p = prim_mst(adj_p, 0, 5)
    print(f"MST weight: {total_p}, edges: {mst_p}")
    assert total_p == 12

    print("\nAll tests passed!")
