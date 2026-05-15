# Week 18 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Coin Change — Number of Ways (Unbounded)

**Spec**:
Read `k`, `n`, `target`, and `n` coin denominations. Print the number of distinct combinations (order does **not** matter) that sum to `target`, where each coin can be used unlimited times. Use 1D DP with the coins as the outer loop (this is the key trick — outer coins, inner amount — to avoid counting permutations).

**Constraints**:
- `1 <= n <= 100`, `1 <= target <= 5000`
- Time: O(n * target)
- Memory: O(target)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=3 target=5 coins=1 2 5` | `4` |
| `n=1 target=3 coins=2` | `0` |
| `n=1 target=10 coins=10` | `1` |
| `n=4 target=10 coins=2 5 3 6` | `5` |
| `n=2 target=0 coins=1 2` | `1` (empty combination) |

**Stretch**: Number of distinct ordered tuples (sequences) — different DP structure (outer amount, inner coins).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Longest Increasing Subsequence in O(n log n)

**Spec**:
Read `n` and `n` integers. Print the length of the longest strictly increasing subsequence. Required complexity O(n log n) using patience sorting (maintain `tails[k]` = smallest tail of any increasing subsequence of length `k+1`; binary-search to update). The O(n^2) classic DP is forbidden.

**Constraints**:
- `1 <= n <= 10^6`, values up to `10^9`
- Time: O(n log n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=8 / 10 9 2 5 3 7 101 18` | `4` (e.g. `2 3 7 18`) |
| `n=5 / 5 4 3 2 1` | `1` |
| `n=5 / 1 2 3 4 5` | `5` |
| `n=1 / 7` | `1` |
| `n=6 / 0 8 4 12 2 10` | `3` |

**Stretch**: Also reconstruct the actual subsequence (track parent pointers).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Edit Distance With Path Reconstruction

**Spec**:
Read two strings `a` and `b`. Compute the Levenshtein distance (insert/delete/substitute, each cost 1). Then reconstruct one optimal edit script as a sequence of operations: `INSERT x`, `DELETE x`, `SUBSTITUTE x y`, `MATCH x`. Print the distance, then the script.

**Constraints**:
- `1 <= |a|, |b| <= 2000`
- Time: O(|a| * |b|)
- Memory: O(|a| * |b|) for reconstruction; O(min(|a|,|b|)) for distance only

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `a=horse b=ros` | `3` with one valid script (e.g., DELETE h, SUBSTITUTE r r, MATCH o, DELETE s, MATCH e?...) — verify by recomputing distance from script |
| `a=intention b=execution` | `5` |
| `a=abc b=abc` | `0`, all MATCH |
| `a=abc b=(empty)` | `3`, all DELETE |

**Stretch**: Hirschberg's algorithm — distance + reconstruction in O(|a| * |b|) time, O(min(|a|,|b|)) memory.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: 0/1 Knapsack With Item Reconstruction

**Spec**:
Read `n`, `W`, and `n` `(weight, value)` pairs. Print the maximum total value achievable with total weight `<= W`, and the indices (1-indexed) of one optimal item set. Use the standard O(n W) DP table; reconstruct by walking backward.

**Constraints**:
- `1 <= n <= 1000`, `1 <= W <= 10^5`
- Time: O(n W)
- Memory: O(n W)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=4 W=5 / (2,3)(3,4)(4,5)(5,6)` | value `7`, items `{1,2}` |
| `n=1 W=0 / (1,1)` | `0`, `{}` |
| `n=3 W=50 / (10,60)(20,100)(30,120)` | `220`, `{2,3}` |
| `n=1 W=1 / (1,1000)` | `1000`, `{1}` |

**Stretch**: Solve with O(W) memory and still reconstruct (trickier; one technique is divide-and-conquer over the items).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
