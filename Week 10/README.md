# Week 10

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
