# Week 19 — Practice Problems

Topics covered this week: greedy algorithms, exchange arguments, interval scheduling, activity selection.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Jump Game | Medium | Reach-tracking greedy | https://leetcode.com/problems/jump-game/ | Amazon, Meta, Microsoft, Apple |
| 2 | Jump Game II | Medium | BFS-style greedy | https://leetcode.com/problems/jump-game-ii/ | Amazon, Meta, Microsoft |
| 3 | Gas Station | Medium | Total-sum + reset | https://leetcode.com/problems/gas-station/ | Amazon, Google, Apple |
| 4 | Task Scheduler | Medium | Greedy + counts | https://leetcode.com/problems/task-scheduler/ | Amazon, Meta, Microsoft, Bloomberg |
| 5 | Non-overlapping Intervals | Medium | Sort by end | https://leetcode.com/problems/non-overlapping-intervals/ | Amazon, Google, Apple |
| 6 | Partition Labels | Medium | Last-index sweep | https://leetcode.com/problems/partition-labels/ | Amazon, Meta, Google |
| 7 | Lemonade Change | Easy | Cash greedy | https://leetcode.com/problems/lemonade-change/ | Amazon, Google, Common |
| 8 | Best Time to Buy and Sell Stock II | Medium | Sum positive deltas | https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/ | Amazon, Meta, Microsoft |
| 9 | Assign Cookies | Easy | Sort + two pointer | https://leetcode.com/problems/assign-cookies/ | Amazon, Google, Common |
| 10 | Queue Reconstruction by Height | Medium | Sort + insert | https://leetcode.com/problems/queue-reconstruction-by-height/ | Amazon, Google, Common |

## Stretch Problems

Bonus problems for deeper practice:

- [Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) — interval greedy.
- [Candy](https://leetcode.com/problems/candy/) — two-pass greedy.
- [Reorganize String](https://leetcode.com/problems/reorganize-string/) — greedy with counts.

## Patterns to Master This Week

- Sort-by-end interval greedy: schedule the earliest finishing first. Pitfall: ties break by smaller start.
- Maintain a running "best so far" and update locally — many greedy problems are O(n) one-pass. Pitfall: not proving the greedy choice property.
- Disprove "obvious" greedy with a 3-element counterexample before coding. Pitfall: assuming local optimum implies global without verifying.
