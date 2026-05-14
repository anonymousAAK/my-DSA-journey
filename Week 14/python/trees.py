"""
Week 14 — Trees (Binary Trees & Binary Search Trees)
======================================================
Topics covered:
  Binary Tree:
    - TreeNode class
    - Traversals: inorder, preorder, postorder, level-order
      (recursive + iterative versions)
    - Height (max depth)
    - Diameter
    - Mirror / invert a binary tree
  Binary Search Tree (BST):
    - Insert, delete, search
    - Validate BST
    - Lowest Common Ancestor (LCA)
    - k-th smallest element
  Serialization:
    - Serialize / deserialize using preorder traversal

Each function includes time/space complexity analysis.
"""

from __future__ import annotations

from collections import deque
from typing import Iterator, List, Optional


# ===========================================================================
# TreeNode
# ===========================================================================

class TreeNode:
    """A node in a binary tree."""

    __slots__ = ("val", "left", "right")

    def __init__(
        self,
        val: int = 0,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


# ===========================================================================
# Binary Tree Traversals — Recursive
# ===========================================================================

def inorder_recursive(root: TreeNode | None) -> List[int]:
    """Left → Root → Right.

    Time: O(n)  Space: O(h) — recursion depth, h = height
    """
    if not root:
        return []
    return inorder_recursive(root.left) + [root.val] + inorder_recursive(root.right)


def preorder_recursive(root: TreeNode | None) -> List[int]:
    """Root → Left → Right.

    Time: O(n)  Space: O(h)
    """
    if not root:
        return []
    return [root.val] + preorder_recursive(root.left) + preorder_recursive(root.right)


def postorder_recursive(root: TreeNode | None) -> List[int]:
    """Left → Right → Root.

    Time: O(n)  Space: O(h)
    """
    if not root:
        return []
    return postorder_recursive(root.left) + postorder_recursive(root.right) + [root.val]


def level_order(root: TreeNode | None) -> List[List[int]]:
    """BFS level-order traversal, returning values grouped by level.

    Time: O(n)  Space: O(n) — the queue
    """
    if not root:
        return []
    result: list[list[int]] = []
    queue: deque[TreeNode] = deque([root])
    while queue:
        level_size = len(queue)
        level_vals: list[int] = []
        for _ in range(level_size):
            node = queue.popleft()
            level_vals.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level_vals)
    return result


# ===========================================================================
# Binary Tree Traversals — Iterative
# ===========================================================================

def inorder_iterative(root: TreeNode | None) -> List[int]:
    """Iterative inorder using an explicit stack.

    Time: O(n)  Space: O(h)
    """
    result: list[int] = []
    stack: list[TreeNode] = []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result


def preorder_iterative(root: TreeNode | None) -> List[int]:
    """Iterative preorder using a stack.

    Time: O(n)  Space: O(h)
    """
    if not root:
        return []
    result: list[int] = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        # Push right first so left is processed first
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result


def postorder_iterative(root: TreeNode | None) -> List[int]:
    """Iterative postorder using two stacks.

    Approach: modified preorder (Root → Right → Left) pushed onto a second
    stack, then the second stack gives Left → Right → Root.

    Time: O(n)  Space: O(n)
    """
    if not root:
        return []
    stack1: list[TreeNode] = [root]
    stack2: list[int] = []
    while stack1:
        node = stack1.pop()
        stack2.append(node.val)
        if node.left:
            stack1.append(node.left)
        if node.right:
            stack1.append(node.right)
    return stack2[::-1]


# ===========================================================================
# Height / Max Depth
# ===========================================================================

def height(root: TreeNode | None) -> int:
    """Return the height (max depth) of the tree.  An empty tree has height 0.

    Time: O(n)  Space: O(h)
    """
    if not root:
        return 0
    return 1 + max(height(root.left), height(root.right))


# ===========================================================================
# Diameter
# ===========================================================================

def diameter(root: TreeNode | None) -> int:
    """Return the diameter of the tree (length of the longest path between
    any two nodes, measured in number of edges).

    Time: O(n)  Space: O(h)
    """
    best = 0

    def _depth(node: TreeNode | None) -> int:
        nonlocal best
        if not node:
            return 0
        left_d = _depth(node.left)
        right_d = _depth(node.right)
        best = max(best, left_d + right_d)
        return 1 + max(left_d, right_d)

    _depth(root)
    return best


# ===========================================================================
# Mirror / Invert Binary Tree
# ===========================================================================

def mirror(root: TreeNode | None) -> TreeNode | None:
    """Invert a binary tree (swap left and right children at every node).

    Time: O(n)  Space: O(h)
    """
    if not root:
        return None
    root.left, root.right = mirror(root.right), mirror(root.left)
    return root


# ===========================================================================
# BST — Insert
# ===========================================================================

def bst_insert(root: TreeNode | None, val: int) -> TreeNode:
    """Insert *val* into a BST and return the (possibly new) root.

    Time: O(h)  Space: O(h) recursion, or O(1) iterative
    """
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = bst_insert(root.left, val)
    elif val > root.val:
        root.right = bst_insert(root.right, val)
    # Duplicate values are ignored
    return root


# ===========================================================================
# BST — Search
# ===========================================================================

def bst_search(root: TreeNode | None, val: int) -> TreeNode | None:
    """Search for *val* in a BST.  Return the node or None.

    Time: O(h)  Space: O(1) iterative
    """
    while root:
        if val == root.val:
            return root
        elif val < root.val:
            root = root.left
        else:
            root = root.right
    return None


# ===========================================================================
# BST — Delete
# ===========================================================================

def bst_delete(root: TreeNode | None, val: int) -> TreeNode | None:
    """Delete *val* from a BST and return the root.

    Three cases:
      1. Leaf → simply remove.
      2. One child → replace with child.
      3. Two children → replace with inorder successor (smallest in right
         subtree), then delete the successor.

    Time: O(h)  Space: O(h)
    """
    if not root:
        return None

    if val < root.val:
        root.left = bst_delete(root.left, val)
    elif val > root.val:
        root.right = bst_delete(root.right, val)
    else:
        # Found the node to delete
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        # Two children: find inorder successor
        successor = root.right
        while successor.left:
            successor = successor.left
        root.val = successor.val
        root.right = bst_delete(root.right, successor.val)

    return root


# ===========================================================================
# BST — Validate
# ===========================================================================

def is_valid_bst(root: TreeNode | None) -> bool:
    """Return True if the tree is a valid BST.

    Uses the property that inorder traversal of a BST is strictly increasing.

    Time: O(n)  Space: O(h)
    """

    def _validate(
        node: TreeNode | None, lo: float, hi: float
    ) -> bool:
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return (
            _validate(node.left, lo, node.val)
            and _validate(node.right, node.val, hi)
        )

    return _validate(root, float("-inf"), float("inf"))


# ===========================================================================
# BST — Lowest Common Ancestor
# ===========================================================================

def bst_lca(
    root: TreeNode | None, p: int, q: int
) -> TreeNode | None:
    """Find the Lowest Common Ancestor of nodes with values *p* and *q*
    in a BST.

    Exploit BST ordering: if both values are smaller, go left; if both
    are larger, go right; otherwise, current node is the LCA.

    Time: O(h)  Space: O(1)
    """
    while root:
        if p < root.val and q < root.val:
            root = root.left
        elif p > root.val and q > root.val:
            root = root.right
        else:
            return root
    return None


# ===========================================================================
# BST — k-th Smallest Element
# ===========================================================================

def kth_smallest(root: TreeNode | None, k: int) -> int:
    """Return the k-th smallest value (1-indexed) in a BST using iterative
    inorder traversal.

    Time: O(h + k)  Space: O(h)
    """
    stack: list[TreeNode] = []
    curr = root
    count = 0

    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        count += 1
        if count == k:
            return curr.val
        curr = curr.right

    raise ValueError(f"k={k} is out of range")


# ===========================================================================
# Serialize / Deserialize (Preorder)
# ===========================================================================

_NULL = "#"
_SEP = ","


def serialize(root: TreeNode | None) -> str:
    """Serialize a binary tree to a string using preorder traversal.

    Null nodes are represented by '#'.

    Time: O(n)  Space: O(n)
    """
    tokens: list[str] = []

    def _preorder(node: TreeNode | None) -> None:
        if not node:
            tokens.append(_NULL)
            return
        tokens.append(str(node.val))
        _preorder(node.left)
        _preorder(node.right)

    _preorder(root)
    return _SEP.join(tokens)


def deserialize(data: str) -> TreeNode | None:
    """Reconstruct a binary tree from a preorder-serialized string.

    Time: O(n)  Space: O(n)
    """
    tokens = iter(data.split(_SEP))

    def _build() -> TreeNode | None:
        token = next(tokens)
        if token == _NULL:
            return None
        node = TreeNode(int(token))
        node.left = _build()
        node.right = _build()
        return node

    return _build()


# ---------------------------------------------------------------------------
# Helper: build a BST from a list of values (for testing)
# ---------------------------------------------------------------------------

def _build_bst(values: list[int]) -> TreeNode | None:
    root: TreeNode | None = None
    for v in values:
        root = bst_insert(root, v)
    return root


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Build a sample BST:
    #         5
    #        / \
    #       3   7
    #      / \ / \
    #     2  4 6  8
    bst = _build_bst([5, 3, 7, 2, 4, 6, 8])

    # ---- Traversals (recursive) ----
    assert inorder_recursive(bst) == [2, 3, 4, 5, 6, 7, 8]
    assert preorder_recursive(bst) == [5, 3, 2, 4, 7, 6, 8]
    assert postorder_recursive(bst) == [2, 4, 3, 6, 8, 7, 5]
    assert level_order(bst) == [[5], [3, 7], [2, 4, 6, 8]]
    print("[PASS] Traversals — recursive + level-order")

    # ---- Traversals (iterative) ----
    assert inorder_iterative(bst) == [2, 3, 4, 5, 6, 7, 8]
    assert preorder_iterative(bst) == [5, 3, 2, 4, 7, 6, 8]
    assert postorder_iterative(bst) == [2, 4, 3, 6, 8, 7, 5]
    print("[PASS] Traversals — iterative")

    # ---- Height ----
    assert height(bst) == 3
    assert height(None) == 0
    print("[PASS] Height")

    # ---- Diameter ----
    assert diameter(bst) == 4  # path: 2-3-5-7-8 (or similar)
    print("[PASS] Diameter")

    # ---- Mirror ----
    mirrored = _build_bst([5, 3, 7, 2, 4, 6, 8])
    mirror(mirrored)
    assert inorder_recursive(mirrored) == [8, 7, 6, 5, 4, 3, 2]
    print("[PASS] Mirror / invert")

    # ---- BST Search ----
    assert bst_search(bst, 4) is not None
    assert bst_search(bst, 4).val == 4  # type: ignore[union-attr]
    assert bst_search(bst, 99) is None
    print("[PASS] BST search")

    # ---- BST Delete ----
    bst2 = _build_bst([5, 3, 7, 2, 4, 6, 8])
    bst2 = bst_delete(bst2, 3)
    assert 3 not in inorder_recursive(bst2)
    assert inorder_recursive(bst2) == [2, 4, 5, 6, 7, 8]
    print("[PASS] BST delete")

    # ---- Validate BST ----
    assert is_valid_bst(bst) is True
    # Create an invalid BST
    bad = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
    assert is_valid_bst(bad) is False
    print("[PASS] Validate BST")

    # ---- LCA ----
    assert bst_lca(bst, 2, 4).val == 3  # type: ignore[union-attr]
    assert bst_lca(bst, 2, 8).val == 5  # type: ignore[union-attr]
    assert bst_lca(bst, 6, 8).val == 7  # type: ignore[union-attr]
    print("[PASS] BST LCA")

    # ---- k-th Smallest ----
    assert kth_smallest(bst, 1) == 2
    assert kth_smallest(bst, 3) == 4
    assert kth_smallest(bst, 5) == 6
    print("[PASS] k-th smallest in BST")

    # ---- Serialize / Deserialize ----
    serialized = serialize(bst)
    restored = deserialize(serialized)
    assert inorder_recursive(restored) == inorder_recursive(bst)
    assert preorder_recursive(restored) == preorder_recursive(bst)
    # Round-trip on empty tree
    assert serialize(None) == "#"
    assert deserialize("#") is None
    print("[PASS] Serialize / deserialize (preorder)")

    print("\nAll Week 14 tests passed!")
