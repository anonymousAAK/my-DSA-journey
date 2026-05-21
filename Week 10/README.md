# Week 10 — 2D Arrays & Matrix

> Self-check: `./scripts/journey quiz 10`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/2.spiral_and_diagonal_traversal.py`](python/2.spiral_and_diagonal_traversal.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_10/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify spiral_traversal workbook/week_10/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 10`

If you got stuck: open [`python/2.spiral_and_diagonal_traversal.py`](python/2.spiral_and_diagonal_traversal.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **2D Arrays & Matrix**. You'll touch: MatrixBasics, SpiralAndDiagonalTraversal. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Capstone: [`capstones/phase_2_text_search_tool.md`](../capstones/phase_2_text_search_tool.md) | Phase 2 capstone — apply what you learned in weeks 6-10 |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | MatrixBasics | `java/1.MatrixBasics.java` | `python/1.matrix_basics.py` | `cpp/1.matrix_basics.cpp` | `rust/s01_matrix_basics.rs` | `web/1.matrix_basics.html` |
| 2 | SpiralAndDiagonalTraversal | `java/2.SpiralAndDiagonalTraversal.java` | `python/2.spiral_and_diagonal_traversal.py` | `cpp/2.spiral_and_diagonal_traversal.cpp` | `rust/s02_spiral_and_diagonal_traversal.rs` | `web/2.spiral_and_diagonal_traversal.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Matrix | — | `python/matrix.py` | `cpp/matrix.cpp` | `rust/matrix.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. MatrixBasics**
- **2. SpiralAndDiagonalTraversal**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: 2-D matrix traversal (spiral order, diagonals).

| Approach | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Four-boundary shrinking (top/bottom/left/right) | O(R·C) | O(1) | Medium | Spiral traversal — clearest invariant |
| Direction-vector + visited matrix | O(R·C) | O(R·C) | Medium | When the boundary logic feels error-prone |
| Layer-by-layer recursion | O(R·C) | O(min(R,C)) | High | Pedagogy; rotating a matrix in layers |
| Transpose + reverse (for rotation) | O(R·C) | O(1) | Low | 90° rotation of a square matrix |

| Approach (search in sorted matrix) | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Treat as flat array, binary search | O(log(R·C)) | O(1) | Low | Strictly row-major sorted matrix |
| Staircase search from top-right | O(R+C) | O(1) | Low | Each row and column sorted independently |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Indexing `matrix[col][row]` because that's how you'd say "x, y"** — Java is row-major: `matrix[row][col]`. Mixing these gives you ArrayIndexOutOfBounds in some cases and silently-wrong answers in square matrices.
- **Allocating a new matrix to rotate in place** — defeats the "in place" requirement. Use the transpose-then-reverse trick to rotate with O(1) extra space.
- **Boundary checks scattered through a four-direction step** — collect into one helper `inBounds(r, c)`. Inlining `r >= 0 && r < R && c >= 0 && c < C` four times is where typos live.
- **Forgetting to update the boundary when shrinking in a spiral** — after walking a side, you must move the corresponding boundary inward *before* checking the loop condition. Doing it after produces duplicate visits or skips on odd dimensions.
- **Treating a jagged 2-D array as rectangular** — `matrix[i].length` can differ per row in Java. Cache row length once per row.

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
- If you had to teach spiral traversal to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
