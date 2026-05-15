# Week 7

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | StringBasics | `java/1.StringBasics.java` | `python/1.string_basics.py` | `cpp/1.string_basics.cpp` | `rust/s01_string_basics.rs` | `web/1.string_basics.html` |
| 2 | PalindromeAndAnagram | `java/2.PalindromeAndAnagram.java` | `python/2.palindrome_and_anagram.py` | `cpp/2.palindrome_and_anagram.cpp` | `rust/s02_palindrome_and_anagram.rs` | `web/2.palindrome_and_anagram.html` |
| 3 | KMPSearch | `java/3.KMPSearch.java` | `python/3.kmp_search.py` | `cpp/3.kmp_search.cpp` | `rust/s03_kmp_search.rs` | `web/3.kmp_search.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Strings | — | `python/strings.py` | `cpp/strings.cpp` | `rust/strings.rs` | — |
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

- **1. StringBasics**
- **2. PalindromeAndAnagram**
- **3. KMPSearch**
