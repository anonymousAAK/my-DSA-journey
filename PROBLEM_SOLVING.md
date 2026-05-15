# Problem-Solving — The Mindset Manifesto

> A 30-week DSA curriculum can teach you *what* the algorithms are. This file is about *how to think* when a problem you've never seen before lands on your screen. Read this once. Then read it again after Week 10. Then again after Week 20.

---

## Why this exists

The repository teaches data structures and algorithms. That's not the same as teaching problem solving.

A **coder** knows the syntax, the standard library, and a catalog of named algorithms. Give them a problem with the right keyword in it ("sorted array" → binary search) and they ship.

A **problem solver** is something different. They sit with an unfamiliar prompt and don't panic. They restate it until it stops being slippery. They build a small example by hand. They write a brute-force solution they know is too slow, *on purpose*, because that solution exposes the structure of the problem. Then they ask the single question that drives every optimization in computer science: *what work is being wasted?* Their answer is the algorithm.

You are not here to memorize 200 LeetCode patterns. You are here to become someone who, faced with a problem nobody has solved, can still make progress. The patterns are scaffolding. The mindset is the thing.

---

## Polya's four steps

George Polya's *How to Solve It* (1945) is older than every textbook in your reading list and more useful than most of them. The four steps:

### 1. Understand the problem
Read it twice. Then read it three times. Write down, in your own words:
- What are the inputs? (types, ranges, are they sorted, can they have duplicates, can they be empty)
- What is the output? (a single value, a structure, all valid configurations)
- What does "valid" or "best" mean here?
- What does the problem *not* say? (often the most important question)

**Example.** "Find the longest substring with at most K distinct characters." Before doing anything: is K guaranteed ≥ 1? Are characters ASCII or Unicode? If the string is empty, is the answer 0 or undefined? Is "substring" contiguous (yes, by convention) or "subsequence" (not contiguous)? If you skip this step you will solve the wrong problem and not notice for twenty minutes.

### 2. Devise a plan
Before writing a line of code, articulate the approach in English. "I'll use a sliding window where the right pointer expands until the window has K+1 distinct chars, then the left pointer shrinks until it has K again. I track the max length along the way." If you cannot say it in two sentences, you do not yet have a plan.

This is also where you connect the new problem to old ones. "This feels like 'minimum window substring'." "This is just BFS on an implicit graph." Pattern recognition is a planning skill, not a memorization skill.

### 3. Carry out the plan
Now you write code. The translation from plan to code should be mechanical. If you find yourself making big decisions while typing, stop — you skipped step 2.

### 4. Look back
The step everyone skips. After it passes:
- Can I derive a tighter complexity bound?
- Can I simplify the code? (rename variables, collapse special cases, remove an unused branch)
- What was the *key insight*? Write it down in one sentence. That sentence is what transfers to the next problem.
- What family does this belong to? Add it to your mental index.

**Worked example — Two Sum.**
1. *Understand.* Given `nums` and `target`, return indices of two numbers summing to `target`. Exactly one solution. Cannot use the same element twice. Indices, not values.
2. *Plan.* Brute force is O(n²) pairs. Better: for each `x`, we need `target - x`. Lookup is O(1) with a hash. Walk once, ask the hash if `target - nums[i]` has been seen, otherwise store `nums[i] → i`.
3. *Execute.* Ten lines of code.
4. *Look back.* Key insight: *we don't need to search for the pair; we need to ask whether the complement exists*. That reframing — "search → existence query" — is exactly the move behind 3Sum, 4Sum, two-pointers-on-sorted, etc. The technique is portable; remember the move, not the code.

---

## Restating ambiguous problems

Real problems — at work, in research, in interviews — arrive vague. Practice tightening them.

| Vague prompt | Tightened version |
|---|---|
| "Find duplicates in this array." | "Return the set of values that appear more than once. Order doesn't matter. The array fits in memory. Values are 32-bit integers." |
| "Schedule the meetings." | "Given a list of `(start, end)` intervals, return the maximum number of mutually non-overlapping intervals. Two intervals sharing only an endpoint do not overlap." |
| "Find the shortest path." | "Unweighted, undirected graph with up to 10⁵ nodes; return the number of edges in the shortest path from `s` to `t`, or `-1` if unreachable." |
| "Compress this string." | "Replace each run of `k ≥ 2` identical characters with `c` followed by the count in decimal. Runs of length 1 are left alone. Output must be shorter than input, otherwise return input unchanged." |
| "Find the best route." | "*Best* by what metric — distance, time, fuel, fewest transfers? Are edges weighted? Can weights be negative? Is the graph dense or sparse?" |

Notice the pattern: vague prompts have **implicit constraints** that the asker has in their head and you do not. Until the constraints are on paper, the problem is not a problem — it's a wish.

When working alone (no asker to interrogate), restate the problem to yourself and **lock the constraints**. Write them at the top of your scratch file. They are now part of the spec.

---

## Identifying constraints — what each one *tells you*

Constraints are the most under-read part of a problem statement. They are also the loudest hints in the room. Read them like a compiler reads types.

**Input size N.** This single number narrows your algorithm class more than any other piece of information.

| N up to | Algorithms that fit (~1 sec budget) |
|---|---|
| ~10 | Anything. Even O(N!) brute force is fine. Backtracking, permutations. |
| ~20 | O(2^N) bitmask DP, meet-in-the-middle. |
| ~500 | O(N³) is fine — Floyd-Warshall, interval DP. |
| ~5,000 | O(N²) is fine — quadratic DP, all-pairs scans. |
| ~10⁵ | O(N log N) — sorting, segment trees, Dijkstra with heap. |
| ~10⁶ | O(N) or O(N log log N) — linear scans, sieves, hashing. |
| ~10⁸+ | O(log N) or O(1) per query — preprocessed, math, or you're streaming. |

If the problem says `N ≤ 20` and you're reaching for a polynomial DP, you're overthinking. If `N ≤ 10⁶` and your plan is O(N²), you're under-thinking.

**Time limit.** "2 seconds" combined with N tells you the same story from the other side. Modern machines do roughly 10⁸–10⁹ simple operations per second. Multiply your N by your big-O and check that the product fits.

**Memory limit.** 256 MB is roughly 6×10⁷ ints. If the problem hands you N=10⁶ and asks for an N×N table, you need O(N) or O(log N) space — that pushes you toward space-optimized DP, rolling arrays, or in-place algorithms.

**Ordering / sortedness.** "The array is sorted" is a giant flashing sign reading *binary search, two pointers, or merge*. "The values are distinct" rules out duplicate-handling edge cases. "The input is a permutation of 1..N" opens the door to cycle decomposition and counting tricks.

**Mutability.** Can you modify the input? If yes, in-place tricks (negative-marking, swap-to-index) become free. If no, you need O(N) auxiliary space at minimum.

**Real numbers vs. integers.** Integer-only opens counting sort, bitmask, modular arithmetic, and exact comparison. Floats force you to think about precision, epsilon comparisons, and numerically stable formulations.

**Online vs. offline.** Offline means you see all queries upfront — you can reorder them, batch them, sweep. Online means you must answer each query before seeing the next — segment trees, balanced BSTs, persistent structures.

**Read constraints first, then the problem.** That's not a typo. The constraints often tell you the answer's shape before you've read what the question is.

---

## The brute → better → optimal ladder

The single most important habit in this whole document.

**Step 1 — Brute force.** Write the dumbest correct solution you can. Try every pair, every subset, every path. Do not skip this. If brute force is too slow even to type out, write the *recurrence* for it on paper.

Why this matters:
- It pins down what "correct" means — you now have a reference implementation to test against.
- It exposes the **structure**. The bottleneck of the brute solution is where the optimization lives.
- It defangs the problem. You went from "I don't know how to solve this" to "I have a working O(N³) solution and I'd like to make it faster" — these are different psychological states.

**Step 2 — Ask the one question.** *What work is brute force doing that's wasted?*

This question is the engine of nearly every algorithmic improvement ever invented:

| Wasted work | Optimization it produces |
|---|---|
| Recomputing the same subproblem | Memoization → DP |
| Re-scanning a range we just scanned | Prefix sums, sliding window |
| Searching linearly through sorted data | Binary search |
| Searching for a value we could have indexed | Hash map |
| Repeated `min` over a moving window | Monotonic deque |
| Re-traversing a tree we just traversed | Euler tour, DFS reuse |
| Trying obviously dominated choices | Greedy + exchange argument |
| Examining edges that can't improve the answer | Dijkstra's relaxation |

**Step 3 — Optimal (or good enough).** Apply the optimization. Verify against the brute solution on small inputs. *Then* worry about constants, SIMD, and cache behavior — and usually you don't need to.

Skipping step 1 is the single most common mistake intermediate programmers make. They reach for the clever solution, miss a case, and now they're debugging a clever solution they don't fully understand. Brute force first. Always.

---

## When to bail — symptoms you're on the wrong track

You will get stuck. Getting stuck is fine. Staying stuck because of ego is not. Signals that your current plan is dead:

- **30+ minutes with no working code and no shrinking problem.** Not stuck on a bug — stuck on the approach. Start over with a fresh page.
- **Your edge cases keep multiplying.** Every fix introduces two new cases. The data structure is wrong, or the invariant is wrong.
- **Your complexity analysis won't close.** You can't even bound it on paper. The plan is incoherent; you don't actually know what it does.
- **You're patching symptoms.** You added `if (i == 0)` then `if (n == 1)` then `if (arr[i] < 0)`. Each patch is a tell that your core logic doesn't handle a case it should have handled by construction.
- **You're tired and the same bug keeps coming back.** Walk away for ten minutes. This isn't laziness, it's debugging.

**How to backtrack without ego.** Write down — literally write — what your current approach assumes. Which assumption is the weakest? Drop it. Often the right algorithm is a sibling of the one you tried, separated by a single design choice (BFS vs. DFS, sort by start vs. end, top-down vs. bottom-up).

Bailing early is a skill. The cost of switching approaches at minute 15 is small. The cost at minute 90 is catastrophic.

---

## Common cognitive traps

These are the recurring failure modes. Name them so you can spot them in yourself.

- **Premature optimization.** Reaching for the segment tree before you've checked whether a prefix sum would do. Constant-factor tweaks before correctness. The discipline: *correct, then clear, then fast*.
- **Anchoring on the first idea.** Your first plan feels like *the* plan because you thought of it. Force yourself to generate at least three approaches before picking one. The act of comparing is what produces insight.
- **Refusing to write brute force.** "It's beneath me." "It's obviously too slow." Write it anyway. It's a reference implementation, a test oracle, and a thinking aid. It costs four minutes.
- **Fearing recursion.** Recursion is a notation, not a magic spell. If you can write the recurrence, you can write the function. If the recursion is too deep, convert to a stack — that's a mechanical transformation, not a creative leap.
- **Skipping pen and paper.** Every problem fits on an index card. Drawing the array, sketching the tree, walking through the first three iterations by hand — these find bugs faster than any debugger. The keyboard is for typing, not for thinking.
- **Reading the solution too soon.** Twenty minutes of productive struggle teaches more than two hours of reading. If you must peek, peek at the *idea* (one sentence) and then close the tab.
- **Generalizing from one example.** Your code works on `[1,2,3]`. Try `[]`, `[5]`, `[5,5]`, `[5,4,3,2,1]`, `[-1,-2]`, and the largest input. Edge cases are not optional.
- **Misreading complexity.** "It's O(N log N) because I sorted." But the inner loop is O(N), so it's O(N² log N). Recompute when in doubt.

---

## The 7 problem archetypes

Most coding-interview and competitive problems are one of these in disguise. Each has a "smell" — the surface feature that hints at the underlying shape.

| Archetype | Smell | Where in this repo |
|---|---|---|
| **Search & sort** | "Sorted array", "find the K-th", "smallest such that…" | Weeks 8–9 |
| **Two pointers** | "Pair with property X in a sorted array", "in-place rearrange" | Week 30 |
| **Sliding window** | "Longest/shortest contiguous subarray with property X" | Weeks 6, 13, 30 |
| **BFS / DFS** | "Reachable", "connected", "shortest in unweighted graph", "explore all" | Week 17 |
| **Dynamic programming** | "Count the number of ways", "min/max over choices", "optimal substructure with overlap" | Weeks 18, 23 |
| **Greedy** | "Schedule", "fewest of X", "you can prove the local choice is safe" | Week 19 |
| **Divide & conquer** | "Recurse on halves", "merge results", "O(N log N) is plausible" | Week 9 (merge/quick sort), Week 27 (closest pair) |

These overlap. Sliding window is a specialization of two pointers. DP often emerges from divide & conquer with memoization. Greedy is DP when you can prove only one choice ever matters. The boundaries are blurry — the labels are scaffolding, not categories of truth.

When a new problem arrives, run a quick triage: which of the seven smells does it have? If two, the answer probably combines them.

---

## Closing reading list

- **Polya, *How to Solve It* (1945).** Short. Old. Still the best book on this topic. Read once a year.
- **Skiena, *The Algorithm Design Manual*, 3rd ed.** Chapters 1–3 for problem-solving philosophy; the "war stories" are the gold. The catalog in the second half is a working programmer's reference.
- **CLRS (Cormen, Leiserson, Rivest, Stein), *Introduction to Algorithms*, 4th ed.**
  - Chapter 1 — The role of algorithms.
  - Chapter 2 — Getting started (insertion sort as a worked Polya example).
  - Chapter 4 — Divide and conquer (recurrences, master theorem).
  - Chapter 15 — Dynamic programming (the rod-cutting derivation is the canonical brute → better → optimal walkthrough).
  - Chapter 16 — Greedy algorithms (and how to prove correctness).
- **Bentley, *Programming Pearls*.** Column 2 ("Aha! Algorithms") and Column 8 ("Algorithm Design Techniques") are the most useful for this mindset.
- **Kleinberg & Tardos, *Algorithm Design*.** Chapter 1's gale-shapley walkthrough is a masterclass in turning a vague problem into a precise one.

Read these alongside the curriculum, not after. The point is not to finish them — it's to have them open when you're stuck.

---

> The algorithms in this repo are tools. *Problem solving* is the workshop. Spend more time in the workshop than the toolbox.
