# Week 27 — Computational Geometry

> Self-check: `./scripts/journey quiz 27`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/convex_hull.py`](python/convex_hull.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_27/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify cross_product_sign workbook/week_27/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 27`

If you got stuck: open [`python/convex_hull.py`](python/convex_hull.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Computational Geometry**. You'll touch: closest pair, convex hull, geometry, line intersection, sweep line. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | closest pair | `java/closest_pair.java` | `python/closest_pair.py` | `cpp/closest_pair.cpp` | `rust/closest_pair.rs` | `web/closest_pair.html` |
| 2 | convex hull | `java/convex_hull.java` | `python/convex_hull.py` | `cpp/convex_hull.cpp` | `rust/convex_hull.rs` | `web/convex_hull.html` |
| 3 | geometry | `java/geometry.java` | `python/geometry.py` | `cpp/geometry.cpp` | `rust/geometry.rs` | — |
| 4 | line intersection | `java/line_intersection.java` | `python/line_intersection.py` | `cpp/line_intersection.cpp` | `rust/line_intersection.rs` | `web/line_intersection.html` |
| 5 | sweep line | `java/sweep_line.java` | `python/sweep_line.py` | `cpp/sweep_line.cpp` | `rust/sweep_line.rs` | `web/sweep_line.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. closest pair**
- **2. convex hull**
- **3. geometry**
- **4. line intersection**
- **5. sweep line**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


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

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Comparing floating-point coordinates with `==`** — almost guarantees nondeterministic behavior. Use an epsilon tolerance, or — better — work with integer coordinates and the cross product so all comparisons are exact.
- **Cross product computed as `a.x * b.x + a.y * b.y`** — that's the dot product. The 2-D cross is `a.x * b.y - a.y * b.x`. Mixing them up corrupts orientation tests and every algorithm downstream.
- **Convex hull with duplicate or collinear points handled inconsistently** — decide whether collinear points belong on the hull, then enforce it with `cross ≤ 0` vs `cross < 0` in your turn test. Different conventions produce different (both valid) hulls.
- **Sweep-line events stored in a `HashSet`** — you need *ordered* events, sorted by x (and a tiebreak rule). Use a TreeSet/PQ; HashSet drops the order you depend on.
- **Point-in-polygon by signed-area sum** — works only for convex polygons. For general polygons use ray casting (count crossings) or winding number.

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
- If you had to teach the cross-product orientation test to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
