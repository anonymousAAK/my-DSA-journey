# Weekly Digest — 2026-07-13 (ISO 2026-W29)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**Git's Commit Graph as a DAG, Why Topological Sort Matters**

Git tracks the history of a codebase. Every commit references its parent commit(s), forming a graph. That graph is a **directed acyclic graph** — directed (commits point to their parents, time flows one way), and acyclic (you can't be your own ancestor). Almost every interesting Git operation is a graph-algorithm query on this DAG: "Is commit A an ancestor of commit B?" "What's the most recent common ancestor of these two branches?" "List all commits between these two tags in a sensible order."

Read it in full: [`case_studies/real_world/06_git_dag.md`](case_studies/real_world/06_git_dag.md)

## Pattern drill
_From Week 10 (drill #10)._

> Given an `n × n` matrix, find the saddle point if any (minimum in its row AND maximum in its column).

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 10/patterns.md`](Week 10/patterns.md)

## Hard-mode challenge
### Challenge 2 (Week 10): Set Matrix Zeroes With O(1) Extra Space

**Spec**:
Read an `m x n` matrix of integers. If a cell is 0, set its entire row and column to 0. Do it in place with O(1) extra space — you may not use a `boolean[m] + boolean[n]` (that's O(m+n)).

Hint: use the first row and first column themselves as the markers, but save two flags to remember whether the first row/column originally contained a zero.

**Constraints**:
- Input size: `1 <= m, n <= 1000`
- Time: O(m * n)
- Memory: O(1) extra

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 10/challenges.md`](Week 10/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
