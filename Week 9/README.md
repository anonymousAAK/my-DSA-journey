# Week 9

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | BubbleSelectionInsertion | `java/1.BubbleSelectionInsertion.java` | `python/1.bubble_selection_insertion.py` | `cpp/1.bubble_selection_insertion.cpp` | `rust/s01_bubble_selection_insertion.rs` | `web/1.bubble_selection_insertion.html` |
| 2 | MergeSort | `java/2.MergeSort.java` | `python/2.merge_sort.py` | `cpp/2.merge_sort.cpp` | `rust/s02_merge_sort.rs` | `web/2.merge_sort.html` |
| 3 | QuickSort | `java/3.QuickSort.java` | `python/3.quick_sort.py` | `cpp/3.quick_sort.cpp` | `rust/s03_quick_sort.rs` | `web/3.quick_sort.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Sorting | — | `python/sorting.py` | `cpp/sorting.cpp` | `rust/sorting.rs` | — |
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

- **1. BubbleSelectionInsertion**
- **2. MergeSort**
- **3. QuickSort**
