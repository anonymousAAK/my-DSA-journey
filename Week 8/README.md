# Week 8 — Searching Algorithms

> Self-check: `./scripts/journey quiz 8`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/1.binary_search.py`](python/1.binary_search.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_08/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify binary_search workbook/week_08/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 8`

If you got stuck: open [`python/1.binary_search.py`](python/1.binary_search.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Searching Algorithms**. You'll touch: BinarySearch, BinarySearchOnAnswer. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Visualization: [`viz/binary_search.html`](../viz/binary_search.html) | You want to SEE the search bounds collapse step by step |
| Mock interview: [`mock_interviews/01_two_sum_warm_up.md`](../mock_interviews/01_two_sum_warm_up.md) | Searching/array problems discussed conversationally |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | BinarySearch | `java/1.BinarySearch.java` | `python/1.binary_search.py` | `cpp/1.binary_search.cpp` | `rust/s01_binary_search.rs` | `web/1.binary_search.html` |
| 2 | BinarySearchOnAnswer | `java/2.BinarySearchOnAnswer.java` | `python/2.binary_search_on_answer.py` | `cpp/2.binary_search_on_answer.cpp` | `rust/s02_binary_search_on_answer.rs` | `web/2.binary_search_on_answer.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Searching | — | `python/searching.py` | `cpp/searching.cpp` | `rust/searching.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. BinarySearch**
- **2. BinarySearchOnAnswer**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Binary Search (plain and on the answer).

| Approach | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Linear scan | O(N) | O(1) | Low | N ≤ 10³, or unsorted data |
| Standard binary search | O(log N) | O(1) | Low | Sorted array, find exact match |
| Lower / upper bound (search-for-boundary) | O(log N) | O(1) | Medium | Find first/last position of a value or first index satisfying a predicate |
| Binary search on answer | O(log(range) · check) | O(1) | Medium | Monotonic-feasibility problems (capacity, min/max threshold) |
| Exponential / galloping search | O(log N) | O(1) | Medium | Unbounded arrays, or when the target is near the front |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **`mid = (lo + hi) / 2` overflow** — for large `int` values `lo + hi` overflows. Use `lo + (hi - lo) / 2` instead. Trips you up exactly when the input is large enough to matter.
- **Mixing `lo <= hi` with `hi = mid` updates** — those two patterns lead to infinite loops. Choose one invariant and stick: either inclusive bounds with `mid ± 1` updates, or half-open with `hi = mid`.
- **Binary searching on unsorted data** — the precondition is non-negotiable. If your data isn't sorted on the key you're searching, binary search returns nonsense without erroring.
- **Forgetting to verify "answer is monotonic" before binary-searching on answer** — the predicate must be monotone (all `false`s then all `true`s). If it isn't, you're using binary search on a non-bisectable function and the result is undefined.
- **Returning `mid` immediately when finding the *first* occurrence** — for first/last occurrence you must keep searching the relevant half even after a hit. Returning early gives "an" occurrence, not "the first" one.

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
- If you had to teach "binary search on the answer" to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
