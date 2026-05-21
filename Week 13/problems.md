# Week 13 — Practice Problems

Topics covered this week: queues, deques, circular queues, BFS preview, sliding windows on deques.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Implement Queue using Stacks | Easy | Two stacks | https://leetcode.com/problems/implement-queue-using-stacks/ | Microsoft, Amazon, Bloomberg |
| 2 | Implement Stack using Queues | Easy | Inverse construct | https://leetcode.com/problems/implement-stack-using-queues/ | Microsoft, Amazon, Bloomberg |
| 3 | Design Circular Queue | Medium | Ring buffer | https://leetcode.com/problems/design-circular-queue/ | Amazon, Google, Common |
| 4 | Design Circular Deque | Medium | Doubly-ended ring | https://leetcode.com/problems/design-circular-deque/ | Common |
| 5 | Number of Recent Calls | Easy | Sliding queue | https://leetcode.com/problems/number-of-recent-calls/ | Amazon, Common |
| 6 | Sliding Window Maximum | Hard | Monotonic deque | https://leetcode.com/problems/sliding-window-maximum/ | Amazon, Meta, Google, Microsoft |
| 7 | Open the Lock | Medium | BFS on states | https://leetcode.com/problems/open-the-lock/ | Google, Amazon, Common |
| 8 | Perfect Squares | Medium | BFS / DP | https://leetcode.com/problems/perfect-squares/ | Common |
| 9 | Rotting Oranges | Medium | Multi-source BFS | https://leetcode.com/problems/rotting-oranges/ | Amazon, Meta, Google, Microsoft |
| 10 | Walls and Gates | Medium | Multi-source BFS | https://leetcode.com/problems/walls-and-gates/ | Meta, Amazon, Google |

## Stretch Problems

Bonus problems for deeper practice:

- [Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/) — BFS on a grid.
- [01 Matrix](https://leetcode.com/problems/01-matrix/) — distance transform via BFS.
- [Find the Winner of the Circular Game](https://leetcode.com/problems/find-the-winner-of-the-circular-game/) — queue simulation.

## Patterns to Master This Week

- Two-stack queue: `pushStack` for enqueue, `popStack` for dequeue (amortized O(1)). Pitfall: only transfer when `popStack` is empty.
- BFS template: queue + visited set; track level to compute shortest distance. Pitfall: mark visited at enqueue time, not dequeue, to avoid duplicates.
- Monotonic deque for sliding window max: O(n) total. Pitfall: pop from front when index leaves the window.
