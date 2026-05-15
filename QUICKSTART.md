# Quickstart — 4 Hours to See if This Repo Works for You

If 30 weeks feels intimidating: don't start there. Spend 4 focused hours on this curated path. By the end you'll have practiced the full methodology on 8 representative problems across 5 difficulty levels. If it works for you, the long path is just more reps of the same loop.

The loop is the same one taught in [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md):

> Understand → Plan (brute → better → optimal) → Execute → Look back (journal).

You will do that loop eight times today.

---

## Before you start (10 min)

1. Read [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) — at least skim the **"Polya's four steps"** and **"The brute → better → optimal ladder"** sections.
2. Copy [`docs/SOLUTION_JOURNAL.md`](docs/SOLUTION_JOURNAL.md) to `my_journal.md` in your working directory (not committed). You will append one entry per problem.
3. Set a 4-hour timer. If you blow past a budget by more than 5 minutes on any problem, stop, peek at the reference file, and move on. The point today is *coverage of the loop*, not perfect solutions.
4. Open your scratch editor with two panes: the problem on the left, your journal on the right.

> **One rule, non-negotiable.** Attempt every problem *before* opening the reference file. Reading the answer first turns this from training into entertainment.

---

## Hour 1 — Foundations (recognize a pattern)

Goal: feel the difference between brute force and the "right tool." Two short problems, then a pattern drill.

### Problem 1: Two Sum (15 min, Easy)
- **Reference (peek only after attempting)**: [`Week 16/java/1.HashingAndHashMap.java`](Week%2016/java/1.HashingAndHashMap.java) — skim only the `twoSum` function (around line 43).
- **Spec**: given `nums` and `target`, return the two indices whose values sum to `target`. Assume exactly one solution.
- **Task**: solve it in your language of choice WITHOUT looking. Write the brute-force `O(N²)` first, then the hash-map `O(N)` version.
- **Journal (2 min)**: What pattern did you use? Why was brute-force `O(N²)`? Write the *key insight* in one sentence — that sentence is what transfers.

### Problem 2: Maximum Subarray / Kadane (15 min, Easy)
- **Reference**: [`Week 6/python/4.prefix_sum_and_kadane.py`](Week%206/python/4.prefix_sum_and_kadane.py) — Part B, Kadane's algorithm.
- **Spec**: given an integer array (values may be negative), find the contiguous subarray with the maximum sum. Return the sum.
- **Task**: brute-force first (try every `(i, j)` pair, O(N²) or O(N³)), then derive Kadane's `O(N)` running-best recurrence. Don't peek until both are written.
- **Journal (2 min)**: What work was wasted by brute force? What invariant does Kadane maintain at each step?

### Problem 3: Pattern Recognition Drill (10 min)
- Open [`Week 6/patterns.md`](Week%206/patterns.md). Do **drills 1–5** cold (don't peek at the rest of the file or any solution).
- For each, write one line: which pattern (two pointers / sliding window / prefix sum / Kadane / Dutch flag / hash) and a one-sentence justification.
- Then check yourself against the answer key at the bottom of the same file.

### Hour 1 wrap (5 min)
In your journal, write 3 sentences answering:
1. What did you struggle with — restating the problem, choosing the pattern, or coding it?
2. Which problem felt "obvious in hindsight"? Why wasn't it obvious upfront?
3. Did you actually write brute force first on Problem 2, or did you jump to Kadane?

---

## Hour 2 — Structures (build the right tool)

Goal: see that *picking the data structure* often *is* the algorithm.

### Problem 4: Merge Two Sorted Linked Lists (25 min, Medium)
- **Reference**: [`Week 11/python/2.MergeSortedListsAndLRU.py`](Week%2011/python/2.MergeSortedListsAndLRU.py) — the merge function only. Do NOT read the LRU section yet.
- **Spec**: given two sorted singly linked lists, return one merged sorted list. Reuse nodes (no copying).
- **Task**: first sketch on paper. Draw two lists, two pointers, and trace which node you splice next. Then code it. Use a dummy/sentinel head — it eliminates the "first node is special" case.
- **Journal (3 min)**: Why does a dummy head make the code shorter? What's the time and space complexity, and where does the space go?

### Problem 5: Binary Tree — Maximum Depth (15 min, Easy–Medium)
- **Reference**: [`Week 14/python/1.BinaryTree.py`](Week%2014/python/1.BinaryTree.py) — find the depth / height function.
- **Spec**: given the root of a binary tree, return its depth (number of nodes on the longest root-to-leaf path).
- **Task**: write it recursively in three lines. Then write the iterative version using a queue (level-order, count levels).
- **Journal (2 min)**: Write the recurrence in one line: `depth(root) = ...`. This is the same shape as a DP recurrence; you will see it again.

### Hour 2 wrap (5 min)
- Which structure surprised you — the linked list or the tree?
- Could you have solved Problem 5 with the same recursion habit you used in [`Week 5/python/3.recursion_basics.py`](Week%205/python/3.recursion_basics.py)? Open it briefly and confirm — recursion *is* the through-line.

---

## Hour 3 — Algorithms (pick the right approach)

Goal: graduate from "what's the data structure?" to "what's the *technique*?"

### Problem 6: Longest Substring with At Most K Distinct Characters (25 min, Medium)
- **Reference**: [`Week 30/python/sliding_window.py`](Week%2030/python/sliding_window.py) — the variable-size window template.
- **Spec**: given a string `s` and integer `k`, return the length of the longest substring containing at most `k` distinct characters.
- **Task**: brute force first (every substring, count distinct → `O(N²)` or `O(N³)`). Then derive the sliding window: expand right, shrink left while distinct count exceeds `k`, track best length. `O(N)`.
- **Journal (3 min)**: What invariant does the window maintain? Why is each character visited at most twice (once by `right`, once by `left`)?

### Problem 7a (warm-up before the open challenge): BFS reasoning (15 min, Medium)
- **Reference**: [`Week 17/python/1.GraphRepresentations.py`](Week%2017/python/1.GraphRepresentations.py) — BFS function.
- **Spec**: given an unweighted undirected graph as an adjacency list and two nodes `s` and `t`, return the number of edges on a shortest path, or `-1` if unreachable.
- **Task**: write BFS from scratch. Use a queue and a visited set. Track depth either by storing `(node, depth)` tuples or by processing the queue one level at a time.
- **Journal (2 min)**: Why does BFS give shortest *unweighted* paths but not shortest *weighted* paths? (If you don't know, this is your signpost toward Week 22.)

### Hour 3 wrap (5 min)
Sliding window and BFS are both "expand a frontier carefully." Note in your journal: what they share, and what makes them different (one moves along a 1-D array, the other through an arbitrary graph).

---

## Hour 4 — Synthesis (do it under simulated pressure)

Goal: combine the loop end-to-end on a problem you have not been spoon-fed.

### Problem 8: Open-ended challenge (40 min, Hard)
Pick **one** challenge from [`Week 8/challenges.md`](Week%208/challenges.md) — recommended: **Challenge 1 (Closest Element in a Rotated Sorted Array)** if you've seen binary search before, else **Challenge 2** from the same file.

Rules:
1. Restate the spec in your own words at the top of your journal entry. Write down the constraints.
2. Sketch the approach in English in 2 sentences *before* writing code.
3. Implement. No peeking at any file under `Week 8/python/`, `Week 8/java/`, etc.
4. Test against the inputs given in the challenge file.
5. Only after it works (or after 40 min, whichever comes first), diff your solution against the canonical one. What did you do differently?

### Problem 9: Mock interview self-review (15 min)
Read [`mock_interviews/01_two_sum_warm_up.md`](mock_interviews/01_two_sum_warm_up.md) — the full annotated transcript from Hour 1's first problem.

- Compare your Hour-1 thought process to the transcript's annotated good habits (the ️ callouts).
- What did *you* do that the transcript flagged as "good"? (e.g. asking about duplicates, restating the problem, narrating tradeoffs.)
- What did you skip? (e.g. did you announce your complexity? did you mention the brute force before solving?)

### Hour 4 wrap (5 min)
Write in your journal:
- Was your Hour-4 challenge solution closer to brute force, "better," or optimal? Why?
- Which of Polya's four steps did you skip most often today? (Most learners skip step 4, "Look back.")
- What would you do differently next time?

---

## What now?

You've just done a microcosm of the full curriculum. Eight problems, five difficulty levels, every layer of the loop. If it felt valuable:

- **Take the diagnostic** ([`docs/diagnostic.md`](docs/diagnostic.md)) to find your actual starting point. Skip the weeks you've already mastered.
- **8 weeks of focused interview prep**: follow [Learning Path 2 (Interview Prep)](README.md#path-2-interview-prep-8-weeks) in the root README — Weeks 6, 8, 11, 14, 16, 17, 18, 30.
- **Full 30 weeks**: start at Week 1 and journal every problem. Most people who finish do it this way.
- **Competitive programming**: follow [Path 3](README.md#path-3-competitive-programming-10-weeks).

If it didn't feel valuable, before you bounce, check honestly:

- Did you actually attempt every problem before peeking?
- Did you journal, or just read?
- Did you write the brute force *first* on Problems 2, 6, and 7a — or did you skip straight to the clever solution?
- Did you compare your code against the canonical version on Problem 8?

Most "this didn't work for me" outcomes trace back to one specific skip: the journaling step. The journal is where the methodology actually lives. The code is the byproduct.

---

> Once you've done the loop eight times, you've done it eight times. That's not nothing. That's how the habit starts.
