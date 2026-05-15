# Week 26

> Self-check: `./scripts/journey quiz 26` — run the mastery checkpoints for this week.

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | bipartite matching | `java/bipartite_matching.java` | `python/bipartite_matching.py` | `cpp/bipartite_matching.cpp` | `rust/bipartite_matching.rs` | `web/bipartite_matching.html` |
| 2 | dinic | `java/dinic.java` | `python/dinic.py` | `cpp/dinic.cpp` | `rust/dinic.rs` | `web/dinic.html` |
| 3 | edmonds karp | `java/edmonds_karp.java` | `python/edmonds_karp.py` | `cpp/edmonds_karp.cpp` | `rust/edmonds_karp.rs` | `web/edmonds_karp.html` |
| 4 | ford fulkerson | `java/ford_fulkerson.java` | `python/ford_fulkerson.py` | `cpp/ford_fulkerson.cpp` | `rust/ford_fulkerson.rs` | `web/ford_fulkerson.html` |
| 5 | min cut | `java/min_cut.java` | `python/min_cut.py` | `cpp/min_cut.cpp` | `rust/min_cut.rs` | `web/min_cut.html` |
| 6 | network flow | `java/network_flow.java` | `python/network_flow.py` | `cpp/network_flow.cpp` | `rust/network_flow.rs` | — |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
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

- **1. bipartite matching**
- **2. dinic**
- **3. edmonds karp**
- **4. ford fulkerson**
- **5. min cut**
- **6. network flow**

## Tradeoff Matrix

Flagship topic: Network flow (Ford–Fulkerson, Edmonds–Karp, Dinic, bipartite matching, min cut).

| Approach | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Ford–Fulkerson (DFS augmenting paths) | O(E · max_flow) | O(V + E) | Integer capacities, small max_flow; can loop forever on irrationals |
| Edmonds–Karp (BFS augmenting paths) | O(V · E²) | O(V + E) | General case, simple to implement |
| Dinic's algorithm | O(V² · E) general, O(E √V) unit capacities | O(V + E) | Default for large graphs and bipartite matching |
| Push–Relabel | O(V² √E) | O(V + E) | Dense graphs; great practical constants |
| ISAP (improved push–relabel) | O(V² √E) | O(V + E) | Highest practical throughput |
| Hopcroft–Karp (bipartite matching) | O(E √V) | O(V + E) | Pure bipartite matching |

| Approach (min cut) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Max-flow then reachability from source | O(max-flow algorithm) | O(V + E) | s-t min cut |
| Stoer–Wagner | O(V·E + V² log V) | O(V²) | Global min cut on undirected graphs |
| Karger's randomized | O(V²) per run, O(V² log V) high-prob | O(V + E) | Approximation; simple Monte Carlo |

## Anti-patterns to avoid

- **Ford–Fulkerson on capacities given as floats** — augmenting-path search can choose paths whose sum never reaches max flow (classic Zwick example). Stick to integers, or use Edmonds–Karp/Dinic which terminate regardless.
- **Forgetting to add reverse edges with capacity 0** — without them, augmenting paths can't "undo" earlier choices and you'll under-report max flow. Every edge `u→v` needs a back-edge `v→u` initialized to 0.
- **Modeling vertex capacities by clamping flow at a vertex** — the standard trick is to split each vertex into `v_in → v_out` with the vertex capacity on that edge. Trying to enforce it post-hoc never works.
- **Bipartite matching by greedy augmenting without alternating paths** — greedy matching is a 1/2-approximation, not optimal. Use augmenting-path search (Hungarian/Hopcroft–Karp) for maximum matching.
- **Reading Dinic's BFS level graph but not maintaining a `currentEdge[]` pointer** — without it, each DFS revisits saturated edges and the complexity bound breaks. The `currentEdge[]` ("dead end" pointer) is what makes Dinic Dinic.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach max-flow / min-cut duality to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
