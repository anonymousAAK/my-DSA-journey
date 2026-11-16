# Weekly Digest — 2026-11-16 (ISO 2026-W47)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**LRU vs LFU vs ARC in Redis**

Redis is an in-memory data store, often used as a cache in front of slower databases. A user configures Redis with a max memory cap. When that cap is hit and a new write arrives, Redis must **evict** something. The choice of *what* to evict is shockingly impactful: a wrong policy can collapse cache hit rate from 90% to 40% and double your database load. The eviction policy is also one of the most well-studied algorithmic problems in computer systems — it's essentially the page replacement problem, which was the subject of OS research literature for decades.

Read it in full: [`case_studies/real_world/08_lru_in_redis.md`](case_studies/real_world/08_lru_in_redis.md)

## Pattern drill
_From Week 28 (drill #8)._

> Two players alternate moves on a 6×7 connect-four board. Compute the perfect-play outcome from the empty board.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 28/patterns.md`](Week 28/patterns.md)

## Hard-mode challenge
### Challenge 3 (Week 28): Sprague–Grundy on a Custom Nim Variant

**Spec**:
"Staircase Nim": there are `n` piles indexed `1..n`. A move: pick a pile `i >= 1` and move some positive number of stones from pile `i` to pile `i-1` (stones moved to pile 0 are removed). Last player to move wins. Determine the winner from a given starting configuration.

Required: prove (in journal) that the Grundy value of the game is XOR of pile sizes at **odd-indexed** piles only. Then implement.

**Constraints**:
- `1 <= n <= 10^5`, pile sizes up to `10^9`
- Time: O(n)
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 28/challenges.md`](Week 28/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
