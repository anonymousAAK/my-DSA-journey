"""Reference: topological sort via Kahn's algorithm.

Because many valid orderings may exist, this driver always uses an indegree-0
queue that pops the smallest available vertex first (a deterministic
tie-break). The fixture's `expected` values are produced under the same rule.
Returns None if a cycle is detected.
"""

from __future__ import annotations
import heapq
from typing import List, Optional, Tuple


def topologicalSort(V: int, edges: List[Tuple[int, int]]) -> Optional[List[int]]:
    adj: List[List[int]] = [[] for _ in range(V)]
    indeg = [0] * V
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1

    heap: List[int] = [i for i in range(V) if indeg[i] == 0]
    heapq.heapify(heap)

    result: List[int] = []
    while heap:
        u = heapq.heappop(heap)
        result.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)

    return result if len(result) == V else None
