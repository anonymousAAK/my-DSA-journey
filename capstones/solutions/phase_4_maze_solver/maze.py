"""Maze: generator + four solvers (BFS / DFS / Dijkstra / A*).

Run ``python maze.py`` for a self-demo: generate a 21x21 maze, run each
solver, print a comparison table.

The maze is a 2D grid of cells where each cell stores walls toward its four
neighbours. We expose ``neighbors(cell)`` which yields *passable* neighbours,
so the solvers only see the graph view.
"""
from __future__ import annotations

import heapq
import json
import random
import sys
from collections import deque
from dataclasses import dataclass, field
from typing import Iterable


Cell = tuple[int, int]  # (row, col)


@dataclass
class Maze:
    rows: int
    cols: int
    # walls[r][c] is a set of "N"/"S"/"E"/"W" still present
    walls: list[list[set[str]]] = field(default_factory=list)
    # weights[r][c]: cost to enter cell (default 1). Dijkstra/A* use this.
    weights: list[list[int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.walls:
            self.walls = [
                [{"N", "S", "E", "W"} for _ in range(self.cols)] for _ in range(self.rows)
            ]
        if not self.weights:
            self.weights = [[1] * self.cols for _ in range(self.rows)]

    def in_bounds(self, c: Cell) -> bool:
        r, col = c
        return 0 <= r < self.rows and 0 <= col < self.cols

    def neighbors(self, c: Cell) -> Iterable[Cell]:
        r, col = c
        walls = self.walls[r][col]
        if "N" not in walls and r > 0:
            yield (r - 1, col)
        if "S" not in walls and r < self.rows - 1:
            yield (r + 1, col)
        if "E" not in walls and col < self.cols - 1:
            yield (r, col + 1)
        if "W" not in walls and col > 0:
            yield (r, col - 1)

    def carve(self, a: Cell, b: Cell) -> None:
        """Remove the wall between adjacent cells a and b."""
        ar, ac = a
        br, bc = b
        if ar == br and bc == ac + 1:
            self.walls[ar][ac].discard("E"); self.walls[br][bc].discard("W")
        elif ar == br and bc == ac - 1:
            self.walls[ar][ac].discard("W"); self.walls[br][bc].discard("E")
        elif ac == bc and br == ar + 1:
            self.walls[ar][ac].discard("S"); self.walls[br][bc].discard("N")
        elif ac == bc and br == ar - 1:
            self.walls[ar][ac].discard("N"); self.walls[br][bc].discard("S")
        else:
            raise ValueError(f"{a} and {b} are not adjacent")

    def render_ascii(self, path: list[Cell] | None = None) -> str:
        pset = set(path or [])
        out: list[str] = []
        # Top border
        out.append("+" + "---+" * self.cols)
        for r in range(self.rows):
            row_top = "|"
            row_bot = "+"
            for c in range(self.cols):
                walls = self.walls[r][c]
                mid = " * " if (r, c) in pset else "   "
                row_top += mid + ("|" if "E" in walls else " ")
                row_bot += ("---" if "S" in walls else "   ") + "+"
            out.append(row_top)
            out.append(row_bot)
        return "\n".join(out)

    def to_json(self) -> str:
        return json.dumps({
            "rows": self.rows,
            "cols": self.cols,
            "walls": [[sorted(list(w)) for w in row] for row in self.walls],
            "weights": self.weights,
        })


# --- Generator: recursive backtracker ----------------------------------------

def generate(rows: int, cols: int, seed: int | None = None) -> Maze:
    rng = random.Random(seed)
    m = Maze(rows, cols)
    visited = [[False] * cols for _ in range(rows)]
    stack: list[Cell] = [(0, 0)]
    visited[0][0] = True
    while stack:
        r, c = stack[-1]
        candidates: list[Cell] = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                candidates.append((nr, nc))
        if not candidates:
            stack.pop()
            continue
        nxt = rng.choice(candidates)
        m.carve((r, c), nxt)
        visited[nxt[0]][nxt[1]] = True
        stack.append(nxt)
    return m


# --- Solver result ------------------------------------------------------------

@dataclass
class SolveResult:
    algorithm: str
    explored: int
    path: list[Cell]

    @property
    def path_length(self) -> int:
        return len(self.path)


# --- Solvers ------------------------------------------------------------------

def _reconstruct(parent: dict[Cell, Cell], start: Cell, goal: Cell) -> list[Cell]:
    if goal not in parent and start != goal:
        return []
    out = [goal]
    while out[-1] != start:
        out.append(parent[out[-1]])
    out.reverse()
    return out


def bfs(m: Maze, start: Cell, goal: Cell) -> SolveResult:
    seen = {start}
    parent: dict[Cell, Cell] = {}
    q: deque[Cell] = deque([start])
    while q:
        cur = q.popleft()
        if cur == goal:
            break
        for nb in m.neighbors(cur):
            if nb not in seen:
                seen.add(nb)
                parent[nb] = cur
                q.append(nb)
    return SolveResult("BFS", len(seen), _reconstruct(parent, start, goal))


def dfs(m: Maze, start: Cell, goal: Cell) -> SolveResult:
    seen = {start}
    parent: dict[Cell, Cell] = {}
    stack: list[Cell] = [start]
    while stack:
        cur = stack.pop()
        if cur == goal:
            break
        for nb in m.neighbors(cur):
            if nb not in seen:
                seen.add(nb)
                parent[nb] = cur
                stack.append(nb)
    return SolveResult("DFS", len(seen), _reconstruct(parent, start, goal))


def dijkstra(m: Maze, start: Cell, goal: Cell) -> SolveResult:
    dist: dict[Cell, int] = {start: 0}
    parent: dict[Cell, Cell] = {}
    pq: list[tuple[int, Cell]] = [(0, start)]
    explored: set[Cell] = set()
    while pq:
        d, cur = heapq.heappop(pq)
        if cur in explored:
            continue
        explored.add(cur)
        if cur == goal:
            break
        for nb in m.neighbors(cur):
            nd = d + m.weights[nb[0]][nb[1]]
            if nd < dist.get(nb, 1 << 30):
                dist[nb] = nd
                parent[nb] = cur
                heapq.heappush(pq, (nd, nb))
    return SolveResult("Dijkstra", len(explored), _reconstruct(parent, start, goal))


def manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(m: Maze, start: Cell, goal: Cell) -> SolveResult:
    g: dict[Cell, int] = {start: 0}
    parent: dict[Cell, Cell] = {}
    pq: list[tuple[int, int, Cell]] = [(manhattan(start, goal), 0, start)]
    explored: set[Cell] = set()
    counter = 0
    while pq:
        _, gc, cur = heapq.heappop(pq)
        if cur in explored:
            continue
        explored.add(cur)
        if cur == goal:
            break
        for nb in m.neighbors(cur):
            ng = gc + m.weights[nb[0]][nb[1]]
            if ng < g.get(nb, 1 << 30):
                g[nb] = ng
                parent[nb] = cur
                f = ng + manhattan(nb, goal)
                counter += 1
                heapq.heappush(pq, (f, ng, nb))
    return SolveResult("A*", len(explored), _reconstruct(parent, start, goal))


# --- Demo --------------------------------------------------------------------

def main(argv: list[str]) -> int:
    rows, cols = 21, 21
    if len(argv) >= 3:
        rows, cols = int(argv[1]), int(argv[2])
    seed = 42
    m = generate(rows, cols, seed=seed)
    start: Cell = (0, 0)
    goal: Cell = (rows - 1, cols - 1)

    results = [bfs(m, start, goal), dfs(m, start, goal),
               dijkstra(m, start, goal), astar(m, start, goal)]

    print(m.render_ascii(results[0].path))
    print()
    print(f"{'algorithm':<12}{'explored':>10}{'path_len':>10}")
    print("-" * 32)
    for r in results:
        print(f"{r.algorithm:<12}{r.explored:>10}{r.path_length:>10}")

    out_path = "maze.json"
    try:
        with open(out_path, "w") as fh:
            fh.write(m.to_json())
        print(f"\nmaze exported to {out_path}")
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
