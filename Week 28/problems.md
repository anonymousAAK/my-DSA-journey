# Week 28 — Practice Problems

Topics covered this week: game theory, minimax, Nim/Sprague-Grundy, optimal play DP, win/lose state analysis.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Nim Game | Easy | Nim parity | https://leetcode.com/problems/nim-game/ |
| 2 | Stone Game | Medium | Minimax DP | https://leetcode.com/problems/stone-game/ |
| 3 | Stone Game II | Medium | DP with state | https://leetcode.com/problems/stone-game-ii/ |
| 4 | Stone Game III | Hard | DP with three choices | https://leetcode.com/problems/stone-game-iii/ |
| 5 | Stone Game IV | Hard | DP from base wins | https://leetcode.com/problems/stone-game-iv/ |
| 6 | Predict the Winner | Medium | Interval minimax DP | https://leetcode.com/problems/predict-the-winner/ |
| 7 | Can I Win | Medium | Bitmask + memo | https://leetcode.com/problems/can-i-win/ |
| 8 | Divisor Game | Easy | Parity / DP | https://leetcode.com/problems/divisor-game/ |
| 9 | Cat and Mouse | Hard | Multi-state game DP | https://leetcode.com/problems/cat-and-mouse/ |
| 10 | Flip Game II | Medium | Recursive minimax | https://leetcode.com/problems/flip-game-ii/ |
| 11 | Guess Number Higher or Lower II | Medium | Minimax DP | https://leetcode.com/problems/guess-number-higher-or-lower-ii/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Stone Game VII](https://leetcode.com/problems/stone-game-vii/) — interval DP with score difference.
- [Stone Game VIII](https://leetcode.com/problems/stone-game-viii/) — clever prefix-sum DP.
- [Minimum Number of Moves to Make Palindrome](https://leetcode.com/problems/minimum-number-of-moves-to-make-palindrome/) — adversarial-ish two-pointer.

## Patterns to Master This Week

- Minimax DP: `dp[state]` = best outcome assuming optimal play; alternate max/min levels. Pitfall: track whose turn it is.
- Score-difference trick: define DP as `max(current player score − opponent score)` to drop the turn parameter. Pitfall: signs flip on recursion.
- Sprague-Grundy / Nim XOR: combine independent games via XOR of Grundy values. Pitfall: applicable only to impartial games.
