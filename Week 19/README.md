# Week 19 — Greedy Algorithms

> Self-check: `./scripts/journey quiz 19`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/1.GreedyAlgorithms.py`](python/1.GreedyAlgorithms.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_19/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify activity_selection_sort workbook/week_19/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 19`

If you got stuck: open [`python/1.GreedyAlgorithms.py`](python/1.GreedyAlgorithms.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Greedy Algorithms**. You'll touch: GreedyAlgorithms. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Mock interview: [`mock_interviews/02_meeting_rooms_intervals.md`](../mock_interviews/02_meeting_rooms_intervals.md) | Greedy / interval problems in a conversation |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | GreedyAlgorithms | `java/1.GreedyAlgorithms.java` | `python/1.GreedyAlgorithms.py` | `cpp/1.GreedyAlgorithms.cpp` | `rust/s01_GreedyAlgorithms.rs` | `web/1.GreedyAlgorithms.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Greedy | — | `python/greedy.py` | `cpp/greedy.cpp` | `rust/greedy.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. GreedyAlgorithms**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Greedy algorithms (activity selection, fractional knapsack, Huffman).

| Approach (interval scheduling) | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Brute force enumerate subsets | O(2ⁿ) | O(n) | Low | n ≤ 20, oracle for correctness |
| DP on sorted intervals | O(N log N) | O(N) | Medium | Weighted interval scheduling |
| Greedy by earliest finish time | O(N log N) | O(1) extra | Low | Unweighted activity selection — provably optimal |
| Greedy by earliest start time | O(N log N) | O(1) | Low | **Wrong** for activity selection — counterexample exists |

| Approach (knapsack) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Greedy by value/weight ratio | O(N log N) | O(1) | Fractional knapsack — optimal |
| Greedy by ratio (0/1 version) | O(N log N) | O(1) | **Heuristic only** — can be arbitrarily bad |
| DP | O(N·W) | O(W) | 0/1 knapsack — correct |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Reaching for greedy because the problem "feels easy"** — greedy is correct only when the problem has the *exchange* / *matroid* property. Always sketch a counterexample attempt before committing.
- **Sorting by the wrong key** — interval scheduling needs finish time, not start time or duration. The choice of key is the entire algorithm; getting it wrong yields a plausible-looking algorithm that fails on adversarial inputs.
- **Confusing greedy correctness with greedy efficiency** — even a correct greedy strategy needs O(N log N) sorting; calling a method "greedy" doesn't make it O(N).
- **Mixing fractional and 0/1 knapsack** — fractional admits the ratio-greedy proof; 0/1 does not. Items 0/1 with `(w=1, v=2), (w=2, v=3), (w=3, v=4)` and capacity 4 is the classic counterexample.
- **Forgetting tie-breaking** — when two intervals have the same finish time, the greedy can still be correct but the *count of distinct optimal solutions* may not be. Make tie-breaking deterministic if reproducibility matters.

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
- If you had to teach the "earliest finish time" proof in one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
