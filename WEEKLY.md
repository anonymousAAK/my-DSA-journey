# Weekly Digest — 2026-08-17 (ISO 2026-W34)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**B-trees vs LSM Trees vs Hash Indexes**

A relational database needs to find rows fast. The table might have a billion rows; finding by primary key needs to be sub-millisecond. The database also needs to insert, update, and delete rows, *and* support range queries (`WHERE created_at BETWEEN ? AND ?`). All this while the data lives on disk — far slower than RAM — and while concurrent transactions are mutating things.

Read it in full: [`case_studies/real_world/11_database_indexes_btree.md`](case_studies/real_world/11_database_indexes_btree.md)

## Pattern drill
_From Week 15 (drill #5)._

> Given an array of CPU tasks with cooldown constraints (same task needs ≥ n idle time between consecutive runs), return the minimum total time. Up to 10^4 tasks.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 15/patterns.md`](Week 15/patterns.md)

## Hard-mode challenge
### Challenge 3 (Week 15): K-th Largest Element With Constant-Memory Online Selection

**Spec**:
Process a stream and, after every insert, print the `k`-th largest value seen so far (or `-1` if fewer than `k` values). Required: O(log k) per insert, O(k) memory. Technique: a min-heap of size `k` — the heap's root is the k-th largest.

**Constraints**:
- `1 <= k <= 10^5`, stream up to `10^7`
- Time: O(log k) per insert
- Memory: O(k)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 15/challenges.md`](Week 15/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
