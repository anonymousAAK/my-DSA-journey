# Week 15 — Heaps & Priority Queues

> Self-check: `./scripts/journey quiz 15`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/1.HeapAndPriorityQueue.py`](python/1.HeapAndPriorityQueue.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_15/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify kth_largest workbook/week_15/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 15`

If you got stuck: open [`python/1.HeapAndPriorityQueue.py`](python/1.HeapAndPriorityQueue.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Heaps & Priority Queues**. You'll touch: HeapAndPriorityQueue. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Mock interview: [`mock_interviews/03_lru_cache.md`](../mock_interviews/03_lru_cache.md) | Heap and LRU-style problems discussed conversationally |
| Capstone: [`capstones/phase_3_visualizer_for_trees_and_heaps.md`](../capstones/phase_3_visualizer_for_trees_and_heaps.md) | Phase 3 capstone — apply what you learned in weeks 11-15 |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | HeapAndPriorityQueue | `java/1.HeapAndPriorityQueue.java` | `python/1.HeapAndPriorityQueue.py` | `cpp/1.HeapAndPriorityQueue.cpp` | `rust/s01_HeapAndPriorityQueue.rs` | `web/1.HeapAndPriorityQueue.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Heaps | — | `python/heaps.py` | `cpp/heaps.cpp` | `rust/heaps.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. HeapAndPriorityQueue**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Heap / Priority Queue (and Kth-largest type problems).

| Approach (Kth largest) | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Sort and pick index | O(N log N) | O(1) | Low | One-shot, small N |
| Max-heap of size N, pop k times | O(N + k log N) | O(N) | Medium | k close to N |
| Min-heap of size k | O(N log k) | O(k) | Medium | Streaming or k much smaller than N |
| Quickselect | O(N) avg, O(N²) worst | O(1) | Medium | One-shot, large N, willing to randomize |
| Counting sort variant | O(N + range) | O(range) | Low | Bounded integer keys |

| Approach (merge k sorted lists) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Concatenate and sort | O(N log N) | O(N) | Tiny inputs |
| Min-heap of heads | O(N log k) | O(k) | Default |
| Pairwise merge (tournament) | O(N log k) | O(1) extra | When the lists are linked lists |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Using `PriorityQueue` and expecting iteration order to be sorted** — `PriorityQueue.iterator()` does *not* return elements in priority order. You must `poll()` them out.
- **Comparator that returns `a - b` for `Integer`** — overflows for large or negative values (`Integer.MIN_VALUE - 1` wraps). Use `Integer.compare(a, b)`.
- **Reusing a min-heap to find Kth largest with `peek()` after `N` inserts** — that gives you the smallest, not the kth largest. Either flip the comparator (max-heap) or keep size capped at k and `peek()` for kth largest.
- **Rebuilding a heap after every update with `heapify`** — that's O(N) per update. Use `siftUp`/`siftDown` on the changed index for O(log N).
- **Removing an arbitrary element via `pq.remove(x)`** — it's O(N) because it linearly searches. If you need decrease-key or arbitrary removal in O(log N), pair the heap with a HashMap of positions.

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
- If you had to teach the "min-heap of size k" trick to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
