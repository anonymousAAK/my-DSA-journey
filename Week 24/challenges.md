# Week 24 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: 2-SAT in Linear Time

**Spec**:
Read `n` variables and `m` clauses, each of the form `(l_i OR l_j)` where each literal is a variable or its negation. Decide satisfiability and, if SAT, print a satisfying assignment. Required: build the implication graph (each clause `(a OR b)` adds edges `¬a -> b` and `¬b -> a`), find SCCs (Tarjan), and assign each variable based on the topological order of SCCs.

**Constraints**:
- `1 <= n, m <= 10^5`
- Time: O(n + m)
- Memory: O(n + m)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=2 m=2 clauses=(x1 OR x2) (¬x1 OR ¬x2)` | SAT, e.g. `x1=true x2=false` |
| `n=2 m=4 clauses=(x1 OR x1) (¬x1 OR ¬x1) (x2 OR x2) (¬x2 OR ¬x2)` | UNSAT |
| `n=1 m=1 clauses=(x1 OR x1)` | `x1=true` |

**Stretch**: Approximate MAX-2-SAT (NP-hard): random assignment achieves expected 0.75 of clauses; can you do better with a derandomization argument?

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Vertex Cover Approximation (2-Approximation Greedy)

**Spec**:
Read an undirected graph. Output a vertex cover (a set of vertices such that every edge has at least one endpoint in the set) of size at most `2 * OPT`. Greedy approximation: repeatedly pick an uncovered edge, add **both** endpoints to the cover, remove all incident edges, repeat. Prove (in journal) the 2-approximation bound.

**Constraints**:
- `1 <= n, m <= 10^5`
- Time: O(n + m)
- Memory: O(n + m)

**Test inputs**:
| Input | Expected behavior |
|-------|-------------------|
| `n=4 edges=(1,2)(2,3)(3,4)` (path) | OPT = 2, your output `<= 4` |
| `n=5 K_5` | OPT = 4, your output `<= 8` (which clamps to 5 anyway) |
| `n=3 edges=(1,2)(1,3)` (star) | OPT = 1, your output `<= 2` |

**Stretch**: LP-rounding 2-approximation: solve LP relaxation, include any vertex with `x_v >= 0.5`.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: TSP Approximation (Christofides-Lite: MST + Double Tree)

**Spec**:
Given a metric TSP instance (triangle inequality holds), output a tour of length at most `2 * OPT`. Algorithm: compute MST, do a DFS preorder traversal listing each vertex on first visit, return to start. Prove the 2-approximation.

**Constraints**:
- `1 <= n <= 1000`, distances satisfy triangle inequality
- Time: O(n^2 log n) for MST
- Memory: O(n^2)

**Test inputs**:
| Input | Expected behavior |
|-------|-------------------|
| 4 points at corners of a unit square | OPT = 4, your output `<= 8` |
| 3 collinear points | OPT = 2 * range, your output similar |
| `n=1` | tour `[0]`, cost 0 |

**Stretch**: Full Christofides (perfect matching on odd-degree vertices of MST, then Eulerian tour, then shortcut) — proven 1.5-approximation. Hard to implement (needs min-weight perfect matching).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Subset Sum FPTAS (Fully Polynomial-Time Approximation)

**Spec**:
Read `n`, target `T`, integers `a_1..a_n`, and accuracy parameter `ε > 0`. Output a sum `S <= T` such that `S >= (1 - ε) * OPT`, where OPT is the best achievable sum `<= T`. Implementation: maintain a list of reachable sums; after each insertion, "trim" the list so consecutive entries differ by factor `>= 1 + ε/(2n)`. Polynomial in `n` and `1/ε`.

**Constraints**:
- `1 <= n <= 100`, values up to `10^9`, `ε` in `(0, 1)`
- Time: O(n^2 / ε)
- Memory: O(n / ε)

**Test inputs**:
| Input | Expected behavior |
|-------|-------------------|
| `n=4 T=10 a=[1, 4, 5, 7] ε=0.1` | OPT = 10, your S in `[9, 10]` |
| `n=1 T=5 a=[3] ε=0.5` | OPT = 3, your S = 3 |

**Stretch**: Prove the approximation ratio formally and verify empirically across random instances.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: Randomized Min-Cut (Karger's Algorithm)

**Spec**:
Read an undirected multigraph. Estimate the min-cut size by repeatedly running Karger's contraction algorithm: pick a random edge, contract its endpoints into one super-node (removing self-loops), repeat until 2 super-nodes remain; the number of edges between them is a candidate cut. Run `O(n^2 log n)` trials and return the minimum.

**Constraints**:
- `1 <= n <= 200`
- Time: O(n^4) total (Karger–Stein improves to O(n^2 log^3 n))
- Memory: O(n + m)

**Test inputs**:
| Input | Expected output (min cut) |
|-------|---------------------------|
| `K_4` (complete on 4) | `3` |
| barbell graph (two K_3's joined by one edge) | `1` |
| `n=2 edges=(1,2)(1,2)(1,2)` (parallel) | `3` |

**Stretch**: Implement Karger–Stein (recursive contraction with success-probability boosting).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
