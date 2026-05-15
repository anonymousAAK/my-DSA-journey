# Week 15 — Practice Problems

Topics covered this week: heaps, priority queues, heapify, top-K patterns, two-heap median, scheduling with PQ.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Kth Largest Element in an Array | Medium | Min-heap of size k | https://leetcode.com/problems/kth-largest-element-in-an-array/ |
| 2 | Kth Largest Element in a Stream | Easy | Streaming heap | https://leetcode.com/problems/kth-largest-element-in-a-stream/ |
| 3 | Top K Frequent Elements | Medium | Heap on counts | https://leetcode.com/problems/top-k-frequent-elements/ |
| 4 | Top K Frequent Words | Medium | Heap with tiebreak | https://leetcode.com/problems/top-k-frequent-words/ |
| 5 | Find Median from Data Stream | Hard | Two heaps | https://leetcode.com/problems/find-median-from-data-stream/ |
| 6 | Merge k Sorted Lists | Hard | Heap of heads | https://leetcode.com/problems/merge-k-sorted-lists/ |
| 7 | Task Scheduler | Medium | Greedy + heap | https://leetcode.com/problems/task-scheduler/ |
| 8 | K Closest Points to Origin | Medium | Max-heap of size k | https://leetcode.com/problems/k-closest-points-to-origin/ |
| 9 | Last Stone Weight | Easy | Max-heap simulation | https://leetcode.com/problems/last-stone-weight/ |
| 10 | Reorganize String | Medium | Greedy via heap | https://leetcode.com/problems/reorganize-string/ |

## Stretch Problems

Bonus problems for deeper practice:

- [IPO](https://leetcode.com/problems/ipo/) — two heaps for "capital available, max profit".
- [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/) — heap-driven event sweep.
- [Sliding Window Median](https://leetcode.com/problems/sliding-window-median/) — two heaps with lazy deletion.

## Patterns to Master This Week

- Min-heap of size k for "k largest" → O(n log k). Pitfall: forgetting to peek-before-poll when comparing.
- Two-heap median: max-heap for lower half, min-heap for upper half, rebalance after each insert. Pitfall: tie-breaking when sizes differ.
- Greedy-with-heap pattern (task scheduler, reorganize string): always extract the most "urgent" item next. Pitfall: cooling/cooldown logic.
