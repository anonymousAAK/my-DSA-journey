# Weekly Digest — 2026-08-10 (ISO 2026-W33)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**Bloom Filters for Safe Browsing**

Google's Safe Browsing service maintains a list of millions of URLs known to host malware or phishing. Chrome checks every URL you navigate to against this list and warns you before loading dangerous pages. The catch: shipping the entire list to every Chrome client is unreasonable — it's gigabytes. Querying Google for every URL you visit would leak your entire browsing history. So the local check has to be **on-device**, *fast*, and **compact**.

Read it in full: [`case_studies/real_world/10_bloom_filters_at_chrome.md`](case_studies/real_world/10_bloom_filters_at_chrome.md)

## Pattern drill
_From Week 14 (drill #4)._

> Given two nodes `u` and `v` in a binary tree, find their lowest common ancestor. n ≤ 10^5.

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 14/patterns.md`](Week 14/patterns.md)

## Hard-mode challenge
### Challenge 2 (Week 14): Lowest Common Ancestor in a BST and in a General Binary Tree

**Spec**:
Implement two LCA functions:
1. For a BST: O(h) using the BST property (descend left/right based on comparisons).
2. For a general binary tree: O(n) using a single recursive postorder pass that returns either the found node or null.

Read the tree (level-order with `null`), then read pairs `(u, v)` and print their LCA value.

**Constraints**:
- Up to `10^5` nodes
- Time: BST O(h), general O(n) per query
- Memory: O(h) recursion

**Test inputs**:
| Tree | Query | Expected |
|

Full spec: [`Week 14/challenges.md`](Week 14/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
