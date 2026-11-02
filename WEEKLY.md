# Weekly Digest — 2026-11-02 (ISO 2026-W45)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**Git's Commit Graph as a DAG, Why Topological Sort Matters**

Git tracks the history of a codebase. Every commit references its parent commit(s), forming a graph. That graph is a **directed acyclic graph** — directed (commits point to their parents, time flows one way), and acyclic (you can't be your own ancestor). Almost every interesting Git operation is a graph-algorithm query on this DAG: "Is commit A an ancestor of commit B?" "What's the most recent common ancestor of these two branches?" "List all commits between these two tags in a sensible order."

Read it in full: [`case_studies/real_world/06_git_dag.md`](case_studies/real_world/06_git_dag.md)

## Pattern drill
_From Week 26 (drill #6)._

> Distractor: Given a DAG, find the longest path. (Network flow?)

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 26/patterns.md`](Week 26/patterns.md)

## Hard-mode challenge
### Challenge 1 (Week 26): Max-Flow via Dinic's Algorithm

**Spec**:
Read `n`, `m`, `s`, `t`, and `m` directed edges `(u, v, capacity)`. Compute and print the maximum flow from `s` to `t`. Required: Dinic's algorithm — BFS for level graph, then DFS with blocking flows + current-arc optimization. Don't use Edmonds–Karp (BFS-augment-only); that's O(V E^2) and the canonical implementation.

**Constraints**:
- `1 <= n <= 1000`, `1 <= m <= 10^5`, capacities up to `10^9`
- Time: O(V^2 E), much faster in practice
- Memory: O(V + E)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 26/challenges.md`](Week 26/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
