# Week 26

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | bipartite matching | `java/bipartite_matching.java` | `python/bipartite_matching.py` | `cpp/bipartite_matching.cpp` | `rust/bipartite_matching.rs` | `web/bipartite_matching.html` |
| 2 | dinic | `java/dinic.java` | `python/dinic.py` | `cpp/dinic.cpp` | `rust/dinic.rs` | `web/dinic.html` |
| 3 | edmonds karp | `java/edmonds_karp.java` | `python/edmonds_karp.py` | `cpp/edmonds_karp.cpp` | `rust/edmonds_karp.rs` | `web/edmonds_karp.html` |
| 4 | ford fulkerson | `java/ford_fulkerson.java` | `python/ford_fulkerson.py` | `cpp/ford_fulkerson.cpp` | `rust/ford_fulkerson.rs` | `web/ford_fulkerson.html` |
| 5 | min cut | `java/min_cut.java` | `python/min_cut.py` | `cpp/min_cut.cpp` | `rust/min_cut.rs` | `web/min_cut.html` |
| 6 | network flow | `java/network_flow.java` | `python/network_flow.py` | `cpp/network_flow.cpp` | `rust/network_flow.rs` | — |

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

- **1. bipartite matching**
- **2. dinic**
- **3. edmonds karp**
- **4. ford fulkerson**
- **5. min cut**
- **6. network flow**
