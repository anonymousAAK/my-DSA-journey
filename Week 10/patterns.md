# Week 10 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which matrix pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given an `n × n` integer matrix, rotate it 90° clockwise in place. n ≤ 1000.
Pattern: ______
Why: ______

### 2. Given an `m × n` matrix, print its elements in spiral order starting from the top-left.
Pattern: ______
Why: ______

### 3. Given an `m × n` matrix and a target value, decide if the value exists. Each row is sorted left-to-right and each column is sorted top-to-bottom.
Pattern: ______
Why: ______

### 4. Given an `m × n` 0/1 matrix, set entire row and column to 0 if any cell in them is 0. In place, O(1) extra space.
Pattern: ______
Why: ______

### 5. Given an `m × n` matrix of non-negative integers and a target sum, count the submatrices whose sum equals the target. n, m ≤ 200.
Pattern: ______
Why: ______

### 6. Transpose a non-square `m × n` matrix into an `n × m` output.
Pattern: ______
Why: ______

### 7. Distractor: Given an `n × n` grid where each cell holds a non-negative cost, find the minimum-cost path from top-left to bottom-right moving only right or down. (Is this matrix traversal?)
Pattern: ______
Why: ______

### 8. Given an `n × n` matrix, print its diagonals (both main-direction and anti-diagonal). n ≤ 1000.
Pattern: ______
Why: ______

### 9. Given an `m × n` boolean grid of land/water, count the number of "island" connected components (4-connectivity).
Pattern: ______
Why: ______

### 10. Given an `n × n` matrix, find the saddle point if any (minimum in its row AND maximum in its column).
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Transpose + reverse rows. **Why**: standard in-place 90° rotation trick.
2. **Pattern**: Layered traversal with 4 boundaries (top/bottom/left/right). **Why**: shrink the rectangle layer by layer.
3. **Pattern**: Staircase search from top-right. **Why**: if cell > target go left, if < go down — O(m+n).
4. **Pattern**: Use first row/column as markers (constant extra). **Why**: classic O(1) extra trick — store flags in the matrix itself.
5. **Pattern**: 2-D prefix sums + hashmap (or compress one dim and reuse 1-D subarray-sum-equals-k). **Why**: O(m^2 · n) by fixing row pair and running 1-D map.
6. **Pattern**: Direct index swap into a new matrix. **Why**: `b[j][i] = a[i][j]`.
7. **Pattern**: Distractor — this is DP on a grid (Week 18), not pure traversal. **Why**: matrix structure but it's an optimization problem with overlapping subproblems.
8. **Pattern**: Loop on diagonal index `d = i+j` (or `i-j`). **Why**: each diagonal is a fixed sum/difference of indices.
9. **Pattern**: BFS/DFS flood fill on the grid. **Why**: this is matrix-shaped but really a Week 17 graph problem — recognize the crossover.
10. **Pattern**: Row-min then column-max check. **Why**: precompute row minima, then verify each candidate is its column max — O(n^2).

</details>
