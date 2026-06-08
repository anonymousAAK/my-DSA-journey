# Weekly Digest — 2026-06-08 (ISO 2026-W24)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**How Priority Queues Power a Real-Time Feed**

When you open Twitter (or any timeline-based social app — Mastodon, Bluesky, Instagram), you see a stream of posts ordered by some notion of "what's most relevant or recent." For a single user that's a manageable computation. For *every* user, where each follows hundreds or thousands of others, where new posts arrive at ~thousands per second globally — naively recomputing each feed on each page load is impossible.

Read it in full: [`case_studies/real_world/05_twitter_feed_heap.md`](case_studies/real_world/05_twitter_feed_heap.md)

## Pattern drill
_From Week 5 (drill #5)._

> Compute `gcd(a, b)` for positive integers a, b ≤ 10^9.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 5/patterns.md`](Week 5/patterns.md)

## Hard-mode challenge
### Challenge 2 (Week 5): Mutual Recursion: Hofstadter Female/Male

**Spec**:
Implement Hofstadter's mutually recursive sequences:
- `F(0) = 1`, `M(0) = 0`
- `F(n) = n - M(F(n-1))` for `n > 0`
- `M(n) = n - F(M(n-1))` for `n > 0`

Read `n` and print `F(n)` and `M(n)` on one line, space-separated. Implement naively first to feel the recursion blow up, then add memoization. Compare wall-clock times in your journal.

**Constraints**:
- Input size: `0 <= n <= 10000` (memoized) / `0 <= n <= 30` (naive)
- Time (memoized): O(n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output (F M) |
|

Full spec: [`Week 5/challenges.md`](Week 5/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
