# Weekly Digest — 2026-09-21 (ISO 2026-W39)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**real\_world**



Read it in full: [`case_studies/real_world/README.md`](case_studies/real_world/README.md)

## Pattern drill
_From Week 20 (drill #10)._

> Distractor: Given n ≤ 1000 items with weights and a knapsack capacity, find the maximum value subset. (Backtracking?)

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 20/patterns.md`](Week 20/patterns.md)

## Hard-mode challenge
### Challenge 5 (Week 20): Generate All Valid Parentheses Combinations

**Spec**:
Read `n`. Print all distinct strings of `n` pairs of matched parentheses (so length `2n`). Use backtracking constrained by two counters: `open < n` allows adding `(`; `close < open` allows adding `)`. Print in lex order.

**Constraints**:
- `0 <= n <= 12` (Catalan number explosion)
- Time: O(C_n * n) where `C_n` is the n-th Catalan number
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 20/challenges.md`](Week 20/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
