# Week 22 — Advanced Graph Algorithms

> Self-check: `./scripts/journey quiz 22`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/1.ShortestPaths.py`](python/1.ShortestPaths.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_22/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify dijkstra_shortest_path workbook/week_22/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 22`

If you got stuck: open [`python/1.ShortestPaths.py`](python/1.ShortestPaths.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Advanced Graph Algorithms**. You'll touch: ShortestPaths, MinimumSpanningTree. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Visualization: [`viz/dijkstra.html`](../viz/dijkstra.html) | You want to SEE Dijkstra relax edges step by step |
| Mock interview: [`mock_interviews/04_word_ladder_bfs.md`](../mock_interviews/04_word_ladder_bfs.md) | Graph / shortest-path problems discussed conversationally |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | ShortestPaths | `java/1.ShortestPaths.java` | `python/1.ShortestPaths.py` | `cpp/1.ShortestPaths.cpp` | `rust/s01_ShortestPaths.rs` | `web/1.ShortestPaths.html` |
| 2 | MinimumSpanningTree | `java/2.MinimumSpanningTree.java` | `python/2.MinimumSpanningTree.py` | `cpp/2.MinimumSpanningTree.cpp` | `rust/s02_MinimumSpanningTree.rs` | `web/2.MinimumSpanningTree.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Advanced Graphs | — | `python/advanced_graphs.py` | `cpp/advanced_graphs.cpp` | `rust/advanced_graphs.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. ShortestPaths**
- **2. MinimumSpanningTree**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Shortest paths and Minimum Spanning Trees.

| Approach (shortest path) | Time | Space | Restrictions | When to prefer |
|----------|------|-------|--------------|----------------|
| BFS | O(V + E) | O(V) | Unweighted / unit weights | Unweighted SSSP |
| Dijkstra (binary heap) | O((V + E) log V) | O(V) | Non-negative weights | Default for weighted SSSP |
| Dijkstra (Fibonacci heap) | O(E + V log V) | O(V) | Non-negative weights | Theory; rarely worth the constants in practice |
| Bellman–Ford | O(V·E) | O(V) | Detects negative cycles | Negative weights, or you need cycle detection |
| SPFA (queue-based BF) | O(V·E) worst, fast avg | O(V) | Same as BF | Practical Bellman–Ford on sparse graphs |
| Floyd–Warshall | O(V³) | O(V²) | All pairs | Dense, V ≤ ~400 |
| 0-1 BFS | O(V + E) | O(V) | Weights in {0, 1} | Faster than Dijkstra for binary weights |

| Approach (MST) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Kruskal (Union-Find) | O(E log E) | O(V) | Sparse graphs, edge list available |
| Prim (binary heap) | O((V+E) log V) | O(V) | Dense graphs, adjacency list |
| Borůvka | O(E log V) | O(V) | Parallelizable, theoretical interest |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Running Dijkstra on a graph with negative edges** — relaxation is no longer monotone; popped nodes might still be reducible. Use Bellman–Ford, or transform with Johnson's algorithm.
- **Reusing a `dist[]` array without re-initializing to `+∞`** — leftover values from a previous run look like reachable nodes. Reset (or use a `Map`) every call.
- **Pushing duplicates into the heap and forgetting to skip stale entries** — when you find a shorter path, the old (longer) heap entry is still there. Either implement decrease-key, or check `if (d > dist[u]) continue;` on each pop.
- **Kruskal without Union-Find** — cycle detection via DFS on every edge is O(V·E). Union-Find with path compression turns it into nearly O(α(V)).
- **Floyd–Warshall with the loops in the wrong order** — the `k` (intermediate) loop must be the *outermost*. Putting it inside breaks the dynamic-programming invariant and gives wrong answers on most graphs.

</details>

## Reference: how to run a topic file

<details>
<summary>Java / Python / C++ / Rust / Web one-liners</summary>


From the week's directory:

```bash
# Java
javac java/<file>.java && java -cp java <ClassName>

# Python
python3 python/<file>.py

# C++
g++ -std=c++17 cpp/<file>.cpp -o /tmp/a && /tmp/a

# Rust
rustc --edition 2021 rust/<file>.rs -o /tmp/a && /tmp/a

# Web — open in a browser
open web/<file>.html   # macOS
xdg-open web/<file>.html   # Linux
```

</details>

## Reflection prompts


- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach Dijkstra's relaxation step to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
