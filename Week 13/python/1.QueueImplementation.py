"""
WEEK 13 - PYTHON DSA
Topic: Queue Implementations + Sliding Window Maximum
File: 1.QueueImplementation.py

CONCEPT:
A queue is FIFO: enqueue at the back, dequeue from the front. Variants:
- Circular queue (fixed-size array with modular arithmetic).
- Queue from two stacks (classic interview problem).
- Deque (double-ended) — used here for sliding window maximum.

KEY POINTS:
- Standard ops: enqueue/offer (add rear), dequeue/poll (remove front),
  peek/front (read front), is_empty.
- For the sliding window maximum we use a monotonic deque storing INDICES
  whose values are strictly decreasing from front to back.

ALGORITHM / APPROACH:
- CircularQueue: front, rear, size; rear = (rear+1) % capacity on enqueue;
  front advances similarly on dequeue.
- QueueUsingStacks: push to inbox; on dequeue, if outbox empty, drain inbox
  into outbox (reversing order). Amortized O(1).
- slidingWindowMax: for each i:
    * pop indices from the front that fall out of the window
    * pop indices from the back whose values < arr[i] (they can never be
      the max for any current/future window)
    * push i; record arr[front] when i >= k-1.

PYTHON-SPECIFIC NOTES:
- collections.deque is a doubly-linked-list-of-blocks giving O(1) on both
  ends. It's the canonical queue/deque in Python.
- queue.Queue is for thread-safe producer/consumer use, NOT general use.
- Type hints + Optional.

DRY RUN:
Example 1: CircularQueue capacity=4
  enqueue 1,2,3,4 -> data=[1,2,3,4] front=0 rear=0 (wrap) size=4 full
  dequeue -> 1; front=1; size=3
  enqueue 5 -> data[rear=0]=5; rear=1; size=4
  peek -> data[front=1] = 2

Example 2: slidingWindowMax([1,3,-1,-3,5,3,6,7], k=3)
  i=0: deque=[0]
  i=1: pop 0 (1<3); deque=[1]; window not full
  i=2: deque=[1,2]; res[0]=arr[1]=3
  i=3: deque=[1,2,3]; res[1]=arr[1]=3
  i=4: pop 3 (-3<5); pop 2 (-1<5); pop 1 (3<5); deque=[4]; res[2]=5
  ...
  Final: [3,3,5,5,6,7]

COMPLEXITY:
  CircularQueue: O(1) per op
  QueueUsingStacks: amortized O(1) per op
  slidingWindowMax: O(n) total (each element pushed/popped at most once)
"""

from __future__ import annotations
from collections import deque
from typing import Deque, List, Optional


class CircularQueue:
    """Fixed-capacity ring buffer."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.data: List[Optional[int]] = [None] * capacity
        self.front = 0
        self.rear = 0
        self.size = 0

    def enqueue(self, x: int) -> bool:
        if self.size == self.capacity:
            return False  # full
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
        return True

    def dequeue(self) -> int:
        if self.size == 0:
            raise IndexError("Queue empty")
        v = self.data[self.front]
        assert v is not None
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return v

    def peek(self) -> int:
        if self.size == 0:
            raise IndexError("Queue empty")
        v = self.data[self.front]
        assert v is not None
        return v

    def is_empty(self) -> bool: return self.size == 0
    def is_full(self) -> bool: return self.size == self.capacity


class QueueUsingStacks:
    """Two-stacks queue. Amortized O(1) per op."""

    def __init__(self) -> None:
        self.inbox: List[int] = []
        self.outbox: List[int] = []

    def enqueue(self, x: int) -> None:
        self.inbox.append(x)

    def _shift(self) -> None:
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def dequeue(self) -> int:
        self._shift()
        if not self.outbox:
            raise IndexError("Queue empty")
        return self.outbox.pop()

    def peek(self) -> int:
        self._shift()
        if not self.outbox:
            raise IndexError("Queue empty")
        return self.outbox[-1]

    def is_empty(self) -> bool: return not self.inbox and not self.outbox


def sliding_window_max(arr: List[int], k: int) -> List[int]:
    """Monotonic deque solution. O(n) time, O(k) space."""
    n = len(arr)
    if n == 0 or k == 0:
        return []
    result: List[int] = []
    dq: Deque[int] = deque()  # indices, arr[dq] strictly decreasing
    for i in range(n):
        # remove indices outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # remove smaller values from back
        while dq and arr[dq[-1]] < arr[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(arr[dq[0]])
    return result


def main() -> None:
    print("=== Circular Queue ===")
    cq = CircularQueue(4)
    for v in [1, 2, 3, 4]: cq.enqueue(v)
    print("Full:", cq.is_full())
    print("Dequeue:", cq.dequeue())
    cq.enqueue(5)
    print("Peek:", cq.peek())

    print("\n=== Queue using Two Stacks ===")
    q = QueueUsingStacks()
    for v in [1, 2, 3]: q.enqueue(v)
    print("dequeue:", q.dequeue())
    print("dequeue:", q.dequeue())
    q.enqueue(4)
    print("peek:", q.peek())
    print("dequeue:", q.dequeue())
    print("dequeue:", q.dequeue())

    print("\n=== Python deque as Queue ===")
    dq: Deque[int] = deque()
    for v in [10, 20, 30]: dq.append(v)
    print("peek:", dq[0])
    print("poll:", dq.popleft())
    print("poll:", dq.popleft())

    print("\n=== Sliding Window Maximum ===")
    arr = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print("Array:", arr, "k =", k)
    print("Max in each window:", sliding_window_max(arr, k))  # [3,3,5,5,6,7]

    arr2 = [9, 11]
    print("\nArray:", arr2, "k=2")
    print("Max:", sliding_window_max(arr2, 2))


if __name__ == "__main__":
    main()


"""
NOTES (vs. Java):
- Java's recommended Queue is ArrayDeque. The Python equivalent is
  collections.deque. Both are O(1) at both ends.
- queue.Queue is a thread-safe blocking queue (vs. java.util.concurrent
  BlockingQueue) — different beast.
- Python lists used as stacks are O(1) for append/pop at the END only;
  popping from the front is O(n). Use deque for double-ended ops.
"""
