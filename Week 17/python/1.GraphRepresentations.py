"""
WEEK 17 - PYTHON DSA
Topic: Graph Representations + BFS/DFS
File: 1.GraphRepresentations.py

CONCEPT:
    A graph G = (V, E) is a set of vertices and edges. Edges may be
    directed/undirected, weighted/unweighted. Two storage forms dominate:

        Adjacency MATRIX  - V x V grid; mat[u][v]==1 if edge.   O(V^2) space.
        Adjacency LIST    - dict / list-of-lists of neighbours. O(V+E) space.

    Most real graphs are sparse (E << V^2), so adjacency lists win.

KEY POINTS:
    - BFS uses a FIFO queue; explores level by level; finds shortest unweighted
      path; O(V + E).
    - DFS uses recursion or an explicit stack; goes as deep as possible;
      O(V + E); foundation of cycle detection, topological sort, components.
    - Cycle detection (undirected): during DFS, finding a visited neighbour
      that isn't the parent means there is a back edge.
    - Bipartite check: 2-colour with BFS; conflict means odd cycle exists.

ALGORITHM / APPROACH:
    BFS(src):
        visited[src] = True; queue = [src]
        while queue:
            u = queue.popleft()
            yield u
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)

    DFS(u):
        visited[u] = True
        yield u
        for v in adj[u]:
            if not visited[v]: DFS(v)

PYTHON-SPECIFIC NOTES:
    - `collections.deque` is the right structure for the BFS queue
      (popleft is O(1) — list.pop(0) would be O(n)).
    - Use list of lists `adj: List[List[int]]` indexed by vertex.
    - Recursion limit defaults to 1000; for huge graphs prefer an iterative
      DFS with a manual stack.
    - Type hints come from `typing` (`List`, `Optional`).

DRY RUN:
    Graph (undirected, V=6):  edges 0-1,1-2,2-5,5-4,4-3,3-0,1-4
        adj[0]=[1,3]  adj[1]=[0,2,4]  adj[2]=[1,5]
        adj[3]=[4,0]  adj[4]=[5,3,1]  adj[5]=[2,4]

    BFS(0):
        queue=[0] visited={0}; pop 0 -> add 1,3   queue=[1,3]
        pop 1 -> add 2,4                          queue=[3,2,4]
        pop 3                                     queue=[2,4]
        pop 2 -> add 5                            queue=[4,5]
        pop 4                                     queue=[5]
        pop 5                                     queue=[]
        result: [0,1,3,2,4,5]

    countComponents(g2 with edges 0-1,1-2,3-4 and isolated 5):
        DFS(0) covers {0,1,2}; DFS(3) covers {3,4}; DFS(5) covers {5}.
        => 3 components.

COMPLEXITY:
    Build       O(V + E)
    BFS/DFS     O(V + E)
    components  O(V + E)
    cycle/bipartite  O(V + E)
"""

from __future__ import annotations
from collections import deque
from typing import List, Optional


class Graph:
    """Undirected/directed graph stored as an adjacency list."""

    def __init__(self, v: int) -> None:
        self.V: int = v
        self.adj: List[List[int]] = [[] for _ in range(v)]

    def add_edge(self, u: int, v: int) -> None:
        """Undirected edge."""
        self.adj[u].append(v)
        self.adj[v].append(u)

    def add_directed_edge(self, u: int, v: int) -> None:
        self.adj[u].append(v)

    # BFS visit order from src
    def bfs(self, src: int) -> List[int]:
        visited = [False] * self.V
        order: List[int] = []
        q: deque[int] = deque([src])
        visited[src] = True
        while q:
            u = q.popleft()
            order.append(u)
            for v in self.adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append(v)
        return order

    # BFS shortest unweighted distance from src; -1 means unreachable
    def shortest_distances(self, src: int) -> List[int]:
        dist = [-1] * self.V
        dist[src] = 0
        q: deque[int] = deque([src])
        while q:
            u = q.popleft()
            for v in self.adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)
        return dist

    # DFS recursive
    def dfs(self, src: int) -> List[int]:
        visited = [False] * self.V
        order: List[int] = []

        def go(u: int) -> None:
            visited[u] = True
            order.append(u)
            for v in self.adj[u]:
                if not visited[v]:
                    go(v)

        go(src)
        return order

    def count_components(self) -> int:
        visited = [False] * self.V

        def go(u: int) -> None:
            visited[u] = True
            for v in self.adj[u]:
                if not visited[v]:
                    go(v)

        count = 0
        for i in range(self.V):
            if not visited[i]:
                go(i)
                count += 1
        return count

    # Cycle in UNDIRECTED graph
    def has_cycle(self) -> bool:
        visited = [False] * self.V

        def go(u: int, parent: int) -> bool:
            visited[u] = True
            for v in self.adj[u]:
                if not visited[v]:
                    if go(v, u):
                        return True
                elif v != parent:
                    return True       # back edge -> cycle
            return False

        for i in range(self.V):
            if not visited[i] and go(i, -1):
                return True
        return False

    # Bipartite check via BFS 2-colouring
    def is_bipartite(self) -> bool:
        color = [0] * self.V          # 0 unvisited, 1/-1 are the two colours
        for start in range(self.V):
            if color[start] != 0:
                continue
            color[start] = 1
            q: deque[int] = deque([start])
            while q:
                u = q.popleft()
                for v in self.adj[u]:
                    if color[v] == 0:
                        color[v] = -color[u]
                        q.append(v)
                    elif color[v] == color[u]:
                        return False
        return True


# Adjacency MATRIX representation — included to mirror Java commentary.
class GraphMatrix:
    def __init__(self, v: int) -> None:
        self.V = v
        self.mat: List[List[int]] = [[0] * v for _ in range(v)]

    def add_edge(self, u: int, v: int) -> None:
        self.mat[u][v] = 1
        self.mat[v][u] = 1

    def neighbours(self, u: int) -> List[int]:
        return [v for v in range(self.V) if self.mat[u][v]]


def main() -> None:
    #  0 -- 1 -- 2
    #  |    |    |
    #  3 -- 4 -- 5
    g = Graph(6)
    for u, v in [(0, 1), (1, 2), (2, 5), (5, 4), (4, 3), (3, 0), (1, 4)]:
        g.add_edge(u, v)

    print("BFS from 0:", g.bfs(0))
    print("DFS from 0:", g.dfs(0))
    print("Distances from 0:", g.shortest_distances(0))
    print("Components:", g.count_components())   # 1
    print("Has cycle:", g.has_cycle())           # True
    print("Bipartite:", g.is_bipartite())

    # Disconnected graph
    g2 = Graph(6)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(3, 4)
    print("\nDisconnected components:", g2.count_components())  # 3
    print("BFS from 0:", g2.bfs(0))

    # K_{2,3} bipartite
    bip = Graph(5)
    for u in (0, 1):
        for v in (2, 3, 4):
            bip.add_edge(u, v)
    print("\nK_{2,3} bipartite:", bip.is_bipartite())  # True

    # Triangle (odd cycle) -> not bipartite
    tri = Graph(3)
    tri.add_edge(0, 1)
    tri.add_edge(1, 2)
    tri.add_edge(2, 0)
    print("Triangle bipartite:", tri.is_bipartite())   # False

    # Show matrix representation too
    m = GraphMatrix(4)
    m.add_edge(0, 1)
    m.add_edge(1, 2)
    m.add_edge(2, 3)
    print("\nMatrix neighbours of 1:", m.neighbours(1))


if __name__ == "__main__":
    main()


"""
NOTES (Python vs Java):
    - Java uses LinkedList<Integer> for the BFS queue; Python's
      collections.deque is the equivalent O(1)-popleft container.
    - Java's `boolean[]` is a primitive array; Python uses [False]*n.
    - Recursive DFS is convenient in both but Python's recursion limit
      (sys.getrecursionlimit() == 1000) bites earlier. For very deep graphs,
      raise the limit or rewrite iteratively.
    - Defining a closure (`def go(u): ...`) lets us capture `visited`
      without passing it explicitly — cleaner than Java's helper signatures.
    - Adjacency-list as `list[list[int]]` is cache-friendly enough for most
      problems. For very dense graphs, swap to a numpy 2D array.
"""
