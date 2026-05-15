"""
WEEK 11 - PYTHON DSA
Topic: Merge Two Sorted Lists + LRU Cache
File: 2.MergeSortedListsAndLRU.py

CONCEPT:
PART A - Merge two sorted singly-linked lists into one sorted list with O(1)
extra memory by re-wiring next pointers (no node copies).
PART B - An LRU (Least-Recently-Used) cache with O(1) get/put. The trick is
combining a hashmap (key -> node) with a doubly-linked list whose head holds
the most-recently-used entry and tail the least-recently-used.

KEY POINTS:
- Merge: dummy sentinel head simplifies wiring; loop while both non-empty,
  attach the smaller, then attach the leftover tail.
- LRU: every get/put moves the touched node to the front (MRU). On insert
  past capacity we drop the node before the tail sentinel.
- Both head and tail are sentinels (dummy nodes), so we never special-case
  empty list / single-node edges.

ALGORITHM / APPROACH:
- mergeSortedLists(l1, l2): walk both lists with pointers; pick smaller head.
- LRU.get(k): if not present return -1; otherwise remove node from current
  position and re-insert after head, return its value.
- LRU.put(k, v): update value if present (and bump to front); else, if at
  capacity evict tail.prev, then insert new node after head.

PYTHON-SPECIFIC NOTES:
- Built-in `collections.OrderedDict` already provides O(1) reorder semantics
  via `move_to_end`. We include a second LRU implementation that demonstrates
  this Pythonic approach (idiomatic vs. the hand-rolled DLL).
- We could also use `functools.lru_cache` decorator — but that wraps a
  function, not a key/value store; it's not a drop-in replacement here.
- Type hints use `Optional` and forward refs.
- No reliance on garbage timing — the hashmap reference is what keeps a node
  alive; once removed from both map and DLL it's eligible for GC.

DRY RUN:
Example 1: merge [1,2,4] + [1,3,4]
  dummy -> ?
  l1=1, l2=1 -> attach l1; curr=1; l1=2
  l1=2, l2=1 -> attach l2; curr=1; l2=3
  l1=2, l2=3 -> attach l1; curr=2; l1=4
  l1=4, l2=3 -> attach l2; curr=3; l2=4
  l1=4, l2=4 -> attach l1; curr=4; l1=None
  attach remainder l2=4
  result: 1 -> 1 -> 2 -> 3 -> 4 -> 4

Example 2: LRUCache(capacity=3) operations
  put(1,1): cache state head <-> [1] <-> tail
  put(2,2): head <-> [2] <-> [1] <-> tail
  put(3,3): head <-> [3] <-> [2] <-> [1] <-> tail
  get(1) -> 1; bump 1 to front: head <-> [1] <-> [3] <-> [2] <-> tail
  put(4,4): full, evict 2: head <-> [4] <-> [1] <-> [3] <-> tail
  get(2) -> -1 (evicted)

COMPLEXITY:
  mergeSortedLists: O(m+n) time, O(1) extra space
  LRU.get / LRU.put: O(1) amortized time, O(capacity) space
"""

from __future__ import annotations
from collections import OrderedDict
from dataclasses import dataclass
from typing import Iterable, Optional


# ----- PART A: Merge sorted lists -----

@dataclass(slots=True)
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def build_list(vals: Iterable[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next


def print_list(head: Optional[ListNode]) -> str:
    parts = []
    while head is not None:
        parts.append(str(head.val))
        head = head.next
    return " -> ".join(parts)


def merge_sorted_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode(0)
    curr = dummy
    while l1 is not None and l2 is not None:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 if l1 is not None else l2
    return dummy.next


# ----- PART B: LRU Cache (hand-rolled DLL + dict) -----

class _DLNode:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int, val: int) -> None:
        self.key = key
        self.val = val
        self.prev: Optional[_DLNode] = None
        self.next: Optional[_DLNode] = None


class LRUCache:
    """Classic LRU: O(1) get/put via dict + doubly-linked list."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.map: dict[int, _DLNode] = {}
        # sentinels — head side is MRU, tail side is LRU
        self.head = _DLNode(0, 0)
        self.tail = _DLNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _DLNode) -> None:
        node.prev.next = node.next  # type: ignore[union-attr]
        node.next.prev = node.prev  # type: ignore[union-attr]

    def _insert_after_head(self, node: _DLNode) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node  # type: ignore[union-attr]
        self.head.next = node

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        self._remove(node)
        self._insert_after_head(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        node = self.map.get(key)
        if node is not None:
            node.val = value
            self._remove(node)
            self._insert_after_head(node)
            return
        if len(self.map) == self.capacity:
            lru = self.tail.prev
            assert lru is not None and lru is not self.head
            self._remove(lru)
            del self.map[lru.key]
        new_node = _DLNode(key, value)
        self._insert_after_head(new_node)
        self.map[key] = new_node

    def state(self) -> str:
        parts = []
        curr = self.head.next
        while curr is not None and curr is not self.tail:
            parts.append(f"[{curr.key}={curr.val}]")
            curr = curr.next
        return "Cache (MRU->LRU): " + " -> ".join(parts)


# ----- LRU using OrderedDict (idiomatic Python variant) -----

class LRUCacheOrderedDict:
    """Same semantics as LRUCache but built on collections.OrderedDict.

    OrderedDict.move_to_end(key) is O(1). popitem(last=False) removes the
    oldest entry in O(1). This is the idiomatic Python implementation.
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: "OrderedDict[int, int]" = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # MRU is now at the right end
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # evict LRU (left end)

    def state(self) -> str:
        # rightmost is MRU here (opposite of the DLL version's head side)
        items = " -> ".join(f"[{k}={v}]" for k, v in reversed(self.cache.items()))
        return "Cache (MRU->LRU): " + items


def main() -> None:
    print("=== Merge Sorted Lists ===")
    l1 = build_list([1, 2, 4])
    l2 = build_list([1, 3, 4])
    print("L1:", print_list(l1))
    print("L2:", print_list(l2))
    print("Merged:", print_list(merge_sorted_lists(l1, l2)))

    l3 = build_list([1, 3, 5, 7])
    l4 = build_list([2, 4, 6, 8, 10])
    print("Merged:", print_list(merge_sorted_lists(l3, l4)))

    print("\n=== LRU Cache (DLL + dict, capacity=3) ===")
    cache = LRUCache(3)
    cache.put(1, 1); print(cache.state())
    cache.put(2, 2); print(cache.state())
    cache.put(3, 3); print(cache.state())
    print("get(1) =", cache.get(1)); print(cache.state())
    cache.put(4, 4); print(cache.state())
    print("get(2) =", cache.get(2))
    print("get(3) =", cache.get(3))
    print("get(4) =", cache.get(4))
    print(cache.state())

    print("\n=== LRU Cache (OrderedDict variant, capacity=3) ===")
    od = LRUCacheOrderedDict(3)
    od.put(1, 1); od.put(2, 2); od.put(3, 3)
    print(od.state())
    od.get(1); print("after get(1):", od.state())
    od.put(4, 4); print("after put(4,4):", od.state())
    print("get(2) =", od.get(2))


if __name__ == "__main__":
    main()


"""
NOTES (vs. Java):
- Java's HashMap<Integer,DLNode> becomes a plain dict[int, _DLNode]. Python
  dicts already have very efficient hashing for ints.
- The OrderedDict variant has no Java analogue prior to LinkedHashMap (which
  ALSO supports access-order via constructor flag — would have been an even
  closer parallel).
- We use sentinels exactly like the Java version to avoid edge cases.
- Optional[...] is the Python equivalent of Java's nullable references.
"""
