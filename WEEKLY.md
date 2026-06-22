# Weekly Digest — 2026-06-22 (ISO 2026-W26)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**How Ranking Interacts with Sorting + Priority Queues**

Facebook's News Feed ranks thousands of candidate posts per user per visit. Each user has hundreds of friends, follows hundreds of pages, may be in dozens of groups. For each session, the feed serves the "best" ~30 posts. The candidate set per user is in the low thousands; the ranking is done by an ML model that scores each candidate with a relevance prediction. Then we sort and emit the top 30. All within ~100ms of you opening the app.

Read it in full: [`case_studies/real_world/07_facebook_news_feed_ranking.md`](case_studies/real_world/07_facebook_news_feed_ranking.md)

## Pattern drill
_From Week 7 (drill #7)._

> Distractor: Given two strings `s` and `t` of length up to 10^6, decide whether `t` occurs in `s`. (Naïve is too slow — what now?)

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 7/patterns.md`](Week 7/patterns.md)

## Hard-mode challenge
### Challenge 3 (Week 7): KMP With Multiple Patterns at Once

**Spec**:
Read a text `t` followed by `k` patterns `p_1..p_k`. For each pattern, print on one line: the pattern, a colon, and a space-separated list of all starting indices where it occurs in `t`. You may not run KMP separately `k` times — implement Aho–Corasick (a multi-pattern generalization that builds a trie + failure links analogous to KMP's failure function).

**Constraints**:
- Input size: `|t| <= 10^6`, total pattern length `<= 10^5`, `k <= 10^4`
- Time: O(|t| + total pattern length + total occurrences)
- Memory: O(total pattern length)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 7/challenges.md`](Week 7/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
