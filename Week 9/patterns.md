# Week 9 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which sorting pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Sort `n ≤ 10^5` integers in ascending order. No constraint on values. Time limit 1 s.
Pattern: ______
Why: ______

### 2. Sort `n ≤ 10^7` integers where every value lies in `[0, 1000]`. Time limit 1 s.
Pattern: ______
Why: ______

### 3. Sort `n ≤ 10^6` floats uniformly distributed in `[0, 1)`. Time limit 1 s.
Pattern: ______
Why: ______

### 4. Sort an almost-sorted array where each element is at most k positions from its correct location. k ≤ 100, n ≤ 10^6.
Pattern: ______
Why: ______

### 5. Given `n ≤ 10^5` strings, sort them lexicographically.
Pattern: ______
Why: ______

### 6. Given a list of intervals `[l_i, r_i]`, sort them by start, breaking ties by end. n ≤ 10^5.
Pattern: ______
Why: ______

### 7. Distractor: Given `n ≤ 10^7` integers, find the k-th smallest. (Don't just sort — what's better?)
Pattern: ______
Why: ______

### 8. Count the number of inversions in an array (pairs `i < j` with `a[i] > a[j]`). n ≤ 10^5.
Pattern: ______
Why: ______

### 9. Sort an array containing only 0/1 values in place, single pass, O(1) extra space.
Pattern: ______
Why: ______

### 10. Given a stream of 10^9 integers arriving one at a time and only constant memory available, you must report the sorted order at the end. (Distractor — what's the catch?)
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Comparison sort (merge sort / `Arrays.sort`). **Why**: general unconstrained integers → O(n log n) is optimal.
2. **Pattern**: Counting sort. **Why**: small fixed value range — O(n + V).
3. **Pattern**: Bucket sort. **Why**: uniform distribution in [0,1) → distribute into n buckets, sort each — expected O(n).
4. **Pattern**: Heap of size k+1 (or insertion sort). **Why**: locality bound means each element only needs to compete with O(k) neighbours.
5. **Pattern**: Comparison sort with string comparator (or radix sort if alphabet small). **Why**: standard library handles it; radix is the optimization route.
6. **Pattern**: Comparison sort with custom comparator. **Why**: lexicographic compare on (start, end) — `Arrays.sort` with a lambda.
7. **Pattern**: Quickselect. **Why**: expected O(n) — don't fully sort; the distractor is "of course I sort first" thinking.
8. **Pattern**: Merge sort with cross-count. **Why**: each merge step counts inversions across the split — O(n log n).
9. **Pattern**: Two-pointer partition (or counting). **Why**: degenerate Dutch flag — count 0s, fill, then fill 1s; or partition pointer.
10. **Pattern**: Distractor — impossible in O(1) memory; needs external sort (disk-backed merge sort). **Why**: streams + constant memory ≠ in-memory sort.

</details>
