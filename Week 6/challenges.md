# Week 6 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Kadane That Returns the Subarray (Plus One Removal)

**Spec**:
Read `n` and then `n` integers. Find the maximum-sum contiguous subarray **with at most one element removed**, and print both the maximum sum and the actual subarray (start index, end index, removed index or `-1`, the array slice). Empty subarray is allowed and has sum 0; report `-1 -1 -1` indices in that case.

**Constraints**:
- Input size: `1 <= n <= 10^5`, values in `[-10^4, 10^4]`
- Time: O(n)
- Memory: O(n) or O(1) auxiliary

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `5 / 1 -2 0 3 4` | sum `8`, indices `0..4`, removed `1`, slice `[1,0,3,4]` |
| `4 / -1 -1 -1 -1` | sum `0`, empty subarray |
| `5 / 1 -10 5 -10 5` | sum `10`, removed one of the `-10`s |
| `6 / -3 1 2 3 -1 4` | sum `10`, removed `-1` |

**Stretch**: Allow up to `k` removals.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: In-Place Multi-Block Rotation

**Spec**:
Read `n`, `k`, and `n` integers. Rotate the array left by `k` positions **in place** using O(1) extra memory. Don't use slicing into a new buffer. Required technique: three-reversal trick OR cyclic-replacement using gcd. Print the final array.

**Constraints**:
- Input size: `1 <= n <= 10^6`, `0 <= k <= 10^9`
- Time: O(n)
- Memory: O(1) auxiliary

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `5 2 / 1 2 3 4 5` | `3 4 5 1 2` |
| `5 7 / 1 2 3 4 5` | `3 4 5 1 2` (k mod n) |
| `1 100 / 42` | `42` |
| `6 3 / 1 2 3 4 5 6` | `4 5 6 1 2 3` |

**Stretch**: Now rotate by `k` to the **right** instead. Then: support an array of `n` "blocks" each of size `b`, and rotate at the block level, still in place.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Three-Way Partition Around a Range

**Spec**:
Read `n`, `lo`, `hi`, and `n` integers. Rearrange the array in place so that all elements `< lo` come first, then all in `[lo, hi]`, then all `> hi`. Within each group, relative order is **not** required to be preserved. Use a single pass (Dutch National Flag generalization) with O(1) extra memory.

**Constraints**:
- Input size: `1 <= n <= 10^6`
- Time: O(n)
- Memory: O(1)

**Test inputs**:
| Input | Expected output (one valid permutation) |
|-------|-----------------------------------------|
| `7 3 6 / 1 8 2 7 3 5 6` | e.g. `1 2 3 5 6 7 8` |
| `5 0 0 / 0 0 0 0 0` | `0 0 0 0 0` |
| `5 10 20 / 5 25 15 30 10` | `5 15 10 30 25` (or any valid three-way) |
| `1 0 100 / 50` | `50` |

**Stretch**: Same problem but you must also preserve relative order within each group (stable three-way partition) using O(n) extra memory.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Missing AND Repeated Numbers in [1..n]

**Spec**:
You are given an array of length `n` that should contain each integer in `[1..n]` exactly once, but one value `a` appears twice and another value `b` is missing. Find both. Use **only O(1) extra memory**. Don't sort the array; don't use a frequency array sized `n`.

Hint: XOR all values with `1..n`; you get `a XOR b`. Then split into two groups using a set bit of that XOR.

**Constraints**:
- Input size: `1 <= n <= 10^7`
- Time: O(n)
- Memory: O(1)

**Test inputs**:
| Input | Expected output (`a b`) |
|-------|-------------------------|
| `4 / 1 2 2 4` | `2 3` |
| `1 / 1` | impossible (need n >= 2; test guard) |
| `5 / 3 1 2 5 3` | `3 4` |
| `6 / 1 1 2 3 4 5` | `1 6` |

**Stretch**: Same problem but now **two** values are repeated and **two** are missing. (Harder; needs more care with grouping.)

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
