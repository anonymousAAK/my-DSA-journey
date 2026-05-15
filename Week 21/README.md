# Week 21

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | SegmentTreeAndBIT | `java/1.SegmentTreeAndBIT.java` | `python/1.SegmentTreeAndBIT.py` | `cpp/1.SegmentTreeAndBIT.cpp` | `rust/s01_SegmentTreeAndBIT.rs` | `web/1.SegmentTreeAndBIT.html` |
| 2 | Trie | `java/2.Trie.java` | `python/2.Trie.py` | `cpp/2.Trie.cpp` | `rust/s02_Trie.rs` | `web/2.Trie.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Advanced Trees | — | `python/advanced_trees.py` | `cpp/advanced_trees.cpp` | `rust/advanced_trees.rs` | — |
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

- **1. SegmentTreeAndBIT**
- **2. Trie**
