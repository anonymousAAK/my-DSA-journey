# Week 8 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which search pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given a sorted array of n ≤ 10^6 integers and a target value, decide if the target exists in the array. Per-query time must be O(log n).
Pattern: ______
Why: ______

### 2. Given a sorted array with duplicates, find the index of the first occurrence of a target value, or −1 if absent.
Pattern: ______
Why: ______

### 3. Given an array of bananas piles (sizes up to 10^9) and h hours, find the minimum integer eating speed `k` such that all piles are eaten within h hours. n ≤ 10^5.
Pattern: ______
Why: ______

### 4. Given a rotated sorted array (rotated once, no duplicates), find a target element in O(log n).
Pattern: ______
Why: ______

### 5. Distractor: Given a sorted array of n integers, find a pair summing to target. n ≤ 10^5. (Yes, you *could* binary-search, but is that what you'd reach for?)
Pattern: ______
Why: ______

### 6. Given a monotonically increasing function `f : int → int` defined on `[1, 10^9]` accessible only as a black box, find the smallest `x` such that `f(x) ≥ K`.
Pattern: ______
Why: ______

### 7. Given an array, split it into `m` contiguous parts so that the maximum part-sum is minimized. n ≤ 10^4.
Pattern: ______
Why: ______

### 8. Find the integer square root of n (largest `k` with `k*k ≤ n`), n up to 10^18.
Pattern: ______
Why: ______

### 9. Distractor: Given an unsorted array, find the maximum element. (Why is this *not* a Week 8 problem?)
Pattern: ______
Why: ______

### 10. Given two sorted arrays of sizes m and n, find the median of the combined collection in O(log(min(m,n))).
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Classical binary search. **Why**: sorted + O(log n) requirement → halve the search range.
2. **Pattern**: Lower-bound binary search. **Why**: binary-search the leftmost index where `a[i] >= target`; check equality.
3. **Pattern**: Binary search on the answer. **Why**: predicate "can finish at speed k?" is monotone in k — search the smallest feasible k.
4. **Pattern**: Modified binary search on rotated array. **Why**: one half is always sorted; pick the side containing the target.
5. **Pattern**: Two pointers (NOT binary search). **Why**: sorted + pair-sum is two-pointer territory; binary searching each element is O(n log n) vs O(n). This is the disambiguation drill.
6. **Pattern**: Binary search on monotone predicate (lower bound). **Why**: f monotone → search smallest x with f(x) ≥ K; possibly exponential-search bounds first.
7. **Pattern**: Binary search on the answer (parametric search). **Why**: feasibility "can split with max-part ≤ S?" is monotone in S; binary-search smallest feasible S.
8. **Pattern**: Binary search on the answer. **Why**: `k*k ≤ n` is monotone — bisect over [0, 2·10^9].
9. **Pattern**: Distractor — linear scan O(n). **Why**: unsorted → can't binary search; this checks whether the learner blindly reaches for binary search.
10. **Pattern**: Binary search partitioning. **Why**: search the partition point in the smaller array — the canonical hard binary-search problem.

</details>
