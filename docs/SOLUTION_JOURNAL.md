# Solution Journal — Template

> Copy this template into a new file every time you solve a problem. The act of filling it in matters more than the file existing. Don't skip sections — empty sections are a signal that you didn't actually understand something.

The goal is not documentation. The goal is to force the *look back* step from Polya that everyone skips. Future-you reading this entry should be able to re-derive the solution without looking at the code.

---

## Template

### Problem
> One paragraph, in your own words. Don't copy the prompt. If you can't restate it, you don't understand it yet.

### Constraints & inputs
- Input types and shapes:
- Size bounds (N ≤ ?, value range, etc.):
- Time / memory limits (if any):
- Sorted? Unique? Mutable? Online or offline?:
- Implicit assumptions you're locking in:

### Worked example (by hand)
> Pick one non-trivial input. Trace the answer step by step on paper. Include at least one edge case (empty, single element, all-same, negative, max-size).

### Approaches considered (≥ 3)
List at least three. Each gets a time and space estimate. The first should usually be brute force.

1. **Brute force —** time / space:
2. **Better —** time / space:
3. **Optimal (or good enough) —** time / space:
4. *(optional)* Approaches considered and rejected, and why:

### Chosen approach + why
> Which one you picked and the reason. "It fits the constraints" is fine if you say which constraint. "It's elegant" is not.

### Implementation notes / gotchas
- Off-by-one risks:
- Integer overflow / underflow risks:
- Mutability of inputs:
- Initialization values (especially for DP tables, min/max trackers):
- Anything you got wrong on the first attempt:

### Edge cases tested
- [ ] Empty input
- [ ] Single element
- [ ] All elements equal
- [ ] Already sorted / reverse sorted
- [ ] Negative numbers / zero
- [ ] Maximum size input
- [ ] Other problem-specific cases:

### Complexity (final)
- Time:
- Space:
- Tightness — is this the proven lower bound, or could it be faster?

### What I'd do differently / what I learned
> The single most important section. One sentence on the *key insight*. One sentence on what tripped you up. One sentence on the pattern this belongs to, so you'll recognize the next instance.

---

## Worked example — filled in for "Two Sum"

### Problem
Given an integer array `nums` and an integer `target`, return the indices of the two distinct elements whose values sum to `target`. Exactly one such pair is guaranteed to exist. The same index cannot be used twice.

### Constraints & inputs
- Input: `nums: int[]`, `target: int`. Output: `int[2]`.
- `2 ≤ nums.length ≤ 10⁴`; values in `[-10⁹, 10⁹]`; `target` in same range.
- Time limit informal (~1 s). Memory not tight.
- Not sorted. Duplicates allowed. Mutability not required. Offline.
- Locked assumption: exactly one solution → no need to handle "no answer" or "multiple answers".

### Worked example (by hand)
`nums = [3, 2, 4]`, `target = 6`.
- i=0: complement of 3 is 3. Hash is empty. Store `{3: 0}`.
- i=1: complement of 2 is 4. Hash has no 4. Store `{3:0, 2:1}`.
- i=2: complement of 4 is 2. Hash has 2 at index 1. Return `[1, 2]`. Done.

Edge case `nums = [3, 3], target = 6`: at i=1, complement of 3 is 3, hash has `{3:0}` from i=0, return `[0,1]`. Good — the "no double-use" rule is enforced naturally because we look up *before* inserting the current index.

### Approaches considered

1. **Brute force — nested loop.** For each `i`, scan `j > i` checking `nums[i] + nums[j] == target`. Time O(N²), space O(1). At N=10⁴ that's 10⁸ ops — borderline but probably fine in C++, slow in Python.
2. **Sort + two pointers.** Sort, then walk left/right pointers. Time O(N log N), space O(N) because we need to remember original indices (we're returning *indices*, not values, so sorting loses information unless we pair each value with its original index).
3. **Hash map (one pass).** For each `i`, ask the hash if `target - nums[i]` was seen. If yes, return. If no, store `nums[i] → i`. Time O(N) average, space O(N).

### Chosen approach + why
Hash map, one pass. Strictly better than approach 2 in both time and space (no sort, single traversal), and dominates brute force at the upper end of N. The constraint that pushed me here: N up to 10⁴ doesn't *force* O(N), but the hash solution is simpler than the sort-with-index-pairs version, so simpler wins.

### Implementation notes / gotchas
- Look up the complement *before* inserting the current element. Otherwise an input like `[3, 3], target = 6` self-matches at i=0 and returns `[0, 0]`, which violates "two distinct indices".
- Values can be negative, so the complement can also be negative — using a hash (not an array indexed by value) is necessary.
- Return order: the problem doesn't specify, but matching the convention `[smaller_index, larger_index]` falls out naturally because we discover the earlier index first.

### Edge cases tested
- [x] Smallest input: `[1, 2], target = 3` → `[0, 1]`.
- [x] Duplicates that form the pair: `[3, 3], target = 6` → `[0, 1]`.
- [x] Negative values: `[-1, -2, -3, -4], target = -7` → `[2, 3]`.
- [x] Target involves zero: `[0, 4, 3, 0], target = 0` → `[0, 3]`.
- [x] Large-ish input (N = 10⁴, random) — runs in milliseconds.

### Complexity (final)
- Time: O(N) average. Worst case O(N²) if the hash adversarially collides, but practically O(N).
- Space: O(N) for the hash.
- Tightness: O(N) is a proven lower bound for unsorted input — you must look at every element at least once in the worst case.

### What I'd do differently / what I learned
**Key insight:** I don't have to *search for the pair*; I only have to ask whether the complement *exists*. Search-to-existence-query is a portable move — it also drives 3Sum (fix one, two-sum the rest), 4Sum, and "subarray sum equals K" (prefix-sum hash). **What tripped me up:** my first attempt inserted before looking up, which broke the duplicate case. **Pattern:** hash-for-complement. Any problem of the form "find x, y such that f(x, y) = target" where f is invertible in one argument fits this mold.
