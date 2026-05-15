# Week 20 — Practice Problems

Topics covered this week: backtracking, choice trees, pruning, subsets/permutations/combinations, constraint propagation.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Subsets | Medium | Power-set backtracking | https://leetcode.com/problems/subsets/ |
| 2 | Subsets II | Medium | Skip duplicates | https://leetcode.com/problems/subsets-ii/ |
| 3 | Permutations | Medium | Pick-and-skip | https://leetcode.com/problems/permutations/ |
| 4 | Permutations II | Medium | Dedupe permutations | https://leetcode.com/problems/permutations-ii/ |
| 5 | Combinations | Medium | k-of-n choose | https://leetcode.com/problems/combinations/ |
| 6 | Combination Sum | Medium | Unbounded backtracking | https://leetcode.com/problems/combination-sum/ |
| 7 | Word Search | Medium | Grid backtracking | https://leetcode.com/problems/word-search/ |
| 8 | N-Queens | Hard | Constraint backtracking | https://leetcode.com/problems/n-queens/ |
| 9 | Palindrome Partitioning | Medium | String backtracking | https://leetcode.com/problems/palindrome-partitioning/ |
| 10 | Letter Combinations of a Phone Number | Medium | Multi-branch recursion | https://leetcode.com/problems/letter-combinations-of-a-phone-number/ |
| 11 | Restore IP Addresses | Medium | Position partition | https://leetcode.com/problems/restore-ip-addresses/ |
| 12 | Sudoku Solver | Hard | Full backtracking | https://leetcode.com/problems/sudoku-solver/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) — classic introduction to pruning.
- [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) — each number used once + dedupe.
- [Word Search II](https://leetcode.com/problems/word-search-ii/) — backtracking + trie combo.

## Patterns to Master This Week

- Choose / explore / unchoose template: mutate state, recurse, then revert. Pitfall: forgetting to revert breaks sibling branches.
- Dedupe at the same recursion depth by sorting + `if (i > start && a[i] == a[i-1]) continue;`. Pitfall: applying it across depths produces wrong results.
- Prune early with feasibility checks (sum already too big, conflicting constraint). Pitfall: aggressive pruning that drops valid branches.
