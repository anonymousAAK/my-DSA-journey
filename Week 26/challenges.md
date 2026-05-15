# Week 26 — Hard Mode Challenges (Boss Level)

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Max-Flow via Dinic's Algorithm

**Spec**:
Read `n`, `m`, `s`, `t`, and `m` directed edges `(u, v, capacity)`. Compute and print the maximum flow from `s` to `t`. Required: Dinic's algorithm — BFS for level graph, then DFS with blocking flows + current-arc optimization. Don't use Edmonds–Karp (BFS-augment-only); that's O(V E^2) and the canonical implementation.

**Constraints**:
- `1 <= n <= 1000`, `1 <= m <= 10^5`, capacities up to `10^9`
- Time: O(V^2 E), much faster in practice
- Memory: O(V + E)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=4 m=5 edges=(1,2,3)(1,3,2)(2,3,5)(2,4,2)(3,4,3) s=1 t=4` | `5` |
| `n=2 m=1 edges=(1,2,7) s=1 t=2` | `7` |
| classic bottleneck graph | matches min cut |
| `n=6 m=10` (Cormen Fig 26.6) | `23` |

**Stretch**: For unit-capacity graphs, Dinic runs in O(E sqrt(V)). Verify empirically.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Min-Cut Reconstruction from Max-Flow

**Spec**:
Using your Dinic implementation, after computing max flow on `(s, t)`, find an actual min-cut: the set of vertices `S` reachable from `s` in the residual graph. Edges from `S` to its complement form the min-cut. Print the cut edges and verify their capacities sum to the max-flow value.

**Constraints**:
- `1 <= n <= 1000`, `1 <= m <= 10^5`
- Time: O(n + m) post-flow
- Memory: O(n + m)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| same as Challenge 1's first case | cut edges with total capacity `5` |
| trivial `s -> t` with capacity 7 | cut edge `(s, t)` |

**Stretch**: Enumerate **all** min cuts (there can be exponentially many).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Bipartite Matching via Hopcroft–Karp

**Spec**:
Read a bipartite graph with `L` left vertices, `R` right vertices, and `m` edges. Compute the maximum matching using Hopcroft–Karp: BFS to compute layers, then DFS finds vertex-disjoint augmenting paths in the layered graph. Achieves O(E sqrt(V)).

**Constraints**:
- `1 <= L, R <= 10^5`, `m <= 10^6`
- Time: O(E sqrt(V))
- Memory: O(V + E)

**Test inputs**:
| Input | Expected matching size |
|-------|------------------------|
| `L=3 R=3 edges=(1,1)(1,2)(2,2)(3,3)` | `3` |
| `L=4 R=4 K_{4,4}` | `4` |
| `L=3 R=3 edges=(1,1)(2,1)(3,1)` (all on right vertex 1) | `1` |
| empty edges | `0` |

**Stretch**: Output the actual matching pairs. Then output a minimum vertex cover (König's theorem).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Min-Cost Max-Flow With Potentials (Johnson's Reweighting)

**Spec**:
Read a directed graph with edge `(u, v, capacity, cost)`. Compute the maximum flow from `s` to `t` of minimum total cost. Required: successive shortest paths with **Johnson's potentials** so each augmenting-path search uses Dijkstra (not Bellman–Ford). Bellman–Ford is allowed only once at the start to initialize potentials.

**Constraints**:
- `1 <= n <= 500`, `1 <= m <= 10^4`, costs may be negative initially
- Time: O(F * (V + E) log V) where F = max flow value
- Memory: O(V + E)

**Test inputs**:
| Input | Expected (flow, cost) |
|-------|-----------------------|
| `n=4 edges=(1,2,2,1)(1,3,1,2)(2,3,1,1)(2,4,1,3)(3,4,2,1) s=1 t=4` | flow `3`, cost `8` (verify) |
| trivial single edge | match capacity, cost = capacity * unit-cost |

**Stretch**: Min-cost flow on a graph with negative-cost cycles (canceling them up front).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: Project Selection (Closure / Min-Cut Reduction)

**Spec**:
You have `n` projects. Each project has a profit `p_i` (positive or negative). Some projects have prerequisites: project `i` requires project `j`. Pick a subset of projects (respecting prerequisites) to maximize total profit. Required: model as min s-t cut: source -> positive-profit project with capacity `p`; negative-profit project -> sink with capacity `-p`; prerequisite edges with infinite capacity. Max profit = sum of positive profits - min cut.

**Constraints**:
- `1 <= n <= 100`, prerequisites up to `n^2`
- Time: dominated by max-flow
- Memory: O(n^2)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=3 profits=[10, -5, 7] prereqs=(2,1)(3,2)` (3 requires 2 requires 1) | best subset; verify by brute force |
| `n=2 profits=[5, 5] no prereqs` | `10` (take both) |
| `n=2 profits=[-3, -4] no prereqs` | `0` (take none) |

**Stretch**: Build a small executable test harness that brute-forces the answer for `n <= 15` and confirms your min-cut answer.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
