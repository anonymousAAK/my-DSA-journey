"""Reference: reverse a singly-linked list.

Cases represent lists as arrays of node values. This driver builds a linked
list from the input array, performs the iterative reversal, and serialises
the resulting list back to an array of values.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class _Node:
    val: int
    next: Optional["_Node"] = None


def _build(vals: List[int]) -> Optional[_Node]:
    head: Optional[_Node] = None
    for v in reversed(vals):
        head = _Node(v, head)
    return head


def _to_list(head: Optional[_Node]) -> List[int]:
    out: List[int] = []
    curr = head
    while curr is not None:
        out.append(curr.val)
        curr = curr.next
    return out


def reverseList(vals: List[int]) -> List[int]:
    head = _build(vals)
    prev: Optional[_Node] = None
    curr = head
    while curr is not None:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return _to_list(prev)
