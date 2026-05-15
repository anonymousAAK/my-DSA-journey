# Week 17

> Self-check: `./scripts/journey quiz 17` — run the mastery checkpoints for this week.

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | GraphRepresentations | `java/1.GraphRepresentations.java` | `python/1.GraphRepresentations.py` | `cpp/1.GraphRepresentations.cpp` | `rust/s01_GraphRepresentations.rs` | `web/1.GraphRepresentations.html` |
| 2 | TopologicalSort | `java/2.TopologicalSort.java` | `python/2.TopologicalSort.py` | `cpp/2.TopologicalSort.cpp` | `rust/s02_TopologicalSort.rs` | `web/2.TopologicalSort.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Graphs | — | `python/graphs.py` | `cpp/graphs.cpp` | `rust/graphs.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

## How to run a topic file

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

## Topic roadmap

- **1. GraphRepresentations**
- **2. TopologicalSort**

## Tradeoff Matrix

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

## Anti-patterns to avoid

- **Topological sort on a cyclic graph and pretending the output is valid** — Kahn's stops with nodes still having in-degree > 0; you must check `processed == V` and report the cycle, not silently return a partial order.
- **Marking a node visited *after* recursing into its neighbors** — you'll revisit the same node many times, blowing up to exponential time. Mark visited *before* recursing.
- **One `visited` array for cycle detection in a *directed* graph** — you need three states (unvisited / in-stack / done) to distinguish a cycle from a cross-edge to a finished node. Two states only work on undirected graphs.
- **Adjacency-matrix for sparse graphs with V=10⁵** — that's a 10¹⁰-entry matrix; it won't fit in memory. Use an adjacency list.
- **Building an undirected graph by adding `u → v` only** — every undirected edge needs both `u → v` and `v → u`. Forgetting the symmetric add is the most common reason BFS finds nothing.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach Kahn's algorithm to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
