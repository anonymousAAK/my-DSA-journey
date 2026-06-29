# Weekly Digest — 2026-06-29 (ISO 2026-W27)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**LRU vs LFU vs ARC in Redis**

Redis is an in-memory data store, often used as a cache in front of slower databases. A user configures Redis with a max memory cap. When that cap is hit and a new write arrives, Redis must **evict** something. The choice of *what* to evict is shockingly impactful: a wrong policy can collapse cache hit rate from 90% to 40% and double your database load. The eviction policy is also one of the most well-studied algorithmic problems in computer systems — it's essentially the page replacement problem, which was the subject of OS research literature for decades.

Read it in full: [`case_studies/real_world/08_lru_in_redis.md`](case_studies/real_world/08_lru_in_redis.md)

## Pattern drill
_From Week 8 (drill #8)._

> Find the integer square root of n (largest `k` with `k*k ≤ n`), n up to 10^18.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 8/patterns.md`](Week 8/patterns.md)

## Hard-mode challenge
### Challenge 4 (Week 8): Aggressive Cows / Maximum Minimum Distance

**Spec**:
Read `n`, `k`, and `n` stall positions on a number line (1D coordinates). Place `k` cows in stalls so that the **minimum** distance between any two cows is maximized. Print that maximum-min distance. Sort positions first, then binary search on the distance: for a candidate `d`, greedily place cows from left to right whenever they are at least `d` apart.

**Constraints**:
- Input size: `2 <= k <= n <= 10^5`, positions up to `10^9`
- Time: O(n log n + n log(max position))
- Memory: O(1) past sorting

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 8/challenges.md`](Week 8/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
