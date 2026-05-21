# Week 4 — Practice Problems

Topics covered this week: pattern printing (pyramids, triangles, diamonds), nested loop reasoning, row/column logic.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Pascal's Triangle | Easy | Row generation | https://leetcode.com/problems/pascals-triangle/ | Amazon, Apple, Bloomberg |
| 2 | Pascal's Triangle II | Easy | In-place row | https://leetcode.com/problems/pascals-triangle-ii/ | Amazon, Apple, Common |
| 3 | Generate Parentheses | Medium | Pattern building (preview) | https://leetcode.com/problems/generate-parentheses/ | Amazon, Meta, Microsoft, Google |
| 4 | Spiral Matrix | Medium | Layered traversal | https://leetcode.com/problems/spiral-matrix/ | Microsoft, Amazon, Google, Meta |
| 5 | Spiral Matrix II | Medium | Generate spiral pattern | https://leetcode.com/problems/spiral-matrix-ii/ | Common |
| 6 | Count and Say | Medium | String pattern generation | https://leetcode.com/problems/count-and-say/ | Meta, Amazon, Apple, Google |
| 7 | Diagonal Traverse | Medium | Index pattern | https://leetcode.com/problems/diagonal-traverse/ | Amazon, Walmart, Common |
| 8 | Print in Order | Easy | Sequential pattern | https://leetcode.com/problems/print-in-order/ | Common |

## Stretch Problems

Bonus problems for deeper practice:

- [Spiral Matrix III](https://leetcode.com/problems/spiral-matrix-iii/) — advanced layered movement.
- [Zigzag Conversion](https://leetcode.com/problems/zigzag-conversion/) — translate visual zigzag into row math.
- [Image Smoother](https://leetcode.com/problems/image-smoother/) — nested-loop 3x3 window walking.

## Patterns to Master This Week

- "Outer i, inner j" reasoning: outer loop = rows, inner = columns. Pitfall: confusing `i+j`/`i-j` invariants for diagonals.
- Layer/peel pattern (process row top, col right, row bottom, col left): O(m*n) time. Pitfall: off-by-one when the matrix is non-square.
- Build-on-previous-row idea (Pascal): O(n^2) time, O(n) space. Pitfall: in-place needs reverse iteration.
