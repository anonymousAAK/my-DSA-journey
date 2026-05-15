# Week 23

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | AdvancedDP | `java/1.AdvancedDP.java` | `python/1.AdvancedDP.py` | `cpp/1.AdvancedDP.cpp` | `rust/s01_AdvancedDP.rs` | `web/1.AdvancedDP.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Advanced Dp | — | `python/advanced_dp.py` | `cpp/advanced_dp.cpp` | `rust/advanced_dp.rs` | — |
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

- **1. AdvancedDP**

## Tradeoff Matrix

Flagship topic: Advanced DP (bitmask DP, digit DP, DP on trees, DP optimizations).

| Approach (TSP-style) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Brute force permutations | O(N!) | O(N) | N ≤ 10 |
| Bitmask DP (Held–Karp) | O(N² · 2ᴺ) | O(N · 2ᴺ) | N ≤ ~20 |
| Branch and bound | Exponential, pruned | varies | Real TSP instances |
| Approximation (Christofides) | O(N³) | O(N²) | When exact is infeasible and you need a guaranteed factor |

| Approach (DP on tree) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Single DFS, return aggregates | O(N) | O(N) | Most subtree-DP problems |
| Rerooting / "DP on tree, twice" | O(N) | O(N) | Answers for every root |
| Heavy-Light Decomposition | O(N log² N) per query | O(N) | Path queries on trees |

| Approach (DP optimization) | Improvement | When to apply |
|----------|------|----------------|
| Convex Hull Trick | O(N²) → O(N log N) | DP transitions with `min/max` over linear functions |
| Divide & Conquer DP | O(N²) → O(N log N) | Monotone opt(i) on partition DP |
| Knuth's optimization | O(N³) → O(N²) | Quadrangle-inequality interval DPs |
| Aliens trick / parametric search | adds a log factor for one less dim | "exactly k" partition problems |

## Anti-patterns to avoid

- **Bitmask DP without verifying the state space fits** — `2²⁵` states × 25 transitions is fine; `2³⁰` is not. Compute the product before coding.
- **Iterating subsets the slow way** — to iterate all subsets of a mask, use `for (int s = mask; s > 0; s = (s-1) & mask)`. The naive `for (i in 0..(1<<n))` plus filter is exponentially slower for sum-over-subsets style DPs.
- **Digit DP without "tight" / "leading zero" flags** — these two flags are what make digit DP correct. Omitting them produces results that are wrong by exactly the digits-with-leading-zero issue.
- **Rerooting DP that doesn't subtract the child's contribution carefully** — if your aggregate isn't reversible (e.g. min/max instead of sum), rerooting requires keeping top-2 values per node. Treating min/max as sum is the single most common bug here.
- **Applying CHT without checking the slope ordering** — Convex Hull Trick requires lines to be added in sorted slope order (or you need Li Chao tree). Adding arbitrary lines to a monotonic deque silently corrupts the hull.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach bitmask DP to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
