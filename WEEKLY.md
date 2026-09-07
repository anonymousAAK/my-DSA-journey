# Weekly Digest — 2026-09-07 (ISO 2026-W37)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**PageRank as a Graph Algorithm**

Imagine you've just built the first web crawler, and you have a corpus of millions of pages. A user types "computer science"; thousands of pages match. Which do you show first? The pre-Google search engines (AltaVista, Lycos, Excite) ranked by keyword frequency, page length, and other content-only features. The result was a mess of keyword-stuffed garbage. Sergey Brin and Larry Page's 1998 insight: **use the link structure of the web itself as a quality signal**. If many pages link to a page, it's probably important. If important pages link to it, it's even more important.

Read it in full: [`case_studies/real_world/14_pagerank_eigenvectors.md`](case_studies/real_world/14_pagerank_eigenvectors.md)

## Pattern drill
_From Week 18 (drill #8)._

> Given a string of length n ≤ 500, find the length of the longest palindromic subsequence (not necessarily contiguous).

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 18/patterns.md`](Week 18/patterns.md)

## Hard-mode challenge
### Challenge 2 (Week 18): Longest Increasing Subsequence in O(n log n)

**Spec**:
Read `n` and `n` integers. Print the length of the longest strictly increasing subsequence. Required complexity O(n log n) using patience sorting (maintain `tails[k]` = smallest tail of any increasing subsequence of length `k+1`; binary-search to update). The O(n^2) classic DP is forbidden.

**Constraints**:
- `1 <= n <= 10^6`, values up to `10^9`
- Time: O(n log n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 18/challenges.md`](Week 18/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
