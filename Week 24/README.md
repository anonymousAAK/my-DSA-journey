# Week 24

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | ResearchLevelTopics | `java/1.ResearchLevelTopics.java` | `python/1.ResearchLevelTopics.py` | `cpp/1.ResearchLevelTopics.cpp` | `rust/s01_ResearchLevelTopics.rs` | `web/1.ResearchLevelTopics.html` |
| 2 | NPCompletenessAndApproximation | `java/2.NPCompletenessAndApproximation.java` | `python/2.NPCompletenessAndApproximation.py` | `cpp/2.NPCompletenessAndApproximation.cpp` | `rust/s02_NPCompletenessAndApproximation.rs` | `web/2.NPCompletenessAndApproximation.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Research Level | — | `python/research_level.py` | `cpp/research_level.cpp` | `rust/research_level.rs` | — |
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

- **1. ResearchLevelTopics**
- **2. NPCompletenessAndApproximation**
