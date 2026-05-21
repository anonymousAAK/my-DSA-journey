# Week 14 — Practice Problems

Topics covered this week: binary trees, traversals (in/pre/post/level), recursive properties, BST operations, LCA.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Maximum Depth of Binary Tree | Easy | Recursion | https://leetcode.com/problems/maximum-depth-of-binary-tree/ | Amazon, Microsoft, LinkedIn |
| 2 | Symmetric Tree | Easy | Mirror recursion | https://leetcode.com/problems/symmetric-tree/ | Amazon, Microsoft, LinkedIn |
| 3 | Same Tree | Easy | Structural compare | https://leetcode.com/problems/same-tree/ | Amazon, Google, Microsoft |
| 4 | Invert Binary Tree | Easy | Recursive swap | https://leetcode.com/problems/invert-binary-tree/ | Google, Amazon, Meta |
| 5 | Binary Tree Level Order Traversal | Medium | BFS | https://leetcode.com/problems/binary-tree-level-order-traversal/ | Amazon, Meta, Microsoft, LinkedIn |
| 6 | Diameter of Binary Tree | Easy | Post-order recursion | https://leetcode.com/problems/diameter-of-binary-tree/ | Meta, Amazon, Google |
| 7 | Validate Binary Search Tree | Medium | In-order / range | https://leetcode.com/problems/validate-binary-search-tree/ | Amazon, Meta, Microsoft, Bloomberg |
| 8 | Lowest Common Ancestor of a Binary Tree | Medium | Recursive search | https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/ | Amazon, Meta, Microsoft, Apple |
| 9 | Binary Tree Zigzag Level Order Traversal | Medium | BFS with toggle | https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/ | Amazon, Meta, Microsoft |
| 10 | Path Sum | Easy | Top-down DFS | https://leetcode.com/problems/path-sum/ | Amazon, Apple, Microsoft |
| 11 | Binary Tree Maximum Path Sum | Hard | Post-order with global max | https://leetcode.com/problems/binary-tree-maximum-path-sum/ | Amazon, Meta, Microsoft, Apple |
| 12 | Serialize and Deserialize Binary Tree | Hard | Tree encoding | https://leetcode.com/problems/serialize-and-deserialize-binary-tree/ | Amazon, Meta, LinkedIn, Microsoft |

## Stretch Problems

Bonus problems for deeper practice:

- [Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) — index map trick.
- [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) — in-order with counter.
- [Flatten Binary Tree to Linked List](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/) — reverse post-order.

## Patterns to Master This Week

- Recursive "do something at each node": choose pre/in/post order based on when info is needed. Pitfall: confusing what each order yields.
- BFS via queue for level information; size-snapshot trick to separate levels. Pitfall: dequeue order vs enqueue order.
- BST in-order traversal yields sorted sequence — basis for validation, kth element, and range queries.
