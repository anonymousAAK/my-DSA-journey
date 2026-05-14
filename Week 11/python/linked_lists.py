"""
Week 11 — Linked Lists
========================
Topics covered:
  - SinglyLinkedList class:
      • insert at head / tail
      • delete by value
      • search
      • reverse (iterative + recursive)
      • find middle (slow/fast pointers)
      • detect cycle (Floyd's algorithm)
  - Merge two sorted linked lists
  - LRU Cache:
      • Simple approach using collections.OrderedDict
      • Manual approach using a doubly-linked list + dict

Each class/function includes time/space complexity analysis.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Iterator, Optional


# ===========================================================================
# Node class
# ===========================================================================

class ListNode:
    """A node in a singly linked list."""

    __slots__ = ("val", "next")

    def __init__(self, val: int = 0, nxt: ListNode | None = None) -> None:
        self.val = val
        self.next = nxt

    def __repr__(self) -> str:
        return f"ListNode({self.val})"


# ===========================================================================
# Singly Linked List
# ===========================================================================

class SinglyLinkedList:
    """Singly linked list with common operations.

    Space: O(n) for n nodes.
    """

    def __init__(self) -> None:
        self.head: ListNode | None = None

    # ---- Insertion ----

    def insert_head(self, val: int) -> None:
        """Insert a node at the head.  O(1)"""
        self.head = ListNode(val, self.head)

    def insert_tail(self, val: int) -> None:
        """Insert a node at the tail.  O(n)"""
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    # ---- Deletion ----

    def delete(self, val: int) -> bool:
        """Delete the first node with the given value.  Returns True if found.

        Time: O(n)
        """
        if not self.head:
            return False
        if self.head.val == val:
            self.head = self.head.next
            return True
        curr = self.head
        while curr.next:
            if curr.next.val == val:
                curr.next = curr.next.next
                return True
            curr = curr.next
        return False

    # ---- Search ----

    def search(self, val: int) -> bool:
        """Return True if *val* exists in the list.  O(n)"""
        curr = self.head
        while curr:
            if curr.val == val:
                return True
            curr = curr.next
        return False

    # ---- Reverse ----

    def reverse_iterative(self) -> None:
        """Reverse the list in-place iteratively.

        Time: O(n)  Space: O(1)
        """
        prev, curr = None, self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    def reverse_recursive(self) -> None:
        """Reverse the list in-place recursively.

        Time: O(n)  Space: O(n) — call stack
        """

        def _reverse(node: ListNode | None) -> ListNode | None:
            if not node or not node.next:
                return node
            new_head = _reverse(node.next)
            node.next.next = node
            node.next = None
            return new_head

        self.head = _reverse(self.head)

    # ---- Find Middle ----

    def find_middle(self) -> ListNode | None:
        """Return the middle node using the slow/fast pointer technique.

        For even-length lists, returns the second of the two middle nodes.

        Time: O(n)  Space: O(1)
        """
        if not self.head:
            return None
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next  # type: ignore[union-attr]
            fast = fast.next.next
        return slow

    # ---- Cycle Detection ----

    def has_cycle(self) -> bool:
        """Detect a cycle using Floyd's tortoise-and-hare algorithm.

        Time: O(n)  Space: O(1)
        """
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next  # type: ignore[union-attr]
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    # ---- Utilities ----

    def to_list(self) -> list[int]:
        """Convert linked list to a Python list for easy comparison."""
        result: list[int] = []
        curr = self.head
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result

    @classmethod
    def from_list(cls, values: list[int]) -> SinglyLinkedList:
        """Create a SinglyLinkedList from a Python list."""
        sll = cls()
        for val in reversed(values):
            sll.insert_head(val)
        return sll

    def __repr__(self) -> str:
        return " -> ".join(str(v) for v in self.to_list()) + " -> None"


# ===========================================================================
# Merge Two Sorted Linked Lists
# ===========================================================================

def merge_sorted_lists(
    l1: ListNode | None, l2: ListNode | None
) -> ListNode | None:
    """Merge two sorted linked lists into one sorted list.

    Returns the head of the merged list (new nodes are NOT created;
    existing nodes are re-linked).

    Time:  O(n + m)
    Space: O(1)  — only pointer manipulation
    """
    dummy = ListNode(0)
    tail = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    tail.next = l1 if l1 else l2
    return dummy.next


# ===========================================================================
# LRU Cache — OrderedDict Approach
# ===========================================================================

class LRUCacheOrdered:
    """Least Recently Used cache using collections.OrderedDict.

    get / put are both O(1) amortized.
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        """Return value for *key* or -1 if absent.  Marks key as recently used."""
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        """Insert or update *key*.  Evicts the LRU item if at capacity."""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # remove LRU (front)


# ===========================================================================
# LRU Cache — Manual Doubly-Linked List + Dict
# ===========================================================================

class _DLLNode:
    """Node for the internal doubly-linked list of LRUCacheManual."""
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0) -> None:
        self.key = key
        self.val = val
        self.prev: _DLLNode | None = None
        self.next: _DLLNode | None = None


class LRUCacheManual:
    """LRU Cache using a doubly-linked list (for O(1) removal/insertion)
    and a hash map (for O(1) lookup).

    get / put are both O(1).
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: dict[int, _DLLNode] = {}
        # Sentinel nodes simplify edge-case handling
        self._head = _DLLNode()  # dummy head (LRU side)
        self._tail = _DLLNode()  # dummy tail (MRU side)
        self._head.next = self._tail
        self._tail.prev = self._head

    # ---- Internal helpers ----

    def _remove(self, node: _DLLNode) -> None:
        """Remove *node* from the doubly-linked list."""
        prev_node, next_node = node.prev, node.next
        prev_node.next = next_node  # type: ignore[union-attr]
        next_node.prev = prev_node  # type: ignore[union-attr]

    def _add_to_tail(self, node: _DLLNode) -> None:
        """Add *node* right before the dummy tail (most recently used)."""
        prev_node = self._tail.prev
        prev_node.next = node  # type: ignore[union-attr]
        node.prev = prev_node
        node.next = self._tail
        self._tail.prev = node

    # ---- Public API ----

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_tail(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = _DLLNode(key, value)
        self._add_to_tail(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            # Evict LRU — the node right after the dummy head
            lru = self._head.next
            self._remove(lru)  # type: ignore[arg-type]
            del self.cache[lru.key]  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ---- SinglyLinkedList basics ----
    sll = SinglyLinkedList.from_list([1, 2, 3, 4, 5])
    assert sll.to_list() == [1, 2, 3, 4, 5]
    sll.insert_head(0)
    sll.insert_tail(6)
    assert sll.to_list() == [0, 1, 2, 3, 4, 5, 6]
    assert sll.search(3) is True
    assert sll.search(99) is False
    sll.delete(3)
    assert sll.to_list() == [0, 1, 2, 4, 5, 6]
    sll.delete(0)
    assert sll.to_list() == [1, 2, 4, 5, 6]
    print("[PASS] SinglyLinkedList — insert, delete, search")

    # ---- Reverse ----
    sll = SinglyLinkedList.from_list([1, 2, 3, 4])
    sll.reverse_iterative()
    assert sll.to_list() == [4, 3, 2, 1]
    sll.reverse_recursive()
    assert sll.to_list() == [1, 2, 3, 4]
    print("[PASS] Reverse — iterative & recursive")

    # ---- Find Middle ----
    sll = SinglyLinkedList.from_list([1, 2, 3, 4, 5])
    assert sll.find_middle().val == 3  # type: ignore[union-attr]
    sll = SinglyLinkedList.from_list([1, 2, 3, 4])
    assert sll.find_middle().val == 3  # type: ignore[union-attr]  # second middle
    print("[PASS] Find middle")

    # ---- Cycle Detection ----
    sll = SinglyLinkedList.from_list([1, 2, 3])
    assert sll.has_cycle() is False
    # Manually create a cycle: 3 -> 1
    node1 = sll.head
    node3 = node1.next.next  # type: ignore[union-attr]
    node3.next = node1  # type: ignore[union-attr]
    assert sll.has_cycle() is True
    print("[PASS] Cycle detection (Floyd's)")

    # ---- Merge Two Sorted Lists ----
    a = SinglyLinkedList.from_list([1, 3, 5])
    b = SinglyLinkedList.from_list([2, 4, 6])
    merged_head = merge_sorted_lists(a.head, b.head)
    merged = SinglyLinkedList()
    merged.head = merged_head
    assert merged.to_list() == [1, 2, 3, 4, 5, 6]
    print("[PASS] Merge two sorted lists")

    # ---- LRU Cache (both implementations) ----
    for CacheClass in (LRUCacheOrdered, LRUCacheManual):
        cache = CacheClass(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1
        cache.put(3, 3)  # evicts key 2
        assert cache.get(2) == -1
        cache.put(4, 4)  # evicts key 1
        assert cache.get(1) == -1
        assert cache.get(3) == 3
        assert cache.get(4) == 4
    print("[PASS] LRU Cache — OrderedDict & manual DLL+dict")

    print("\nAll Week 11 tests passed!")
