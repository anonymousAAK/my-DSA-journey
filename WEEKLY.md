# Weekly Digest — 2026-10-26 (ISO 2026-W44)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**How Priority Queues Power a Real-Time Feed**

When you open Twitter (or any timeline-based social app — Mastodon, Bluesky, Instagram), you see a stream of posts ordered by some notion of "what's most relevant or recent." For a single user that's a manageable computation. For *every* user, where each follows hundreds or thousands of others, where new posts arrive at ~thousands per second globally — naively recomputing each feed on each page load is impossible.

Read it in full: [`case_studies/real_world/05_twitter_feed_heap.md`](case_studies/real_world/05_twitter_feed_heap.md)

## Pattern drill
_From Week 25 (drill #5)._

> Given two strings of equal length n, decide whether one is a rotation of the other in O(n).

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 25/patterns.md`](Week 25/patterns.md)

## Hard-mode challenge
### Challenge 5 (Week 25): Palindromic Tree (Eertree)

**Spec**:
Build the palindromic tree for string `s` and output:
- The number of distinct palindromic substrings of `s`.
- The longest palindromic substring.
- For each position `i`, the number of palindromes ending at `i`.

Eertree construction: each node represents a distinct palindrome; suffix links point to the longest proper palindromic suffix.

**Constraints**:
- `1 <= |s| <= 10^6`
- Time: O(n * alphabet) or O(n log alphabet)
- Memory: O(n)

**Test inputs**:
| Input | Distinct palindromic substrings | Longest |
|

Full spec: [`Week 25/challenges.md`](Week 25/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
