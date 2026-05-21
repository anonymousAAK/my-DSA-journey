# Week 20 — Backtracking

> Self-check: `./scripts/journey quiz 20`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/1.Backtracking.py`](python/1.Backtracking.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_20/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify n_queens_count workbook/week_20/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 20`

If you got stuck: open [`python/1.Backtracking.py`](python/1.Backtracking.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Backtracking**. You'll touch: Backtracking. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Capstone: [`capstones/phase_4_maze_solver.md`](../capstones/phase_4_maze_solver.md) | Phase 4 capstone — apply what you learned in weeks 16-20 |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | Backtracking | `java/1.Backtracking.java` | `python/1.Backtracking.py` | `cpp/1.Backtracking.cpp` | `rust/s01_Backtracking.rs` | `web/1.Backtracking.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Backtracking | — | `python/backtracking.py` | `cpp/backtracking.cpp` | `rust/backtracking.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. Backtracking**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Backtracking (N-Queens, permutations, subsets, Sudoku).

| Approach (N-Queens) | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Brute force all placements | O(Nⁿ) | O(N) | Low | N ≤ 4 |
| Permutations of columns | O(N!) | O(N) | Medium | Removes one type of conflict for free |
| Backtracking + diagonal/column sets | O(N!) but pruned heavily | O(N) | Medium | Default; solves N=20 in seconds |
| Bitmask backtracking | O(N!) pruned | O(N) | Medium | Same asymptotics, much faster constants |
| Branch and bound with constraint propagation | varies | varies | High | Solving Sudoku / ASP-style problems |

| Approach (subsets) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Recursion (include/exclude) | O(2ⁿ · n) | O(n) | Default |
| Iterative bitmask enumeration | O(2ⁿ · n) | O(1) extra | Branch-free, easy to parallelize |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Forgetting to undo the change after the recursive call** — backtracking *requires* you to restore state so the caller sees the original input. Mutating without undoing turns a search tree into spaghetti.
- **Adding `new ArrayList<>(current)` to the result on every leaf** — correct, but if you forget the copy and add `current` directly, all your results point to the same (final, empty) list. Copy the snapshot.
- **Pruning incorrectly so you miss valid solutions** — pruning must be a *necessary* condition for failure. "It probably won't work" is not enough; the proof has to be airtight.
- **Building the board as `String` and concatenating** — turns each push into an allocation. Use `char[][]` and mutate in place, undoing on backtrack.
- **Choosing the next variable arbitrarily** — for Sudoku-like problems, picking the most-constrained cell (MRV heuristic) reduces the search space by orders of magnitude. Picking row-major order is naive but acceptable for learning.

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
- If you had to teach "choose / explore / un-choose" to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
