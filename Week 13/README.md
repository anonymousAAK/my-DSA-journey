# Week 13 — Queues

> Self-check: `./scripts/journey quiz 13`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/1.QueueImplementation.py`](python/1.QueueImplementation.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_13/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify sliding_window_max workbook/week_13/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 13`

If you got stuck: open [`python/1.QueueImplementation.py`](python/1.QueueImplementation.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Queues**. You'll touch: QueueImplementation. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | QueueImplementation | `java/1.QueueImplementation.java` | `python/1.QueueImplementation.py` | `cpp/1.QueueImplementation.cpp` | `rust/s01_QueueImplementation.rs` | `web/1.QueueImplementation.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Queues | — | `python/queues.py` | `cpp/queues.cpp` | `rust/queues.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. QueueImplementation**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Queue implementation (array circular, linked, deque).

| Approach | Time per op | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| `LinkedList` as `Queue` | O(1) | O(N) + per-node overhead | Low | Quick prototype |
| `ArrayDeque` | O(1) amortized | O(N) | Low | Production default |
| Hand-rolled circular array | O(1) | O(capacity) | Medium | Bounded queues, embedded systems |
| Two stacks → queue | O(1) amortized | O(N) | Medium | Interview classic; teaches amortized analysis |
| `java.util.concurrent` queues | O(1) | O(N) | Low | Cross-thread producer/consumer |

| Approach (sliding window max) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Brute force | O(N·k) | O(1) | Tiny k |
| Heap (priority queue) | O(N log k) | O(k) | When you also need order statistics |
| Monotonic deque | O(N) | O(k) | Default — optimal |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Using `LinkedList` and accessing by index** — `get(i)` is O(N) on a linked list. If you need random access, use `ArrayList`/`ArrayDeque`, not `LinkedList`.
- **Circular queue with `front == rear` ambiguity** — `front == rear` means both "empty" and "full" unless you track size separately or leave one slot unused. Pick one and document it.
- **Calling `queue.remove()` to peek** — `remove()` removes and returns; `peek()`/`element()` look without removing. Confusing them eats your data.
- **`null` element in a `Deque`** — `ArrayDeque` and most `Queue` implementations reject `null` because `null` is used as a sentinel for "empty". Storing `null` throws `NullPointerException`.
- **Implementing BFS with a Stack** — BFS needs FIFO (a queue). Using a stack gives you DFS, which finds *a* path, not the shortest one.

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
- If you had to teach a circular buffer to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
