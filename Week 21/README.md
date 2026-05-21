# Week 21 — Advanced Trees

> Self-check: `./scripts/journey quiz 21`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/1.SegmentTreeAndBIT.py`](python/1.SegmentTreeAndBIT.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_21/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify avl_balance_factor workbook/week_21/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 21`

If you got stuck: open [`python/1.SegmentTreeAndBIT.py`](python/1.SegmentTreeAndBIT.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Advanced Trees**. You'll touch: SegmentTreeAndBIT, Trie. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Visualization: [`viz/segment_tree.html`](../viz/segment_tree.html) | You want to SEE the segment tree update and query |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | SegmentTreeAndBIT | `java/1.SegmentTreeAndBIT.java` | `python/1.SegmentTreeAndBIT.py` | `cpp/1.SegmentTreeAndBIT.cpp` | `rust/s01_SegmentTreeAndBIT.rs` | `web/1.SegmentTreeAndBIT.html` |
| 2 | Trie | `java/2.Trie.java` | `python/2.Trie.py` | `cpp/2.Trie.cpp` | `rust/s02_Trie.rs` | `web/2.Trie.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Advanced Trees | — | `python/advanced_trees.py` | `cpp/advanced_trees.cpp` | `rust/advanced_trees.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. SegmentTreeAndBIT**
- **2. Trie**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


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

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Building a segment tree on 2N size when you need 4N** — for arbitrary N (not a power of 2), allocate `4 * N` to be safe. Allocating `2 * N` segfaults on odd N.
- **Forgetting lazy propagation on range updates** — without lazy, a range update is O(N log N), defeating the point. Push the pending update down before any read or recursion into children.
- **BIT 1-indexed off-by-one** — Fenwick trees are easiest 1-indexed. Mixing 0-indexed input with 1-indexed BIT internals is a common bug; pick one convention and translate at the boundary.
- **Trie children as `HashMap<Character, Node>` when you only have 26 letters** — fixed-size array `Node[26]` is faster and uses less memory. Map is only worth it for large/sparse alphabets.
- **Storing `isEnd` only at leaves** — once a longer word is inserted, the shorter word's endpoint isn't a leaf anymore. The `isEnd` flag must live on the node, regardless of whether it's a leaf.

</details>

## Reference: how to run a topic file

<details>
<summary>Java / Python / C++ / Rust / Web one-liners</summary>


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

</details>

## Reflection prompts


- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach BIT's `i & -i` trick to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
