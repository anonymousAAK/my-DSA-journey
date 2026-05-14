"""
WEEK 17 - PYTHON DSA
Topic: Topological Sort (DFS post-order + Kahn's BFS)
File: 2.TopologicalSort.py

CONCEPT:
    A topological order of a DAG (Directed Acyclic Graph) is any linear
    sequence of vertices in which every edge u -> v has u BEFORE v.
    It does not exist if the graph contains a cycle.

KEY POINTS:
    - Only DAGs have topological orders; multiple valid orders may exist.
    - Two standard algorithms:
        DFS:    finish-time stack — push v after recursing on all its successors.
        Kahn:   repeatedly remove nodes whose in-degree is 0.
    - Kahn doubles as cycle detection: if some nodes remain with in-degree > 0
      after the loop, those nodes participate in a cycle.
    - DFS with three colour-states (white/grey/black) detects cycles in
      directed graphs without computing any order.

ALGORITHM / APPROACH:
    DFS topo:
        for each unvisited u:
            DFS(u)                               # visits all descendants
        DFS(u):
            mark u visited
            for v in adj[u]:
                if not visited[v]: DFS(v)
            stack.append(u)                      # POST-ORDER push
        result = stack reversed

    Kahn:
        compute indegree[v] for every v
        queue = nodes with indegree 0
        while queue:
            u = queue.popleft(); result.append(u)
            for v in adj[u]:
                indegree[v] -= 1
                if indegree[v] == 0: queue.append(v)
        if len(result) != V: cycle detected

PYTHON-SPECIFIC NOTES:
    - `collections.deque` for the Kahn queue.
    - DFS uses recursion — for huge DAGs, switch to an iterative variant.
    - Indegree array: a plain `list[int]` of length V works perfectly.
    - Returning `Optional[List[int]]` (None == cycle) mirrors Java's null sentinel.

DRY RUN:
    Edges: 5->2, 5->0, 4->0, 4->1, 2->3, 3->1
    Indegrees: [0:2, 1:2, 2:1, 3:1, 4:0, 5:0]
    Kahn:  queue=[4,5]
        pop 4 -> result=[4]; dec 0,1 -> indeg [1,1,1,1,_,_]
        pop 5 -> result=[4,5]; dec 2,0 -> indeg [0,1,0,1,_,_]
        pop 0 -> result=[4,5,0]
        pop 2 -> result=[4,5,0,2]; dec 3 -> indeg[3]=0
        pop 3 -> result=[4,5,0,2,3]; dec 1 -> indeg[1]=0
        pop 1 -> result=[4,5,0,2,3,1]   (length == V, valid)

    Cyclic graph 0->1->2->3->1 :
        indegrees [0,2,1,1]; queue=[0]
        pop 0 -> indeg[1]=1; queue empty
        only 1 of 4 produced -> cycle

COMPLEXITY:
    Both algorithms: O(V + E) time, O(V) extra space.
"""

from __future__ import annotations
from collections import deque
from typing import List, Optional


class DiGraph:
    def __init__(self, v: int) -> None:
        self.V = v
        self.adj: List[List[int]] = [[] for _ in range(v)]

    def add_edge(self, u: int, v: int) -> None:
        self.adj[u].append(v)

    # APPROACH 1: DFS post-order
    def topo_sort_dfs(self) -> List[int]:
        visited = [False] * self.V
        stack: List[int] = []

        def dfs(u: int) -> None:
            visited[u] = True
            for v in self.adj[u]:
                if not visited[v]:
                    dfs(v)
            stack.append(u)                       # POST-ORDER push

        for i in range(self.V):
            if not visited[i]:
                dfs(i)
        stack.reverse()
        return stack

    # APPROACH 2: Kahn's BFS / indegree algorithm
    def topo_sort_kahn(self) -> Optional[List[int]]:
        indeg = [0] * self.V
        for u in range(self.V):
            for v in self.adj[u]:
                indeg[v] += 1

        q: deque[int] = deque(i for i in range(self.V) if indeg[i] == 0)
        result: List[int] = []
        while q:
            u = q.popleft()
            result.append(u)
            for v in self.adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

        return result if len(result) == self.V else None

    # Cycle detection in a directed graph using 3-colour DFS.
    def has_cycle(self) -> bool:
        WHITE, GREY, BLACK = 0, 1, 2
        state = [WHITE] * self.V

        def dfs(u: int) -> bool:
            state[u] = GREY
            for v in self.adj[u]:
                if state[v] == GREY:              # back edge -> cycle
                    return True
                if state[v] == WHITE and dfs(v):
                    return True
            state[u] = BLACK
            return False

        return any(state[i] == WHITE and dfs(i) for i in range(self.V))


def main() -> None:
    # 5->2, 5->0, 4->0, 4->1, 2->3, 3->1
    g = DiGraph(6)
    for u, v in [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]:
        g.add_edge(u, v)

    print("DFS topological sort: ", g.topo_sort_dfs())
    print("Kahn topological sort:", g.topo_sort_kahn())
    print("Has cycle:", g.has_cycle())   # False

    # Graph WITH a cycle
    cyclic = DiGraph(4)
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 1)]:
        cyclic.add_edge(u, v)
    print("\nCyclic graph:")
    print("Has cycle:", cyclic.has_cycle())          # True
    print("Kahn (None on cycle):", cyclic.topo_sort_kahn())

    # Build-system example
    print("\n=== Build System ===")
    build = DiGraph(5)   # 0=download, 1=compile, 2=test, 3=package, 4=deploy
    for u, v in [(0, 1), (1, 2), (1, 3), (2, 3), (3, 4)]:
        build.add_edge(u, v)
    print("Build order:", build.topo_sort_kahn())


if __name__ == "__main__":
    main()


"""
NOTES (Python vs Java):
    - Java's Deque<Integer> stack with push/pop matches Python's list .append/.pop.
    - Returning None (instead of null) for the "cycle detected" branch is
      idiomatic; pair it with `Optional[List[int]]` in the type hint.
    - The 3-colour cycle-detection DFS uses small int constants; Python lacks
      enums by default but a simple WHITE/GREY/BLACK = 0,1,2 is clearest.
    - Recursive DFS is fine for medium graphs; switch to iterative + manual
      stack when V exceeds ~50,000 to avoid hitting recursionlimit.
    - `deque(i for i in range(V) if indeg[i] == 0)` builds the seed queue
      lazily — same as Java's filtered for-loop, in one line.
"""
