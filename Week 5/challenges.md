# Week 5 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Tower of Hanoi With 4 Pegs (Frame–Stewart)

**Spec**:
Solve Tower of Hanoi with **four** pegs instead of three. Read `n` (number of disks). Print the minimum number of moves required and the move sequence (one move per line as `MOVE disk from peg A to peg C`). Use the Frame–Stewart algorithm: choose some `k`, recursively move the top `k` disks to a spare peg using all four pegs, move the remaining `n-k` disks using three pegs, then move the `k` disks onto the destination using all four pegs. Choose `k` to minimize total moves (the optimal `k` for small n is well-known).

**Constraints**:
- Input size: `1 <= n <= 16`
- Time: roughly O(2^sqrt(2n)) moves printed
- Memory: O(n) recursion

**Test inputs**:
| Input | Expected minimum moves |
|-------|------------------------|
| `1` | `1` |
| `3` | `5` |
| `4` | `9` |
| `8` | `33` |
| `15` | `129` |

**Stretch**: Generalize to `p` pegs and `n` disks. The OEIS sequence is A007664.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Mutual Recursion: Hofstadter Female/Male

**Spec**:
Implement Hofstadter's mutually recursive sequences:
- `F(0) = 1`, `M(0) = 0`
- `F(n) = n - M(F(n-1))` for `n > 0`
- `M(n) = n - F(M(n-1))` for `n > 0`

Read `n` and print `F(n)` and `M(n)` on one line, space-separated. Implement naively first to feel the recursion blow up, then add memoization. Compare wall-clock times in your journal.

**Constraints**:
- Input size: `0 <= n <= 10000` (memoized) / `0 <= n <= 30` (naive)
- Time (memoized): O(n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output (F M) |
|-------|-----------------------|
| `0` | `1 0` |
| `1` | `1 0` |
| `5` | `3 3` |
| `10` | `6 6` |
| `20` | `13 12` |

**Stretch**: Find the smallest `n` such that `F(n) != M(n)`, and explain in your journal.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Print All Subsets Without Auxiliary Array

**Spec**:
Read a space-separated list of distinct integers. Print all subsets, one per line, in any order. Use recursion (the include/exclude pattern) but **do not** maintain a separate "current subset" list — pass the subset by appending and removing characters in a single mutable `StringBuilder`/`String`, or by passing slices, depending on language. The aim is to feel the call stack as the data structure.

**Constraints**:
- Input size: up to 16 integers (so up to 65536 subsets)
- Time: O(2^n * n)
- Memory: O(n) recursion depth

**Test inputs**:
| Input | Expected output count |
|-------|-----------------------|
| (empty) | 1 (empty subset) |
| `1` | 2: `{}`, `{1}` |
| `1 2 3` | 8 subsets, including `{}`, `{1}`, `{2}`, `{3}`, `{1,2}`, `{1,3}`, `{2,3}`, `{1,2,3}` |
| `1 2 3 4` | 16 subsets |

**Stretch**: Print them in Gray code order — each consecutive subset differs from the previous by adding or removing exactly one element.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
