# Weekly Digest — 2026-10-12 (ISO 2026-W42)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**Why Your CDN Uses Consistent Hashing (and What Happens Without It)**

A content delivery network has a fleet of edge servers around the world — let's say 10,000 of them — and a catalog of cacheable objects (images, JS bundles, video chunks): billions of them. When a request comes in for object `cat.jpg`, you need to pick *which* edge server caches it. The same object should land on the same cache every time (so cache hits work). When you add or remove edge servers (which happens constantly — autoscaling, failures, rolling deploys), the mapping can't change for *most* objects, or you'd invalidate the entire cache and the origin servers would melt under the traffic spike.

Read it in full: [`case_studies/real_world/03_cdn_consistent_hashing.md`](case_studies/real_world/03_cdn_consistent_hashing.md)

## Pattern drill
_From Week 23 (drill #3)._

> Count the integers in `[L, R]` (up to 10^18) whose decimal digit sum is divisible by 7.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 23/patterns.md`](Week 23/patterns.md)

## Hard-mode challenge
### Challenge 3 (Week 23): SOS DP — Sum Over Subsets

**Spec**:
Read `n` and `2^n` values `f(S)` indexed by subset `S` of `[0..n-1]`. Compute `g(S) = sum over T subset of S of f(T)`. Required: O(n * 2^n) using the SOS DP recurrence (iterate over each bit; for each subset that includes the bit, add the value at the subset with that bit removed).

**Constraints**:
- `1 <= n <= 20`
- Time: O(n * 2^n)
- Memory: O(2^n)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 23/challenges.md`](Week 23/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
