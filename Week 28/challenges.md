# Week 28 — Hard Mode Challenges (Boss Level)

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Game Solver With Memoized Minimax (Tic-Tac-Toe Variant)

**Spec**:
Implement a perfect Tic-Tac-Toe player on a 4x4 board with the rule "first to make 4 in a row wins". Use minimax with memoization over a canonical state hash (the board encoded in base-3). Print the value of the initial position (`WIN`, `LOSS`, or `DRAW`) and one optimal first move for X.

**Constraints**:
- 4x4 board, branching ~16
- Time: must terminate within a few seconds (state space is large; symmetry reduction helps)
- Memory: hashmap of states

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| empty 4x4 board | likely `DRAW` (verify) |
| 3x3 standard Tic-Tac-Toe (sanity check) | `DRAW` |
| board with X having a winning move next | `WIN` and the move |

**Stretch**: Use symmetry (rotations + reflections, 8-fold) to shrink the state space by ~8x; canonicalize each state before hashing.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Alpha–Beta Pruning on Connect-Four

**Spec**:
Implement a Connect-Four bot for the standard 7-wide, 6-tall board. Use iterative deepening with alpha–beta pruning and a transposition table. Move ordering: try center columns first.

Required interface: read a board state (rows top-down, dots for empty, X/O for pieces, then a single char indicating whose turn) and print the bot's chosen column (0–6) along with the search depth reached.

**Constraints**:
- Time budget per move: 2 seconds (tune depth accordingly)
- Memory: ~100MB transposition table acceptable

**Test inputs**:
| Input | Expected behavior |
|-------|-------------------|
| empty board, X to move | center column (`3`) |
| board with immediate 3-in-a-row for X | X plays the winning column |
| board with immediate 3-in-a-row for O | X blocks |

**Stretch**: Add bitboard representation (two 64-bit integers per player) for O(1) win detection.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Sprague–Grundy on a Custom Nim Variant

**Spec**:
"Staircase Nim": there are `n` piles indexed `1..n`. A move: pick a pile `i >= 1` and move some positive number of stones from pile `i` to pile `i-1` (stones moved to pile 0 are removed). Last player to move wins. Determine the winner from a given starting configuration.

Required: prove (in journal) that the Grundy value of the game is XOR of pile sizes at **odd-indexed** piles only. Then implement.

**Constraints**:
- `1 <= n <= 10^5`, pile sizes up to `10^9`
- Time: O(n)
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=3 piles=[3, 2, 5]` | first player wins (XOR of odd-index piles: 3 XOR 5 = 6 != 0) |
| `n=2 piles=[4, 4]` | first player wins (XOR = 4) |
| `n=4 piles=[3, 5, 3, 5]` | XOR of indices 1,3 = 3 XOR 3 = 0 — second player wins |
| `n=1 piles=[0]` | second player wins |

**Stretch**: Implement a full game-tree search to verify Grundy values for `n <= 4`, small piles.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Stone Game DP (LC 1140-Style)

**Spec**:
A row of `n` piles of stones (positive integers). Two players alternate; on each turn, a player takes 1 or 2 piles from the **left** end. Both play optimally to maximize their own total. Print the first player's score.

Required: DP with state `(i, lastMove)` where `i` is the current left end and `lastMove` records constraints (or use a simpler `dp[i]` = best score for the player to move on `a[i..n-1]`).

**Constraints**:
- `1 <= n <= 10^4`, values up to `10^4`
- Time: O(n^2) (or O(n) for the simpler variant)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=4 / 2 7 9 4 4` | first player score = 10 |
| `n=1 / 5` | `5` |
| `n=2 / 1 2` | `3` (take both) |
| `n=5 / 1 100 1 1 100` | depends on optimal play — verify by brute force |

**Stretch**: Now players take from either end (LC 877) — different recursion with `(i, j)` state.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: Wythoff's Game

**Spec**:
Two piles of stones. Moves: remove any positive number from one pile, OR remove the same positive number from both piles. Last to move wins. Given `(a, b)` print which player wins.

Required: derive and implement the closed-form solution using the golden ratio `φ`: `(a, b)` with `a <= b` is a P-position iff `a = floor(k * φ)` and `b = floor(k * φ^2)` for some `k`. Use rational arithmetic or careful float to avoid edge errors.

**Constraints**:
- `0 <= a, b <= 10^9`
- Time: O(1)
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `(0, 0)` | second player (P-position) |
| `(1, 2)` | second player (P-position; k=1) |
| `(3, 5)` | second player (P-position; k=2) |
| `(2, 2)` | first player (N-position) |
| `(4, 7)` | second player (k=3) |

**Stretch**: Verify your closed-form answer against a brute-force Grundy computation for `a, b <= 30`.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
