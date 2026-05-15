# Week 25

> Self-check: `./scripts/journey quiz 25` — run the mastery checkpoints for this week.

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

## Tradeoff Matrix

Flagship topic: String matching algorithms (KMP, Rabin–Karp, Z).

| Approach | Preprocessing | Search | Space | When to prefer |
|----------|------|--------|-------|----------------|
| Naive | 0 | O(N·M) | O(1) | Small inputs, or as a baseline |
| KMP (failure function) | O(M) | O(N) | O(M) | Single pattern, worst-case guarantee |
| Rabin–Karp (rolling hash) | O(M) | O(N) avg, O(N·M) worst | O(1) | Multiple patterns of same length, plagiarism detection |
| Z-algorithm | O(N+M) | included | O(N+M) | Need all matches plus prefix info |
| Boyer–Moore (bad char + good suffix) | O(M + Σ) | O(N/M) best, O(N·M) worst | O(M + Σ) | Long patterns, large alphabet (`grep`'s default) |
| Aho–Corasick | O(Σ Mi) | O(N + matches) | O(Σ Mi · Σ) | Many patterns at once |
| Suffix Automaton / Suffix Array | O(N) / O(N log N) | varies | O(N) | Repeated queries on one fixed text |

## Anti-patterns to avoid

- **Computing KMP's failure function with a single nested loop and `if (s[i]==s[j]) j++; else j=0`** — resetting `j` to 0 on mismatch is the bug version. The correct fallback is `j = failure[j-1]` (recursively), which is the entire point of KMP.
- **Rabin–Karp with a single hash and no verification** — collisions happen; once you find a match by hash you must verify character-by-character. Without verification you'll occasionally report false positives.
- **Using `String.substring` inside the matching loop** — in modern Java that's an O(M) allocation per index, turning your O(N) algorithm into O(N·M). Compare characters with `charAt` directly.
- **Z-algorithm with the `[l, r]` window updated incorrectly** — when `i + Z[i-l] >= r`, you must extend by character comparison and update `(l, r)`. Skipping that update breaks every subsequent index.
- **Treating Boyer–Moore as "obviously faster"** — its worst case on patterns like `aaaa...a` in text `aaaa...ab` is O(N·M). For adversarial inputs use KMP, which is worst-case O(N+M).

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach a rolling hash to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
