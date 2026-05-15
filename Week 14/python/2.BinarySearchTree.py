"""
WEEK 14 - PYTHON DSA
Topic: Binary Search Tree (BST)
File: 2.BinarySearchTree.py

CONCEPT:
A BST is a binary tree obeying the ordering invariant: for every node, all
keys in the left subtree are strictly less than the node's key and all keys
in the right subtree are strictly greater. This invariant makes search,
insert, and delete O(h) where h is the tree height.

KEY POINTS:
- Balanced BST: h = O(log n) -> O(log n) ops.
- Unbalanced BST: h can degrade to O(n) (looks like a linked list).
- Delete has 3 cases:
    1. Leaf -> just unlink.
    2. One child -> replace node with that child.
    3. Two children -> replace value with inorder successor (min of right
       subtree), then delete that successor recursively.
- isValidBST: pass min/max bounds down (more efficient than rebuilding the
  inorder list).
- LCA in a BST is the first node where p,q "split" (one <= node <= other).

ALGORITHM / APPROACH:
- insert(node, val): recurse left/right based on comparison; create node
  when recursion hits None.
- search: same recursion comparing the key.
- delete(node, val): recurse to find; on match handle the three cases.
- kth_smallest: in-order traversal that decrements a counter; return when
  counter hits 0.

PYTHON-SPECIFIC NOTES:
- We model BST.root as Optional[Node] and recursion returns the (possibly
  new) subtree root, mirroring the Java pattern.
- `math.inf` and `-math.inf` are clean sentinels for the bounds in
  isValidBST (vs. Java's Long.MIN_VALUE / MAX_VALUE).

DRY RUN:
Insert 5,3,7,1,4,6,8 into empty BST:
        5
       / \
      3   7
     / \ / \
    1  4 6  8
Inorder -> 1 3 4 5 6 7 8 (sorted, validates BST).

Delete 3 (two children):
  Find 3; right subtree is [4]; inorder successor = 4.
  Copy 4 into the deleted node's slot; delete 4 from right subtree.
        5
       / \
      4   7
     /   / \
    1   6   8

Delete 5 (root, two children):
  Successor in right subtree = 6.
  Copy 6 to root; delete 6 from right.
        6
       / \
      4   7
     /     \
    1       8

COMPLEXITY:
  insert/search/delete: O(h)  (O(log n) average for random insertion order)
  isValidBST: O(n)
  lca: O(h)
  kth_smallest: O(h + k)
"""

from __future__ import annotations
from dataclasses import dataclass
from math import inf
from typing import Optional


@dataclass(slots=True)
class Node:
    val: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


class BST:
    def __init__(self) -> None:
        self.root: Optional[Node] = None

    # --- insert ---
    def insert(self, val: int) -> None:
        self.root = self._insert(self.root, val)

    def _insert(self, node: Optional[Node], val: int) -> Node:
        if node is None: return Node(val)
        if val < node.val:   node.left = self._insert(node.left, val)
        elif val > node.val: node.right = self._insert(node.right, val)
        # duplicate val: ignore
        return node

    # --- search ---
    def search(self, val: int) -> bool:
        return self._search(self.root, val)

    def _search(self, node: Optional[Node], val: int) -> bool:
        if node is None: return False
        if val == node.val: return True
        return self._search(node.left, val) if val < node.val else self._search(node.right, val)

    # --- delete ---
    def delete(self, val: int) -> None:
        self.root = self._delete(self.root, val)

    def _min(self, node: Node) -> Node:
        while node.left is not None:
            node = node.left
        return node

    def _delete(self, node: Optional[Node], val: int) -> Optional[Node]:
        if node is None: return None
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            if node.left is None: return node.right   # cases 1 & 2
            if node.right is None: return node.left   # case 2
            # case 3: two children
            succ = self._min(node.right)
            node.val = succ.val
            node.right = self._delete(node.right, succ.val)
        return node

    # --- inorder print (sorted) ---
    def sorted_values(self) -> list[int]:
        out: list[int] = []
        def go(n: Optional[Node]) -> None:
            if n is None: return
            go(n.left); out.append(n.val); go(n.right)
        go(self.root)
        return out

    # --- validation ---
    def is_valid_bst(self) -> bool:
        def check(n: Optional[Node], lo: float, hi: float) -> bool:
            if n is None: return True
            if not (lo < n.val < hi): return False
            return check(n.left, lo, n.val) and check(n.right, n.val, hi)
        return check(self.root, -inf, inf)

    # --- LCA ---
    def lca(self, p: int, q: int) -> int:
        n = self.root
        while n is not None:
            if p < n.val and q < n.val: n = n.left
            elif p > n.val and q > n.val: n = n.right
            else: return n.val
        return -1

    # --- kth smallest ---
    def kth_smallest(self, k: int) -> int:
        # iterative inorder; stop at k-th
        stack: list[Node] = []
        curr = self.root
        cnt = 0
        while curr is not None or stack:
            while curr is not None:
                stack.append(curr); curr = curr.left
            curr = stack.pop()
            cnt += 1
            if cnt == k: return curr.val
            curr = curr.right
        return -1


def main() -> None:
    bst = BST()
    for v in [5, 3, 7, 1, 4, 6, 8]:
        bst.insert(v)

    print("Inserted: 5, 3, 7, 1, 4, 6, 8")
    print("Inorder (sorted):", bst.sorted_values())

    print("Search 4:", bst.search(4))
    print("Search 9:", bst.search(9))
    print("Is valid BST:", bst.is_valid_bst())

    print("LCA(1,4) =", bst.lca(1, 4))  # 3
    print("LCA(1,8) =", bst.lca(1, 8))  # 5
    print("LCA(6,8) =", bst.lca(6, 8))  # 7

    print("2nd smallest:", bst.kth_smallest(2))  # 3
    print("5th smallest:", bst.kth_smallest(5))  # 6

    bst.delete(3)
    print("\nAfter deleting 3:", bst.sorted_values())

    bst.delete(5)
    print("After deleting root (5):", bst.sorted_values())


if __name__ == "__main__":
    main()


"""
NOTES (vs. Java):
- Java uses Long.MIN_VALUE / MAX_VALUE as bounds in isValidBST. Python uses
  math.inf / -math.inf — cleaner and unbounded.
- We provide an iterative kth_smallest (vs. Java's recursive helper with
  mutable counter array). Both are O(h+k).
- Recursion depth is bounded; for huge BSTs prefer iterative versions.
"""
