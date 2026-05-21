# Week 27 — Practice Problems

Topics covered this week: computational geometry — points, lines, convex hull, line sweep, polygon area, line/segment intersections.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Erect the Fence | Hard | Convex hull | https://leetcode.com/problems/erect-the-fence/ | Google, Amazon, Common |
| 2 | Max Points on a Line | Hard | Slope hashing | https://leetcode.com/problems/max-points-on-a-line/ | Google, LinkedIn, Bloomberg |
| 3 | Rectangle Overlap | Easy | Bounding box | https://leetcode.com/problems/rectangle-overlap/ | Amazon, Google, Microsoft |
| 4 | Largest Triangle Area | Easy | Shoelace formula | https://leetcode.com/problems/largest-triangle-area/ | Common |
| 5 | Minimum Area Rectangle | Medium | Pair-of-points geometry | https://leetcode.com/problems/minimum-area-rectangle/ | Google, Microsoft, Common |
| 6 | Minimum Area Rectangle II | Medium | Diagonals geometry | https://leetcode.com/problems/minimum-area-rectangle-ii/ | Common |
| 7 | Valid Square | Medium | Squared distances | https://leetcode.com/problems/valid-square/ | Amazon, Google, Common |
| 8 | Check If It Is a Straight Line | Easy | Cross product | https://leetcode.com/problems/check-if-it-is-a-straight-line/ | Amazon, Google, Common |
| 9 | The Skyline Problem | Hard | Sweep line | https://leetcode.com/problems/the-skyline-problem/ | Amazon, Meta, Google, Microsoft |
| 10 | Rectangle Area II | Hard | Coordinate compression + sweep | https://leetcode.com/problems/rectangle-area-ii/ | Common |
| 11 | K Closest Points to Origin | Medium | Distance heap | https://leetcode.com/problems/k-closest-points-to-origin/ | Meta, Amazon, LinkedIn, Microsoft |

## Stretch Problems

Bonus problems for deeper practice:

- [Perfect Rectangle](https://leetcode.com/problems/perfect-rectangle/) — area + corner-counting trick.
- [Minimum Number of Lines to Cover Points](https://leetcode.com/problems/minimum-lines-to-represent-a-line-chart/) — slope grouping.
- [Self Crossing](https://leetcode.com/problems/self-crossing/) — careful case analysis.

## Patterns to Master This Week

- Cross product sign tells turn direction (CCW vs CW vs collinear). Pitfall: comparing slopes as doubles → use cross product to avoid precision issues.
- Convex hull via Andrew's monotone chain: sort points, build lower then upper hull in O(n log n). Pitfall: handle collinear points based on problem requirements.
- Sweep line: sort events by x, maintain active set in a sorted structure. Pitfall: tie-breaking (start before end vs end before start) matters.
