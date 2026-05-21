# Week 18 — Dynamic Programming

> Self-check: `./scripts/journey quiz 18`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/1.DynamicProgramming.py`](python/1.DynamicProgramming.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_18/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify coin_change workbook/week_18/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 18`

If you got stuck: open [`python/1.DynamicProgramming.py`](python/1.DynamicProgramming.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Dynamic Programming**. You'll touch: DynamicProgramming. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Visualization: [`viz/dp_table.html`](../viz/dp_table.html) | You want to SEE the DP table fill in |
| Mock interview: [`mock_interviews/05_dp_house_robber_iii.md`](../mock_interviews/05_dp_house_robber_iii.md) | DP problems discussed conversationally |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | DynamicProgramming | `java/1.DynamicProgramming.java` | `python/1.DynamicProgramming.py` | `cpp/1.DynamicProgramming.cpp` | `rust/s01_DynamicProgramming.rs` | `web/1.DynamicProgramming.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Dynamic Programming | — | `python/dynamic_programming.py` | `cpp/dynamic_programming.cpp` | `rust/dynamic_programming.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. DynamicProgramming**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Dynamic Programming (0/1 knapsack, LIS, edit distance, coin change).

| Approach | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Plain recursion | O(branches^depth) | O(depth) | Low | Sanity oracle, very small inputs |
| Memoized recursion (top-down) | O(states · transition) | O(states + depth) | Medium | When state space is sparse or hard to enumerate |
| Tabulation (bottom-up) | O(states · transition) | O(states) | Medium | When you need the full table, or to drop a dimension later |
| Tabulation + rolling array | O(states · transition) | O(slice) | High | When memory is the bottleneck and you only need O(1) previous rows |
| Closed form / math | O(1) or O(log N) | O(1) | Varies | Problems with a known formula (e.g. Catalan) |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Memoizing on a mutable state object** — if the memo key changes after lookup, you'll get cross-talk between unrelated states. Use immutable keys (tuples, encoded ints).
- **Confusing 0/1 knapsack and unbounded knapsack** — the iteration order of the inner loop differs. For 0/1, iterate capacity *descending*; for unbounded, iterate *ascending*. Reversing the wrong one silently gives the wrong answer.
- **Initializing the DP table to 0 when the identity element is `+∞` or `-∞`** — for "minimum" problems, 0 looks like a valid (and very good) answer. Initialize to `Integer.MAX_VALUE` / `MIN_VALUE` and handle saturation.
- **Computing LIS in O(N²) when you need O(N log N)** — the longest-increasing-subsequence with patience-sort + binary search is the standard interview expectation. The O(N²) DP is fine pedagogically but won't pass tight constraints.
- **Forgetting space optimization erases earlier states you'll still need** — rolling-array DP requires checking your transition only reads from the previous row(s). If it reads further back, you can't roll.

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
- If you had to teach the 0/1 knapsack recurrence to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
