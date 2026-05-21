# Week 9 — Sorting Algorithms

> Self-check: `./scripts/journey quiz 9`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/2.merge_sort.py`](python/2.merge_sort.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_09/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify merge_sort workbook/week_09/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 9`

If you got stuck: open [`python/2.merge_sort.py`](python/2.merge_sort.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Sorting Algorithms**. You'll touch: BubbleSelectionInsertion, MergeSort, QuickSort. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Visualization: [`viz/sorts.html`](../viz/sorts.html) | You want to SEE the sorting algorithms in motion |
| Mock interview: [`mock_interviews/02_meeting_rooms_intervals.md`](../mock_interviews/02_meeting_rooms_intervals.md) | Sorting / interval problems in a conversation |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | BubbleSelectionInsertion | `java/1.BubbleSelectionInsertion.java` | `python/1.bubble_selection_insertion.py` | `cpp/1.bubble_selection_insertion.cpp` | `rust/s01_bubble_selection_insertion.rs` | `web/1.bubble_selection_insertion.html` |
| 2 | MergeSort | `java/2.MergeSort.java` | `python/2.merge_sort.py` | `cpp/2.merge_sort.cpp` | `rust/s02_merge_sort.rs` | `web/2.merge_sort.html` |
| 3 | QuickSort | `java/3.QuickSort.java` | `python/3.quick_sort.py` | `cpp/3.quick_sort.cpp` | `rust/s03_quick_sort.rs` | `web/3.quick_sort.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Sorting | — | `python/sorting.py` | `cpp/sorting.cpp` | `rust/sorting.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. BubbleSelectionInsertion**
- **2. MergeSort**
- **3. QuickSort**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: sorting algorithms (Bubble / Selection / Insertion / Merge / Quick).

| Approach | Time (avg) | Time (worst) | Space | Stable? | When to prefer |
|----------|------|------|-------|---------|----------------|
| Bubble sort | O(N²) | O(N²) | O(1) | Yes | Teaching only — never in production |
| Selection sort | O(N²) | O(N²) | O(1) | No | When writes are expensive (minimizes swaps) |
| Insertion sort | O(N²) | O(N²) | O(1) | Yes | Nearly-sorted data, small N (~16), inner loop of hybrid sorts |
| Merge sort | O(N log N) | O(N log N) | O(N) | Yes | Stability matters, linked lists, external sorting |
| Quick sort (random pivot) | O(N log N) | O(N²) | O(log N) | No | General-purpose in-memory, cache-friendly |
| Heap sort | O(N log N) | O(N log N) | O(1) | No | Worst-case guarantees with O(1) space |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Picking the first or last element as quicksort pivot on sorted input** — degrades to O(N²). Randomize or use median-of-three to defeat adversarial inputs.
- **Treating merge sort's "merge" as the hard part and sloppily slicing arrays** — repeatedly copying sub-arrays turns O(N log N) memory into O(N²). Pass index ranges, not new arrays.
- **Believing "stable" means "fast"** — stability is about preserving order of equal keys, nothing about speed. Quick sort is faster than merge sort on average yet unstable.
- **Sorting a `List<Integer>` and assuming primitive performance** — boxing/unboxing adds significant overhead and breaks cache locality. Use `int[]` and `Arrays.sort` when performance matters.
- **Calling `Arrays.sort` on primitive arrays expecting a stable sort** — Java's `Arrays.sort(int[])` uses dual-pivot quicksort and is *not* stable. `Arrays.sort(Object[])` uses TimSort and *is* stable.

</details>

## Reference: how to run a topic file

<details>
<summary>Java / Python / C++ / Rust / Web one-liners</summary>


From the week's directory:

```bash
# Java
javac java/<file>.java && java -cp java <ClassName>

# Python
python3 python/<file>.py

# C++
g++ -std=c++17 cpp/<file>.cpp -o /tmp/a && /tmp/a

# Rust
rustc --edition 2021 rust/<file>.rs -o /tmp/a && /tmp/a

# Web — open in a browser
open web/<file>.html   # macOS
xdg-open web/<file>.html   # Linux
```

</details>

## Reflection prompts


- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach the merge step of merge sort to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
