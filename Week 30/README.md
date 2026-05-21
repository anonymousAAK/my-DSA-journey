# Week 30 — Interview Patterns & Mastery

> Self-check: `./scripts/journey quiz 30`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/two_pointers.py`](python/two_pointers.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_30/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify two_pointers_when workbook/week_30/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 30`

If you got stuck: open [`python/two_pointers.py`](python/two_pointers.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Interview Patterns & Mastery**. You'll touch: fast slow pointers, interview patterns, merge intervals, sliding window, top k elements, two pointers. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Capstone: [`capstones/phase_6_tinyurl_with_consistent_hashing.md`](../capstones/phase_6_tinyurl_with_consistent_hashing.md) | Phase 6 capstone — apply what you learned in weeks 26-30 |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | fast slow pointers | `java/fast_slow_pointers.java` | `python/fast_slow_pointers.py` | `cpp/fast_slow_pointers.cpp` | `rust/fast_slow_pointers.rs` | `web/fast_slow_pointers.html` |
| 2 | interview patterns | `java/interview_patterns.java` | `python/interview_patterns.py` | `cpp/interview_patterns.cpp` | `rust/interview_patterns.rs` | — |
| 3 | merge intervals | `java/merge_intervals.java` | `python/merge_intervals.py` | `cpp/merge_intervals.cpp` | `rust/merge_intervals.rs` | `web/merge_intervals.html` |
| 4 | sliding window | `java/sliding_window.java` | `python/sliding_window.py` | `cpp/sliding_window.cpp` | `rust/sliding_window.rs` | `web/sliding_window.html` |
| 5 | top k elements | `java/top_k_elements.java` | `python/top_k_elements.py` | `cpp/top_k_elements.cpp` | `rust/top_k_elements.rs` | `web/top_k_elements.html` |
| 6 | two pointers | `java/two_pointers.java` | `python/two_pointers.py` | `cpp/two_pointers.cpp` | `rust/two_pointers.rs` | `web/two_pointers.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. fast slow pointers**
- **2. interview patterns**
- **3. merge intervals**
- **4. sliding window**
- **5. top k elements**
- **6. two pointers**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Interview patterns (sliding window, two pointers, fast/slow, merge intervals, top-K).

| Approach (top-K elements) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Sort | O(N log N) | O(1) | One-off, small N |
| Min-heap of size k | O(N log k) | O(k) | Streaming or k ≪ N |
| Quickselect | O(N) avg, O(N²) worst | O(1) | Single batch, large N |
| Bucket / counting | O(N) | O(range) | Bounded value range (e.g. top-k frequent) |

| Approach (sliding window) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Fixed-size window | O(N) | O(k) | Window length given |
| Variable-size window (expand/shrink) | O(N) | O(distinct) | "Longest/shortest substring satisfying X" |
| Window + monotonic deque | O(N) | O(k) | Window max/min |

| Approach (cycle detection / linked-list mid) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| HashSet of visited | O(N) | O(N) | When you need the actual visited set |
| Floyd's tortoise & hare | O(N) | O(1) | Default — constant space |
| Brent's algorithm | O(N) | O(1) | ~36% fewer iterations than Floyd's in practice |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Sliding window where `right` and `left` advance in tangled loops** — the canonical shape is one outer `for right` and an inner `while (invariant broken) left++`. Reaching for two `while`s nested arbitrarily turns O(N) into O(N²) and breaks the invariant proof.
- **Two-pointer on an unsorted array** — most two-pointer techniques (sorted-pair sum, container-with-most-water variant aside) assume sortedness. Sort first, or use a different pattern.
- **Floyd's cycle detection that starts the second phase from the wrong pointer** — after meeting inside the cycle, you must restart one pointer at the head, move both at speed 1, and the meeting point is the cycle entry. Restarting at the meeting point gives a different (wrong) node.
- **Merging intervals without sorting first** — the entire correctness argument depends on sorted-by-start order. Without it you'll merge non-overlapping intervals and miss overlapping ones.
- **Top-K with a max-heap of size N** — works, but is O(N + k log N). A *min-heap of size k* is O(N log k), which is strictly better when k ≪ N. Inverting the heap by mistake is also why some people get "smallest k" when they wanted "largest k".

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
- If you had to teach the expand/shrink sliding window to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern? (Bonus: schedule that revisit on your calendar now.)
