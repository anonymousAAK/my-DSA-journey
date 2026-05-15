# Week 28

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | alpha beta | `java/alpha_beta.java` | `python/alpha_beta.py` | `cpp/alpha_beta.cpp` | `rust/alpha_beta.rs` | `web/alpha_beta.html` |
| 2 | game theory | `java/game_theory.java` | `python/game_theory.py` | `cpp/game_theory.cpp` | `rust/game_theory.rs` | — |
| 3 | minimax | `java/minimax.java` | `python/minimax.py` | `cpp/minimax.cpp` | `rust/minimax.rs` | `web/minimax.html` |
| 4 | nim | `java/nim.java` | `python/nim.py` | `cpp/nim.cpp` | `rust/nim.rs` | `web/nim.html` |
| 5 | sprague grundy | `java/sprague_grundy.java` | `python/sprague_grundy.py` | `cpp/sprague_grundy.cpp` | `rust/sprague_grundy.rs` | `web/sprague_grundy.html` |

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

- **1. alpha beta**
- **2. game theory**
- **3. minimax**
- **4. nim**
- **5. sprague grundy**
