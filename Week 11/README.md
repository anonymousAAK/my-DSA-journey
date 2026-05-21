# Week 11 — Linked Lists

> Self-check: `./scripts/journey quiz 11`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/1.SinglyLinkedList.py`](python/1.SinglyLinkedList.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_11/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify reverse_linked_list workbook/week_11/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 11`

If you got stuck: open [`python/1.SinglyLinkedList.py`](python/1.SinglyLinkedList.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Linked Lists**. You'll touch: SinglyLinkedList, MergeSortedListsAndLRU. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Mock interview: [`mock_interviews/03_lru_cache.md`](../mock_interviews/03_lru_cache.md) | Linked list + LRU cache discussed conversationally |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | SinglyLinkedList | `java/1.SinglyLinkedList.java` | `python/1.SinglyLinkedList.py` | `cpp/1.SinglyLinkedList.cpp` | `rust/s01_SinglyLinkedList.rs` | `web/1.SinglyLinkedList.html` |
| 2 | MergeSortedListsAndLRU | `java/2.MergeSortedListsAndLRU.java` | `python/2.MergeSortedListsAndLRU.py` | `cpp/2.MergeSortedListsAndLRU.cpp` | `rust/s02_MergeSortedListsAndLRU.rs` | `web/2.MergeSortedListsAndLRU.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Linked Lists | — | `python/linked_lists.py` | `cpp/linked_lists.cpp` | `rust/linked_lists.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. SinglyLinkedList**
- **2. MergeSortedListsAndLRU**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Linked List operations (singly LL, merge two sorted lists, LRU cache).

| Approach (reverse linked list) | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Iterative three-pointer (`prev`, `curr`, `next`) | O(N) | O(1) | Low | Default — clean and O(1) space |
| Recursive | O(N) | O(N) stack | Medium | When recursion is asked for; risks stack overflow on long lists |
| Stack-based | O(N) | O(N) | Low | Pedagogy; never optimal |

| Approach (LRU cache) | Time per op | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| HashMap + doubly linked list | O(1) | O(capacity) | Medium | Canonical interview answer |
| `LinkedHashMap` (`accessOrder=true`) | O(1) | O(capacity) | Low | When you can use the JDK's built-in |
| Array + timestamps | O(N) lookup | O(capacity) | Low | Tiny caches only |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Forgetting to handle the head-pointer change** — operations that may delete or insert at the head must return the (possibly new) head, or you'll silently leak/skip nodes. Use a sentinel/dummy node to make head-and-rest uniform.
- **Updating only one direction in a doubly linked list** — every insert/delete needs four pointer updates. Miss one and you get a list that walks fine forward but crashes backward.
- **Using `.equals` on node references when you mean identity** — for cycle detection or pointer comparisons you want `==`, not `.equals`. Two different nodes can be "equal" by value but are still distinct.
- **Floyd's cycle detection started with both pointers at head and a `while (slow != fast)`** — they're equal at the start, so the loop never executes. Initialize one pointer ahead, or check inside the body.
- **Implementing LRU with only a HashMap** — you also need ordering. A `HashMap` gives O(1) lookup but no eviction order; without the linked list (or `LinkedHashMap`) you can't find the least-recent in O(1).

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
- If you had to teach LRU cache to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
