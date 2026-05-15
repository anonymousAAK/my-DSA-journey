# Week 21

> Self-check: `./scripts/journey quiz 21` — run the mastery checkpoints for this week.

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | SegmentTreeAndBIT | `java/1.SegmentTreeAndBIT.java` | `python/1.SegmentTreeAndBIT.py` | `cpp/1.SegmentTreeAndBIT.cpp` | `rust/s01_SegmentTreeAndBIT.rs` | `web/1.SegmentTreeAndBIT.html` |
| 2 | Trie | `java/2.Trie.java` | `python/2.Trie.py` | `cpp/2.Trie.cpp` | `rust/s02_Trie.rs` | `web/2.Trie.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Advanced Trees | — | `python/advanced_trees.py` | `cpp/advanced_trees.cpp` | `rust/advanced_trees.rs` | — |
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

- **1. SegmentTreeAndBIT**
- **2. Trie**

## Tradeoff Matrix

Flagship topic: Range queries (Segment Tree / BIT) and prefix structures (Trie).

| Approach (range sum / point update) | Build | Update | Query | When to prefer |
|----------|------|--------|-------|----------------|
| Naive array | O(N) | O(1) | O(N) | Tiny inputs |
| Prefix sum array | O(N) | O(N) | O(1) | Read-mostly, updates rare |
| Binary Indexed Tree (Fenwick) | O(N log N) | O(log N) | O(log N) | Simpler code; sum/XOR-style queries |
| Segment tree | O(N) | O(log N) | O(log N) | General; supports min/max/gcd, lazy propagation |
| Sqrt decomposition | O(N) | O(√N) | O(√N) | Off-line and easier to reason about |

| Approach (Trie use case) | Time per op | Space | When to prefer |
|----------|------|-------|----------------|
| HashSet of strings | O(L) avg | O(total chars) | When you only need exact membership |
| Trie | O(L) | O(total chars × Σ) | Prefix queries, autocomplete, XOR-max (binary trie) |
| Suffix automaton / array | O(N) build | O(N) | All-substrings queries |

## Anti-patterns to avoid

- **Building a segment tree on 2N size when you need 4N** — for arbitrary N (not a power of 2), allocate `4 * N` to be safe. Allocating `2 * N` segfaults on odd N.
- **Forgetting lazy propagation on range updates** — without lazy, a range update is O(N log N), defeating the point. Push the pending update down before any read or recursion into children.
- **BIT 1-indexed off-by-one** — Fenwick trees are easiest 1-indexed. Mixing 0-indexed input with 1-indexed BIT internals is a common bug; pick one convention and translate at the boundary.
- **Trie children as `HashMap<Character, Node>` when you only have 26 letters** — fixed-size array `Node[26]` is faster and uses less memory. Map is only worth it for large/sparse alphabets.
- **Storing `isEnd` only at leaves** — once a longer word is inserted, the shorter word's endpoint isn't a leaf anymore. The `isEnd` flag must live on the node, regardless of whether it's a leaf.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach BIT's `i & -i` trick to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
