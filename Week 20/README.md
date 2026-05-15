# Week 20

> Self-check: `./scripts/journey quiz 20` — run the mastery checkpoints for this week.

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | Backtracking | `java/1.Backtracking.java` | `python/1.Backtracking.py` | `cpp/1.Backtracking.cpp` | `rust/s01_Backtracking.rs` | `web/1.Backtracking.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Backtracking | — | `python/backtracking.py` | `cpp/backtracking.cpp` | `rust/backtracking.rs` | — |
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

- **1. Backtracking**

## Tradeoff Matrix

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

## Anti-patterns to avoid

- **Forgetting to undo the change after the recursive call** — backtracking *requires* you to restore state so the caller sees the original input. Mutating without undoing turns a search tree into spaghetti.
- **Adding `new ArrayList<>(current)` to the result on every leaf** — correct, but if you forget the copy and add `current` directly, all your results point to the same (final, empty) list. Copy the snapshot.
- **Pruning incorrectly so you miss valid solutions** — pruning must be a *necessary* condition for failure. "It probably won't work" is not enough; the proof has to be airtight.
- **Building the board as `String` and concatenating** — turns each push into an allocation. Use `char[][]` and mutate in place, undoing on backtrack.
- **Choosing the next variable arbitrarily** — for Sudoku-like problems, picking the most-constrained cell (MRV heuristic) reduces the search space by orders of magnitude. Picking row-major order is naive but acceptable for learning.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach "choose / explore / un-choose" to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
