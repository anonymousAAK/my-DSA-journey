# Weekly Digest — 2026-07-06 (ISO 2026-W28)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**Token Bucket vs Sliding Window at Cloudflare/AWS**

A public API needs to throttle clients. Each client is allowed, say, 1,000 requests per minute. Above that, return HTTP 429. The naïve implementation breaks in a dozen ways at scale: clock skew between machines, bursty legitimate traffic, distributed state across thousands of front-ends, the desire to support multiple rate-limit tiers (per second, per minute, per day) on the same client. Cloudflare processes tens of millions of req/sec at edge; AWS API Gateway is similar. Their rate limiter has to be both algorithmically right and operationally fast.

Read it in full: [`case_studies/real_world/09_rate_limiting_at_scale.md`](case_studies/real_world/09_rate_limiting_at_scale.md)

## Pattern drill
_From Week 9 (drill #9)._

> Sort an array containing only 0/1 values in place, single pass, O(1) extra space.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 9/patterns.md`](Week 9/patterns.md)

## Hard-mode challenge
### Challenge 1 (Week 9): Count Inversions Using Merge Sort

**Spec**:
Read `n` and `n` integers. An inversion is a pair `(i, j)` with `i < j` and `a[i] > a[j]`. Print the total number of inversions. The brute O(n^2) solution is forbidden. Solve in O(n log n) by adapting merge sort: when merging two halves, every time you take an element from the right half before an element from the left half, the remaining elements in the left half all form inversions.

**Constraints**:
- Input size: `1 <= n <= 10^6`, values in `[-10^9, 10^9]`
- Time: O(n log n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 9/challenges.md`](Week 9/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
