# Weekly Digest — 2026-11-09 (ISO 2026-W46)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**How Ranking Interacts with Sorting + Priority Queues**

Facebook's News Feed ranks thousands of candidate posts per user per visit. Each user has hundreds of friends, follows hundreds of pages, may be in dozens of groups. For each session, the feed serves the "best" ~30 posts. The candidate set per user is in the low thousands; the ranking is done by an ML model that scores each candidate with a relevance prediction. Then we sort and emit the top 30. All within ~100ms of you opening the app.

Read it in full: [`case_studies/real_world/07_facebook_news_feed_ranking.md`](case_studies/real_world/07_facebook_news_feed_ranking.md)

## Pattern drill
_From Week 27 (drill #7)._

> Distractor: Given n ≤ 10^5 points, find the pair with maximum Euclidean distance. (Closest-pair algorithm?)

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 27/patterns.md`](Week 27/patterns.md)

## Hard-mode challenge
### Challenge 2 (Week 27): Closest Pair of Points (Divide and Conquer)

**Spec**:
Read `n` 2D points. Print the distance between the closest pair and one such pair. Required: divide-and-conquer in O(n log n) — sort by x, recurse on halves, then check the strip of points within `δ` of the dividing line, sorted by y, with the "look at at most 7 next points" optimization. Brute O(n^2) and KD-tree solutions are forbidden.

**Constraints**:
- `2 <= n <= 10^6`
- Time: O(n log n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 27/challenges.md`](Week 27/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
