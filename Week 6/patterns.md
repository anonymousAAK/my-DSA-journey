# Week 6 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which array pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given an array of `n` integers (n ≤ 10^5, values may be negative), find the contiguous subarray with maximum sum. Return the sum.
Pattern: ______
Why: ______

### 2. You are given an array containing only the values 0, 1, and 2 in arbitrary order. Sort it in place in a single pass without using any sorting library. n ≤ 10^6.
Pattern: ______
Why: ______

### 3. Given an array of size n and an integer k, rotate the array to the right by k positions, in place, using O(1) extra space.
Pattern: ______
Why: ______

### 4. Given an array `a` of length n and many queries `(l, r)` each asking the sum of `a[l..r]`, answer each query in O(1).
Pattern: ______
Why: ______

### 5. Distractor: Given a sorted array, find two indices whose values sum to a target. (Looks like Week 6, but what's the cleanest approach?)
Pattern: ______
Why: ______

### 6. Given an array, move all zeros to the end, preserving the relative order of non-zero elements. In place.
Pattern: ______
Why: ______

### 7. Given an array of integers, find the element that appears more than n/2 times (a "majority element"). Guaranteed to exist. O(n) time, O(1) space.
Pattern: ______
Why: ______

### 8. Given an array, return a new array where `out[i]` is the product of all elements except `a[i]`. No division allowed. O(n).
Pattern: ______
Why: ______

### 9. Given an unsorted array of n positive integers, find the smallest positive integer missing from it. O(n) time, O(1) extra space.
Pattern: ______
Why: ______

### 10. Given an array of stock prices (one per day), compute the maximum profit you could earn with at most one buy-sell pair.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Kadane's algorithm. **Why**: running `max(curr+a[i], a[i])` — DP collapsed to two scalars.
2. **Pattern**: Dutch national flag (three pointers). **Why**: low/mid/high partition for 3 distinct values, single pass.
3. **Pattern**: Three reversals trick. **Why**: reverse whole, reverse first k, reverse rest — O(n) time, O(1) space.
4. **Pattern**: Prefix sum. **Why**: precompute once, each query is `P[r+1]-P[l]`.
5. **Pattern**: Two pointers (NOT hashing). **Why**: sorted input → move `lo`/`hi` toward target; this is the canonical disambiguation between Week 6 two-pointer and Week 16 hashing.
6. **Pattern**: Two pointers (write index + read index). **Why**: classic stable partition.
7. **Pattern**: Boyer–Moore majority vote. **Why**: maintain a candidate + count, flipping when count hits 0.
8. **Pattern**: Prefix product from left × suffix product from right. **Why**: two passes building both, then combine — bypasses division.
9. **Pattern**: Cyclic placement (in-place hashing using indices). **Why**: put `a[i]` at index `a[i]-1`; first index where mismatch occurs is the answer.
10. **Pattern**: Single pass tracking minimum so far + best profit. **Why**: degenerate Kadane on price-differences.

</details>
