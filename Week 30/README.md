# Week 30

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | fast slow pointers | `java/fast_slow_pointers.java` | `python/fast_slow_pointers.py` | `cpp/fast_slow_pointers.cpp` | `rust/fast_slow_pointers.rs` | `web/fast_slow_pointers.html` |
| 2 | interview patterns | `java/interview_patterns.java` | `python/interview_patterns.py` | `cpp/interview_patterns.cpp` | `rust/interview_patterns.rs` | — |
| 3 | merge intervals | `java/merge_intervals.java` | `python/merge_intervals.py` | `cpp/merge_intervals.cpp` | `rust/merge_intervals.rs` | `web/merge_intervals.html` |
| 4 | sliding window | `java/sliding_window.java` | `python/sliding_window.py` | `cpp/sliding_window.cpp` | `rust/sliding_window.rs` | `web/sliding_window.html` |
| 5 | top k elements | `java/top_k_elements.java` | `python/top_k_elements.py` | `cpp/top_k_elements.cpp` | `rust/top_k_elements.rs` | `web/top_k_elements.html` |
| 6 | two pointers | `java/two_pointers.java` | `python/two_pointers.py` | `cpp/two_pointers.cpp` | `rust/two_pointers.rs` | `web/two_pointers.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
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

- **1. fast slow pointers**
- **2. interview patterns**
- **3. merge intervals**
- **4. sliding window**
- **5. top k elements**
- **6. two pointers**
