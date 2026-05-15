# Week 13

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | QueueImplementation | `java/1.QueueImplementation.java` | `python/1.QueueImplementation.py` | `cpp/1.QueueImplementation.cpp` | `rust/s01_QueueImplementation.rs` | `web/1.QueueImplementation.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Queues | — | `python/queues.py` | `cpp/queues.cpp` | `rust/queues.rs` | — |
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

- **1. QueueImplementation**

## Tradeoff Matrix

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

## Anti-patterns to avoid

- **Using `LinkedList` and accessing by index** — `get(i)` is O(N) on a linked list. If you need random access, use `ArrayList`/`ArrayDeque`, not `LinkedList`.
- **Circular queue with `front == rear` ambiguity** — `front == rear` means both "empty" and "full" unless you track size separately or leave one slot unused. Pick one and document it.
- **Calling `queue.remove()` to peek** — `remove()` removes and returns; `peek()`/`element()` look without removing. Confusing them eats your data.
- **`null` element in a `Deque`** — `ArrayDeque` and most `Queue` implementations reject `null` because `null` is used as a sentinel for "empty". Storing `null` throws `NullPointerException`.
- **Implementing BFS with a Stack** — BFS needs FIFO (a queue). Using a stack gives you DFS, which finds *a* path, not the shortest one.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach a circular buffer to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
