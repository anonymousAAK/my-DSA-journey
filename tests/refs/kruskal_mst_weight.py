"""Reference: total weight of a minimum spanning tree via Kruskal + union-find."""

from __future__ import annotations
from typing import List, Tuple


class _DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
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


def kruskalMST(V: int, edges: List[Tuple[int, int, int]]) -> int:
    edges_sorted = sorted(edges, key=lambda e: e[2])
    dsu = _DSU(V)
    total = 0
    used = 0
    for u, v, w in edges_sorted:
        if dsu.union(u, v):
            total += w
            used += 1
            if used == V - 1:
                break
    return total
