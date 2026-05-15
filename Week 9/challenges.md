# Week 9 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Count Inversions Using Merge Sort

**Spec**:
Read `n` and `n` integers. An inversion is a pair `(i, j)` with `i < j` and `a[i] > a[j]`. Print the total number of inversions. The brute O(n^2) solution is forbidden. Solve in O(n log n) by adapting merge sort: when merging two halves, every time you take an element from the right half before an element from the left half, the remaining elements in the left half all form inversions.

**Constraints**:
- Input size: `1 <= n <= 10^6`, values in `[-10^9, 10^9]`
- Time: O(n log n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=5 / 1 2 3 4 5` | `0` |
| `n=5 / 5 4 3 2 1` | `10` |
| `n=4 / 2 4 1 3` | `3` |
| `n=6 / 3 1 4 1 5 9` | `3` |

**Stretch**: Count "significant" inversions: pairs where `a[i] > 2 * a[j]`. Same complexity, different merge step.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Quickselect — k-th Smallest in Expected O(n)

**Spec**:
Read `n`, `k`, and `n` integers. Print the `k`-th smallest (1-indexed). Use quickselect with **randomized pivot**. Don't fully sort. Implement Lomuto or Hoare partition from scratch.

**Constraints**:
- Input size: `1 <= k <= n <= 10^7`, values up to `10^9`
- Time: expected O(n)
- Memory: O(1) extra (recursion may be eliminated via tail call / loop)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=5 k=1 / 3 1 4 1 5` | `1` |
| `n=5 k=3 / 3 1 4 1 5` | `3` |
| `n=5 k=5 / 3 1 4 1 5` | `5` |
| `n=1 k=1 / 42` | `42` |
| `n=7 k=4 / 7 6 5 4 3 2 1` | `4` |

**Stretch**: Worst-case O(n) using the median-of-medians pivot selection ("BFPRT" / "Introselect"). Compare wall time to the randomized version.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Stable Sort In Place Without `O(n log n)` Auxiliary

**Spec**:
Implement a stable sort that uses O(1) auxiliary memory beyond the input array (no merge sort with a side buffer). Two acceptable approaches: a careful insertion sort (O(n^2) but stable) for small `n`, OR an in-place merge sort using block rotations (Kronrod's algorithm — hard). Pick one and implement.

For grading: with `n <= 5000`, expect O(n^2) insertion sort. Stability is verified by sorting pairs `(key, original_index)` and checking original indices remain ascending within equal-key groups.

**Constraints**:
- Input size: `1 <= n <= 5000`
- Time: O(n^2) acceptable
- Memory: O(1) auxiliary

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| pairs `(3,0)(1,1)(3,2)(2,3)(1,4)` | sorted: `(1,1)(1,4)(2,3)(3,0)(3,2)` |
| `n=5 / 5 4 3 2 1` | `1 2 3 4 5` |
| `n=6 / 4 2 4 2 4 2` | `2 2 2 4 4 4` (original indices preserved within ties) |

**Stretch**: Implement true in-place stable merge sort with block rotations, achieving O(n log n) time.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: External / Bucket Sort for 1B Integers (Conceptual + Mini Implementation)

**Spec**:
Imagine sorting 1 billion 32-bit integers that don't fit in RAM. Implement a small-scale demo: read `n` integers from stdin where `n` may exceed your imagined "memory budget" of `B`. Split into chunks of `B`, sort each chunk in memory, write each chunk to a temp file, then k-way merge the chunks (use a small heap of size = number of chunks). Print the sorted output.

Treat `B` as a parameter (read on the first line). Use real temp files (you must write to disk and read back).

**Constraints**:
- Input size: `1 <= n <= 10^6`, `B` small (e.g. 1000)
- Time: O(n log n) total, but with disk I/O
- Memory: O(B)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `B=2 n=5 / 3 1 4 1 5` | `1 1 3 4 5` |
| `B=4 n=10 / random ints` | sorted ascending |
| `B=1 n=4 / 9 7 5 3` | `3 5 7 9` (each chunk size 1) |

**Stretch**: Implement parallel merge (multi-threaded read of chunks).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
