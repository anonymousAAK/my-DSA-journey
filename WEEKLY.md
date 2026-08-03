# Weekly Digest — 2026-08-03 (ISO 2026-W32)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**Token Bucket vs Sliding Window at Cloudflare/AWS**

A public API needs to throttle clients. Each client is allowed, say, 1,000 requests per minute. Above that, return HTTP 429. The naïve implementation breaks in a dozen ways at scale: clock skew between machines, bursty legitimate traffic, distributed state across thousands of front-ends, the desire to support multiple rate-limit tiers (per second, per minute, per day) on the same client. Cloudflare processes tens of millions of req/sec at edge; AWS API Gateway is similar. Their rate limiter has to be both algorithmically right and operationally fast.

Read it in full: [`case_studies/real_world/09_rate_limiting_at_scale.md`](case_studies/real_world/09_rate_limiting_at_scale.md)

## Pattern drill
_From Week 13 (drill #3)._

> Given an undirected graph with up to 10^5 nodes, find the shortest path (in edges) from node `s` to every other node.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 13/patterns.md`](Week 13/patterns.md)

## Hard-mode challenge
### Challenge 1 (Week 13): Sliding Window Maximum via Monotonic Deque

**Spec**:
Read `n`, `k`, and `n` integers. For every window of size `k`, print the maximum. Required complexity O(n) using a monotonic-decreasing deque of indices. The O(n log k) heap approach is acceptable for stretch credit only; the O(n k) brute force is forbidden.

**Constraints**:
- `1 <= k <= n <= 10^6`
- Time: O(n)
- Memory: O(k)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 13/challenges.md`](Week 13/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
