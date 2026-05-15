# Week 4 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Hollow Diamond With Border

**Spec**:
Read an odd integer `n >= 3`. Print a "hollow diamond" of total height `n`. The diamond has `*` on its border only — interior is spaces. The widest row has `n` stars positioned with the leftmost and rightmost being `*` and everything between being a space (or just one `*` for n = 1 / first row). Use only nested loops over rows and columns. No string multiplication operators.

**Constraints**:
- Input size: `n` odd, `3 <= n <= 99`
- Time: O(n^2)
- Memory: O(1) extra

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `3` | ` * ` / `* *` / ` * ` |
| `5` | `  *  ` / ` * * ` / `*   *` / ` * * ` / `  *  ` |
| `7` | hollow diamond of height 7 with two slanted edges and spaces inside |

**Stretch**: Fill the inside with the digits `0..9` cycling row-by-row instead of spaces (still keep border `*`).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Pascal's Triangle as a Pattern

**Spec**:
Read an integer `n` (`1 <= n <= 20`). Print the first `n` rows of Pascal's triangle, centered, with each entry right-padded to a fixed width derived from the largest number in the last row. Compute each entry using `C(i, j) = C(i-1, j-1) + C(i-1, j)` — do not call any factorial library, and do not allocate a full 2D array of size `n^2` unless that's truly your simplest approach (try rolling rows).

**Constraints**:
- Input size: `1 <= n <= 20`
- Time: O(n^2)
- Memory: O(n) (rolling) or O(n^2) (naive — note in journal)

**Test inputs**:
| Input | Expected output (row count) |
|-------|-----------------------------|
| `1` | `1` |
| `3` | `  1  ` / ` 1 1 ` / `1 2 1` |
| `5` | rows for n=5, last row `1 4 6 4 1` |
| `7` | rows for n=7, last row `1 6 15 20 15 6 1` |

**Stretch**: Replace each entry with `entry mod 2` and observe the Sierpinski triangle pattern for large `n`.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Rotating Spiral Letter Pattern

**Spec**:
Read `n` (`1 <= n <= 26`). Print an `n x n` grid where cell `(0,0)` is `A`, `(0,1)` is `B`, ... laid out as an inward-going spiral starting from the top-left, going right, then down, then left, then up. Cycle through the alphabet (`A..Z` then back to `A`). Use only nested loops and four direction variables — no extra grid traversal libraries.

**Constraints**:
- Input size: `1 <= n <= 26`
- Time: O(n^2)
- Memory: O(n^2) for the grid

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `1` | `A` |
| `3` | `ABC` / `HIB` (wait — verify) / Actually: `ABC` / `HID` / `GFE` |
| `4` | `ABCD` / `LMNE` / `KPOF` / `JIHG` |
| `5` | spiral with `Y` at the center (25 letters fit perfectly) |

**Stretch**: Same problem but spiral *outward* from the center.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
