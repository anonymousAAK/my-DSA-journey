# Week 6 — Practice Problems

Topics covered this week: arrays, 1D traversal, prefix/suffix techniques, in-place tricks, two-pointer basics, Kadane's algorithm.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Contains Duplicate | Easy | Array / Hash set | https://leetcode.com/problems/contains-duplicate/ |
| 2 | Missing Number | Easy | Math / XOR | https://leetcode.com/problems/missing-number/ |
| 3 | Move Zeroes | Easy | Two pointers | https://leetcode.com/problems/move-zeroes/ |
| 4 | Best Time to Buy and Sell Stock | Easy | Single pass | https://leetcode.com/problems/best-time-to-buy-and-sell-stock/ |
| 5 | Maximum Subarray | Medium | Kadane's algorithm | https://leetcode.com/problems/maximum-subarray/ |
| 6 | Rotate Array | Medium | Reverse trick | https://leetcode.com/problems/rotate-array/ |
| 7 | Product of Array Except Self | Medium | Prefix / Suffix products | https://leetcode.com/problems/product-of-array-except-self/ |
| 8 | Find All Numbers Disappeared in an Array | Easy | Index marking | https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/ |
| 9 | Majority Element | Easy | Boyer-Moore vote | https://leetcode.com/problems/majority-element/ |
| 10 | Merge Sorted Array | Easy | Two pointers from end | https://leetcode.com/problems/merge-sorted-array/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) — Kadane variant tracking min/max.
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) — prefix sum + hashmap.
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) — two-pointer masterpiece.

## Patterns to Master This Week

- Kadane's algorithm: `current = max(num, current + num)`; O(n) time. Pitfall: reset rule when all-negatives.
- Two pointers (same end vs opposite ends): swap/compact in O(n). Pitfall: write index lagging behind read index.
- Prefix/suffix arrays vs in-place rolling products: trade O(n) extra space for clarity.
