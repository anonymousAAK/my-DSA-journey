# Week 21 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which advanced-structure pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given an array of n ≤ 10^5 integers and up to 10^5 queries each asking the sum of `a[l..r]`, with point updates `a[i] = v` interspersed, answer each operation in O(log n).
Pattern: ______
Why: ______

### 2. Given n ≤ 10^5 integers and queries asking the *minimum* in `a[l..r]`. No updates.
Pattern: ______
Why: ______

### 3. Given n ≤ 10^5 integers, support two operations: add `v` to all values in `a[l..r]`, and read `a[i]`. Up to 10^5 ops total.
Pattern: ______
Why: ______

### 4. Given up to 10^5 strings (sum of lengths ≤ 10^6), support queries asking "how many stored strings start with prefix P?".
Pattern: ______
Why: ______

### 5. Given n ≤ 10^5 integers, count the number of inversions (pairs `i < j` with `a[i] > a[j]`).
Pattern: ______
Why: ______

### 6. Given a stream of integer insertions and queries "how many values inserted so far are ≤ x?", answer each in O(log V).
Pattern: ______
Why: ______

### 7. Distractor: Given an immutable array and many range-sum queries, answer each in O(1). (Need a segment tree?)
Pattern: ______
Why: ______

### 8. Given a stream of (word, weight) pairs and queries with a prefix, return the top-3 words by weight with that prefix.
Pattern: ______
Why: ______

### 9. Given n ≤ 10^5 intervals, support insert/delete and queries "is point `x` covered by any current interval?".
Pattern: ______
Why: ______

### 10. Distractor: Given n ≤ 10^5 integers, answer queries `kth smallest in a[l..r]`. (Plain segment tree?)
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Fenwick tree (BIT) or segment tree, range-sum/point-update. **Why**: both ops in O(log n) — BIT is simpler for sums.
2. **Pattern**: Sparse table (or segment tree). **Why**: static idempotent range query → O(n log n) build, O(1) query.
3. **Pattern**: BIT with difference-array trick (range update, point query). **Why**: update `(l, +v)` and `(r+1, -v)`; query is prefix sum.
4. **Pattern**: Trie with subtree-count. **Why**: each node carries count of strings passing through it.
5. **Pattern**: Fenwick over compressed values (or merge sort, Week 9). **Why**: for each i, count of already-inserted values > a[i] via BIT suffix sum.
6. **Pattern**: Fenwick on coordinate-compressed values. **Why**: prefix sum on a frequency BIT.
7. **Pattern**: Distractor — prefix sum array (Week 6). **Why**: no updates → simple precompute beats segment tree; over-engineering check.
8. **Pattern**: Trie with a heap of best entries at each node. **Why**: walk to prefix node, return top-k from its aggregate.
9. **Pattern**: Segment tree with lazy propagation on cover-count. **Why**: range +1/−1 on insert/delete; query is point value > 0.
10. **Pattern**: Distractor — merge-sort tree / persistent segment tree. **Why**: plain segment tree doesn't support k-th order statistics in a range; need advanced variant.

</details>
