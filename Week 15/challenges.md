# Week 15 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Build a Binary Heap From an Array in O(n)

**Spec**:
Read `n` and `n` integers. Convert the array into a max-heap **in place** in O(n) time. Don't `siftUp` for each element — that's O(n log n). Use the classic Floyd build-heap: iterate from `n/2 - 1` down to 0 and `siftDown` each. Print the array post-heapify and prove (in your journal) the O(n) bound via the telescoping sum.

**Constraints**:
- `1 <= n <= 10^7`
- Time: O(n)
- Memory: O(1)

**Test inputs**:
| Input | Expected output (one valid heap) |
|-------|----------------------------------|
| `n=5 / 3 1 4 1 5` | e.g. `5 3 4 1 1` (parent >= children at every index) |
| `n=1 / 7` | `7` |
| `n=6 / 1 2 3 4 5 6` | one valid max-heap |
| `n=3 / 9 9 9` | `9 9 9` |

**Stretch**: Build a min-heap; then implement heapsort in O(n log n) using the heap.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Running Median from a Stream

**Spec**:
Process a stream of integers; after each new integer, print the median of all integers received so far. Required: O(log n) per insertion using two heaps (max-heap of lower half, min-heap of upper half) kept balanced (size difference at most 1). The O(n) "insert into sorted array" approach is forbidden.

**Constraints**:
- Stream length up to `10^6`
- Time: O(log n) per insert
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `2 1 5 7 2 0 5` | `2 1.5 2 3 2 2 2` |
| `1` | `1` |
| `1 2` | `1 1.5` |
| `5 4 3 2 1` | `5 4.5 4 3.5 3` |

**Stretch**: After each insert, also print the running mode (most frequent value). Use a hashmap-of-counts plus a "counts-to-set-of-values" map.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: K-th Largest Element With Constant-Memory Online Selection

**Spec**:
Process a stream and, after every insert, print the `k`-th largest value seen so far (or `-1` if fewer than `k` values). Required: O(log k) per insert, O(k) memory. Technique: a min-heap of size `k` — the heap's root is the k-th largest.

**Constraints**:
- `1 <= k <= 10^5`, stream up to `10^7`
- Time: O(log k) per insert
- Memory: O(k)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `k=3 / 4 5 8 2 3 6 1 5` | `-1 -1 4 4 4 5 5 5` |
| `k=1 / 1 2 3` | `1 2 3` |
| `k=5 / 10 20` | `-1 -1` |

**Stretch**: Same problem but support deletions too (lazy deletion: keep a "removed" multiset and skip stale tops).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Merge K Sorted Streams With a Tournament Heap

**Spec**:
Given `k` infinite sorted streams (simulate via a generator/iterator per stream), produce the merged sorted stream lazily. Each element of the merged output must be produced in O(log k). Memory must be O(k) — you may never materialize a stream fully.

**Constraints**:
- `1 <= k <= 10^4`, demonstrate first 1000 elements of merged output
- Time: O(log k) per output element
- Memory: O(k)

**Test inputs**:
| Input | Expected first 10 of merged |
|-------|-----------------------------|
| `k=3 streams: [1,4,7,...], [2,5,8,...], [3,6,9,...]` (arithmetic progressions) | `1 2 3 4 5 6 7 8 9 10` |
| `k=2 streams: even ints, odd ints` | `0 1 2 3 4 5 6 7 8 9` |
| `k=4 streams: [n], [n^2], [n^3], [n^4] for n=1,2,3,...` | `1 1 1 1 2 4 8 16 3 9` (interleaved by value) |

**Stretch**: Lazy K-way merge of `k` streams where `k` itself grows over time (you discover new streams as you go).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
