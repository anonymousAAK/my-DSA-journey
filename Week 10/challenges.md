# Week 10 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: In-Place 90° Matrix Rotation

**Spec**:
Read `n` followed by an `n x n` integer matrix. Rotate the matrix 90° clockwise **in place** (O(1) extra memory). Don't allocate a new matrix. Two acceptable techniques: (a) transpose then reverse each row, or (b) rotate in 4-element cycles ring-by-ring.

**Constraints**:
- Input size: `1 <= n <= 1000`
- Time: O(n^2)
- Memory: O(1) extra

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=2 / 1 2 / 3 4` | `3 1 / 4 2` |
| `n=3 / 1 2 3 / 4 5 6 / 7 8 9` | `7 4 1 / 8 5 2 / 9 6 3` |
| `n=1 / 42` | `42` |
| `n=4 / 1..16` | rotated 4x4 |

**Stretch**: Rotate by any multiple of 90° given as a parameter (`90`, `180`, `270`).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Set Matrix Zeroes With O(1) Extra Space

**Spec**:
Read an `m x n` matrix of integers. If a cell is 0, set its entire row and column to 0. Do it in place with O(1) extra space — you may not use a `boolean[m] + boolean[n]` (that's O(m+n)).

Hint: use the first row and first column themselves as the markers, but save two flags to remember whether the first row/column originally contained a zero.

**Constraints**:
- Input size: `1 <= m, n <= 1000`
- Time: O(m * n)
- Memory: O(1) extra

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `2 3 / 1 1 1 / 1 0 1` | `1 0 1 / 0 0 0` |
| `3 3 / 0 1 2 / 3 4 5 / 1 3 1` | `0 0 0 / 0 4 5 / 0 3 1` |
| `1 1 / 0` | `0` |
| `1 1 / 5` | `5` |

**Stretch**: Same problem but you must also count and report how many cells changed.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Search a Row- and Column-Sorted Matrix in O(m + n)

**Spec**:
Read `m`, `n`, a target, and an `m x n` matrix where each row is sorted ascending and each column is sorted ascending. Print `1` if target is present, else `0`. Required complexity O(m + n) — binary search per row is O(m log n) and acceptable for partial credit, but the staircase walk (start from top-right, move left if too big, down if too small) is the target solution.

**Constraints**:
- Input size: `1 <= m, n <= 10^4`, values up to `10^9`
- Time: O(m + n)
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `m=3 n=3 target=5 / 1 4 7 / 2 5 8 / 3 6 9` | `1` |
| `m=3 n=3 target=10 / 1 4 7 / 2 5 8 / 3 6 9` | `0` |
| `m=1 n=1 target=1 / 1` | `1` |
| `m=4 n=4 target=15 / 1 5 9 13 / 2 6 10 14 / 3 7 11 15 / 4 8 12 16` | `1` |

**Stretch**: Now also return the (row, col) coordinates. If multiple matches, return the one with the smallest row, then smallest col.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Maximum Rectangle of 1s in a Binary Matrix

**Spec**:
Read `m`, `n`, and a binary `m x n` matrix. Find the area of the largest axis-aligned rectangle consisting entirely of `1`s. Required complexity O(m * n). Technique: for each row, build a histogram of consecutive 1s ending at that row, then find the largest rectangle in the histogram using a monotonic stack.

**Constraints**:
- Input size: `1 <= m, n <= 1000`
- Time: O(m * n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `m=4 n=5 / 1 0 1 0 0 / 1 0 1 1 1 / 1 1 1 1 1 / 1 0 0 1 0` | `6` |
| `m=1 n=1 / 0` | `0` |
| `m=2 n=2 / 1 1 / 1 1` | `4` |
| `m=3 n=3 / 0 1 1 / 1 1 1 / 1 1 0` | `4` |

**Stretch**: Largest **square** of 1s (different problem — DP with `dp[i][j] = min(neighbors)+1`).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
