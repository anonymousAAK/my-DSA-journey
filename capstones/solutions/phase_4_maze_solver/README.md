# Phase 4 — Maze Solver (reference implementation)

```
$ python maze.py            # 21x21 maze, all four algorithms, comparison table, JSON export
$ python maze.py 31 31      # custom size
$ python test_maze.py
```

## Files

- `maze.py` — `Maze` data type + recursive-backtracker generator + BFS / DFS / Dijkstra / A* solvers, single file.
- `test_maze.py` — property-style tests across multiple random seeds.
- `maze.json` — written by `maze.py` on the last run; consumable by the optional `maze_visual.html`.

## How it's structured

`Maze` owns the wall data (`walls[r][c] : set[str]` over `{"N","S","E","W"}`) and the optional per-cell weights. It exposes only `neighbors(cell)` to the solvers, so the solvers operate against a pure graph view — no knowledge of grid geometry leaks in. That makes it trivial to swap the generator (e.g. for a Kruskal-based one) without touching the solvers, or to add new solvers without touching the maze.

Each solver returns a `SolveResult` with `algorithm`, `explored` (cells expanded), and `path` (full cell sequence including start and goal). This is the comparison currency.

## Generator: recursive backtracker

Standard DFS with random neighbour selection. Carves out a *perfect maze* — every cell reachable from every other, no loops, exactly one path between any two cells. That last property makes the BFS-vs-DFS comparison cleaner: both *must* find the same path on a perfect maze, because there's only one. If you want a more interesting comparison, sprinkle in extra carves (called "braiding") to introduce loops.

## When does each solver actually win?

| Solver | Best for | Why |
|--------|----------|-----|
| BFS | Unweighted graph, shortest path needed | Optimal, O(V+E), uses a queue. |
| DFS | Just need *a* path, memory matters | Stack-based, can find a path fast but it's almost certainly not the shortest. |
| Dijkstra | Weighted graph, no heuristic available | Optimal with non-negative weights. Same shape as BFS but priority queue ordered by cost. |
| A* | Weighted graph + admissible heuristic | Same correctness as Dijkstra, but explores fewer cells when the heuristic carries information. |

On a **unit-weight perfect maze** with the Manhattan heuristic, our test (`test_astar_explores_le_dijkstra`) confirms A* explores `≤` Dijkstra on every random seed. The wins are real but modest (e.g. 74 vs 81 cells in the demo) because a maze's twists routinely send you *away* from the goal, so the heuristic is often misleading. A* shines more on open grids and roadmaps where the straight-line distance is closer to the truth.

On **weighted** mazes, A* and Dijkstra both still find optimal paths; only A*'s exploration count drops. BFS and DFS don't account for weights at all, so they're not even in the running.

## Trade-offs made

- **Recursive backtracker generator.** Easy to understand, gives long winding corridors. If you want short corridors and many branches, use Kruskal's or Wilson's.
- **Manhattan heuristic.** Admissible and consistent on a 4-connected unit-weight grid, which is what A* needs to remain optimal. If you switch to 8-connected (diagonal moves), use Chebyshev. If you mix in real-valued weights with no spatial meaning, A* degenerates to Dijkstra.
- **In-memory only.** A 1000×1000 maze fits comfortably in a few hundred MB. Bigger than that and you want the walls packed into bitfields (4 bits per cell) instead of Python sets.
- **No visualization in `maze.py` itself.** The ASCII renderer is fine for sanity-checking. The companion `maze_visual.html` (optional, future work) reads `maze.json` and draws SVG; the data export is already in place.

## What the next iteration would add

- **Step-by-step animation** of the frontier expansion (publish exploration events the way the Phase 3 visualizer does).
- **JPS (Jump Point Search)** for grid maps — strictly better than A* on uniform-cost grids.
- **Bidirectional BFS / A***. Cut exploration roughly in half when start and goal are both known.
- **Loops & weighted regions** for a more interesting Dijkstra vs A* comparison (mud, water, hills).
