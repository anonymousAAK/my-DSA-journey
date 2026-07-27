# Weekly Digest — 2026-07-27 (ISO 2026-W31)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**LRU vs LFU vs ARC in Redis**

Redis is an in-memory data store, often used as a cache in front of slower databases. A user configures Redis with a max memory cap. When that cap is hit and a new write arrives, Redis must **evict** something. The choice of *what* to evict is shockingly impactful: a wrong policy can collapse cache hit rate from 90% to 40% and double your database load. The eviction policy is also one of the most well-studied algorithmic problems in computer systems — it's essentially the page replacement problem, which was the subject of OS research literature for decades.

Read it in full: [`case_studies/real_world/08_lru_in_redis.md`](case_studies/real_world/08_lru_in_redis.md)

## Pattern drill
_From Week 12 (drill #2)._

> Evaluate a postfix arithmetic expression with tokens `+ - * /` and integer operands. Length up to 10^5.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 12/patterns.md`](Week 12/patterns.md)

## Hard-mode challenge
### Challenge 4 (Week 12): Next Greater Element — Circular Array Variant

**Spec**:
Read `n` and `n` integers viewed as a **circular** array (after the last element comes the first). For each index `i`, find the next greater element when scanning forward (with wrap-around). If none exists, output `-1`. Required complexity O(n) using a monotonic stack on a "doubled" iteration of indices.

**Constraints**:
- `1 <= n <= 10^6`, values in `[-10^9, 10^9]`
- Time: O(n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 12/challenges.md`](Week 12/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
