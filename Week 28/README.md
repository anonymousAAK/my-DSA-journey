# Week 28

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | alpha beta | `java/alpha_beta.java` | `python/alpha_beta.py` | `cpp/alpha_beta.cpp` | `rust/alpha_beta.rs` | `web/alpha_beta.html` |
| 2 | game theory | `java/game_theory.java` | `python/game_theory.py` | `cpp/game_theory.cpp` | `rust/game_theory.rs` | — |
| 3 | minimax | `java/minimax.java` | `python/minimax.py` | `cpp/minimax.cpp` | `rust/minimax.rs` | `web/minimax.html` |
| 4 | nim | `java/nim.java` | `python/nim.py` | `cpp/nim.cpp` | `rust/nim.rs` | `web/nim.html` |
| 5 | sprague grundy | `java/sprague_grundy.java` | `python/sprague_grundy.py` | `cpp/sprague_grundy.cpp` | `rust/sprague_grundy.rs` | `web/sprague_grundy.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
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

- **1. alpha beta**
- **2. game theory**
- **3. minimax**
- **4. nim**
- **5. sprague grundy**

## Tradeoff Matrix

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

## Anti-patterns to avoid

- **Alpha–beta with `alpha` and `beta` swapped on the recursive call** — must call as `(-beta, -alpha)` in negamax form, or pass the right windows in classic form. Swapping them silently turns pruning off (best case) or returns wrong values (worst case).
- **Move ordering by insertion order** — the speedup from alpha–beta hinges on examining best moves first. Sort by a cheap heuristic (captures first, transposition-table hint) or you'll get worst-case `b^d`.
- **Computing Grundy values by `XOR`-ing children directly** — the Grundy value of a position is `mex` (minimum excludant) of its children's Grundy values, not their XOR. XOR is for combining independent subgames in a sum.
- **Forgetting the game must be *impartial* before applying Sprague–Grundy** — chess, checkers, and any game where the two players have different move sets are *partisan*. Sprague–Grundy doesn't apply; you need surreal numbers or game-specific analysis.
- **Treating "the player to move wins iff Nim-sum ≠ 0"** as universal — that's the rule for *normal play* (last move wins). For *misère* play (last move loses), the rule is more subtle and only matches when all piles have size ≤ 1.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach the Nim-sum result to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
