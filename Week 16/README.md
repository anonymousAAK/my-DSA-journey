# Week 16 — Hash Tables & Maps

> Self-check: `./scripts/journey quiz 16`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/1.HashingAndHashMap.py`](python/1.HashingAndHashMap.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_16/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify two_sum workbook/week_16/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 16`

If you got stuck: open [`python/1.HashingAndHashMap.py`](python/1.HashingAndHashMap.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Hash Tables & Maps**. You'll touch: HashingAndHashMap. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Mock interview: [`mock_interviews/01_two_sum_warm_up.md`](../mock_interviews/01_two_sum_warm_up.md) | Hashing two-sum style problems in a conversation |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | HashingAndHashMap | `java/1.HashingAndHashMap.java` | `python/1.HashingAndHashMap.py` | `cpp/1.HashingAndHashMap.cpp` | `rust/s01_HashingAndHashMap.rs` | `web/1.HashingAndHashMap.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Hashing | — | `python/hashing.py` | `cpp/hashing.cpp` | `rust/hashing.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. HashingAndHashMap**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Hashing and HashMap usage.

| Approach (collision resolution) | Lookup time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Separate chaining (linked lists) | O(1) avg, O(N) worst | O(N) | Low | Default — what Java's HashMap uses |
| Chaining with red-black trees (treeify) | O(log N) worst | O(N) | Medium | Java HashMap when a bucket exceeds 8 entries |
| Open addressing (linear probing) | O(1) avg | O(N) | Medium | Cache-friendly, no per-entry pointers |
| Cuckoo hashing | O(1) worst lookup | O(N) | High | When worst-case lookup matters |
| Robin Hood / hopscotch | O(1) | O(N) | High | Specialized: low variance, predictable latency |

| Approach (two-sum) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Brute force | O(N²) | O(1) | N ≤ 10³ |
| Sort + two pointers | O(N log N) | O(1) extra | When you can mutate input and want low memory |
| HashMap of complements | O(N) | O(N) | Default |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Overriding `equals` without overriding `hashCode`** — two objects "equal" by your definition land in different buckets, so the HashMap silently treats them as distinct. Override both, always.
- **Using a mutable object as a HashMap key and mutating it** — once its hash changes, you can't find it in the map again. The entry becomes orphaned. Treat keys as effectively immutable.
- **Iterating a HashMap and modifying it inside the loop** — throws `ConcurrentModificationException`. Use `iterator.remove()` or collect changes and apply afterwards.
- **Relying on `HashMap` iteration order** — it's not guaranteed across JVM versions or even runs. Use `LinkedHashMap` for insertion order, `TreeMap` for sorted order.
- **Building a "hash" with `s.charAt(0) * 31 + s.charAt(1)`** — collides absurdly often and ignores the rest of the string. Use `Objects.hash(...)` or `String.hashCode()` and trust the JDK.

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
- If you had to teach why `hashCode` must match `equals` in one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
