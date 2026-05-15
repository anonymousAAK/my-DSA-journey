# Week 27

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | closest pair | `java/closest_pair.java` | `python/closest_pair.py` | `cpp/closest_pair.cpp` | `rust/closest_pair.rs` | `web/closest_pair.html` |
| 2 | convex hull | `java/convex_hull.java` | `python/convex_hull.py` | `cpp/convex_hull.cpp` | `rust/convex_hull.rs` | `web/convex_hull.html` |
| 3 | geometry | `java/geometry.java` | `python/geometry.py` | `cpp/geometry.cpp` | `rust/geometry.rs` | — |
| 4 | line intersection | `java/line_intersection.java` | `python/line_intersection.py` | `cpp/line_intersection.cpp` | `rust/line_intersection.rs` | `web/line_intersection.html` |
| 5 | sweep line | `java/sweep_line.java` | `python/sweep_line.py` | `cpp/sweep_line.cpp` | `rust/sweep_line.rs` | `web/sweep_line.html` |

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

- **1. closest pair**
- **2. convex hull**
- **3. geometry**
- **4. line intersection**
- **5. sweep line**
