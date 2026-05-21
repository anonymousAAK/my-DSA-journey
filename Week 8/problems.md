# Week 8 — Practice Problems

Topics covered this week: binary search, search space reduction, lower/upper bound, binary search on the answer.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Binary Search | Easy | Classic | https://leetcode.com/problems/binary-search/ | Amazon, Google, Microsoft, Apple |
| 2 | First Bad Version | Easy | Predicate search | https://leetcode.com/problems/first-bad-version/ | Meta, Amazon, Google |
| 3 | Search Insert Position | Easy | Lower bound | https://leetcode.com/problems/search-insert-position/ | Amazon, Microsoft, Apple |
| 4 | Sqrt(x) | Easy | Binary search on math | https://leetcode.com/problems/sqrtx/ | Apple, Bloomberg, Amazon, Microsoft |
| 5 | Search in Rotated Sorted Array | Medium | Modified BS | https://leetcode.com/problems/search-in-rotated-sorted-array/ | Amazon, Meta, Microsoft, Apple |
| 6 | Find Peak Element | Medium | Slope BS | https://leetcode.com/problems/find-peak-element/ | Meta, Google, Microsoft, Amazon |
| 7 | Find Minimum in Rotated Sorted Array | Medium | Pivot BS | https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/ | Amazon, Microsoft, Meta |
| 8 | Find First and Last Position of Element in Sorted Array | Medium | Lower & upper bound | https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/ | Amazon, Meta, LinkedIn |
| 9 | Koko Eating Bananas | Medium | BS on answer | https://leetcode.com/problems/koko-eating-bananas/ | Google, Meta, Amazon |
| 10 | Median of Two Sorted Arrays | Hard | Partition BS | https://leetcode.com/problems/median-of-two-sorted-arrays/ | Amazon, Google, Apple, Microsoft |

## Stretch Problems

Bonus problems for deeper practice:

- [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) — canonical BS-on-answer.
- [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) — hard BS-on-answer.
- [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) — flattened BS.

## Patterns to Master This Week

- Standard BS loop invariant: `lo <= hi`, `mid = lo + (hi-lo)/2` to avoid overflow. Pitfall: choosing `lo<hi` vs `lo<=hi` mismatch.
- Lower/upper bound: returns index of first `>= x` / first `> x`. Pitfall: easy to confuse boundary returns.
- BS on the answer: define monotone predicate `feasible(k)`, then bracket the answer range. Pitfall: predicate must be truly monotone.
