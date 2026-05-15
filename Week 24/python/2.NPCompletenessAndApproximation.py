"""
WEEK 24 - PYTHON ADVANCED DSA
Topic: NP-Completeness & Approximation Algorithms
File: 2.NPCompletenessAndApproximation.py

CONCEPT:
    P:  problems solvable in polynomial time.
    NP: problems verifiable in polynomial time.
    NP-Complete: in NP and every NP problem reduces to it (poly-time).
    For NP-Complete problems we use approximation algorithms with
    provable ratios:
        - Vertex Cover: 2-approximation by maximal matching.
        - Set Cover:    O(log n) greedy.
        - Metric TSP:   2-approximation via MST + DFS preorder.

KEY POINTS:
    - 2-approx vertex cover: for every uncovered edge add BOTH endpoints.
    - Greedy set cover: pick the set with the most uncovered elements.
    - Metric TSP: under triangle inequality, MST -> DFS preorder gives
      a Hamiltonian tour with cost <= 2 * OPT.

ALGORITHM / APPROACH:
    vertex_cover_2approx(V, edges):
        for each edge (u,v): if neither covered, add both to cover.

    set_cover_greedy(U, sets):
        while uncovered:
            pick set with max |S ∩ uncovered|; remove S; add to chosen.

    tsp_2approx(dist):
        1. Build MST via Prim's (O(V^2) with adjacency matrix).
        2. DFS preorder traversal of MST, shortcutting repeats.
        3. Tour cost <= 2 * MST_weight <= 2 * OPT.

PYTHON-SPECIFIC NOTES vs JAVA:
    - Use sets / dicts for clean vertex/element bookkeeping.
    - The 2-approx for vertex cover is a one-liner with a comprehension
      style loop; readability over micro-optimisation.

DRY RUN:
    Vertex cover graph: edges {(0,1),(0,2),(1,3),(2,3),(3,4)}.
        Process (0,1): add 0,1. (0,2): 0 already covered, skip.
        (1,3): 1 covered, skip. (2,3): add 2,3. (3,4): 3 covered, skip.
        Cover {0,1,2,3} (size 4). OPT here is {0,3} (size 2). Ratio 2.

    TSP 2-approx for the symmetric 4-city matrix in main():
        MST weight 50; preorder DFS yields tour cost <= 100.

COMPLEXITY:
    Vertex cover:  O(E).
    Set cover:     O(|sets| * |U|) per iteration; iterations <= |sets|.
    TSP 2-approx:  O(V^2) for Prim with adjacency matrix.
"""

from __future__ import annotations
from typing import List, Set, Tuple


def vertex_cover_2approx(V: int, edges: List[Tuple[int, int]]) -> Set[int]:
    covered = [False] * V
    cover: Set[int] = set()
    for u, v in edges:
        if not covered[u] and not covered[v]:
            covered[u] = True
            covered[v] = True
            cover.add(u)
            cover.add(v)
    return cover


def set_cover_greedy(universe_size: int, sets: List[Set[int]]) -> List[int]:
    uncovered = set(range(universe_size))
    chosen: List[int] = []
    while uncovered:
        best_idx = -1
        best_cnt = 0
        for i, s in enumerate(sets):
            cnt = sum(1 for x in s if x in uncovered)
            if cnt > best_cnt:
                best_cnt = cnt
                best_idx = i
        if best_idx == -1:
            break
        chosen.append(best_idx)
        uncovered -= sets[best_idx]
    return chosen


def tsp_2approx(dist: List[List[int]]) -> Tuple[List[int], int]:
    n = len(dist)
    INF = 10 ** 18
    in_mst = [False] * n
    parent = [-1] * n
    key = [INF] * n
    key[0] = 0
    for _ in range(n - 1):
        u = -1
        for v in range(n):
            if not in_mst[v] and (u == -1 or key[v] < key[u]):
                u = v
        in_mst[u] = True
        for v in range(n):
            if not in_mst[v] and dist[u][v] < key[v]:
                key[v] = dist[u][v]
                parent[v] = u

    mst: List[List[int]] = [[] for _ in range(n)]
    for i in range(1, n):
        mst[parent[i]].append(i)
        mst[i].append(parent[i])

    tour: List[int] = []
    visited = [False] * n
    stack = [0]
    while stack:
        u = stack.pop()
        if visited[u]:
            continue
        visited[u] = True
        tour.append(u)
        for v in reversed(mst[u]):
            if not visited[v]:
                stack.append(v)

    total = sum(dist[tour[i]][tour[(i + 1) % n]] for i in range(n))
    print(f"TSP 2-Approx tour: {tour}, cost: {total}")
    return tour, total


def main() -> None:
    print("=== Vertex Cover (2-approximation) ===")
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
    cover = vertex_cover_2approx(5, edges)
    print("2-approx vertex cover:", sorted(cover))
    print("Cover size:", len(cover))

    print("\n=== Set Cover (greedy) ===")
    sets = [
        {0, 1, 2}, {3, 4, 5}, {4, 5, 6, 7}, {0, 3, 8}, {2, 7, 9}
    ]
    chosen = set_cover_greedy(10, sets)
    print("Chosen set indices:", chosen)
    covered: Set[int] = set()
    for i in chosen:
        covered |= sets[i]
    print("Covered elements:", sorted(covered))

    print("\n=== TSP 2-Approximation (metric) ===")
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    tsp_2approx(dist)
    print("(Optimal tour cost for this instance: 80)")

    print("\n=== P vs NP Key Points ===")
    print("- P: problems solvable in poly time (sorting, shortest path, MST)")
    print("- NP: problems verifiable in poly time (TSP, vertex cover, 3-SAT)")
    print("- NP-Hard: at least as hard as NP-Complete problems")
    print("- If P=NP, all encryption would break (RSA, AES rely on hard problems)")
    print("- Most believe P!=NP (Clay Millennium Prize: $1M for proof)")
    print("- Approximation algorithms: practical solutions with quality guarantees")


if __name__ == "__main__":
    main()
