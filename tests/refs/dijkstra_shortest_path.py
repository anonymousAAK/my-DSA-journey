"""Reference: Dijkstra shortest paths from `src` on a non-negative weighted graph.

Input edges are an undirected list `[u, v, w]`. Returns a list of integer
distances of length V; unreachable nodes report -1 (instead of a float `inf`,
to keep JSON-serialisable fixtures).
"""

from __future__ import annotations
import heapq
import math
from typing import List, Tuple


def dijkstra(V: int, edges: List[Tuple[int, int, int]], src: int) -> List[int]:
    adj: List[List[Tuple[int, int]]] = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    INF = math.inf
    dist: List[float] = [INF] * V
    dist[src] = 0
    pq: List[Tuple[float, int]] = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    return [-1 if d == INF else int(d) for d in dist]
