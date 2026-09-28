# Weekly Digest — 2026-09-28 (ISO 2026-W40)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**How Google Maps Uses Dijkstra (and Why They Also Use Bidirectional A*)**

You open Maps, type an address, and the app gives you a 47-minute route across a continent in under a second. The road network of the United States alone has ~50 million intersections and ~150 million road segments. Computing the *shortest* path through that graph naively is a textbook Dijkstra problem — but textbook Dijkstra on 50M nodes is hundreds of milliseconds at best, and that's per query, with one CPU core, assuming the graph is in RAM. Maps serves billions of queries a day. The math doesn't work.

Read it in full: [`case_studies/real_world/01_google_maps_dijkstra.md`](case_studies/real_world/01_google_maps_dijkstra.md)

## Pattern drill
_From Week 21 (drill #1)._

> Given an array of n ≤ 10^5 integers and up to 10^5 queries each asking the sum of `a[l..r]`, with point updates `a[i] = v` interspersed, answer each operation in O(log n).

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 21/patterns.md`](Week 21/patterns.md)

## Hard-mode challenge
### Challenge 1 (Week 21): Segment Tree With Lazy Propagation (Range Add, Range Sum)

**Spec**:
Build a segment tree over an array of size `n`. Support two operations in O(log n):
- `update l r v`: add `v` to every element in `[l, r]`.
- `query l r`: return the sum of `[l, r]`.

Use lazy propagation: a `lazy[v]` array holds pending updates to push down on traversal.

**Constraints**:
- `1 <= n, q <= 10^5`, values in `[-10^9, 10^9]`
- Time: O(log n) per op
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 21/challenges.md`](Week 21/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
