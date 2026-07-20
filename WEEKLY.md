# Weekly Digest — 2026-07-20 (ISO 2026-W30)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**How Ranking Interacts with Sorting + Priority Queues**

Facebook's News Feed ranks thousands of candidate posts per user per visit. Each user has hundreds of friends, follows hundreds of pages, may be in dozens of groups. For each session, the feed serves the "best" ~30 posts. The candidate set per user is in the low thousands; the ranking is done by an ML model that scores each candidate with a relevance prediction. Then we sort and emit the top 30. All within ~100ms of you opening the app.

Read it in full: [`case_studies/real_world/07_facebook_news_feed_ranking.md`](case_studies/real_world/07_facebook_news_feed_ranking.md)

## Pattern drill
_From Week 11 (drill #1)._

> Given the head of a singly linked list of up to 10^5 nodes, detect whether it contains a cycle. O(1) extra space.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 11/patterns.md`](Week 11/patterns.md)

## Hard-mode challenge
### Challenge 3 (Week 11): LRU Cache From Scratch (No Library Containers)

**Spec**:
Implement an LRU cache with capacity `C`. Operations: `put(key, value)` and `get(key)` (returns `-1` if absent). Each op must be O(1) amortized. You may not use a hashmap-of-doubly-linked-list-from-the-standard-library — build the doubly linked list yourself, and you may use only a *plain* hashmap (with no LRU semantics).

Read a sequence of operations from stdin and print the output of each `get`.

**Constraints**:
- `1 <= C <= 10^5`
- Up to `10^6` ops
- Time: O(1) per op
- Memory: O(C)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 11/challenges.md`](Week 11/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
