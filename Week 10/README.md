# Week 10

> Self-check: `./scripts/journey quiz 10` — run the mastery checkpoints for this week.

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | MatrixBasics | `java/1.MatrixBasics.java` | `python/1.matrix_basics.py` | `cpp/1.matrix_basics.cpp` | `rust/s01_matrix_basics.rs` | `web/1.matrix_basics.html` |
| 2 | SpiralAndDiagonalTraversal | `java/2.SpiralAndDiagonalTraversal.java` | `python/2.spiral_and_diagonal_traversal.py` | `cpp/2.spiral_and_diagonal_traversal.cpp` | `rust/s02_spiral_and_diagonal_traversal.rs` | `web/2.spiral_and_diagonal_traversal.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Matrix | — | `python/matrix.py` | `cpp/matrix.cpp` | `rust/matrix.rs` | — |
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

- **1. MatrixBasics**
- **2. SpiralAndDiagonalTraversal**

## Tradeoff Matrix

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

## Anti-patterns to avoid

- **Indexing `matrix[col][row]` because that's how you'd say "x, y"** — Java is row-major: `matrix[row][col]`. Mixing these gives you ArrayIndexOutOfBounds in some cases and silently-wrong answers in square matrices.
- **Allocating a new matrix to rotate in place** — defeats the "in place" requirement. Use the transpose-then-reverse trick to rotate with O(1) extra space.
- **Boundary checks scattered through a four-direction step** — collect into one helper `inBounds(r, c)`. Inlining `r >= 0 && r < R && c >= 0 && c < C` four times is where typos live.
- **Forgetting to update the boundary when shrinking in a spiral** — after walking a side, you must move the corresponding boundary inward *before* checking the loop condition. Doing it after produces duplicate visits or skips on odd dimensions.
- **Treating a jagged 2-D array as rectangular** — `matrix[i].length` can differ per row in Java. Cache row length once per row.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach spiral traversal to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
