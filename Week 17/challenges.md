# Week 17 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Bidirectional BFS for Word Ladder

**Spec**:
Read a `beginWord`, an `endWord`, and a dictionary of words (all same length, lowercase). Find the length of the shortest transformation sequence where each step changes one letter and every intermediate is in the dictionary. Return 0 if no path. Required: **bidirectional BFS** — expand from both ends, alternating the smaller frontier, until they meet.

**Constraints**:
- Up to `5000` words, length up to 10
- Time: roughly O(b^(d/2)) instead of O(b^d)
- Memory: O(dictionary)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `begin=hit end=cog dict=hot dot dog lot log cog` | `5` |
| `begin=hit end=cog dict=hot dot dog lot log` | `0` |
| `begin=a end=c dict=a b c` | `2` |
| `begin=hot end=hot dict=hot` | `0` (same word, by convention) or `1` — pick a rule and stick with it |

**Stretch**: Also output the actual shortest path (rebuild via parent pointers from both directions).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Count Distinct Shortest Paths in an Unweighted Graph

**Spec**:
Read `n`, `m`, and `m` edges of an undirected unweighted graph (1-indexed vertices). Read `s` and `t`. Print the number of distinct shortest paths from `s` to `t` modulo `10^9 + 7`. Use BFS computing `dist[v]` and `count[v]` simultaneously: when relaxing `v` from `u`, if `dist[v] == dist[u] + 1` add `count[u]` to `count[v]`.

**Constraints**:
- `1 <= n, m <= 10^5`
- Time: O(n + m)
- Memory: O(n + m)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=4 m=4 edges=(1,2)(1,3)(2,4)(3,4) s=1 t=4` | `2` |
| `n=2 m=1 edges=(1,2) s=1 t=2` | `1` |
| `n=3 m=0 s=1 t=3` | `0` |
| `n=5 m=6 edges=(1,2)(1,3)(2,4)(3,4)(4,5)(1,5) s=1 t=5` | `3` (paths via 4 from either 2 or 3, plus direct edge) |

**Stretch**: Same in a weighted DAG (use topological order + DP).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Strongly Connected Components — Tarjan's Algorithm

**Spec**:
Read a directed graph. Print the SCCs, one per line (space-separated vertices in any order; SCCs in any order). Required: a single DFS using Tarjan's `disc`/`low` arrays and a stack. Kosaraju's two-pass DFS is acceptable for partial credit, but Tarjan in one pass is the goal.

**Constraints**:
- `1 <= n, m <= 10^5`
- Time: O(n + m)
- Memory: O(n + m)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=5 m=5 edges=(1,2)(2,3)(3,1)(4,2)(4,5)` | SCCs: `{1,2,3} {4} {5}` |
| `n=1 m=0` | `{1}` |
| `n=3 m=3 edges=(1,2)(2,3)(3,1)` | `{1,2,3}` |
| `n=4 m=3 edges=(1,2)(3,4)(4,3)` | `{1} {2} {3,4}` |

**Stretch**: Build the condensation DAG (each SCC becomes a node) and topologically sort it.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Detect Cycle in a Directed Graph and Print It

**Spec**:
Read a directed graph. If acyclic, print `ACYCLIC`. Otherwise, print one cycle as a sequence of vertices (any cycle is fine). Use DFS with three colors (white/gray/black). When you encounter a gray node, you've found a back edge; walk parents to reconstruct the cycle.

**Constraints**:
- `1 <= n, m <= 10^5`
- Time: O(n + m)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=4 m=4 edges=(1,2)(2,3)(3,4)(4,2)` | cycle `2 3 4 2` (or `4 2 3 4`, any rotation) |
| `n=3 m=2 edges=(1,2)(2,3)` | `ACYCLIC` |
| `n=2 m=2 edges=(1,2)(2,1)` | `1 2 1` |
| `n=1 m=1 edges=(1,1)` (self-loop) | `1 1` |

**Stretch**: Find the **shortest** cycle (BFS from each vertex; O(nm)).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: Topological Sort With Lexicographically Smallest Order

**Spec**:
Read a DAG. Output a topological order that is lexicographically smallest. Required: Kahn's BFS but using a **min-heap** (priority queue) of zero-indegree vertices instead of a plain queue.

**Constraints**:
- `1 <= n, m <= 10^5`
- Time: O((n + m) log n)
- Memory: O(n + m)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=4 m=2 edges=(3,1)(2,1)` | `2 3 1 4` (the lex-smallest valid topo order; note: depends on isolated vertex 4) |
| `n=5 m=4 edges=(1,2)(1,3)(3,4)(2,5)` | `1 2 3 4 5` |
| `n=3 m=0` | `1 2 3` |
| `n=3 m=3 edges=(1,2)(2,3)(3,1)` | `CYCLE` |

**Stretch**: Lexicographically **largest** topo order — use a max-heap, but understand the subtle difference from "reverse(lex-smallest of reversed graph)".

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
