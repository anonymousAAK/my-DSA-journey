# Diagnostic — Where Should You Start?

15 questions across the curriculum. Answer honestly. At the end, we map your answers to a recommended starting week.

**Don't look anything up while taking this. The point is to calibrate, not to score.** Time budget: ~25 minutes total. If you're spending more than two minutes on a single question, write your best guess and move on.

Keep a simple answer sheet: `Q1: C`, `Q2: ...`, etc. Reveal the answer key (collapsed at the bottom) only after you've answered all 15.

---

## Section 1: Foundations & Complexity (Q1–Q3)

### Q1. What's the time complexity of this Python code?

```python
def f(n):
    result = []
    for i in range(n):
        for j in range(i, n):
            result.append(i * j)
    return result
```

- A) O(N)
- B) O(N log N)
- C) O(N²)
- D) O(N³)

### Q2. You have an algorithm that takes 1 second on input size N = 1,000. Assuming the algorithm is O(N log N), roughly how long will it take on N = 1,000,000?

- A) About 1,000 seconds (~17 minutes)
- B) About 2,000 seconds (~33 minutes)
- C) About 1,000,000 seconds (~12 days)
- D) About 10 seconds

### Q3. Short answer. A problem has constraints `1 ≤ N ≤ 20`. Without knowing anything else about the problem, what algorithm class *opens up* at this small N that would be infeasible at N = 10⁵? Answer in one word or short phrase.

---

## Section 2: Arrays & Strings (Q4–Q5)

### Q4. You're given a sorted array of distinct integers and a target. You need to find two indices whose values sum to the target. What's the cleanest approach?

- A) Hash map: for each `x`, look up `target - x`. O(N) time, O(N) space.
- B) Two pointers from both ends, moving inward based on the current sum. O(N) time, O(1) space.
- C) Binary search for each element's complement. O(N log N) time, O(1) space.
- D) Nested loop checking every pair. O(N²) time, O(1) space.

> Multiple choices are *correct* in the sense of "would pass." Pick the one that exploits the **most** structure in the input.

### Q5. You're processing a stream of characters and want to know, at every point, the length of the longest substring ending at the current character with no repeated characters. Which technique applies?

- A) Sort the substring and dedupe.
- B) Sliding window with a hash set: expand right, shrink left while a duplicate is in the window.
- C) Dynamic programming, `dp[i] = dp[i-1] + 1` always.
- D) Suffix array.

---

## Section 3: Hash Maps & Data Structures (Q6–Q8)

### Q6. In an average-case correctly-sized hash table, what's the time complexity of `insert`, `lookup`, and `delete`?

- A) O(log N) all three.
- B) O(1) amortized average all three.
- C) O(N) for insert, O(1) for lookup, O(N) for delete.
- D) O(1) for insert, O(N) for lookup, O(N) for delete.

### Q7. You need a data structure that supports `get(key)` and `put(key, value)` in O(1) average time, AND evicts the least-recently-used key when capacity is exceeded. Which two structures do you compose?

- A) Two stacks.
- B) Hash map + balanced BST.
- C) Hash map + doubly linked list.
- D) Min-heap + hash set.

### Q8. Short answer. In one short sentence: when would you choose a **trie** over a **hash map** for storing a set of strings?

---

## Section 4: Trees, Recursion & Graphs (Q9–Q11)

### Q9. Given the root of a binary tree, you write `depth(root) = 1 + max(depth(left), depth(right))` with base case `depth(None) = 0`. This is a correct, idiomatic implementation. What is its time and space complexity (space = recursion stack), where `N` is the number of nodes and `H` is the tree height?

- A) Time O(N log N), space O(N).
- B) Time O(N), space O(H).
- C) Time O(H), space O(1).
- D) Time O(N²), space O(N).

### Q10. You need the shortest path (in number of edges) from node `s` to node `t` in an **unweighted undirected** graph. Which traversal do you use, and why?

- A) DFS, because it explores deeper first.
- B) BFS, because it visits nodes in non-decreasing order of edge-distance from the source.
- C) Dijkstra, because it's the general shortest-path algorithm.
- D) Topological sort, because it gives an ordering.

### Q11. Short answer. You're asked to detect a cycle in a **directed** graph. You decide to use DFS. What auxiliary state — beyond a "visited" set — do you need, and why? One sentence.

---

## Section 5: DP & Advanced (Q12–Q15)

### Q12. Which of these problems is *most cleanly* solved by dynamic programming (as opposed to greedy, brute force, or a single pass)?

- A) Given coin denominations and an amount, return the **minimum** number of coins to make the amount. Denominations are arbitrary (e.g. `[1, 3, 4]`, amount `6` → `2`, not `3`).
- B) Given a list of intervals, find the maximum number of mutually non-overlapping ones.
- C) Given an array, return its sum.
- D) Given two strings, check whether they are anagrams.

### Q13. You see "find the number of distinct ways to ..." with a recurrence shape `f(n) = f(n-1) + f(n-2)` or similar, and constraints up to `N ≤ 10⁵`. The signal is:

- A) Greedy: take the locally best step at each `n`.
- B) DP: memoize the recurrence (or tabulate it). Watch for overlapping subproblems.
- C) Backtracking: enumerate all configurations.
- D) Hash map of seen `n` values.

### Q14. Which of these is a **segment tree** good at, that a prefix-sum array is *not*?

- A) Answering "sum of `a[l..r]`" in O(1) after O(N) preprocessing, when the array is **static**.
- B) Answering "sum of `a[l..r]`" with point updates `a[i] = x` interleaved with queries, both in O(log N).
- C) Sorting the array in O(N log N).
- D) Finding the median of a stream.

### Q15. Short answer. In one sentence, explain what **network flow** (max-flow / min-cut) lets you model that plain BFS/DFS does not. Don't worry about algorithm names — just the *kind of problem*.

---

## Stop here. Score yourself only after answering all 15.

<details>
<summary><b>Click to reveal answer key + placement</b></summary>

### Answer key

- **Q1: C** — outer loop runs N times; inner runs from `i` to `n`, so total ops = N + (N-1) + ... + 1 = N(N+1)/2 ≈ N²/2. O(N²).
- **Q2: B** — N log N scales by `(N₂/N₁) · (log N₂ / log N₁) = 1000 · (20/10) ≈ 2000`. So roughly 2,000 seconds. Choice C would be O(N³); choice A would be O(N²).
- **Q3** — **Bitmask DP** (or "subset enumeration / 2^N brute force / exponential search"). N ≤ 20 means 2^N ≤ ~10⁶, which fits in a second. Covered in Week 23.
- **Q4: B** — two pointers exploits the **sorted** structure for O(N) time and O(1) space. A works but wastes O(N) space; C wastes a log factor; D ignores the sortedness. The point of the question: pick the technique that uses the *most* of the input's structure.
- **Q5: B** — classic sliding window with a hash set / last-seen-index map. C is wrong because `dp[i]` does **not** always equal `dp[i-1] + 1` — it depends on whether `s[i]` already appears in the current window.
- **Q6: B** — O(1) amortized average for all three. Worst case is O(N) if every key hashes to the same bucket, but the question asks average case.
- **Q7: C** — hash map for O(1) lookup, doubly linked list for O(1) reordering on each access. This is the standard **LRU cache** structure, covered in Weeks 11, 16, and 29.
- **Q8** — When you need **prefix queries** (e.g. autocomplete, "does any stored string start with `pre`?"), or when many stored strings share long common prefixes (memory savings). Hash maps treat keys as opaque; tries exploit shared prefix structure.
- **Q9: B** — every node visited once → O(N) time. Recursion depth equals tree height → O(H) space. For a balanced tree, H = O(log N); for a degenerate (linked-list-like) tree, H = N.
- **Q10: B** — BFS. The level-by-level expansion guarantees that when you first reach a node, you've used the minimum number of edges. Dijkstra works too but is overkill (and has an unnecessary log factor) for unweighted graphs.
- **Q11** — You need a **"currently on the recursion stack" (a.k.a. "gray" or "in-progress")** set in addition to the "fully-visited" (black) set. A back edge to a gray node is a cycle. With only a single visited set you can't distinguish a cross/forward edge in a DAG from a true back edge.
- **Q12: A** — coin change with arbitrary denominations is the canonical DP problem (greedy fails on `[1, 3, 4]` for amount `6` — greedy picks `4 + 1 + 1`; DP finds `3 + 3`). B is greedy (interval scheduling). C and D are single-pass.
- **Q13: B** — DP. The Fibonacci-shaped recurrence with overlapping subproblems is the textbook DP signal. With N ≤ 10⁵, naive recursion is exponential; memoize or tabulate.
- **Q14: B** — segment trees handle **point updates + range queries** in O(log N) each. Prefix-sum arrays can answer range-sum in O(1) but require O(N) per update; they're only competitive when the array is static.
- **Q15** — Network flow models **capacity-constrained routing** through a network — you can send up to `c(u,v)` units along each edge, and you want the maximum total throughput from source to sink. Equivalently (min-cut duality), it solves problems like "what's the smallest set of edges to disconnect `s` from `t`?" Plain BFS/DFS only tells you reachability or shortest path; they don't reason about *capacity* or *aggregate flow*. Many seemingly unrelated problems (bipartite matching, image segmentation, project selection) reduce to max-flow.

### Placement matrix

Count how many you got *fully* right (for short-answer questions, give yourself credit if your answer captures the same idea, even if your wording differs).

| Score | Recommended starting point |
|---|---|
| **0–3** | Start at **Week 1**. The foundations are necessary. Don't skip them — they pay back compound interest. |
| **4–7** | Skim Weeks 1–5 (or skip if Q1–Q3 felt easy). Start serious work at **Week 6** (arrays) or **Week 8** (searching). |
| **8–11** | Start at **Week 11** (linked lists) or **Week 14** (trees), depending on where you missed. If you missed Q9–Q11, start at Week 14. If you missed Q6–Q8, start at Week 16. |
| **12–15** | Start at **Week 17** (graphs) or jump to advanced topics (**Weeks 21+**). If you also nailed Q14–Q15, head straight to Weeks 23–24 (advanced DP & research-level topics). |

**Diagnostic anomalies — read these too:**
- **Aced sections 4–5 (Q9–Q15) but failed section 1 (Q1–Q3)**: unusual. You can write algorithms but can't reason about their cost. Revisit complexity analysis in [`PROBLEM_SOLVING.md`](../PROBLEM_SOLVING.md) — specifically the "Identifying constraints — what each one tells you" section. Then return to Week 8.
- **Aced sections 1–3 but failed sections 4–5**: classic profile. You have solid foundations but haven't built algorithmic vocabulary. Jump to the **8-week interview prep path** in the [root README](../README.md#path-2-interview-prep-8-weeks) — Weeks 6, 8, 11, 14, 16, 17, 18, 30.
- **Got Q3, Q8, Q11, or Q15 fully right (short-answer)**: you have the *vocabulary* of an experienced practitioner. Even if your multiple-choice score is mid, lean into the advanced path.

### What each section tested

| Section | Tested | Covered in |
|---|---|---|
| 1 (Q1–Q3) | Complexity intuition, big-O scaling, constraint reading | Weeks 1–5, 8; [`PROBLEM_SOLVING.md`](../PROBLEM_SOLVING.md) |
| 2 (Q4–Q5) | Array & string idioms — two pointers, sliding window | Weeks 6, 7, 10, 30 |
| 3 (Q6–Q8) | Hash maps, composite data structures, tries | Weeks 11, 16, 21 |
| 4 (Q9–Q11) | Recursion, trees, graph traversal reasoning | Weeks 5, 14, 17 |
| 5 (Q12–Q15) | DP recognition, segment trees, network flow | Weeks 18, 21, 23, 26 |

---

> Whichever week you land on, drop your diagnostic score and recommendation into your journal as the first entry. Six months from now, when you've forgotten what you didn't know, it will be the most honest snapshot of where you started.

</details>

---

## What next?

- New to the methodology? Try the [**Quickstart**](../QUICKSTART.md) first — 4 hours, 8 problems, the full loop.
- Ready to commit? Head to the [**root README**](../README.md) and pick a learning path.
- Want the philosophy behind the curriculum? Read [`PROBLEM_SOLVING.md`](../PROBLEM_SOLVING.md).
