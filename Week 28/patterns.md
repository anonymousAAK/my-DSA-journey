# Week 28 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which game-theory pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Two players alternate taking 1, 2, or 3 stones from a pile of `n`. The player who takes the last stone wins. Decide if the first player wins for given `n`.
Pattern: ______
Why: ______

### 2. Two players play tic-tac-toe optimally. Given a position, decide whether the player to move can force a win.
Pattern: ______
Why: ______

### 3. Two players alternately remove any positive number of stones from one of `k` piles (Nim). Who wins with optimal play?
Pattern: ______
Why: ______

### 4. Given a chess endgame with at most 5 pieces, compute the game-theoretic value (win/draw/loss for white).
Pattern: ______
Why: ______

### 5. Two players alternately pick numbers from either end of an array; each wants to maximize their own sum. Compute player 1's optimal final score.
Pattern: ______
Why: ______

### 6. Given a connected acyclic game graph with terminal payoffs, compute the value at the root under optimal play.
Pattern: ______
Why: ______

### 7. Distractor: Given two players choosing items to maximize their *individual* totals from a pool (no alternation), find the partition. (Game tree?)
Pattern: ______
Why: ______

### 8. Two players alternate moves on a 6×7 connect-four board. Compute the perfect-play outcome from the empty board.
Pattern: ______
Why: ______

### 9. Three players play a turn-based game with arbitrary payoffs. Compute each player's optimal outcome.
Pattern: ______
Why: ______

### 10. Given several independent subgames each with known Sprague–Grundy values, decide the winner of the combined game.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Misère/Nim-style mod-4 analysis. **Why**: losing positions are n ≡ 0 (mod 4).
2. **Pattern**: Minimax on a small game tree. **Why**: ≤ 9 squares makes full exploration trivial.
3. **Pattern**: Nim — XOR of pile sizes. **Why**: first player wins iff XOR ≠ 0 (Sprague–Grundy on single pile = pile size).
4. **Pattern**: Endgame tablebase (retrograde analysis). **Why**: precompute backwards from terminal positions.
5. **Pattern**: Minimax DP on interval. **Why**: `dp[i][j]` = best diff current player can achieve on `a[i..j]`.
6. **Pattern**: Backward induction on DAG. **Why**: topologically process, propagating max-of-children for mover and min for opponent.
7. **Pattern**: Distractor — not a zero-sum sequential game. **Why**: standard combinatorial game theory doesn't apply; treat as optimization/assignment.
8. **Pattern**: Minimax with alpha-beta pruning + transposition table. **Why**: state space too big for brute force; pruning critical.
9. **Pattern**: Multi-player maxn algorithm. **Why**: minimax generalizes to "max your own component of the payoff tuple at your turn".
10. **Pattern**: Sprague–Grundy theorem — XOR of sub-game nimbers. **Why**: composite impartial game = single Nim pile with XORed value.

</details>
