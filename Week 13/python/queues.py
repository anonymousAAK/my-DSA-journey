"""
Week 13 — Queues
==================
Topics covered:
  - Queue using collections.deque
  - Circular queue class (fixed-size ring buffer)
  - Queue using two stacks
  - Sliding window maximum (monotonic deque)

Each class/function includes time/space complexity analysis.
"""

from __future__ import annotations

from collections import deque
from typing import List


# ===========================================================================
# Queue Using collections.deque
# ===========================================================================

class Queue:
    """FIFO queue backed by collections.deque.

    All operations are O(1).
    """

    def __init__(self) -> None:
        self._data: deque[int] = deque()

    def enqueue(self, val: int) -> None:
        """Add *val* to the back of the queue.  O(1)"""
        self._data.append(val)

    def dequeue(self) -> int:
        """Remove and return the front element.  O(1)

        Raises IndexError if the queue is empty.
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def front(self) -> int:
        """Peek at the front element without removing it.  O(1)"""
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._data[0]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Queue({list(self._data)})"


# ===========================================================================
# Circular Queue (Fixed-Size Ring Buffer)
# ===========================================================================

class CircularQueue:
    """Fixed-capacity circular queue using a list as a ring buffer.

    All operations are O(1).
    Space: O(k) where k = capacity.
    """

    def __init__(self, capacity: int) -> None:
        self._buf: list[int | None] = [None] * capacity
        self._capacity = capacity
        self._front = 0
        self._rear = -1
        self._size = 0

    def enqueue(self, val: int) -> bool:
        """Add *val* to the rear.  Returns False if full."""
        if self.is_full():
            return False
        self._rear = (self._rear + 1) % self._capacity
        self._buf[self._rear] = val
        self._size += 1
        return True

    def dequeue(self) -> int:
        """Remove and return the front element.  Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("dequeue from empty circular queue")
        val = self._buf[self._front]
        self._buf[self._front] = None  # optional cleanup
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return val  # type: ignore[return-value]

    def front(self) -> int:
        """Peek at the front element.  Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("front from empty circular queue")
        return self._buf[self._front]  # type: ignore[return-value]

    def rear(self) -> int:
        """Peek at the rear element.  Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("rear from empty circular queue")
        return self._buf[self._rear]  # type: ignore[return-value]

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self._capacity

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        # Collect elements in order for display
        if self.is_empty():
            return "CircularQueue([])"
        items: list[int] = []
        idx = self._front
        for _ in range(self._size):
            items.append(self._buf[idx])  # type: ignore[arg-type]
            idx = (idx + 1) % self._capacity
        return f"CircularQueue({items})"


# ===========================================================================
# Queue Using Two Stacks
# ===========================================================================

class QueueTwoStacks:
    """FIFO queue implemented with two stacks.

    Amortized O(1) per operation.

    - enqueue pushes onto stack_in.
    - dequeue pops from stack_out; if stack_out is empty, all elements
      in stack_in are transferred (reversed) into stack_out first.
    """

    def __init__(self) -> None:
        self._stack_in: list[int] = []
        self._stack_out: list[int] = []

    def enqueue(self, val: int) -> None:
        """O(1)"""
        self._stack_in.append(val)

    def _transfer(self) -> None:
        """Move all elements from stack_in to stack_out (reversing order)."""
        while self._stack_in:
            self._stack_out.append(self._stack_in.pop())

    def dequeue(self) -> int:
        """Amortized O(1)."""
        if not self._stack_out:
            self._transfer()
        if not self._stack_out:
            raise IndexError("dequeue from empty queue")
        return self._stack_out.pop()

    def front(self) -> int:
        """Amortized O(1)."""
        if not self._stack_out:
            self._transfer()
        if not self._stack_out:
            raise IndexError("front from empty queue")
        return self._stack_out[-1]

    def is_empty(self) -> bool:
        return not self._stack_in and not self._stack_out

    def size(self) -> int:
        return len(self._stack_in) + len(self._stack_out)


# ===========================================================================
# Sliding Window Maximum (Monotonic Deque)
# ===========================================================================

def sliding_window_max(nums: List[int], k: int) -> List[int]:
    """Return the maximum value in every contiguous window of size *k*.

    Uses a monotonic deque that stores indices.  The deque is maintained in
    decreasing order of the corresponding values, so the front always holds
    the index of the current window maximum.

    Time:  O(n)  — each element is added and removed at most once
    Space: O(k)  — the deque holds at most k indices
    """
    if not nums or k == 0:
        return []

    dq: deque[int] = deque()  # indices, values in decreasing order
    result: list[int] = []

    for i, val in enumerate(nums):
        # Remove indices that have left the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove indices whose corresponding values are <= current value
        # (they can never be a window max while current is in the window)
        while dq and nums[dq[-1]] <= val:
            dq.pop()

        dq.append(i)

        # Once we have processed at least k elements, record the window max
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ---- Queue (deque-backed) ----
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.front() == 1
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.size() == 1
    print("[PASS] Queue using deque")

    # ---- Circular Queue ----
    cq = CircularQueue(3)
    assert cq.enqueue(1) is True
    assert cq.enqueue(2) is True
    assert cq.enqueue(3) is True
    assert cq.enqueue(4) is False  # full
    assert cq.rear() == 3
    assert cq.is_full() is True
    assert cq.dequeue() == 1
    assert cq.enqueue(4) is True  # now there is room
    assert cq.rear() == 4
    assert cq.front() == 2
    print("[PASS] Circular queue")

    # ---- Queue Using Two Stacks ----
    q2 = QueueTwoStacks()
    q2.enqueue(10)
    q2.enqueue(20)
    q2.enqueue(30)
    assert q2.front() == 10
    assert q2.dequeue() == 10
    assert q2.dequeue() == 20
    q2.enqueue(40)
    assert q2.dequeue() == 30
    assert q2.dequeue() == 40
    assert q2.is_empty() is True
    print("[PASS] Queue using two stacks")

    # ---- Sliding Window Maximum ----
    assert sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert sliding_window_max([1], 1) == [1]
    assert sliding_window_max([1, -1], 1) == [1, -1]
    assert sliding_window_max([9, 11], 2) == [11]
    assert sliding_window_max([4, 3, 2, 1], 2) == [4, 3, 2]
    print("[PASS] Sliding window maximum (monotonic deque)")

    print("\nAll Week 13 tests passed!")
