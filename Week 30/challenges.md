# Week 30 — Hard Mode Challenges (Final Boss)

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

These are the five challenges you should be able to solve at interview pace by the end of this curriculum. If you can't, go back and re-do the weeks they exercise.

---

## Challenge 1: Sliding Window — Minimum Window Substring (LC 76)

**Spec**:
Read strings `s` and `t`. Find the shortest substring of `s` that contains every character of `t` (counting multiplicity). If no such substring exists, print empty. Required: O(|s| + |t|) using a sliding window with a "need vs. have" map and a `matched` counter.

**Constraints**:
- `1 <= |s|, |t| <= 10^5`, ASCII characters
- Time: O(|s| + |t|)
- Memory: O(|t|)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `s=ADOBECODEBANC t=ABC` | `BANC` |
| `s=a t=a` | `a` |
| `s=a t=aa` | (empty) |
| `s=aaaaaaab t=aab` | `aab` |
| `s=abc t=cba` | `abc` |

**Stretch**: Same but `t` may contain wildcards (`?` matches any single char in `s`).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Top-K — K Closest Points to Origin in Expected Linear Time

**Spec**:
Read `n` 2D points and `k`. Print the `k` points closest to the origin (in any order). Required: expected O(n) using quickselect on squared distance. A heap-of-size-k solution is O(n log k) and acceptable for partial credit only.

**Constraints**:
- `1 <= k <= n <= 10^6`
- Time: expected O(n)
- Memory: O(n) (the array itself)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `k=2 points=(1,3)(-2,2)` | `(-2,2)(1,3)` (closest first or any order) |
| `k=1 points=(3,3)(5,-1)(-2,4)` | `(3,3)` |
| `k=3 points=(0,0)(1,1)(2,2)(3,3)` | `(0,0)(1,1)(2,2)` |
| `k=1 points=(5,0)` | `(5,0)` |

**Stretch**: Streaming variant — infinite stream, maintain top-k by smallest distance in O(log k) per point.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Merge Intervals — Insert New Interval Into Sorted Set

**Spec**:
Read a list of non-overlapping intervals sorted by start, then a new interval. Insert and merge in O(n). Print the resulting interval list. Don't re-sort.

Algorithm: copy intervals that end before new starts; merge intervals overlapping the new one (update bounds); copy intervals that start after new ends.

**Constraints**:
- `1 <= n <= 10^6`
- Time: O(n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `[[1,3][6,9]] insert [2,5]` | `[[1,5][6,9]]` |
| `[[1,2][3,5][6,7][8,10][12,16]] insert [4,8]` | `[[1,2][3,10][12,16]]` |
| `[] insert [5,7]` | `[[5,7]]` |
| `[[1,5]] insert [6,8]` | `[[1,5][6,8]]` |
| `[[1,5]] insert [0,0]` | `[[0,0][1,5]]` |

**Stretch**: Online: process a stream of new intervals, maintaining the merged set; each insertion in O(log n) using a balanced BST keyed by start.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Fast/Slow Pointers — Happy Number

**Spec**:
A number is happy if repeatedly replacing it with the sum of squares of its digits eventually reaches 1. Otherwise the iteration enters a cycle. Read `n`; print `1` if happy, else `0`. Required: O(1) extra memory using Floyd's cycle detection (slow/fast pointers on the iteration).

**Constraints**:
- `1 <= n <= 2^31 - 1`
- Time: O(log n) per step, bounded number of steps
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `19` | `1` (19 -> 82 -> 68 -> 100 -> 1) |
| `2` | `0` |
| `1` | `1` |
| `7` | `1` |
| `4` | `0` |

**Stretch**: For all `n` in `[1, N]`, count how many are happy. Compute the cycle for unhappy numbers (it's always `4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4`).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: Two Pointers — Trapping Rain Water in O(n) Time, O(1) Space

**Spec**:
Read `n` and `n` non-negative heights. Compute the total volume of water trapped between bars after rain. Required: O(n) time, **O(1) extra space** (no prefix-max arrays). Technique: two pointers `l`, `r` with running `leftMax`, `rightMax`; at each step move the side with the smaller bar and accumulate water.

**Constraints**:
- `1 <= n <= 10^6`, heights in `[0, 10^5]`
- Time: O(n)
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=12 / 0 1 0 2 1 0 1 3 2 1 2 1` | `6` |
| `n=6 / 4 2 0 3 2 5` | `9` |
| `n=1 / 5` | `0` |
| `n=2 / 5 5` | `0` |
| `n=3 / 5 0 5` | `5` |

**Stretch**: 2D version (LC 407 — trapping rain water in a grid). Use a min-heap of boundary cells.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
