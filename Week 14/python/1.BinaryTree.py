"""
WEEK 14 - PYTHON DSA
Topic: Binary Tree - Structure, Traversals, Properties
File: 1.BinaryTree.py

CONCEPT:
A binary tree is a hierarchical structure where each node has at most two
children (left, right). Each node has data; the topmost node is the root;
leaves are nodes with no children.

KEY POINTS:
- Traversals:
    Inorder    L -> Root -> R   (sorted order if BST)
    Preorder   Root -> L -> R   (used for serialization)
    Postorder  L -> R -> Root   (used for deletion)
    Level-order BFS              (uses a queue)
- Properties: height, count, diameter (longest node-to-node path), mirror.

ALGORITHM / APPROACH:
- Recursive traversals: visit current at the appropriate position.
- Iterative inorder: simulate the recursion stack with an explicit stack.
- Level-order: BFS via collections.deque.
- Diameter: at each node track left height + right height; update global max.

PYTHON-SPECIFIC NOTES:
- Use @dataclass(slots=True) for compact nodes.
- Use list[int] return types for traversals; collections.deque for BFS.
- Recursion depth limit (~1000 by default); for deep trees switch to
  iterative versions or sys.setrecursionlimit (rarely needed for teaching).

DRY RUN:
Sample tree:
            1
          /   \
         2     3
        / \   / \
       4   5 6   7

Inorder:    4 2 5 1 6 3 7
Preorder:   1 2 4 5 3 6 7
Postorder:  4 5 2 6 7 3 1
Level-order: [[1],[2,3],[4,5,6,7]]
Height = 3, Count = 7, Diameter = 4 (path 4-2-1-3-7).

After mirror (in place):
            1
          /   \
         3     2
        / \   / \
       7   6 5   4
Inorder: 7 3 6 1 5 2 4

COMPLEXITY:
  Traversals: O(n) time, O(h) recursion stack.
  Level-order: O(n) time, O(w) where w = max width.
  Height/count/diameter/mirror: O(n) each.
"""

from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class Node:
    val: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def build_sample_tree() -> Node:
    root = Node(1)
    root.left = Node(2); root.right = Node(3)
    root.left.left = Node(4); root.left.right = Node(5)
    root.right.left = Node(6); root.right.right = Node(7)
    return root


def inorder(root: Optional[Node]) -> List[int]:
    out: List[int] = []
    def go(n: Optional[Node]) -> None:
        if n is None: return
        go(n.left); out.append(n.val); go(n.right)
    go(root)
    return out


def preorder(root: Optional[Node]) -> List[int]:
    out: List[int] = []
    def go(n: Optional[Node]) -> None:
        if n is None: return
        out.append(n.val); go(n.left); go(n.right)
    go(root)
    return out


def postorder(root: Optional[Node]) -> List[int]:
    out: List[int] = []
    def go(n: Optional[Node]) -> None:
        if n is None: return
        go(n.left); go(n.right); out.append(n.val)
    go(root)
    return out


def level_order(root: Optional[Node]) -> List[List[int]]:
    out: List[List[int]] = []
    if root is None:
        return out
    q: deque[Node] = deque([root])
    while q:
        level: List[int] = []
        for _ in range(len(q)):
            n = q.popleft()
            level.append(n.val)
            if n.left:  q.append(n.left)
            if n.right: q.append(n.right)
        out.append(level)
    return out


def inorder_iterative(root: Optional[Node]) -> List[int]:
    out: List[int] = []
    stack: List[Node] = []
    curr = root
    while curr is not None or stack:
        while curr is not None:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        out.append(curr.val)
        curr = curr.right
    return out


def height(root: Optional[Node]) -> int:
    if root is None: return 0
    return 1 + max(height(root.left), height(root.right))


def count_nodes(root: Optional[Node]) -> int:
    if root is None: return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def diameter(root: Optional[Node]) -> int:
    best = 0
    def go(n: Optional[Node]) -> int:
        nonlocal best
        if n is None: return 0
        l = go(n.left); r = go(n.right)
        best = max(best, l + r)
        return 1 + max(l, r)
    go(root)
    return best


def mirror(root: Optional[Node]) -> None:
    if root is None: return
    root.left, root.right = root.right, root.left
    mirror(root.left)
    mirror(root.right)


def main() -> None:
    root = build_sample_tree()
    print("Inorder:    ", inorder(root))         # 4 2 5 1 6 3 7
    print("Preorder:   ", preorder(root))        # 1 2 4 5 3 6 7
    print("Postorder:  ", postorder(root))       # 4 5 2 6 7 3 1
    print("Level-order:", level_order(root))     # [[1],[2,3],[4,5,6,7]]
    print("Inorder it: ", inorder_iterative(root))

    print("\nHeight:    ", height(root))         # 3
    print("Node count:", count_nodes(root))      # 7
    print("Diameter:  ", diameter(root))         # 4

    mirror(root)
    print("\nAfter mirror:")
    print("Inorder:", inorder(root))             # 7 3 6 1 5 2 4


if __name__ == "__main__":
    main()


"""
NOTES (vs. Java):
- Java's static inner class Node becomes a module-level @dataclass.
- We use Python's `nonlocal` keyword inside `diameter` to mutate the closure
  variable; Java mutates a length-1 int[] hack or a class field.
- Tuple unpacking `root.left, root.right = root.right, root.left` is the
  Pythonic in-place swap (no temp variable).
- Recursion limit warning: Python's default is ~1000 (vs. Java's larger
  stack); use sys.setrecursionlimit if a tree is very deep.
"""
