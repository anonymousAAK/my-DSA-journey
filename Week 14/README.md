# Week 14

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | BinaryTree | `java/1.BinaryTree.java` | `python/1.BinaryTree.py` | `cpp/1.BinaryTree.cpp` | `rust/s01_BinaryTree.rs` | `web/1.BinaryTree.html` |
| 2 | BinarySearchTree | `java/2.BinarySearchTree.java` | `python/2.BinarySearchTree.py` | `cpp/2.BinarySearchTree.cpp` | `rust/s02_BinarySearchTree.rs` | `web/2.BinarySearchTree.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Trees | — | `python/trees.py` | `cpp/trees.cpp` | `rust/trees.rs` | — |
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

- **1. BinaryTree**
- **2. BinarySearchTree**
