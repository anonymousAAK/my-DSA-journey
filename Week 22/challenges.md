# Week 22 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: K Shortest Paths (Yen's Algorithm or k-Dijkstra)

**Spec**:
Read a weighted directed graph, source `s`, sink `t`, and integer `k`. Print the lengths of the `k` shortest (not necessarily distinct in vertex set) paths from `s` to `t` in ascending order. Required: a modified Dijkstra where you allow each vertex to be popped from the heap up to `k` times.

**Constraints**:
- `1 <= n, m <= 5000`, `1 <= k <= 100`
- Time: O(k * m log n)
- Memory: O(k * n)

**Test inputs**:
| Input | Expected output (k shortest path lengths) |
|-------|-------------------------------------------|
| `n=4 m=5 edges=(1,2,1)(1,3,2)(2,4,2)(3,4,1)(2,3,1) s=1 t=4 k=3` | `3 3 4` |
| `n=2 m=1 edges=(1,2,5) s=1 t=2 k=3` | `5` (only one path) |
| `n=1 s=1 t=1 k=1` | `0` |

**Stretch**: K shortest **simple** paths (no repeated vertices) — much harder, Yen's algorithm in full.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Negative-Weight Cycle Detection (Bellman–Ford)

**Spec**:
Read a weighted directed graph (edges may have negative weight). Print `YES` if there's a negative-weight cycle reachable from vertex 1, else print the shortest distance from 1 to every vertex (or `INF` if unreachable). Bellman–Ford: `n-1` relaxation rounds, then one more round — any edge that still relaxes lies on (or reaches) a negative cycle.

**Constraints**:
- `1 <= n <= 1000`, `1 <= m <= 10^4`, weights in `[-10^4, 10^4]`
- Time: O(n m)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=3 m=3 edges=(1,2,1)(2,3,-1)(3,1,-1)` | `YES` |
| `n=3 m=2 edges=(1,2,4)(2,3,3)` | `0 4 7` |
| `n=2 m=1 edges=(1,2,-5)` | `0 -5` |
| `n=4 m=4 edges=(1,2,1)(2,3,2)(3,2,-5)(3,4,3)` | `YES` |

**Stretch**: Print the actual negative cycle (trace parents from a vertex updated in the `n`-th round).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: All-Pairs Shortest Paths in O(n^3) — Floyd–Warshall + Path

**Spec**:
Read a weighted directed graph. Print the `n x n` shortest-distance matrix (using `INF` for unreachable, `-INF` if a negative cycle is reachable on the path). Then, for `q` queries `(u, v)`, print the actual shortest path. Use the standard `next[u][v]` reconstruction matrix.

**Constraints**:
- `1 <= n <= 400`, `q <= 10^5`
- Time: O(n^3 + q n) for path reconstruction
- Memory: O(n^2)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=3 m=3 edges=(1,2,1)(2,3,2)(1,3,5) / query (1,3)` | distances `0 1 3 / INF 0 2 / INF INF 0`, path `1 2 3` |
| graph with a negative cycle on a path from `u` to `v` | `(u, v)` distance reported as `-INF` |

**Stretch**: Transitive closure via Floyd–Warshall on a boolean matrix (and discuss SCC connection).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: MST via Borůvka's Algorithm

**Spec**:
Read a weighted undirected graph. Compute and print the total weight of a Minimum Spanning Tree and the edge list. Use Borůvka's algorithm (not Kruskal, not Prim): in each round, for each component find the cheapest outgoing edge, then merge. Logarithmically many rounds.

**Constraints**:
- `1 <= n <= 10^5`, `1 <= m <= 10^6`, distinct edge weights
- Time: O(m log n)
- Memory: O(n + m)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=4 m=5 edges=(1,2,1)(2,3,2)(3,4,3)(4,1,4)(1,3,5)` | total `6`, edges `(1,2,1)(2,3,2)(3,4,3)` |
| `n=1 m=0` | `0`, no edges |
| `n=3 m=3 edges=(1,2,1)(2,3,1)(1,3,1)` | total `2`, any two edges |

**Stretch**: MST on a graph too large to fit in memory — Borůvka shines because rounds are parallelizable.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: A* Search on a Grid With Manhattan Heuristic

**Spec**:
Read an `m x n` grid where `0` is free, `1` is blocked, plus a start and a goal. Find the shortest path length (steps; 4-directional moves) using A* with the Manhattan-distance heuristic. Prove (in your journal) that Manhattan is admissible and consistent.

**Constraints**:
- `1 <= m, n <= 1000`
- Time: O(m n log(m n)) worst case (heap of cells)
- Memory: O(m n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `5x5 empty grid, start (0,0), goal (4,4)` | `8` |
| `3x3 with blockers / start (0,0), goal (2,2)` | path length depending on layout |
| start == goal | `0` |
| no path possible (goal walled off) | `-1` |

**Stretch**: Add diagonal moves with cost √2; switch heuristic to Chebyshev or octile distance.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
