# Week 14 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which tree pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given the root of a binary tree, return its inorder traversal as a list. n ≤ 10^5.
Pattern: ______
Why: ______

### 2. Given the root of a binary tree, return its level-order traversal grouped by depth.
Pattern: ______
Why: ______

### 3. Given the root of a binary tree, determine whether it satisfies the BST property.
Pattern: ______
Why: ______

### 4. Given two nodes `u` and `v` in a binary tree, find their lowest common ancestor. n ≤ 10^5.
Pattern: ______
Why: ______

### 5. Given the root of a binary tree, return its diameter (the longest path between any two nodes, measured in edges).
Pattern: ______
Why: ______

### 6. Given a BST and a target value `k`, find the value in the BST closest to `k`.
Pattern: ______
Why: ______

### 7. Distractor: Given a connected undirected graph with `n` nodes and `n-1` edges, find the longest simple path. (Wait — what *kind* of graph is this?)
Pattern: ______
Why: ______

### 8. Serialize a binary tree to a string and reconstruct it from that string.
Pattern: ______
Why: ______

### 9. Given a binary tree, decide if it is balanced (height difference ≤ 1 at every node).
Pattern: ______
Why: ______

### 10. Given the root of a BST and an integer k, find the k-th smallest value. n ≤ 10^5.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: DFS inorder (recursive or stack-based iterative). **Why**: left → root → right.
2. **Pattern**: BFS with queue, tracking level boundaries. **Why**: process one depth at a time.
3. **Pattern**: DFS with `(min, max)` bounds. **Why**: tighten bounds as you descend left/right.
4. **Pattern**: DFS returning ancestor or null. **Why**: post-order check — if both subtrees contain a target, current node is the LCA.
5. **Pattern**: DFS returning height, updating a global max with `leftH + rightH`. **Why**: diameter = best left-height + right-height at any node.
6. **Pattern**: BST descent with running closest. **Why**: O(h) — go left/right by comparison to k.
7. **Pattern**: Tree diameter via two BFS/DFS. **Why**: an n-node connected graph with n−1 edges is a tree — recognize the disguise.
8. **Pattern**: DFS pre-order with null markers (or BFS with sentinels). **Why**: pre-order + nulls fully encode the structure.
9. **Pattern**: DFS returning `-1` on imbalance. **Why**: combine height computation with a balance-fail signal.
10. **Pattern**: Inorder traversal with counter, early stop. **Why**: BST inorder yields sorted order.

</details>
