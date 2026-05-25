# Weekly Digest — 2026-05-25 (ISO 2026-W22)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**Why Your CDN Uses Consistent Hashing (and What Happens Without It)**

A content delivery network has a fleet of edge servers around the world — let's say 10,000 of them — and a catalog of cacheable objects (images, JS bundles, video chunks): billions of them. When a request comes in for object `cat.jpg`, you need to pick *which* edge server caches it. The same object should land on the same cache every time (so cache hits work). When you add or remove edge servers (which happens constantly — autoscaling, failures, rolling deploys), the mapping can't change for *most* objects, or you'd invalidate the entire cache and the origin servers would melt under the traffic spike.

Read it in full: [`case_studies/real_world/03_cdn_consistent_hashing.md`](case_studies/real_world/03_cdn_consistent_hashing.md)

## Pattern drill
_From Week 3 (drill #3)._

> Given an integer `n`, determine whether it is a power of two. n fits in 32 bits.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 3/patterns.md`](Week 3/patterns.md)

## Hard-mode challenge
### Challenge 3 (Week 3): Generalized Fibonacci (Pisano Period)

**Spec**:
Read two non-negative integers `n` and `m`. Print the `n`-th Fibonacci number modulo `m`. `n` can be astronomically large, so you may not iterate `n` times; exploit the **Pisano period**: the sequence `F(i) mod m` is periodic with some period `π(m)`. Find `π(m)` by iterating until you see the pair `(0, 1)` repeat, then reduce `n mod π(m)` and print `F(n mod π(m)) mod m`.

**Constraints**:
- Input size: `n` up to `10^18`, `m` up to `10^4`
- Time: O(π(m)), which is at most ~6m
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 3/challenges.md`](Week 3/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
