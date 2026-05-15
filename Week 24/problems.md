# Week 24 — Practice Problems

Topics covered this week: NP-hard problems, approximation algorithms, TSP, set cover, vertex cover, graph colouring. These problems have no known polynomial exact solutions; focus on heuristics, approximations, and brute force for small inputs.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Shortest Path Visiting All Nodes | Hard | TSP-style bitmask BFS | https://leetcode.com/problems/shortest-path-visiting-all-nodes/ |
| 2 | Find the Shortest Superstring | Hard | TSP reduction | https://leetcode.com/problems/find-the-shortest-superstring/ |
| 3 | Smallest Sufficient Team | Hard | Set cover bitmask DP | https://leetcode.com/problems/smallest-sufficient-team/ |
| 4 | Partition to K Equal Sum Subsets | Medium | Bin-packing brute force | https://leetcode.com/problems/partition-to-k-equal-sum-subsets/ |
| 5 | Maximum Compatibility Score Sum | Medium | Assignment / permutations | https://leetcode.com/problems/maximum-compatibility-score-sum/ |
| 6 | Maximum Students Taking Exam | Hard | Bitmask DP (independent set on grid) | https://leetcode.com/problems/maximum-students-taking-exam/ |
| 7 | Minimum Incompatibility | Hard | Partition bitmask DP | https://leetcode.com/problems/minimum-incompatibility/ |
| 8 | Number of Ways to Wear Different Hats | Hard | Assignment problem | https://leetcode.com/problems/number-of-ways-to-wear-different-hats-to-each-other/ |
| 9 | Parallel Courses III | Hard | DAG longest path | https://leetcode.com/problems/parallel-courses-iii/ |
| 10 | Maximum Score Words Formed by Letters | Hard | Subset enumeration | https://leetcode.com/problems/maximum-score-words-formed-by-letters/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Codeforces Round Robin TSP](https://codeforces.com/) — practice bitmask TSP under time pressure.
- [Minimum Number of Work Sessions to Finish the Tasks](https://leetcode.com/problems/minimum-number-of-work-sessions-to-finish-the-tasks/) — bin packing.
- [Find Minimum Time to Finish All Jobs](https://leetcode.com/problems/find-minimum-time-to-finish-all-jobs/) — partition with binary search.

## Patterns to Master This Week

- Brute force / bitmask DP is reasonable when `n <= 20`. Pitfall: combinatorial explosion beyond that — recognize NP-hardness.
- Approximation thinking: 2-approximation for vertex cover (matching), greedy log(n) factor for set cover. Pitfall: no exact polynomial algorithm is currently known — that's the whole point.
- Branch-and-bound trims the search by computing lower bounds. Pitfall: tight bounds matter more than cleverness.
