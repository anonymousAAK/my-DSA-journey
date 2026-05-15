# Week 20 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which backtracking pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given an array of n ≤ 20 distinct integers, enumerate all subsets.
Pattern: ______
Why: ______

### 2. Given an array of n ≤ 8 distinct integers, enumerate all permutations.
Pattern: ______
Why: ______

### 3. Given n, place n queens on an n×n chessboard so that no two attack each other. Return the count of distinct solutions. n ≤ 14.
Pattern: ______
Why: ______

### 4. Given a 9×9 partially filled Sudoku board, fill it in respecting all constraints.
Pattern: ______
Why: ______

### 5. Given an array and a target sum, return all unique subsets summing to the target. Numbers may repeat in the array. n ≤ 30.
Pattern: ______
Why: ______

### 6. Given a string of digits 2–9, return all letter combinations the digits could represent on a phone keypad. Length ≤ 7.
Pattern: ______
Why: ______

### 7. Distractor: Given n ≤ 10^5 integers, return all subsets that sum to a target. (Why is backtracking the wrong default?)
Pattern: ______
Why: ______

### 8. Given a string, partition it into substrings that are all palindromes; return all such partitions. Length ≤ 16.
Pattern: ______
Why: ______

### 9. Given a 2-D grid of letters and a word, decide whether the word can be formed by a path moving to neighbours (no cell reused). Grid up to 8×8, word ≤ 12.
Pattern: ______
Why: ______

### 10. Distractor: Given n ≤ 1000 items with weights and a knapsack capacity, find the maximum value subset. (Backtracking?)
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Backtracking with include/exclude (or bitmask iteration). **Why**: 2^n choices.
2. **Pattern**: Backtracking with `used[]` flags (or swap-in-place). **Why**: choose next position from remaining unused.
3. **Pattern**: Backtracking row by row + column/diagonal sets. **Why**: classic N-Queens with O(1) attack-check via three boolean arrays.
4. **Pattern**: Backtracking with constraint propagation. **Why**: try digits 1–9 in next empty cell; backtrack on conflict.
5. **Pattern**: Backtracking with sort + skip duplicates. **Why**: prune when running sum exceeds target; skip equal siblings to avoid duplicate sets.
6. **Pattern**: Backtracking / DFS over digit positions. **Why**: branching factor ≤ 4 per digit; depth ≤ 7.
7. **Pattern**: Distractor — backtracking is exponential; this needs DP / meet-in-the-middle. **Why**: n=10^5 forbids 2^n exploration.
8. **Pattern**: Backtracking with palindrome check on each split. **Why**: try every prefix; recurse on suffix when prefix is a palindrome.
9. **Pattern**: DFS backtracking with visited marking. **Why**: explore neighbour grid cells, undo visit on return.
10. **Pattern**: Distractor — DP (0/1 knapsack, Week 18). **Why**: backtracking is 2^n; DP is O(nW). Recognize when state-overlap kills brute force.

</details>
