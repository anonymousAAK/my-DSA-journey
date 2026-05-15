# Week 5

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | MethodBasics | `java/1.MethodBasics.java` | `python/1.method_basics.py` | `cpp/1.method_basics.cpp` | `rust/s01_method_basics.rs` | `web/1.method_basics.html` |
| 2 | MethodOverloading | `java/2.MethodOverloading.java` | `python/2.method_overloading.py` | `cpp/2.method_overloading.cpp` | `rust/s02_method_overloading.rs` | `web/2.method_overloading.html` |
| 3 | RecursionBasics | `java/3.RecursionBasics.java` | `python/3.recursion_basics.py` | `cpp/3.recursion_basics.cpp` | `rust/s03_recursion_basics.rs` | `web/3.recursion_basics.html` |
| 4 | FibonacciRecursion | `java/4.FibonacciRecursion.java` | `python/4.fibonacci_recursion.py` | `cpp/4.fibonacci_recursion.cpp` | `rust/s04_fibonacci_recursion.rs` | `web/4.fibonacci_recursion.html` |
| 5 | TowerOfHanoi | `java/5.TowerOfHanoi.java` | `python/5.tower_of_hanoi.py` | `cpp/5.tower_of_hanoi.cpp` | `rust/s05_tower_of_hanoi.rs` | `web/5.tower_of_hanoi.html` |
| 6 | RecursionPatterns | `java/6.RecursionPatterns.java` | `python/6.recursion_patterns.py` | `cpp/6.recursion_patterns.cpp` | `rust/s06_recursion_patterns.rs` | `web/6.recursion_patterns.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Recursion | — | `python/recursion.py` | `cpp/recursion.cpp` | `rust/recursion.rs` | — |
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

- **1. MethodBasics**
- **2. MethodOverloading**
- **3. RecursionBasics**
- **4. FibonacciRecursion**
- **5. TowerOfHanoi**
- **6. RecursionPatterns**
