"""
WEEK 22 - PYTHON ADVANCED DSA
Topic: Shortest Path Algorithms (Dijkstra, Bellman-Ford, Floyd-Warshall)
File: 1.ShortestPaths.py

CONCEPT:
    Single-source and all-pairs shortest path algorithms on weighted graphs.
    Dijkstra:       single-source, NON-NEGATIVE weights only.
    Bellman-Ford:   single-source, allows negative weights, detects
                    negative-weight cycles.
    Floyd-Warshall: all-pairs, dynamic programming, O(V^3).

KEY POINTS:
    - Dijkstra uses a min-heap keyed by tentative distance.
    - Bellman-Ford relaxes all edges V-1 times. A V-th relaxation that
      still improves a distance proves a negative cycle is reachable.
    - Floyd-Warshall iterates over allowed intermediate vertex set
      {0..k}; recurrence d[i][j] = min(d[i][j], d[i][k] + d[k][j]).
    - Use a "large but safe" sentinel (INF // 2) so additions don't overflow.

ALGORITHM / APPROACH:
    Dijkstra(adj, src):
        dist = [INF] * V; dist[src] = 0
        push (0, src) onto heap
        while heap:
            d, u = heappop
            if d > dist[u]: continue
            for (v, w) in adj[u]:
                if d + w < dist[v]:
                    dist[v] = d + w; push (dist[v], v)

    BellmanFord(V, edges, src):
        for V-1 times: relax every edge.
        for every edge: if still relaxable -> negative cycle.

    FloydWarshall(V, edges):
        d[i][i] = 0; d[u][v] = w for each edge.
        for k in V: for i in V: for j in V:
            d[i][j] = min(d[i][j], d[i][k] + d[k][j])

PYTHON-SPECIFIC NOTES vs JAVA:
    - heapq is a min-heap; push tuples (dist, vertex).
    - math.inf is a clean sentinel; comparisons just work.
    - Adjacency list as list[list[tuple[int,int]]] reads cleanly.
    - List comprehensions replace explicit fills.

DRY RUN (Dijkstra example, undirected):
    V=5, edges {(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5),(3,4,3)}
    Start dist=[0,inf,inf,inf,inf]; pq=[(0,0)].
    Pop (0,0): relax 1->4, 2->1; pq=[(1,2),(4,1)].
    Pop (1,2): relax 1->1+2=3, 3->1+5=6; pq=[(3,1),(4,1),(6,3)].
    Pop (3,1): relax 3->3+1=4; pq=[(4,1),(4,3),(6,3)].
    Pop (4,1) -> stale (3 already known); skip.
    Pop (4,3): relax 4->4+3=7; pq=[(6,3),(7,4)].
    Pop (6,3) stale; pop (7,4) -> nothing new.
    Final: [0, 3, 1, 4, 7].

COMPLEXITY:
    Dijkstra:       O((V + E) log V)
    Bellman-Ford:   O(V * E)
    Floyd-Warshall: O(V^3) time, O(V^2) space.
"""

from __future__ import annotations
import heapq
import math
from typing import List, Tuple, Optional

INF = math.inf


def dijkstra(adj: List[List[Tuple[int, int]]], src: int, V: int) -> List[float]:
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
    return dist


def bellman_ford(V: int, edges: List[Tuple[int, int, int]], src: int) -> Optional[List[float]]:
    dist: List[float] = [INF] * V
    dist[src] = 0
    for _ in range(V - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    # Negative cycle check
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            print("Negative weight cycle detected!")
            return None
    return dist


def floyd_warshall(V: int, edges: List[Tuple[int, int, int]]) -> Optional[List[List[float]]]:
    dist: List[List[float]] = [[INF] * V for _ in range(V)]
    for i in range(V):
        dist[i][i] = 0
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
    for k in range(V):
        for i in range(V):
            dik = dist[i][k]
            if dik == INF:
                continue
            row_i = dist[i]
            row_k = dist[k]
            for j in range(V):
                if dik + row_k[j] < row_i[j]:
                    row_i[j] = dik + row_k[j]
    for i in range(V):
        if dist[i][i] < 0:
            print("Negative cycle!")
            return None
    return dist


def main() -> None:
    print("=== Dijkstra ===")
    V = 5
    adj: List[List[Tuple[int, int]]] = [[] for _ in range(V)]
    edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    print("Shortest distances from 0:", dijkstra(adj, 0, V))  # [0, 3, 1, 4, 7]

    print("\n=== Bellman-Ford ===")
    bf_edges = [(0, 1, -1), (0, 2, 4), (1, 2, 3), (1, 3, 2),
                (1, 4, 2), (3, 2, 5), (3, 1, 1), (4, 3, -3)]
    print("Shortest distances from 0:", bellman_ford(5, bf_edges, 0))  # [0, -1, 2, -2, 1]

    print("\n=== Floyd-Warshall ===")
    fw_edges = [(0, 1, 3), (0, 3, 7), (1, 0, 8), (1, 2, 2),
                (2, 0, 5), (2, 3, 1), (3, 0, 2)]
    ap = floyd_warshall(4, fw_edges)
    print("All-pairs shortest paths:")
    for row in ap or []:
        print("  " + " ".join(f"{('INF' if v == INF else int(v))!s:>4}" for v in row))


if __name__ == "__main__":
    main()
