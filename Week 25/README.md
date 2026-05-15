# Week 25

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | KMP | `java/1.KMP.java` | `python/1.kmp.py` | `cpp/1.kmp.cpp` | `rust/s01_kmp.rs` | `web/1.kmp.html` |
| 2 | RabinKarp | `java/2.RabinKarp.java` | `python/2.rabin_karp.py` | `cpp/2.rabin_karp.cpp` | `rust/s02_rabin_karp.rs` | `web/2.rabin_karp.html` |
| 3 | ZAlgorithm | `java/3.ZAlgorithm.java` | `python/3.z_algorithm.py` | `cpp/3.z_algorithm.cpp` | `rust/s03_z_algorithm.rs` | `web/3.z_algorithm.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| String Algorithms | `java/string_algorithms.java` | `python/string_algorithms.py` | `cpp/string_algorithms.cpp` | `rust/string_algorithms.rs` | `web/string_algorithms.html` |
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

- **1. KMP**
- **2. RabinKarp**
- **3. ZAlgorithm**
