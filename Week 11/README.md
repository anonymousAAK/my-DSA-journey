# Week 11

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | SinglyLinkedList | `java/1.SinglyLinkedList.java` | `python/1.SinglyLinkedList.py` | `cpp/1.SinglyLinkedList.cpp` | `rust/s01_SinglyLinkedList.rs` | `web/1.SinglyLinkedList.html` |
| 2 | MergeSortedListsAndLRU | `java/2.MergeSortedListsAndLRU.java` | `python/2.MergeSortedListsAndLRU.py` | `cpp/2.MergeSortedListsAndLRU.cpp` | `rust/s02_MergeSortedListsAndLRU.rs` | `web/2.MergeSortedListsAndLRU.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Linked Lists | — | `python/linked_lists.py` | `cpp/linked_lists.cpp` | `rust/linked_lists.rs` | — |
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

- **1. SinglyLinkedList**
- **2. MergeSortedListsAndLRU**
