# Capstone — Phase 4: Maze Generator + Multi-Algorithm Solver Comparison

**Time estimate**: 12-15 hours over 2 weekends.
**Prerequisite weeks**: 16-20 (graphs, BFS, DFS, Dijkstra, A*, heuristics).
**Skill checked**: You can implement four pathfinding algorithms, compare them on identical inputs, and explain *why* one wins on each maze topology.

## The Goal
Build a tool — CLI plus a web visualization is the gold standard — that generates random mazes and lets you run BFS, DFS, Dijkstra, and A* on the same maze side by side. The user should *see* the difference: DFS slithering deep, BFS expanding in concentric rings, Dijkstra's bowl-shaped expansion under non-uniform costs, A* shooting like an arrow toward the goal. Comparison stats (nodes expanded, path length, wall-clock time) print at the end. This capstone makes pathfinding *visceral* in a way that LeetCode never will.

## Functional Requirements
- Generate a maze of configurable size (default 30×30) using at least one classical generation algorithm: recursive backtracker, Kruskal's, Prim's, or Wilson's.
- Solve the maze with BFS, DFS, Dijkstra, and A* — same start and goal for all four.
- Visualize the search frontier evolving over time (web frontend) OR produce a per-step text grid (CLI fallback).
- Report per-algorithm statistics: nodes expanded, final path length, wall-clock ms, peak frontier size.
- Should support **weighted** mazes (some cells cost more to enter) — this is what makes Dijkstra meaningfully different from BFS.
- Should allow the user to choose the A* heuristic (Manhattan, Euclidean, Chebyshev) and report how it affects nodes expanded.

## Non-functional Requirements
- Performance: solve a 200×200 maze with all four algorithms under 2 seconds total on a laptop.
- Memory: a 1000×1000 maze must not OOM. Use integer cell IDs and arrays, not dictionaries with tuple keys.
- Code quality: a single `Solver` interface — `def solve(maze, start, goal) -> SolveResult` — implemented by four classes. The harness should be one function that calls each solver and prints a comparison table.
- Tests: at least 20 tests covering generator (every cell reachable from every other), each solver on a hand-built tiny maze (4×4 with a known optimal path), heuristic admissibility.

## Architecture Sketch

```
+-----------+        +---------+        +-------------------+
| Generator | -----> |  Maze   | -----> |  Solver registry  |
+-----------+        +---------+        +-------+-----------+
                                                |
                            +-------------------+-------------------+
                            |                   |                   |
                            v                   v                   v
                         +-----+            +-------+           +-----+
                         | BFS |  ...       |Dijkstra|          | A*  |
                         +--+--+            +---+---+           +--+--+
                            |                   |                  |
                            +---------+---------+----------+-------+
                                      v
                                +-----+------+
                                |  Harness   |
                                | stats &    |
                                | visualizer |
                                +------------+
```

## Implementation Roadmap

1. **Day 1 (3-4h) — Maze representation + generator.**
   Pick a representation. The natural one is a 2D grid of cells where each cell stores 4 wall bits (north/south/east/west). Implement recursive backtracker first: it's the easiest to write and produces mazes with long corridors that show off DFS's character. Add a CLI flag `--algo prim` later if you want a second generator.

   Write a *correctness test*: every cell must be reachable from every other (run a single BFS from cell 0 and assert it visits all cells).

2. **Day 2 (3-4h) — BFS, DFS, Dijkstra.**
   Implement the three uninformed-search-plus-Dijkstra. All three share a frontier abstraction (queue, stack, priority queue) and an "expand" step. Templating helps but be careful — premature abstraction will burn an hour. Get each working in isolation first, *then* extract the common loop.

   For Dijkstra to be interesting you need cell weights. The simplest scheme: each cell has cost 1, but mark some cells as "mud" with cost 5. The maze generator can sprinkle mud after carving corridors.

3. **Day 3 (2-3h) — A* and heuristics.**
   A* is Dijkstra with `f = g + h`. Implement all three heuristics. Verify admissibility: `h(n) ≤ true_cost(n, goal)` for all `n`. Manhattan is admissible in a 4-connected grid; Euclidean is admissible everywhere but slower; Chebyshev is admissible in 8-connected grids only.

   On a 30×30 maze with start at one corner and goal at the other, A* with Manhattan should expand roughly half as many nodes as Dijkstra. Verify and report the ratio.

4. **Day 4 (3-4h) — Visualization + stats.**
   Two options:
   - **Web (recommended)**: render the maze as a canvas grid. Each algorithm runs in its own animation panel — four panels side by side, all four animating simultaneously. Color the frontier, the explored set, and the final path differently.
   - **CLI fallback**: print the maze with ASCII frames, one per N expansions. Cheaper, less impressive.

   Print a final stats table:
   ```
                       BFS     DFS     Dijkstra   A*
   nodes expanded      400     180     400        140
   path length         58      78      58         58
   peak frontier       62       9      62          30
   time (ms)            7       3      11           4
   ```

## Stretch Goals
- Bidirectional BFS / bidirectional A*. The implementation subtleties around "when do the two frontiers meet" are exactly what came up in the Word Ladder mock interview.
- Anytime A* or IDA* on huge mazes where the regular A* blows the memory budget.
- Replace the grid with a hex grid. Watch which heuristics break.
- Add user-placed walls so the visualization is interactive.
- Add a "diagonal moves allowed" toggle and confirm that Manhattan becomes inadmissible.

## Reference Implementation

A working Python reference lives at `capstones/solutions/phase_4_maze_solver/`. **Don't peek before you attempt this yourself** — copying it defeats the entire point of a capstone.

When you're done (or genuinely stuck after 4+ hours of honest effort), open the reference and:

1. Read its `README.md` for the design decisions and tradeoffs the author made.
2. Diff your architecture against theirs. What's different? Whose choices were better, and why?
3. Run its `test_*.py` against your implementation (you may need a thin adapter).
4. Write a journal entry comparing the two implementations.

The reference is *a* solution, not *the* solution. Yours might be cleaner. Yours might be slower. Either is a learning outcome.

## Self-grading rubric
| Criterion | Points | What you're checking |
|-----------|--------|----------------------|
| Correctness on basic inputs | 30 | All four solvers find an optimal-length path (except DFS, which finds *a* path) |
| Handles edge cases | 20 | No path between start and goal, start == goal, single-cell maze |
| Algorithm choice is justified (commit message or README) | 15 | Why each heuristic, why your generator choice, why your frontier data structures |
| Code is readable (function size, naming) | 15 | Common solver interface, no duplicated search loop |
| Tests pass (≥80% coverage on core logic) | 10 | Especially admissibility tests for heuristics |
| Stretch goal implemented | 10 | Bidirectional A* is the meatiest; interactive walls is the most fun |

## When you're done
- Push to a separate repo (or branch) and host the web version. Link from your portfolio. The animation is what will get people to actually click.
- Write a reflection essay in your `SOLUTION_JOURNAL.md`: which solver surprised you, where did you have to re-read the textbook, what's still murky?
- Compare your final architecture to a real product that does the same thing (see `case_studies/real_world/`). Look at how route-planning APIs (OSRM, Valhalla) preprocess road networks (contraction hierarchies, transit-node routing) to make A* irrelevant at scale — your maze A* doesn't preprocess at all.
