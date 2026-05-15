# Week 19 — Practice Problems

Topics covered this week: greedy algorithms, exchange arguments, interval scheduling, activity selection.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Jump Game | Medium | Reach-tracking greedy | https://leetcode.com/problems/jump-game/ |
| 2 | Jump Game II | Medium | BFS-style greedy | https://leetcode.com/problems/jump-game-ii/ |
| 3 | Gas Station | Medium | Total-sum + reset | https://leetcode.com/problems/gas-station/ |
| 4 | Task Scheduler | Medium | Greedy + counts | https://leetcode.com/problems/task-scheduler/ |
| 5 | Non-overlapping Intervals | Medium | Sort by end | https://leetcode.com/problems/non-overlapping-intervals/ |
| 6 | Partition Labels | Medium | Last-index sweep | https://leetcode.com/problems/partition-labels/ |
| 7 | Lemonade Change | Easy | Cash greedy | https://leetcode.com/problems/lemonade-change/ |
| 8 | Best Time to Buy and Sell Stock II | Medium | Sum positive deltas | https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/ |
| 9 | Assign Cookies | Easy | Sort + two pointer | https://leetcode.com/problems/assign-cookies/ |
| 10 | Queue Reconstruction by Height | Medium | Sort + insert | https://leetcode.com/problems/queue-reconstruction-by-height/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) — interval greedy.
- [Candy](https://leetcode.com/problems/candy/) — two-pass greedy.
- [Reorganize String](https://leetcode.com/problems/reorganize-string/) — greedy with counts.

## Patterns to Master This Week

- Sort-by-end interval greedy: schedule the earliest finishing first. Pitfall: ties break by smaller start.
- Maintain a running "best so far" and update locally — many greedy problems are O(n) one-pass. Pitfall: not proving the greedy choice property.
- Disprove "obvious" greedy with a 3-element counterexample before coding. Pitfall: assuming local optimum implies global without verifying.
