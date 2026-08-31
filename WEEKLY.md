# Weekly Digest — 2026-08-31 (ISO 2026-W36)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**What grep / ripgrep Actually Do**

You type `grep "foo" *.log` and a tool scans gigabytes of text looking for matches. You don't think about it — it's instant. But "find substring in a file" is one of the most studied algorithmic problems in computer science, with a rich history of algorithms ranging from "obvious and slow" to "subtle and astonishingly fast." Modern tools (GNU grep, ripgrep, ag) routinely outperform what a naïve implementation could do by 10-100x.

Read it in full: [`case_studies/real_world/13_grep_kmp_aho_corasick.md`](case_studies/real_world/13_grep_kmp_aho_corasick.md)

## Pattern drill
_From Week 17 (drill #7)._

> Distractor: Given a weighted graph with non-negative edges, find the shortest path from `s` to `t`. (Is BFS enough?)

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 17/patterns.md`](Week 17/patterns.md)

## Hard-mode challenge
### Challenge 2 (Week 17): Count Distinct Shortest Paths in an Unweighted Graph

**Spec**:
Read `n`, `m`, and `m` edges of an undirected unweighted graph (1-indexed vertices). Read `s` and `t`. Print the number of distinct shortest paths from `s` to `t` modulo `10^9 + 7`. Use BFS computing `dist[v]` and `count[v]` simultaneously: when relaxing `v` from `u`, if `dist[v] == dist[u] + 1` add `count[u]` to `count[v]`.

**Constraints**:
- `1 <= n, m <= 10^5`
- Time: O(n + m)
- Memory: O(n + m)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 17/challenges.md`](Week 17/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
