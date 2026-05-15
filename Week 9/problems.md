# Week 9 — Practice Problems

Topics covered this week: sorting algorithms (bubble, selection, insertion, merge, quick), comparators, custom orderings, sort-based reductions.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Sort Colors | Medium | Dutch national flag | https://leetcode.com/problems/sort-colors/ |
| 2 | Merge Intervals | Medium | Sort + sweep | https://leetcode.com/problems/merge-intervals/ |
| 3 | Largest Number | Medium | Custom comparator | https://leetcode.com/problems/largest-number/ |
| 4 | Kth Largest Element in an Array | Medium | Quickselect / sort | https://leetcode.com/problems/kth-largest-element-in-an-array/ |
| 5 | Sort an Array | Medium | Merge / quick sort impl | https://leetcode.com/problems/sort-an-array/ |
| 6 | Wiggle Sort | Medium | Sort + interleave | https://leetcode.com/problems/wiggle-sort/ |
| 7 | Meeting Rooms | Easy | Sort intervals | https://leetcode.com/problems/meeting-rooms/ |
| 8 | Meeting Rooms II | Medium | Sort + heap | https://leetcode.com/problems/meeting-rooms-ii/ |
| 9 | Insertion Sort List | Medium | Algorithm on LL | https://leetcode.com/problems/insertion-sort-list/ |
| 10 | Sort Characters By Frequency | Medium | Sort by count | https://leetcode.com/problems/sort-characters-by-frequency/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) — merge-sort inversion counting.
- [Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) — modified merge sort.
- [H-Index](https://leetcode.com/problems/h-index/) — sort or counting sort.

## Patterns to Master This Week

- Comparator pattern in Java: `Arrays.sort(arr, (a, b) -> ...)`. Pitfall: returning `a - b` overflows when negative; use `Integer.compare`.
- Dutch national flag (three-way partitioning): O(n) time, O(1) space. Pitfall: incrementing `mid` only when swapping with `low`.
- Sort-then-sweep idiom for interval problems: O(n log n). Pitfall: sort by start vs end depending on the problem.
