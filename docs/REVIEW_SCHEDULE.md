# Review Schedule — Spaced Repetition & Interleaving

> Studying Week 14 (Trees) and then never thinking about Week 6 (Arrays) again is how you forget Week 6. This file is the antidote: a built-in revisit schedule that runs alongside the 30-week curriculum.

---

## Why interleaving beats blocked practice

The intuitive way to study is *blocked*: do 30 array problems, then 30 string problems, then 30 tree problems. It feels productive because you get fast at the current topic. The trap: you're getting fast at *applying a technique you already know is the right one*. In the real world (interviews, contests, work) you don't get told which technique to use — recognition is the hard part, and blocked practice doesn't train recognition.

**Interleaving** mixes problem types within a session. Performance during practice feels *worse* — you're slower, you mis-classify more — and that's exactly the point. The discomfort is the recognition muscle being worked. Cognitive-science literature (Rohrer, Bjork, et al.) consistently shows interleaved practice produces better retention and transfer than blocked, even though learners universally report it feeling less effective. Trust the data, not the feeling.

Combine with **spaced repetition** — revisit a topic once shortly after learning, then again after a longer gap, then again after a longer one. Week N-3 and Week N-7 are the recommended touch points: close enough that you haven't fully forgotten, far enough that you're actually recalling, not just re-reading.

---

## Suggested rhythm

- **80% new / 20% revisit per session.** If you have 5 hours this week, spend 1 hour on revisits drawn from the table below, and 4 hours on the current week's material.
- **Re-read the *problem*, not the solution.** Cover your old code. Try to re-derive the approach in your head before you peek. If you can't — that's data. That topic needs another pass.
- **Random order.** Don't revisit in a predictable sequence. Shuffle the revisit list each session. Recognition only trains when you can't predict what's coming.
- **Time-boxed.** 10–15 min per revisit problem. If you can't re-derive in that window, skim the old solution, write down the *insight* in one sentence, move on. Don't try to re-solve from scratch — the goal is reinforcement, not perfection.

---

## Weekly revisit table

For each week N, the table picks 2–3 representative problems from Week N-3 and Week N-7 to revisit. Weeks 1–7 have nothing to revisit yet (or only one prior week) — just review the current week's material.

| Studying Week | Revisit from Week N-3 | Revisit from Week N-7 |
|---:|---|---|
| 1  | — | — |
| 2  | — | — |
| 3  | — | — |
| 4  | Week 1 — type casting, arithmetic edge cases | — |
| 5  | Week 2 — nested if-else, ternary tricky cases | — |
| 6  | Week 3 — Fibonacci, prime check, binary↔decimal | — |
| 7  | Week 4 — diamond pattern, mirror patterns | — |
| 8  | Week 5 — factorial recursion, Tower of Hanoi | Week 1 — variables / casting basics |
| 9  | Week 6 — Kadane's algorithm, Dutch National Flag | Week 2 — control-flow loops |
| 10 | Week 7 — palindrome, anagram, string reverse | Week 3 — bitwise operators, prime sieve |
| 11 | Week 8 — binary search variants, search-on-answer | Week 4 — nested-loop patterns |
| 12 | Week 9 — merge sort, quick sort partitioning | Week 5 — recursion, call stack |
| 13 | Week 10 — spiral traversal, search in sorted matrix | Week 6 — prefix sums, rotate array |
| 14 | Week 11 — reverse linked list, detect cycle, LRU | Week 7 — KMP, Rabin-Karp |
| 15 | Week 12 — next greater element, min stack | Week 8 — binary search on answer |
| 16 | Week 13 — sliding window max, BFS preview | Week 9 — quick sort, counting sort |
| 17 | Week 14 — BST validate, LCA, serialize tree | Week 10 — matrix transpose / rotation |
| 18 | Week 15 — K-th largest, merge K sorted, median stream | Week 11 — merge sorted lists, LRU |
| 19 | Week 16 — Two Sum, group anagrams, subarray sum 0 | Week 12 — largest rectangle, parentheses |
| 20 | Week 17 — DFS, BFS, cycle detection, topo sort | Week 13 — monotonic deque, BFS preview |
| 21 | Week 18 — LCS, LIS, coin change, edit distance | Week 14 — BST insert/delete, traversals |
| 22 | Week 19 — interval scheduling, Huffman, gas station | Week 15 — heapify, top-K, merge K sorted |
| 23 | Week 20 — N-Queens, sudoku, permutations | Week 16 — HashMap collisions, group anagrams |
| 24 | Week 21 — segment tree range sum, trie autocomplete | Week 17 — Kahn's topo sort, bipartite check |
| 25 | Week 22 — Dijkstra, Kruskal, Tarjan SCC | Week 18 — knapsack, edit distance |
| 26 | Week 23 — bitmask DP, DP on trees, digit DP | Week 19 — activity selection, job sequencing |
| 27 | Week 24 — amortized analysis, bloom filter, reservoir | Week 20 — N-Queens, word search |
| 28 | Week 25 — Z-algorithm, Manacher, suffix arrays | Week 21 — Fenwick tree, trie pattern match |
| 29 | Week 26 — max flow, Edmonds-Karp, bipartite matching | Week 22 — Bellman-Ford, MST, articulation points |
| 30 | Week 27 — convex hull, closest pair, line intersection | Week 23 — convex hull trick, profile DP |

(Pick 2–3 specific problems per cell; the list above is suggestions, not a mandate. Use your `docs/SOLUTION_JOURNAL.md` entries as the actual revisit queue if you've been filling them in.)

---

## Tip: revisit by *re-deriving*, not re-reading

The temptation when revisiting is to skim your old solution, nod, and move on. That's not revisiting — that's reassuring yourself. Instead:

1. Cover your old code with your hand or close the file.
2. Read the problem fresh, like you've never seen it.
3. State the approach in two sentences.
4. Identify the key insight (the *one* thing that turned brute force into the solution).
5. *Only then* open the old code and check.

If your two-sentence statement matches — great, the memory is consolidated. If it doesn't — also great, you just discovered a gap. Re-solve, take five minutes to update your journal entry with the new insight, and that topic is now stronger than it was before.

---

> Forgetting is not failure. Forgetting is what makes recall worth practicing. The schedule above turns forgetting from an accident into a tool.
