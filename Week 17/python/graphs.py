"""
Week 17: Graphs
================
A graph G = (V, E) consists of vertices V and edges E.  Graphs can be directed
or undirected, weighted or unweighted.

Representation used here: adjacency list via a dict of lists.

Topics covered:
    1. Graph class with adjacency list (directed & undirected)
    2. BFS — returns traversal order and shortest distances (unweighted)
    3. DFS — recursive and iterative
    4. Connected components count (undirected)
    5. Cycle detection — undirected (DFS) + directed (DFS with coloring)
    6. Bipartite check (BFS 2-coloring)
    7. Topological sort — DFS-based + Kahn's BFS-based
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# 1. Graph Class — adjacency list representation
# ---------------------------------------------------------------------------
class Graph:
    """
    Graph represented as an adjacency list.

    Supports both directed and undirected graphs.
    Vertices can be any hashable type (int, str, etc.).
    """

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self.adj: Dict[int, List[int]] = defaultdict(list)
        self._vertices: Set[int] = set()

    def add_edge(self, u: int, v: int) -> None:
        """Add edge u -> v (and v -> u if undirected)."""
        self.adj[u].append(v)
        self._vertices.update([u, v])
        if not self.directed:
            self.adj[v].append(u)

    def add_vertex(self, v: int) -> None:
        """Ensure vertex *v* exists even if it has no edges."""
        self._vertices.add(v)

    @property
    def vertices(self) -> Set[int]:
        return self._vertices

    def __repr__(self) -> str:
        lines = [f"Graph(directed={self.directed})"]
        for v in sorted(self._vertices):
            lines.append(f"  {v} -> {self.adj[v]}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# 2. BFS — Breadth-First Search
# ---------------------------------------------------------------------------
def bfs(graph: Graph, source: int) -> Tuple[List[int], Dict[int, int]]:
    """
    Perform BFS from *source*.

    Returns:
        order     — list of vertices in the order they were visited
        distances — dict mapping each reachable vertex to its shortest
                    distance (number of edges) from *source*

    Time:  O(V + E)
    Space: O(V)
    """
    visited: Set[int] = {source}
    queue: deque[int] = deque([source])
    order: List[int] = []
    distances: Dict[int, int] = {source: 0}

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = distances[node] + 1
                queue.append(neighbor)

    return order, distances


# ---------------------------------------------------------------------------
# 3. DFS — Depth-First Search (recursive + iterative)
# ---------------------------------------------------------------------------
def dfs_recursive(graph: Graph, source: int) -> List[int]:
    """
    Recursive DFS from *source*.  Returns visit order.

    Time:  O(V + E)
    Space: O(V) — recursion stack in worst case (linear graph)
    """
    visited: Set[int] = set()
    order: List[int] = []

    def _dfs(node: int) -> None:
        visited.add(node)
        order.append(node)
        for neighbor in graph.adj[node]:
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(source)
    return order


def dfs_iterative(graph: Graph, source: int) -> List[int]:
    """
    Iterative DFS using an explicit stack.  Returns visit order.

    Note: the visit order may differ from recursive DFS because
    neighbors are pushed in reverse order onto the stack (so that
    the first neighbor is processed first, matching the recursive version).

    Time:  O(V + E)
    Space: O(V)
    """
    visited: Set[int] = set()
    stack: List[int] = [source]
    order: List[int] = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        # Push neighbors in reverse so that the first neighbor is popped first.
        for neighbor in reversed(graph.adj[node]):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


# ---------------------------------------------------------------------------
# 4. Connected Components Count (undirected graph)
# ---------------------------------------------------------------------------
def count_connected_components(graph: Graph) -> int:
    """
    Count the number of connected components in an undirected graph.

    Uses BFS from each unvisited vertex.

    Time:  O(V + E)
    Space: O(V)
    """
    visited: Set[int] = set()
    components = 0

    for v in graph.vertices:
        if v not in visited:
            components += 1
            # BFS to mark all vertices in this component
            queue: deque[int] = deque([v])
            visited.add(v)
            while queue:
                node = queue.popleft()
                for neighbor in graph.adj[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

    return components


# ---------------------------------------------------------------------------
# 5. Cycle Detection
# ---------------------------------------------------------------------------
def has_cycle_undirected(graph: Graph) -> bool:
    """
    Detect a cycle in an undirected graph using DFS.

    During DFS, if we encounter a visited neighbor that is *not* the parent
    of the current node, there is a cycle.

    Time:  O(V + E)
    Space: O(V)
    """
    visited: Set[int] = set()

    def _dfs(node: int, parent: int) -> bool:
        visited.add(node)
        for neighbor in graph.adj[node]:
            if neighbor not in visited:
                if _dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                # Visited neighbor that is not our parent => cycle
                return True
        return False

    for v in graph.vertices:
        if v not in visited:
            if _dfs(v, -1):
                return True
    return False


def has_cycle_directed(graph: Graph) -> bool:
    """
    Detect a cycle in a directed graph using DFS with 3-color marking.

    Colors:
        WHITE (0) — not yet visited
        GRAY  (1) — currently in the recursion stack (being processed)
        BLACK (2) — fully processed

    A back edge to a GRAY node indicates a cycle.

    Time:  O(V + E)
    Space: O(V)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color: Dict[int, int] = {v: WHITE for v in graph.vertices}

    def _dfs(node: int) -> bool:
        color[node] = GRAY
        for neighbor in graph.adj[node]:
            if color.get(neighbor, WHITE) == GRAY:
                return True  # back edge => cycle
            if color.get(neighbor, WHITE) == WHITE:
                if _dfs(neighbor):
                    return True
        color[node] = BLACK
        return False

    for v in graph.vertices:
        if color[v] == WHITE:
            if _dfs(v):
                return True
    return False


# ---------------------------------------------------------------------------
# 6. Bipartite Check (BFS 2-coloring)
# ---------------------------------------------------------------------------
def is_bipartite(graph: Graph) -> bool:
    """
    Check whether an undirected graph is bipartite (2-colorable).

    A graph is bipartite iff it contains no odd-length cycles.

    Strategy: BFS from each unvisited vertex, assigning alternating colors.
    If a neighbor already has the same color as the current node, the graph
    is not bipartite.

    Time:  O(V + E)
    Space: O(V)
    """
    color: Dict[int, int] = {}

    for start in graph.vertices:
        if start in color:
            continue
        # BFS 2-coloring
        queue: deque[int] = deque([start])
        color[start] = 0
        while queue:
            node = queue.popleft()
            for neighbor in graph.adj[node]:
                if neighbor not in color:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
    return True


# ---------------------------------------------------------------------------
# 7. Topological Sort
# ---------------------------------------------------------------------------
def topological_sort_dfs(graph: Graph) -> Optional[List[int]]:
    """
    Topological sort of a directed acyclic graph (DAG) using DFS.

    Algorithm:
        - Run DFS; when a node is fully processed (all descendants visited),
          push it onto a stack.
        - The stack (reversed) gives a valid topological order.

    Returns None if the graph has a cycle.

    Time:  O(V + E)
    Space: O(V)
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color: Dict[int, int] = {v: WHITE for v in graph.vertices}
    result: List[int] = []

    def _dfs(node: int) -> bool:
        """Returns False if a cycle is detected."""
        color[node] = GRAY
        for neighbor in graph.adj[node]:
            if color.get(neighbor, WHITE) == GRAY:
                return False  # cycle
            if color.get(neighbor, WHITE) == WHITE:
                if not _dfs(neighbor):
                    return False
        color[node] = BLACK
        result.append(node)  # post-order
        return True

    for v in sorted(graph.vertices):  # sorted for deterministic output
        if color[v] == WHITE:
            if not _dfs(v):
                return None  # cycle detected

    result.reverse()
    return result


def topological_sort_kahn(graph: Graph) -> Optional[List[int]]:
    """
    Topological sort using Kahn's algorithm (BFS-based).

    Algorithm:
        1. Compute in-degree of every vertex.
        2. Enqueue all vertices with in-degree 0.
        3. Repeatedly dequeue a vertex, append to result, and decrement
           in-degrees of its neighbors.  Enqueue neighbors whose in-degree
           drops to 0.

    If the result contains fewer vertices than the graph, a cycle exists.

    Time:  O(V + E)
    Space: O(V)
    """
    in_degree: Dict[int, int] = {v: 0 for v in graph.vertices}
    for v in graph.vertices:
        for neighbor in graph.adj[v]:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1

    # Start with all zero-in-degree vertices.
    queue: deque[int] = deque(v for v in sorted(graph.vertices) if in_degree[v] == 0)
    result: List[int] = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph.adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(graph.vertices):
        return None  # cycle detected
    return result


# ===========================================================================
# Test Cases
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Week 17 — Graphs")
    print("=" * 60)

    # --- Build an undirected graph -----------------------------------------
    #  0 -- 1 -- 2
    #  |         |
    #  3    4 -- 5
    print("\n--- Undirected Graph ---")
    g = Graph(directed=False)
    for u, v in [(0, 1), (1, 2), (0, 3), (2, 5), (4, 5)]:
        g.add_edge(u, v)
    print(g)

    # --- BFS ---------------------------------------------------------------
    print("\n--- BFS from vertex 0 ---")
    order, dist = bfs(g, 0)
    print(f"Order: {order}, Distances: {dist}")
    assert dist[0] == 0
    assert dist[1] == 1
    assert dist[5] == 2 or dist[5] == 3  # depending on exploration order

    # --- DFS (recursive) ---------------------------------------------------
    print("\n--- DFS (recursive) from vertex 0 ---")
    rec_order = dfs_recursive(g, 0)
    print(f"Order: {rec_order}")
    assert rec_order[0] == 0

    # --- DFS (iterative) ---------------------------------------------------
    print("\n--- DFS (iterative) from vertex 0 ---")
    iter_order = dfs_iterative(g, 0)
    print(f"Order: {iter_order}")
    assert iter_order[0] == 0

    # --- Connected Components ----------------------------------------------
    print("\n--- Connected Components ---")
    g2 = Graph(directed=False)
    for u, v in [(0, 1), (1, 2), (3, 4)]:
        g2.add_edge(u, v)
    g2.add_vertex(5)  # isolated vertex
    cc = count_connected_components(g2)
    print(f"Components in g2: {cc}")
    assert cc == 3  # {0,1,2}, {3,4}, {5}

    # --- Cycle Detection (undirected) --------------------------------------
    print("\n--- Cycle Detection (Undirected) ---")
    g_cycle = Graph(directed=False)
    for u, v in [(0, 1), (1, 2), (2, 0)]:
        g_cycle.add_edge(u, v)
    assert has_cycle_undirected(g_cycle) is True
    print(f"Triangle 0-1-2: has_cycle = {has_cycle_undirected(g_cycle)}")

    g_no_cycle = Graph(directed=False)
    for u, v in [(0, 1), (1, 2)]:
        g_no_cycle.add_edge(u, v)
    assert has_cycle_undirected(g_no_cycle) is False
    print(f"Path 0-1-2: has_cycle = {has_cycle_undirected(g_no_cycle)}")

    # --- Cycle Detection (directed) ----------------------------------------
    print("\n--- Cycle Detection (Directed) ---")
    dg = Graph(directed=True)
    for u, v in [(0, 1), (1, 2), (2, 0)]:
        dg.add_edge(u, v)
    assert has_cycle_directed(dg) is True
    print(f"Directed cycle 0->1->2->0: has_cycle = {has_cycle_directed(dg)}")

    dag = Graph(directed=True)
    for u, v in [(0, 1), (0, 2), (1, 3), (2, 3)]:
        dag.add_edge(u, v)
    assert has_cycle_directed(dag) is False
    print(f"DAG: has_cycle = {has_cycle_directed(dag)}")

    # --- Bipartite Check ---------------------------------------------------
    print("\n--- Bipartite Check ---")
    g_bip = Graph(directed=False)
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 0)]:  # even cycle = bipartite
        g_bip.add_edge(u, v)
    assert is_bipartite(g_bip) is True
    print(f"4-cycle: is_bipartite = {is_bipartite(g_bip)}")

    g_not_bip = Graph(directed=False)
    for u, v in [(0, 1), (1, 2), (2, 0)]:  # triangle = NOT bipartite
        g_not_bip.add_edge(u, v)
    assert is_bipartite(g_not_bip) is False
    print(f"Triangle: is_bipartite = {is_bipartite(g_not_bip)}")

    # --- Topological Sort --------------------------------------------------
    print("\n--- Topological Sort ---")
    # DAG: 5->0, 5->2, 4->0, 4->1, 2->3, 3->1
    dag2 = Graph(directed=True)
    for u, v in [(5, 0), (5, 2), (4, 0), (4, 1), (2, 3), (3, 1)]:
        dag2.add_edge(u, v)

    topo_dfs = topological_sort_dfs(dag2)
    print(f"Topological sort (DFS):   {topo_dfs}")
    assert topo_dfs is not None

    topo_kahn = topological_sort_kahn(dag2)
    print(f"Topological sort (Kahn):  {topo_kahn}")
    assert topo_kahn is not None

    # Verify topological order: for every edge u->v, u appears before v.
    for topo in [topo_dfs, topo_kahn]:
        pos = {v: i for i, v in enumerate(topo)}
        for u in dag2.vertices:
            for v in dag2.adj[u]:
                assert pos[u] < pos[v], f"Edge {u}->{v} violates topological order"

    # Cycle case should return None
    assert topological_sort_dfs(dg) is None
    assert topological_sort_kahn(dg) is None
    print("Topological sort on cyclic graph: None (correct)")

    print("\nAll tests passed!")
