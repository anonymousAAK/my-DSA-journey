# Week 5 — Practice Problems

Topics covered this week: recursion fundamentals, base cases, recursive Fibonacci/factorial, recursion tree, simple divide-and-conquer.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Fibonacci Number | Easy | Classic recursion | https://leetcode.com/problems/fibonacci-number/ |
| 2 | Reverse String | Easy | Recursion on two pointers | https://leetcode.com/problems/reverse-string/ |
| 3 | Power of Two | Easy | Recursive halving | https://leetcode.com/problems/power-of-two/ |
| 4 | Pow(x, n) | Medium | Fast exponentiation | https://leetcode.com/problems/powx-n/ |
| 5 | Climbing Stairs | Easy | Recursion + memo | https://leetcode.com/problems/climbing-stairs/ |
| 6 | Sum of Digits in Base K | Easy | Recursive digit sum | https://leetcode.com/problems/sum-of-digits-in-base-k/ |
| 7 | K-th Symbol in Grammar | Medium | Recursive structure | https://leetcode.com/problems/k-th-symbol-in-grammar/ |
| 8 | Permutations | Medium | Recursion (preview backtracking) | https://leetcode.com/problems/permutations/ |
| 9 | Merge Two Sorted Lists | Easy | Recursive merge | https://leetcode.com/problems/merge-two-sorted-lists/ |
| 10 | Tower of Hanoi (GFG) | Easy | Classic recursion | https://leetcode.com/problems/build-an-array-with-stack-operations/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Different Ways to Add Parentheses](https://leetcode.com/problems/different-ways-to-add-parentheses/) — divide-and-conquer on expressions.
- [House Robber](https://leetcode.com/problems/house-robber/) — first hint of overlapping subproblems.
- [Combination Sum](https://leetcode.com/problems/combination-sum/) — extends recursion to choice-trees.

## Patterns to Master This Week

- Always identify the base case first, then the recurrence. Pitfall: missing base case causes stack overflow.
- Fast exponentiation: `pow(x, n) = pow(x*x, n/2)` for O(log n). Pitfall: forgetting to handle negative `n` and odd `n`.
- Recursion tree depth determines stack memory — pure recursion for Fibonacci is O(2^n) time; memoize to drop to O(n).
