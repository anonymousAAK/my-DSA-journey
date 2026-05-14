"""
WEEK 22 - PYTHON ADVANCED DSA
Topic: Minimum Spanning Tree (Kruskal + Prim) & Union-Find
File: 2.MinimumSpanningTree.py

CONCEPT:
    Given a connected, undirected, weighted graph, an MST is a spanning
    tree (V-1 edges, no cycle, all vertices reached) with minimum total
    edge weight. Two classic greedy algorithms:
        - Kruskal: pick globally cheapest edge that doesn't form a cycle.
        - Prim:    grow a single tree from one vertex by repeatedly adding
                   the cheapest edge crossing the cut.

KEY POINTS:
    - Union-Find (DSU) supports near-O(1) cycle detection for Kruskal.
      Optimisations: path compression (find), union by rank (union).
    - Prim uses a priority queue keyed by candidate edge weight.
    - Both correctly produce an MST due to the cut property: the lightest
      edge crossing any cut belongs to some MST.

ALGORITHM / APPROACH:
    DSU:
        find(x): if parent[x] != x: parent[x] = find(parent[x]); return parent[x]
        union(x,y): if same root, no-op; else attach lighter-rank under heavier.
    Kruskal:
        sort edges by weight
        for each edge (u,v,w):
            if union(u,v): include edge; stop when V-1 edges chosen.
    Prim:
        start key[0]=0, push (0,0); visited=set()
        while pq:
            w, u = heappop
            if u in visited: continue
            visited.add(u); add w to total
            for (v, ew) in adj[u]:
                if v not in visited and ew < key[v]:
                    key[v] = ew; push (ew, v)

PYTHON-SPECIFIC NOTES vs JAVA:
    - heapq for the priority queue.
    - Use a list `parent` and `rank` of length V; integer-keyed.
    - sorted() returns a new list — easier than `Arrays.sort` mutation.

DRY RUN:
    V=4, edges (0,1,4),(0,2,3),(1,2,1),(1,3,2),(2,3,4).
    Sorted: (1,2,1),(1,3,2),(0,2,3),(0,1,4),(2,3,4).
    Kruskal: pick (1,2,1) -> union; pick (1,3,2) -> union; pick (0,2,3) -> union.
    Total weight = 1+2+3 = 6. Three edges chosen, V-1=3, done.

COMPLEXITY:
    DSU:     amortised O(alpha(n)) ~ O(1).
    Kruskal: O(E log E).
    Prim:    O((V+E) log V) with binary heap.
"""

from __future__ import annotations
import heapq
from typing import List, Tuple


class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        # iterative path compression
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            nxt = self.parent[x]
            self.parent[x] = root
            x = nxt
        return root

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


def kruskal_mst(V: int, edges: List[Tuple[int, int, int]]) -> int:
    edges = sorted(edges, key=lambda e: e[2])
    dsu = DSU(V)
    total, used = 0, 0
    print("Kruskal MST edges:")
    for u, v, w in edges:
        if used == V - 1:
            break
        if dsu.union(u, v):
            total += w
            used += 1
            print(f"  Edge ({u} - {v}): weight {w}")
    return total


def prim_mst(V: int, adj: List[List[Tuple[int, int]]]) -> int:
    in_mst = [False] * V
    key = [float("inf")] * V
    parent = [-1] * V
    key[0] = 0
    pq: List[Tuple[float, int]] = [(0, 0)]
    total = 0
    print("Prim MST edges:")
    while pq:
        w, u = heapq.heappop(pq)
        if in_mst[u]:
            continue
        in_mst[u] = True
        total += w
        if parent[u] != -1:
            print(f"  Edge ({parent[u]} - {u}): weight {w}")
        for v, ew in adj[u]:
            if not in_mst[v] and ew < key[v]:
                key[v] = ew
                parent[v] = u
                heapq.heappush(pq, (ew, v))
    return total


def main() -> None:
    V = 4
    edges = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4)]

    print("=== Kruskal's MST ===")
    print("Total MST weight:", kruskal_mst(V, list(edges)))

    adj: List[List[Tuple[int, int]]] = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    print("\n=== Prim's MST ===")
    print("Total MST weight:", prim_mst(V, adj))

    print("\n=== Union-Find Demo ===")
    dsu = DSU(6)
    dsu.union(0, 1); dsu.union(2, 3); dsu.union(4, 5)
    print("0 connected to 1:", dsu.connected(0, 1))  # True
    print("0 connected to 2:", dsu.connected(0, 2))  # False
    dsu.union(0, 2)
    print("0 connected to 3:", dsu.connected(0, 3))  # True


if __name__ == "__main__":
    main()
