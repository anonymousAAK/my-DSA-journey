# Week 17

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
