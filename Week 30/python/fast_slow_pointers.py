"""
WEEK 30 - PYTHON ADVANCED TOPICS
Topic: Fast & Slow Pointers (Floyd's Tortoise and Hare)
File: fast_slow_pointers.py

CONCEPT:
    Use two pointers traversing the same sequence at different speeds (the
    slow advances by 1, the fast by 2). If a cycle exists they must
    eventually coincide. After the meeting, additional walks pinpoint the
    cycle entry. Same idea generalises to any deterministic next-state
    function (digit-square chain for the Happy Number problem).

KEY POINTS:
    - O(n) time, O(1) space — perfect for "detect a loop without modifying
      the structure" or "no extra memory".
    - For finding the cycle entry: reset one pointer to head, advance both
      one step at a time until they meet again.
    - Works on linked lists, integer sequences (Happy Number), graphs with
      deterministic edges (next-state functions).

ALGORITHM / APPROACH:
    HAS CYCLE:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next; fast = fast.next.next
            if slow == fast: return True
        return False
    CYCLE START:
        on collision: reset entry = head; advance both by 1; meeting = entry
    HAPPY NUMBER:
        slow = n; fast = n
        do { slow = step(slow); fast = step(step(fast)); } while slow != fast
        return slow == 1
    MIDDLE OF LIST:
        slow = fast = head
        while fast and fast.next: slow=slow.next; fast=fast.next.next
        return slow

PYTHON-SPECIFIC NOTES:
    - dataclass for ListNode keeps code light.
    - Use `is` for node identity comparisons.

DRY RUN / EXAMPLE:
    List 1 -> 2 -> 3 -> back to 2 (cycle). has_cycle returns True;
    detect_cycle_start returns the node with value 2.
    is_happy(19) -> True; is_happy(2) -> False.

COMPLEXITY:
    Time:  O(n).
    Space: O(1).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def has_cycle(head: Optional[ListNode]) -> bool:
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[union-attr]
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def detect_cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[union-attr]
        fast = fast.next.next
        if slow is fast:
            entry = head
            while entry is not slow:
                entry = entry.next  # type: ignore[union-attr]
                slow = slow.next    # type: ignore[union-attr]
            return entry
    return None


def middle_of_list(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[union-attr]
        fast = fast.next.next
    return slow


def _digit_square_sum(n: int) -> int:
    s = 0
    while n:
        d = n % 10
        s += d * d
        n //= 10
    return s


def is_happy(n: int) -> bool:
    slow, fast = n, n
    while True:
        slow = _digit_square_sum(slow)
        fast = _digit_square_sum(_digit_square_sum(fast))
        if slow == fast:
            return slow == 1


def _demo() -> None:
    # Build 1 -> 2 -> 3 -> back to 2
    a = ListNode(1)
    b = ListNode(2)
    c = ListNode(3)
    a.next = b; b.next = c; c.next = b
    print(f"has_cycle: {has_cycle(a)}")  # True
    start = detect_cycle_start(a)
    print(f"cycle starts at value: {start.val if start else None}")

    # Acyclic 1 -> 2 -> 3 -> 4 -> 5
    n1 = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    print(f"middle value: {middle_of_list(n1).val}")  # 3

    print(f"is_happy(19): {is_happy(19)}")  # True
    print(f"is_happy(2):  {is_happy(2)}")   # False


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * `@dataclass` keeps ListNode definition tight.
#   * Use `is` rather than `==` for node-identity comparison.
#   * Same algorithms; Python's dynamic typing is the main shift.
