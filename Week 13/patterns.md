# Week 13 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which queue/deque pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given an array of n ≤ 10^6 integers and a window of size k, output the maximum within each window as it slides from left to right.
Pattern: ______
Why: ______

### 2. Simulate a task scheduler that processes jobs in FIFO order. Each job has a duration; track the order they finish.
Pattern: ______
Why: ______

### 3. Given an undirected graph with up to 10^5 nodes, find the shortest path (in edges) from node `s` to every other node.
Pattern: ______
Why: ______

### 4. Implement an LRU eviction policy supporting `access(key)` and `evict()`. (Distractor flavor — what data structure family?)
Pattern: ______
Why: ______

### 5. Given a stream of integers, compute the running sum over the last k values for each new arrival.
Pattern: ______
Why: ______

### 6. Given a string and an integer k, find the length of the longest substring containing at most k distinct characters. n ≤ 10^5.
Pattern: ______
Why: ______

### 7. Given a binary matrix where 1 represents land, find the shortest distance from each water cell to the nearest land. m·n ≤ 10^6.
Pattern: ______
Why: ______

### 8. Distractor: Given an array, find the minimum over each window of size k. (Same family as drill 1?)
Pattern: ______
Why: ______

### 9. Given a deck of cards numbered 1..n initially in some order, repeatedly take the top, place the next one at the bottom — until all are revealed in sorted order. Reconstruct the initial deck.
Pattern: ______
Why: ______

### 10. Implement a circular buffer of fixed capacity supporting `push(x)` (drops oldest if full) and `front()` / `back()`.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Monotonic deque. **Why**: maintain decreasing deque of indices; front is the window max — amortized O(n).
2. **Pattern**: Plain FIFO queue. **Why**: literal job order; pop on completion.
3. **Pattern**: BFS using a queue. **Why**: unit-weight shortest path → level-order traversal.
4. **Pattern**: Doubly linked list + hashmap (Week 11). **Why**: queues alone don't support move-to-front in O(1); this is the disambiguation drill.
5. **Pattern**: Sliding window with queue + running sum. **Why**: enqueue new, dequeue old; constant-time update.
6. **Pattern**: Sliding window with frequency map. **Why**: shrink from left while map has > k keys; track max length.
7. **Pattern**: Multi-source BFS. **Why**: enqueue all lands at distance 0, BFS layer by layer.
8. **Pattern**: Monotonic deque (increasing variant). **Why**: same skeleton as drill 1 but front holds min — recognize the symmetric pattern.
9. **Pattern**: Simulate with a deque, in reverse. **Why**: model the reveal process backwards (rotate back-to-front then push) to recover original order.
10. **Pattern**: Circular array with head/tail indices. **Why**: classic ring buffer — modulo arithmetic on capacity.

</details>
