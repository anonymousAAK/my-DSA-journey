# Week 8 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Closest Element in a Rotated Sorted Array

**Spec**:
Read `n`, `target`, and a rotated sorted array (originally ascending, then rotated by some unknown amount, all distinct). Print the element in the array closest in absolute value to `target`. If two elements tie, print the smaller. Required complexity O(log n) — no scanning, no sort. You must first locate the pivot in O(log n), then run two bounded binary searches.

**Constraints**:
- Input size: `1 <= n <= 10^6`, values in `[-10^9, 10^9]`
- Time: O(log n)
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=7 target=3 / 4 5 6 7 0 1 2` | `2` (distance 1) or `4` (distance 1) → smaller: `2` |
| `n=5 target=0 / 3 4 5 1 2` | `1` |
| `n=1 target=42 / 7` | `7` |
| `n=4 target=100 / 7 8 1 5` | `8` |

**Stretch**: Allow duplicates in the array (worst case O(n) for the pivot; analyze when).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Painter's Partition (Binary Search on Answer)

**Spec**:
Read `n`, `k`, and `n` non-negative integers representing board lengths. Partition the boards into `k` contiguous groups so as to minimize the maximum group sum. Print this minimum maximum sum.

You must use binary search on the answer (low = max element, high = total sum; check feasibility greedily). Do not solve it with DP — that's a different problem.

**Constraints**:
- Input size: `1 <= n <= 10^5`, `1 <= k <= n`, values up to `10^9`
- Time: O(n log(total sum))
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=5 k=2 / 10 20 30 40 50` | `90` |
| `n=4 k=4 / 10 20 30 40` | `40` |
| `n=4 k=1 / 10 20 30 40` | `100` |
| `n=7 k=3 / 1 2 3 4 5 6 7` | `11` |

**Stretch**: Output the actual partition (the indices where you cut).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Median of Two Sorted Arrays in O(log min(n,m))

**Spec**:
Read two sorted arrays `A` and `B` (sizes `n` and `m`). Print the median of the combined array. Required complexity O(log min(n, m)). The "merge then take middle" O(n+m) approach is forbidden; do partition-based binary search across the shorter array.

**Constraints**:
- Input size: `0 <= n, m <= 10^6`, at least one non-empty
- Time: O(log min(n, m))
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `A=[1,3] B=[2]` | `2.0` |
| `A=[1,2] B=[3,4]` | `2.5` |
| `A=[] B=[1]` | `1.0` |
| `A=[0,0] B=[0,0]` | `0.0` |
| `A=[1,2,3,4] B=[5,6,7,8,9,10]` | `5.5` |

**Stretch**: Generalize to `k` sorted arrays; what is the best complexity you can achieve?

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Aggressive Cows / Maximum Minimum Distance

**Spec**:
Read `n`, `k`, and `n` stall positions on a number line (1D coordinates). Place `k` cows in stalls so that the **minimum** distance between any two cows is maximized. Print that maximum-min distance. Sort positions first, then binary search on the distance: for a candidate `d`, greedily place cows from left to right whenever they are at least `d` apart.

**Constraints**:
- Input size: `2 <= k <= n <= 10^5`, positions up to `10^9`
- Time: O(n log n + n log(max position))
- Memory: O(1) past sorting

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=5 k=3 / 1 2 8 4 9` | `3` |
| `n=4 k=2 / 1 5 10 20` | `19` |
| `n=5 k=5 / 1 2 3 4 5` | `1` |
| `n=4 k=4 / 1 10 100 1000` | `9` |

**Stretch**: Same but a stall has a "capacity" — multiple cows allowed up to capacity — and you must place exactly `k` cows.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
