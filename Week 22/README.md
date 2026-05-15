# Week 22

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | ShortestPaths | `java/1.ShortestPaths.java` | `python/1.ShortestPaths.py` | `cpp/1.ShortestPaths.cpp` | `rust/s01_ShortestPaths.rs` | `web/1.ShortestPaths.html` |
| 2 | MinimumSpanningTree | `java/2.MinimumSpanningTree.java` | `python/2.MinimumSpanningTree.py` | `cpp/2.MinimumSpanningTree.cpp` | `rust/s02_MinimumSpanningTree.rs` | `web/2.MinimumSpanningTree.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Advanced Graphs | — | `python/advanced_graphs.py` | `cpp/advanced_graphs.cpp` | `rust/advanced_graphs.rs` | — |
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

- **1. ShortestPaths**
- **2. MinimumSpanningTree**
