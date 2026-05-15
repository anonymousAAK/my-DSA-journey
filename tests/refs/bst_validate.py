"""Reference: validate a binary search tree.

The fixture encodes a binary tree as a level-order list using `None` for
missing children (LeetCode-style). The driver reconstructs the tree and runs
the recursive bounds check.

A strict BST requires `lo < node.val < hi`.
"""

from __future__ import annotations
from dataclasses import dataclass
from math import inf
from typing import List, Optional, Any


@dataclass
class _Node:
    val: int
    left: Optional["_Node"] = None
    right: Optional["_Node"] = None


def _build(values: List[Any]) -> Optional[_Node]:
    if not values or values[0] is None:
        return None
    root = _Node(values[0])
    queue: List[_Node] = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values):
            v = values[i]
            if v is not None:
                node.left = _Node(v)
                queue.append(node.left)
            i += 1
        if i < len(values):
            v = values[i]
            if v is not None:
                node.right = _Node(v)
                queue.append(node.right)
            i += 1
    return root


def isValidBST(values: List[Any]) -> bool:
    root = _build(values)

    def check(n: Optional[_Node], lo: float, hi: float) -> bool:
        if n is None:
            return True
        if not (lo < n.val < hi):
            return False
        return check(n.left, lo, n.val) and check(n.right, n.val, hi)

    return check(root, -inf, inf)
