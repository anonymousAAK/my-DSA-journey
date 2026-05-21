# Week 10 — Practice Problems

Topics covered this week: 2D arrays, matrix traversal, row/column operations, rotations, in-place transformations, matrix search.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Spiral Matrix | Medium | Layered traversal | https://leetcode.com/problems/spiral-matrix/ | Microsoft, Amazon, Google, Meta |
| 2 | Rotate Image | Medium | Transpose + reverse | https://leetcode.com/problems/rotate-image/ | Amazon, Microsoft, Apple, Meta |
| 3 | Set Matrix Zeroes | Medium | In-place markers | https://leetcode.com/problems/set-matrix-zeroes/ | Amazon, Microsoft, Meta |
| 4 | Search a 2D Matrix | Medium | BS on flattened matrix | https://leetcode.com/problems/search-a-2d-matrix/ | Amazon, Microsoft, Apple |
| 5 | Search a 2D Matrix II | Medium | Staircase search | https://leetcode.com/problems/search-a-2d-matrix-ii/ | Amazon, Microsoft, Google |
| 6 | Game of Life | Medium | In-place state encoding | https://leetcode.com/problems/game-of-life/ | Google, Amazon, Microsoft, Bloomberg |
| 7 | Word Search | Medium | Backtracking on grid (preview) | https://leetcode.com/problems/word-search/ | Amazon, Meta, Microsoft, Apple |
| 8 | Valid Sudoku | Medium | Row/col/box checks | https://leetcode.com/problems/valid-sudoku/ | Amazon, Apple, Microsoft, Uber |
| 9 | Range Sum Query 2D - Immutable | Medium | 2D prefix sums | https://leetcode.com/problems/range-sum-query-2d-immutable/ | Common |
| 10 | Diagonal Traverse | Medium | Index walking | https://leetcode.com/problems/diagonal-traverse/ | Amazon, Walmart, Common |

## Stretch Problems

Bonus problems for deeper practice:

- [Spiral Matrix II](https://leetcode.com/problems/spiral-matrix-ii/) — generate vs traverse spiral.
- [Maximal Square](https://leetcode.com/problems/maximal-square/) — preview of 2D DP.
- [Number of Islands](https://leetcode.com/problems/number-of-islands/) — bridges to graph BFS/DFS.

## Patterns to Master This Week

- Transpose + reverse rows = 90° clockwise rotation. Pitfall: only iterate upper triangle when transposing.
- Use first row/col as marker storage for "set zeroes" → O(1) extra space. Pitfall: track first row/col flags separately.
- Staircase search from top-right: O(m + n). Pitfall: starting at top-left breaks the invariant.
