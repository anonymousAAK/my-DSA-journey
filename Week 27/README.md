# Week 27

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | closest pair | `java/closest_pair.java` | `python/closest_pair.py` | `cpp/closest_pair.cpp` | `rust/closest_pair.rs` | `web/closest_pair.html` |
| 2 | convex hull | `java/convex_hull.java` | `python/convex_hull.py` | `cpp/convex_hull.cpp` | `rust/convex_hull.rs` | `web/convex_hull.html` |
| 3 | geometry | `java/geometry.java` | `python/geometry.py` | `cpp/geometry.cpp` | `rust/geometry.rs` | — |
| 4 | line intersection | `java/line_intersection.java` | `python/line_intersection.py` | `cpp/line_intersection.cpp` | `rust/line_intersection.rs` | `web/line_intersection.html` |
| 5 | sweep line | `java/sweep_line.java` | `python/sweep_line.py` | `cpp/sweep_line.cpp` | `rust/sweep_line.rs` | `web/sweep_line.html` |

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

- **1. closest pair**
- **2. convex hull**
- **3. geometry**
- **4. line intersection**
- **5. sweep line**

## Tradeoff Matrix

Flagship topic: Computational geometry (convex hull, closest pair, line intersection, sweep line).

| Approach (convex hull) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Brute force (test each edge) | O(N³) | O(1) | N ≤ 100, pedagogy |
| Jarvis march / gift wrapping | O(N · H) | O(N) | Output-sensitive when H (hull points) is small |
| Graham scan | O(N log N) | O(N) | Default |
| Andrew's monotone chain | O(N log N) | O(N) | Simpler than Graham; avoids polar-angle sort |
| Chan's algorithm | O(N log H) | O(N) | Theoretically optimal output-sensitive |
| QuickHull | O(N log N) avg, O(N²) worst | O(N) | Easy to parallelize |

| Approach (closest pair) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Brute force | O(N²) | O(1) | N ≤ 2000 |
| Sort + divide & conquer | O(N log N) | O(N) | Default theoretical answer |
| Sweep line + balanced BST | O(N log N) | O(N) | Same complexity, simpler implementation |
| Randomized grid | O(N) expected | O(N) | Practical for huge N |

## Anti-patterns to avoid

- **Comparing floating-point coordinates with `==`** — almost guarantees nondeterministic behavior. Use an epsilon tolerance, or — better — work with integer coordinates and the cross product so all comparisons are exact.
- **Cross product computed as `a.x * b.x + a.y * b.y`** — that's the dot product. The 2-D cross is `a.x * b.y - a.y * b.x`. Mixing them up corrupts orientation tests and every algorithm downstream.
- **Convex hull with duplicate or collinear points handled inconsistently** — decide whether collinear points belong on the hull, then enforce it with `cross ≤ 0` vs `cross < 0` in your turn test. Different conventions produce different (both valid) hulls.
- **Sweep-line events stored in a `HashSet`** — you need *ordered* events, sorted by x (and a tiebreak rule). Use a TreeSet/PQ; HashSet drops the order you depend on.
- **Point-in-polygon by signed-area sum** — works only for convex polygons. For general polygons use ray casting (count crossings) or winding number.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach the cross-product orientation test to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
