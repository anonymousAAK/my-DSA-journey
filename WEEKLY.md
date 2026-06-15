# Weekly Digest — 2026-06-15 (ISO 2026-W25)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**Git's Commit Graph as a DAG, Why Topological Sort Matters**

Git tracks the history of a codebase. Every commit references its parent commit(s), forming a graph. That graph is a **directed acyclic graph** — directed (commits point to their parents, time flows one way), and acyclic (you can't be your own ancestor). Almost every interesting Git operation is a graph-algorithm query on this DAG: "Is commit A an ancestor of commit B?" "What's the most recent common ancestor of these two branches?" "List all commits between these two tags in a sensible order."

Read it in full: [`case_studies/real_world/06_git_dag.md`](case_studies/real_world/06_git_dag.md)

## Pattern drill
_From Week 6 (drill #6)._

> Given an array, move all zeros to the end, preserving the relative order of non-zero elements. In place.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 6/patterns.md`](Week 6/patterns.md)

## Hard-mode challenge
### Challenge 2 (Week 6): In-Place Multi-Block Rotation

**Spec**:
Read `n`, `k`, and `n` integers. Rotate the array left by `k` positions **in place** using O(1) extra memory. Don't use slicing into a new buffer. Required technique: three-reversal trick OR cyclic-replacement using gcd. Print the final array.

**Constraints**:
- Input size: `1 <= n <= 10^6`, `0 <= k <= 10^9`
- Time: O(n)
- Memory: O(1) auxiliary

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 6/challenges.md`](Week 6/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
