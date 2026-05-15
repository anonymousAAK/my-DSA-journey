# Week 11 — Practice Problems

Topics covered this week: linked lists (singly/doubly), pointers, dummy heads, fast & slow pointers, reversal, cycle detection.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Reverse Linked List | Easy | Iterative + recursive | https://leetcode.com/problems/reverse-linked-list/ |
| 2 | Merge Two Sorted Lists | Easy | Dummy head merge | https://leetcode.com/problems/merge-two-sorted-lists/ |
| 3 | Linked List Cycle | Easy | Floyd's tortoise/hare | https://leetcode.com/problems/linked-list-cycle/ |
| 4 | Linked List Cycle II | Medium | Cycle entry point | https://leetcode.com/problems/linked-list-cycle-ii/ |
| 5 | Middle of the Linked List | Easy | Slow/fast | https://leetcode.com/problems/middle-of-the-linked-list/ |
| 6 | Remove Nth Node From End of List | Medium | Two-pointer gap | https://leetcode.com/problems/remove-nth-node-from-end-of-list/ |
| 7 | Add Two Numbers | Medium | Digit-by-digit + carry | https://leetcode.com/problems/add-two-numbers/ |
| 8 | Palindrome Linked List | Easy | Reverse half | https://leetcode.com/problems/palindrome-linked-list/ |
| 9 | Intersection of Two Linked Lists | Easy | Two-pointer swap | https://leetcode.com/problems/intersection-of-two-linked-lists/ |
| 10 | LRU Cache | Medium | DLL + HashMap | https://leetcode.com/problems/lru-cache/ |
| 11 | Reorder List | Medium | Split + reverse + merge | https://leetcode.com/problems/reorder-list/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) — hard reversal recipe.
- [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) — interleave-and-split trick.
- [Sort List](https://leetcode.com/problems/sort-list/) — bottom-up merge sort on a list.

## Patterns to Master This Week

- Dummy head node simplifies edge cases at the start. Pitfall: forgetting to return `dummy.next`.
- Slow/fast pointers (tortoise & hare): find middle/cycle in O(n) time / O(1) space. Pitfall: off-by-one on even-length lists.
- Iterative reversal with `prev`, `curr`, `next`: classic 3-pointer dance. Pitfall: saving `curr.next` before rewiring.
