# Week 28 — Game Theory & Combinatorics

> Self-check: `./scripts/journey quiz 28`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/nim.py`](python/nim.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_28/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify nim_xor_rule workbook/week_28/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 28`

If you got stuck: open [`python/nim.py`](python/nim.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Game Theory & Combinatorics**. You'll touch: alpha beta, game theory, minimax, nim, sprague grundy. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

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
| 1 | alpha beta | `java/alpha_beta.java` | `python/alpha_beta.py` | `cpp/alpha_beta.cpp` | `rust/alpha_beta.rs` | `web/alpha_beta.html` |
| 2 | game theory | `java/game_theory.java` | `python/game_theory.py` | `cpp/game_theory.cpp` | `rust/game_theory.rs` | — |
| 3 | minimax | `java/minimax.java` | `python/minimax.py` | `cpp/minimax.cpp` | `rust/minimax.rs` | `web/minimax.html` |
| 4 | nim | `java/nim.java` | `python/nim.py` | `cpp/nim.cpp` | `rust/nim.rs` | `web/nim.html` |
| 5 | sprague grundy | `java/sprague_grundy.java` | `python/sprague_grundy.py` | `cpp/sprague_grundy.cpp` | `rust/sprague_grundy.rs` | `web/sprague_grundy.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. alpha beta**
- **2. game theory**
- **3. minimax**
- **4. nim**
- **5. sprague grundy**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Game theory and adversarial search (minimax, alpha-beta, Nim, Sprague–Grundy).

| Approach (game search) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Minimax full tree | O(b^d) | O(d) | Tiny games, sanity oracle |
| Minimax + alpha–beta pruning | O(b^(d/2)) best, O(b^d) worst | O(d) | Default for 2-player zero-sum games |
| Alpha–beta + move ordering | close to O(b^(d/2)) consistently | O(d) | Production engines |
| Iterative deepening + transposition table | O(b^(d/2)) with caching | O(states) | Time-controlled play, repeated positions |
| Monte Carlo Tree Search (UCT) | Per-iteration cheap | O(visits) | Large branching factor, no good eval function |

| Approach (impartial games) | Time | Space | When to prefer |
|----------|------|-------|----------------|
| Compute Grundy/Nim-value by full DP | O(states · transitions) | O(states) | Generic impartial games |
| Sprague–Grundy XOR over independent piles | O(N) per query | O(1) | Sum of games (Nim, staircase Nim) |
| Closed form / parity argument | O(1) | O(1) | Subtraction games with periodic Grundy sequence |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Alpha–beta with `alpha` and `beta` swapped on the recursive call** — must call as `(-beta, -alpha)` in negamax form, or pass the right windows in classic form. Swapping them silently turns pruning off (best case) or returns wrong values (worst case).
- **Move ordering by insertion order** — the speedup from alpha–beta hinges on examining best moves first. Sort by a cheap heuristic (captures first, transposition-table hint) or you'll get worst-case `b^d`.
- **Computing Grundy values by `XOR`-ing children directly** — the Grundy value of a position is `mex` (minimum excludant) of its children's Grundy values, not their XOR. XOR is for combining independent subgames in a sum.
- **Forgetting the game must be *impartial* before applying Sprague–Grundy** — chess, checkers, and any game where the two players have different move sets are *partisan*. Sprague–Grundy doesn't apply; you need surreal numbers or game-specific analysis.
- **Treating "the player to move wins iff Nim-sum ≠ 0"** as universal — that's the rule for *normal play* (last move wins). For *misère* play (last move loses), the rule is more subtle and only matches when all piles have size ≤ 1.

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
- If you had to teach the Nim-sum result to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
