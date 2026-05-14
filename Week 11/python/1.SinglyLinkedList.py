"""
WEEK 11 - PYTHON DSA
Topic: Singly Linked List - Complete Implementation
File: 1.SinglyLinkedList.py

CONCEPT:
A singly linked list is a chain of nodes where each node carries data and a
reference to the next node. The chain ends with a `None` reference. Unlike
arrays we cannot index directly, but head insertions/removals are O(1).

KEY POINTS:
- Node: holds `data` and `next` attribute (default None).
- Head pointer: the only entry point to the list.
- O(1) insert at head, O(n) insert at tail (without a tail pointer).
- O(n) search; no random access.
- Cycle detection / middle finding via Floyd's slow/fast pointer trick.

ALGORITHM / APPROACH:
- insertAtHead: create node, point new.next = head, then head = new.
- insertAtTail: walk to last node (next is None) and append.
- insertAtIndex: walk to index-1, splice new node in.
- delete by value: track previous, unlink the matching node.
- reverse iterative: rewire prev/curr/next links in one pass.
- reverse recursive: recurse to end, flip pointer back through unwinding.
- findMiddle: slow advances 1, fast advances 2.
- hasCycle: same pattern; if slow == fast at any point we found a cycle.

PYTHON-SPECIFIC NOTES:
- We use a `@dataclass` with `__slots__` (`slots=True`, Python 3.10+) to
  reduce per-node memory; otherwise every node has a __dict__ which adds
  significant overhead for large lists. (vs. Java where every reference is
  a managed object pointer with object header).
- Recursion in Python has a default depth limit (~1000); for large lists
  prefer the iterative reverse.
- We expose `__iter__` and `__len__` for Pythonic usage (so `list(ll)` works).
- No null pointer dereference exception; assignment to None is fine.
- Tail pointer is omitted to mirror Java; production code would keep one.

DRY RUN:
Example 1: insertAtTail 1,2,3 then insertAtHead 0
  start: head=None
  insertAtTail(1): head=[1->None]
  insertAtTail(2): walk to 1, attach -> [1->2->None]
  insertAtTail(3): walk to 2, attach -> [1->2->3->None]
  insertAtHead(0): new(0).next=1, head=0 -> [0->1->2->3->None]

Example 2: reverseIterative on [1->2->3]
  prev=None curr=1
  step: next=2; curr.next=None; prev=1; curr=2 -> list: 1->None
  step: next=3; curr.next=1; prev=2; curr=3 -> list: 2->1->None
  step: next=None; curr.next=2; prev=3; curr=None -> list: 3->2->1->None
  head = prev = 3.  Reversed!

COMPLEXITY:
  insertHead/deleteHead: O(1) time, O(1) space
  insertTail/insertAtIndex/deleteByValue/contains/size: O(n) time, O(1) space
  reverseIterative: O(n) time, O(1) space
  reverseRecursive: O(n) time, O(n) space (recursion stack)
  findMiddle / hasCycle: O(n) time, O(1) space
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator, Optional


@dataclass(slots=True)
class Node:
    data: int
    next: Optional["Node"] = None


class LinkedList:
    """Singly linked list of ints (kept simple to mirror the Java demo)."""

    def __init__(self) -> None:
        self.head: Optional[Node] = None

    # --- mutation ---

    def insert_at_head(self, data: int) -> None:
        self.head = Node(data, self.head)

    def insert_at_tail(self, data: int) -> None:
        node = Node(data)
        if self.head is None:
            self.head = node
            return
        curr = self.head
        while curr.next is not None:
            curr = curr.next
        curr.next = node

    def insert_at_index(self, idx: int, data: int) -> None:
        if idx < 0:
            raise IndexError("Index out of bounds")
        if idx == 0:
            self.insert_at_head(data)
            return
        curr = self.head
        for _ in range(idx - 1):
            if curr is None:
                raise IndexError("Index out of bounds")
            curr = curr.next
        if curr is None:
            raise IndexError("Index out of bounds")
        curr.next = Node(data, curr.next)

    def delete_head(self) -> None:
        if self.head is not None:
            self.head = self.head.next

    def delete_by_value(self, val: int) -> bool:
        if self.head is None:
            return False
        if self.head.data == val:
            self.head = self.head.next
            return True
        curr = self.head
        while curr.next is not None:
            if curr.next.data == val:
                curr.next = curr.next.next
                return True
            curr = curr.next
        return False

    # --- queries ---

    def contains(self, val: int) -> bool:
        for x in self:
            if x == val:
                return True
        return False

    def __len__(self) -> int:
        n = 0
        curr = self.head
        while curr is not None:
            n += 1
            curr = curr.next
        return n

    def __iter__(self) -> Iterator[int]:
        curr = self.head
        while curr is not None:
            yield curr.data
            curr = curr.next

    # --- reverse ---

    def reverse_iterative(self) -> None:
        prev: Optional[Node] = None
        curr = self.head
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    def reverse_recursive(self) -> None:
        def helper(node: Optional[Node]) -> Optional[Node]:
            if node is None or node.next is None:
                return node
            new_head = helper(node.next)
            node.next.next = node
            node.next = None
            return new_head
        self.head = helper(self.head)

    # --- Floyd's tortoise & hare ---

    def find_middle(self) -> Optional[Node]:
        slow = fast = self.head
        while fast is not None and fast.next is not None:
            slow = slow.next  # type: ignore[union-attr]
            fast = fast.next.next
        return slow

    def has_cycle(self) -> bool:
        slow = fast = self.head
        while fast is not None and fast.next is not None:
            slow = slow.next  # type: ignore[union-attr]
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    # --- pretty print ---

    def __str__(self) -> str:
        parts = ["HEAD"]
        for v in self:
            parts.append(str(v))
        parts.append("NULL")
        return " -> ".join(parts)


def main() -> None:
    ll = LinkedList()
    for v in (1, 2, 3, 4, 5):
        ll.insert_at_tail(v)
    print(ll)  # HEAD -> 1 -> 2 -> 3 -> 4 -> 5 -> NULL

    ll.insert_at_head(0)
    print(ll)

    ll.insert_at_index(3, 99)
    print(ll)

    ll.delete_by_value(99)
    print(ll)

    print("Size:", len(ll))
    print("Contains 3:", ll.contains(3))
    print("Contains 9:", ll.contains(9))

    mid = ll.find_middle()
    print("Middle:", mid.data if mid else None)

    ll.reverse_iterative()
    print(ll)

    ll.reverse_recursive()
    print(ll)

    print("Has cycle:", ll.has_cycle())


if __name__ == "__main__":
    main()


"""
NOTES (vs. Java):
- Java uses static inner classes (`Node`, `LinkedList`); Python uses module-level
  classes. We rely on `@dataclass(slots=True)` for memory-efficient nodes.
- Python lacks `null` — we use `None` and Optional[...] type hints.
- Java throws IndexOutOfBoundsException; Python raises IndexError (idiomatic).
- We added `__iter__`, `__len__`, and `__str__` for Pythonic ergonomics; the
  Java version had explicit `size()` and `print()` methods.
- Recursion depth limit is real in Python; Java's stack is typically larger.
"""
