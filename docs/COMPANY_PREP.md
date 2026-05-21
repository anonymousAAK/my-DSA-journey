# Company-Targeted Interview Preparation

If you have only a few weeks before a specific company's interview, you
don't have time to run the full 30-week curriculum. This guide picks the
4–5 weeks of the existing curriculum that best match each major company's
question profile, based on widely-circulated public lists of which topics
each company favors.

> **Note on tags.** Each problem in `Week N/problems.md` now carries a
> `Companies` column. When a problem is tagged `Common`, it means we don't
> have a strong public signal for any single company — these are
> frequently-asked problems across many places and are still worth doing.

## How to use this guide

1. Pick the company you're targeting.
2. Work the 4-week curated path in order. Each week is from the main
   curriculum — open the same `Week N/` directory you've been using.
3. Filter `problems.md` to rows whose Companies column contains your
   target. Solve those first, then the rest if you have time.
4. Do at least one capstone from `capstones/` per week, and at least one
   mock from `mock_interviews/`.

The paths below assume you can put in ~15 hours/week. Adjust depth, not
breadth — better to land all four weeks shallowly than two weeks deeply.

---

## Google

**Themes Google emphasizes.** Math/edge-case reasoning, graph algorithms,
matrix problems, system design (for senior loops), bit manipulation, and
"design-it-from-scratch" puzzles (Snake game, calculator, etc.). Expect
careful follow-ups on complexity and corner cases.

**4-week curated path.**

| Week | Focus |
| --- | --- |
| Week 17 — Graphs | BFS, DFS, topological sort, Dijkstra. Google loves graphs. |
| Week 18 — Dynamic Programming | Edit distance, coin change, LIS. |
| Week 14 — Trees | LCA, BST validation, level-order. |
| Week 30 — Interview Patterns | Sliding window, two pointers, intervals — pattern recognition. |

Bonus if you have a 5th week: **Week 25 — Advanced Strings** (Google
sometimes tests KMP / Z-function follow-ups).

---

## Meta (Facebook)

**Themes Meta emphasizes.** Graphs (especially clone-graph and BFS
variants), trees (LCA, serialize/deserialize), strings, intervals, and
"product-flavored" problems (Friend Circles, News Feed sketches).
Behavioral round expects clear decision narratives.

**4-week curated path.**

| Week | Focus |
| --- | --- |
| Week 17 — Graphs | Clone Graph, Word Ladder, Course Schedule. |
| Week 14 — Trees | Serialize/Deserialize, Path Sum variants, LCA. |
| Week 7 — Strings | Group Anagrams, Minimum Window Substring. |
| Week 30 — Interview Patterns | Intervals (Merge / Insert) and sliding window. |

Bonus: **Week 16 — Hash Tables** (Subarray Sum Equals K, Longest
Consecutive Sequence).

---

## Amazon

**Themes Amazon emphasizes.** OOD/LP-flavored design, heaps (top-K
patterns), trees, graphs, and arrays. Behavioral round (Leadership
Principles) is heavily weighted — almost half the loop. Expect at least one
trie or stream problem at L5/L6.

**4-week curated path.**

| Week | Focus |
| --- | --- |
| Week 15 — Heaps | Top-K, K Closest Points, Find Median from Data Stream. |
| Week 17 — Graphs | Number of Islands, Course Schedule, Word Ladder. |
| Week 11 — Linked Lists | LRU Cache, Copy List w/ Random Pointer. |
| Week 29 — System Design | At least one OOD walkthrough (Snake Game, Twitter). |

Bonus: **Week 6 — Arrays** (Best Time to Buy and Sell Stock, Product of
Array Except Self).

---

## Apple

**Themes Apple emphasizes.** Strong fundamentals — arrays, strings, math,
recursion. Less algorithm-y than Google, more "can you carefully write
clean code under pressure?" OOD is common for hardware/firmware roles.

**4-week curated path.**

| Week | Focus |
| --- | --- |
| Week 6 — Arrays | Two Sum, Best Time to Buy and Sell Stock, Merge Sorted Array. |
| Week 7 — Strings | Valid Anagram, String to Integer, Longest Palindromic Substring. |
| Week 11 — Linked Lists | Reverse Linked List, LRU Cache, Add Two Numbers. |
| Week 14 — Trees | Maximum Depth, Path Sum, LCA. |

Bonus: **Week 5 — Functions & Recursion** for the "explain recursion to a
PM" moments.

---

## Microsoft

**Themes Microsoft emphasizes.** Classic CS fundamentals — strings,
arrays, linked lists, trees. Less novel algorithm work than Google.
Expects careful, well-tested code and clear verbal walkthrough.

**4-week curated path.**

| Week | Focus |
| --- | --- |
| Week 7 — Strings | Reverse Words, Group Anagrams, atoi. |
| Week 11 — Linked Lists | Reverse Linked List, Merge Two Sorted Lists, LRU Cache. |
| Week 14 — Trees | Level Order, Validate BST, LCA. |
| Week 6 — Arrays | Rotate Array, Spiral Matrix, Merge Sorted Array. |

Bonus: **Week 12 — Stacks** (Min Stack and Basic Calculator II appear
often).

---

## Netflix

**Themes Netflix emphasizes.** Senior-level system design and deep dives
on a few algorithms (less LeetCode-style breadth). When they do ask
algorithmic questions, expect graph problems and streaming/heap
problems — anything reminiscent of recommendation systems or video
distribution.

**4-week curated path.**

| Week | Focus |
| --- | --- |
| Week 29 — System Design | Multiple deep design walkthroughs. |
| Week 17 — Graphs | Shortest paths, connectivity, BFS variants. |
| Week 15 — Heaps | Streaming top-K, Find Median from Data Stream. |
| Week 22 — Advanced Graphs | MST, Dijkstra variants. |

Bonus: spend an extra week on `case_studies/` if you have one.

---

## Stripe

**Themes Stripe emphasizes.** Practical API-style problems (parse this
input, produce that output), state machines, money/precision arithmetic,
and rate limiters. Less classical algorithm grinding, more "build a small
working thing."

**4-week curated path.**

| Week | Focus |
| --- | --- |
| Week 7 — Strings | Parsing-heavy problems (Basic Calculator II, atoi). |
| Week 16 — Hash Tables | Design HashMap, LRU Cache, Logger Rate Limiter. |
| Week 29 — System Design | Web Crawler, Hit Counter, Design File System. |
| Week 30 — Interview Patterns | Sliding window, intervals — used in rate limiting. |

Bonus: read the `case_studies/` folder for distributed-systems flavor.

---

## Airbnb

**Themes Airbnb emphasizes.** Graphs (Alien Dictionary, Reconstruct
Itinerary appear constantly), trees, design (Design File System / Twitter
patterns), and one tricky DP. Behavioral interview is detailed and values
"explain a hard tradeoff you made".

**4-week curated path.**

| Week | Focus |
| --- | --- |
| Week 17 — Graphs | Alien Dictionary, Reconstruct Itinerary, Number of Islands. |
| Week 22 — Advanced Graphs | MST, Dijkstra. |
| Week 14 — Trees | Validate BST, Serialize/Deserialize. |
| Week 29 — System Design | OOD walkthrough(s). |

Bonus: **Week 18 — Dynamic Programming** (Coin Change variations).

---

## Cross-cutting advice

- **Mock interviews matter more than another 50 LeetCode problems.** Use
  `mock_interviews/` once per week of prep.
- **Time the practice.** Whichever company you're targeting, do at least
  five problems with a 30-minute hard timer.
- **System design.** Even non-senior loops at Amazon/Stripe/Meta increasingly
  include a low-key design question. Week 29 is your friend.
- **Behavioral.** No amount of LeetCode rescues a weak behavioral round at
  Amazon (LP) or Netflix (Keeper Test). Practice STAR stories with
  someone real, ideally a mentor (see `docs/MENTORSHIP.md`).
- **Don't fabricate.** If a problem in `Week N/problems.md` is tagged
  `Common`, the curriculum maintainers couldn't pin it to a single
  company — but it's still worth doing. Don't skip a problem just because
  your target company isn't in the list.
