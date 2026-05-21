# Week 17 — Graphs - Fundamentals & Traversals

> Self-check: `./scripts/journey quiz 17`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/2.TopologicalSort.py`](python/2.TopologicalSort.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_17/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify topological_sort workbook/week_17/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 17`

If you got stuck: open [`python/2.TopologicalSort.py`](python/2.TopologicalSort.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Graphs - Fundamentals & Traversals**. You'll touch: GraphRepresentations, TopologicalSort. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Visualization: [`viz/bfs_dfs.html`](../viz/bfs_dfs.html) | You want to SEE BFS and DFS visit nodes step by step |
| Mock interview: [`mock_interviews/04_word_ladder_bfs.md`](../mock_interviews/04_word_ladder_bfs.md) | Graph / BFS problems discussed conversationally |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | GraphRepresentations | `java/1.GraphRepresentations.java` | `python/1.GraphRepresentations.py` | `cpp/1.GraphRepresentations.cpp` | `rust/s01_GraphRepresentations.rs` | `web/1.GraphRepresentations.html` |
| 2 | TopologicalSort | `java/2.TopologicalSort.java` | `python/2.TopologicalSort.py` | `cpp/2.TopologicalSort.cpp` | `rust/s02_TopologicalSort.rs` | `web/2.TopologicalSort.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Graphs | — | `python/graphs.py` | `cpp/graphs.cpp` | `rust/graphs.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. GraphRepresentations**
- **2. TopologicalSort**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Graph representations and Topological Sort.

| Approach (graph representation) | Memory | Edge query | Neighbors | When to prefer |
|----------|------|-------|-----------|----------------|
| Adjacency matrix | O(V²) | O(1) | O(V) | Dense graphs (E ≈ V²), edge-existence queries |
| Adjacency list (`List<List<Integer>>`) | O(V + E) | O(deg) | O(deg) | Default — sparse graphs |
| Edge list | O(E) | O(E) | O(E) | Kruskal's MST; algorithms that iterate all edges |
| CSR (compressed sparse row) | O(V + E) | O(log deg) | O(deg) | Cache-friendly, immutable graphs |

| Approach (topological sort) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Kahn's algorithm (BFS, in-degrees) | O(V + E) | O(V) | Detects cycles cleanly; can produce lex-smallest order with a PQ |
| DFS post-order reverse | O(V + E) | O(V) | When you're already doing DFS for other reasons |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Topological sort on a cyclic graph and pretending the output is valid** — Kahn's stops with nodes still having in-degree > 0; you must check `processed == V` and report the cycle, not silently return a partial order.
- **Marking a node visited *after* recursing into its neighbors** — you'll revisit the same node many times, blowing up to exponential time. Mark visited *before* recursing.
- **One `visited` array for cycle detection in a *directed* graph** — you need three states (unvisited / in-stack / done) to distinguish a cycle from a cross-edge to a finished node. Two states only work on undirected graphs.
- **Adjacency-matrix for sparse graphs with V=10⁵** — that's a 10¹⁰-entry matrix; it won't fit in memory. Use an adjacency list.
- **Building an undirected graph by adding `u → v` only** — every undirected edge needs both `u → v` and `v → u`. Forgetting the symmetric add is the most common reason BFS finds nothing.

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
- If you had to teach Kahn's algorithm to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
