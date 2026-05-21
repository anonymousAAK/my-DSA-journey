# Week 12 — Stacks

> Self-check: `./scripts/journey quiz 12`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/1.StackImplementation.py`](python/1.StackImplementation.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_12/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify balanced_parens workbook/week_12/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 12`

If you got stuck: open [`python/1.StackImplementation.py`](python/1.StackImplementation.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Stacks**. You'll touch: StackImplementation. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

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
| 1 | StackImplementation | `java/1.StackImplementation.java` | `python/1.StackImplementation.py` | `cpp/1.StackImplementation.cpp` | `rust/s01_StackImplementation.rs` | `web/1.StackImplementation.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Stacks | — | `python/stacks.py` | `cpp/stacks.cpp` | `rust/stacks.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. StackImplementation**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Stack implementation and usage.

| Approach | Time per op | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| `java.util.Stack` | O(1) amortized | O(N) | Lowest | Quick prototypes; legacy code |
| `ArrayDeque` (recommended) | O(1) amortized | O(N) | Low | Production — `Stack` is synchronized and slow |
| `LinkedList` as stack | O(1) | O(N) | Low | Rare — worse cache behavior than `ArrayDeque` |
| Hand-rolled array-backed stack | O(1) amortized | O(N) | Medium | Learning the resize/doubling pattern |
| Hand-rolled linked-node stack | O(1) | O(N) | Medium | When you need true O(1) push (no resize pauses) |

| Approach (next greater element) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Brute force nested loop | O(N²) | O(1) | N ≤ 10³ |
| Monotonic decreasing stack | O(N) | O(N) | Default — every "next greater/smaller" problem |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Using `java.util.Stack` in new code** — it extends `Vector`, which is synchronized; you pay locking cost you don't want, and the iteration order is bottom-to-top, which surprises people. Use `ArrayDeque`.
- **Pushing onto an `ArrayDeque` with `addLast` and popping with `removeFirst`** — that's a queue, not a stack. For stack semantics use `push`/`pop` (which map to `addFirst`/`removeFirst`) consistently.
- **Forgetting to check `isEmpty()` before `pop()`** — popping an empty stack throws `NoSuchElementException` (or `EmptyStackException` for the legacy class). Always guard, especially in matching-brackets problems.
- **Implementing "min stack" with two stacks but pushing onto the min-stack every push** — wastes space. Only push when the new value is `<=` current min, and only pop when the popped value equals current min.
- **Solving "valid parentheses" with a counter instead of a stack** — works for one bracket type but fails the moment you have `()[]{}` because a counter can't tell `(]` from `()`.

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
- If you had to teach the monotonic-stack pattern to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
