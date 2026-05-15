# Week 26 — Practice Problems

Topics covered this week: network flow, max-flow / min-cut, bipartite matching, augmenting paths, Hopcroft-Karp ideas.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Maximum Number of Accepted Invitations | Medium | Bipartite matching | https://leetcode.com/problems/maximum-number-of-accepted-invitations/ |
| 2 | Minimum Number of Days to Disconnect Island | Hard | Min-cut intuition | https://leetcode.com/problems/minimum-number-of-days-to-disconnect-island/ |
| 3 | Escape a Large Maze | Hard | BFS/flow bounded | https://leetcode.com/problems/escape-a-large-maze/ |
| 4 | Maximum Students Taking Exam | Hard | Bipartite matching / DP | https://leetcode.com/problems/maximum-students-taking-exam/ |
| 5 | Minimum Swaps to Make Sequences Increasing | Hard | DP / matching intuition | https://leetcode.com/problems/minimum-swaps-to-make-sequences-increasing/ |
| 6 | Campus Bikes II | Medium | Assignment problem | https://leetcode.com/problems/campus-bikes-ii/ |
| 7 | Optimal Account Balancing | Hard | Flow-like balancing | https://leetcode.com/problems/optimal-account-balancing/ |
| 8 | Number of Operations to Make Network Connected | Medium | Connectivity (related) | https://leetcode.com/problems/number-of-operations-to-make-network-connected/ |
| 9 | Swim in Rising Water | Hard | Max-flow style search | https://leetcode.com/problems/swim-in-rising-water/ |
| 10 | Number of Closed Islands | Medium | Flood-fill (preview to min cut) | https://leetcode.com/problems/number-of-closed-islands/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Bricks Falling When Hit](https://leetcode.com/problems/bricks-falling-when-hit/) — time-reverse flood thinking.
- [Most Stones Removed with Same Row or Column](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/) — bipartite UF.
- Codeforces problems tagged `flows` for exposure to true max-flow implementations.

## Patterns to Master This Week

- Bipartite matching via DFS augmenting paths: O(V*E) worst case. Pitfall: visited array must reset per source.
- Min-cut = Max-flow theorem: reduce "disconnect" problems to cutting edges in a flow network. Pitfall: modeling vertices needs node-splitting trick.
- Hungarian / assignment: matrix-based O(n^3). Pitfall: usually overkill for interviews — bitmask DP is more pragmatic at small n.
