# Week 19

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | GreedyAlgorithms | `java/1.GreedyAlgorithms.java` | `python/1.GreedyAlgorithms.py` | `cpp/1.GreedyAlgorithms.cpp` | `rust/s01_GreedyAlgorithms.rs` | `web/1.GreedyAlgorithms.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Greedy | — | `python/greedy.py` | `cpp/greedy.cpp` | `rust/greedy.rs` | — |
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

- **1. GreedyAlgorithms**

## Tradeoff Matrix

Flagship topic: Greedy algorithms (activity selection, fractional knapsack, Huffman).

| Approach (interval scheduling) | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Brute force enumerate subsets | O(2ⁿ) | O(n) | Low | n ≤ 20, oracle for correctness |
| DP on sorted intervals | O(N log N) | O(N) | Medium | Weighted interval scheduling |
| Greedy by earliest finish time | O(N log N) | O(1) extra | Low | Unweighted activity selection — provably optimal |
| Greedy by earliest start time | O(N log N) | O(1) | Low | **Wrong** for activity selection — counterexample exists |

| Approach (knapsack) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Greedy by value/weight ratio | O(N log N) | O(1) | Fractional knapsack — optimal |
| Greedy by ratio (0/1 version) | O(N log N) | O(1) | **Heuristic only** — can be arbitrarily bad |
| DP | O(N·W) | O(W) | 0/1 knapsack — correct |

## Anti-patterns to avoid

- **Reaching for greedy because the problem "feels easy"** — greedy is correct only when the problem has the *exchange* / *matroid* property. Always sketch a counterexample attempt before committing.
- **Sorting by the wrong key** — interval scheduling needs finish time, not start time or duration. The choice of key is the entire algorithm; getting it wrong yields a plausible-looking algorithm that fails on adversarial inputs.
- **Confusing greedy correctness with greedy efficiency** — even a correct greedy strategy needs O(N log N) sorting; calling a method "greedy" doesn't make it O(N).
- **Mixing fractional and 0/1 knapsack** — fractional admits the ratio-greedy proof; 0/1 does not. Items 0/1 with `(w=1, v=2), (w=2, v=3), (w=3, v=4)` and capacity 4 is the classic counterexample.
- **Forgetting tie-breaking** — when two intervals have the same finish time, the greedy can still be correct but the *count of distinct optimal solutions* may not be. Make tie-breaking deterministic if reproducibility matters.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach the "earliest finish time" proof in one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
