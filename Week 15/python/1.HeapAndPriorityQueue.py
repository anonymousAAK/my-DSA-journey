"""
WEEK 15 - PYTHON DSA
Topic: Heap, Heap Sort, Priority Queue Applications
File: 1.HeapAndPriorityQueue.py

CONCEPT:
A heap is a complete binary tree stored as an array satisfying the heap
property:
  - Max-heap: every parent >= children (root is max).
  - Min-heap: every parent <= children (root is min).
Stored 0-indexed: parent(i) = (i-1)//2; left = 2i+1; right = 2i+2.

KEY POINTS:
- insert: append at end, sift up. O(log n).
- extractMax/Min: swap root with last, shrink, sift down. O(log n).
- buildHeap: O(n) — start from last non-leaf, sift down each. Better than n
  inserts (O(n log n)).
- Heap sort: build max-heap, repeatedly extract max to the end. O(n log n).

ALGORITHM / APPROACH:
- kth largest: maintain a min-heap of size k; the root is the kth largest.
- merge K sorted arrays: min-heap of (value, array_index, element_index).
- median of stream: two heaps. Max-heap holds lower half; min-heap holds
  upper half. Insert into max-heap then push max into min-heap; rebalance
  sizes so max-heap has equal-or-one-more.

PYTHON-SPECIFIC NOTES:
- The standard library `heapq` is a MIN-heap only. To build a max-heap we
  negate values (push -x, pop -x). heapq operates on a Python list.
- heapq.heappush / heappop are O(log n). heapify is O(n).
- For full priority queue API see queue.PriorityQueue (thread-safe).

DRY RUN:
Example 1: build max-heap from [5,3,7,1,9,2,8]
  Inserting 5: [5]
  Insert 3:    [5,3]
  Insert 7:    [5,3,7] -> sift 7 up: [7,3,5]
  Insert 1:    [7,3,5,1]
  Insert 9:    [7,3,5,1,9] -> sift 9 up to root: [9,7,5,1,3]
  Insert 2:    [9,7,5,1,3,2]
  Insert 8:    [9,7,5,1,3,2,8] -> sift 8: [9,7,8,1,3,2,5]
  extractMax order: 9 8 7 5 3 2 1

Example 2: kthLargest([3,2,1,5,6,4], k=2) using min-heap of size 2
  Push 3 -> [3]
  Push 2 -> [2,3]
  Push 1 -> [1,2,3] size>k -> pop 1 -> [2,3]
  Push 5 -> [2,3,5] size>k -> pop 2 -> [3,5]
  Push 6 -> [3,5,6] -> pop 3 -> [5,6]
  Push 4 -> [4,5,6] -> pop 4 -> [5,6]
  Root = 5 = 2nd largest.

COMPLEXITY:
  insert/extract:   O(log n)
  buildHeap:        O(n)
  heapSort:         O(n log n) time, O(1) extra
  kthLargest:       O(n log k)
  median stream:    O(log n) per add, O(1) findMedian
"""

from __future__ import annotations
import heapq
from typing import List


class MaxHeap:
    """Hand-rolled max-heap on a Python list (0-indexed)."""

    def __init__(self) -> None:
        self.data: List[int] = []

    def __len__(self) -> int: return len(self.data)
    def is_empty(self) -> bool: return not self.data
    def peek_max(self) -> int: return self.data[0]

    @staticmethod
    def _parent(i: int) -> int: return (i - 1) // 2
    @staticmethod
    def _left(i: int) -> int: return 2 * i + 1
    @staticmethod
    def _right(i: int) -> int: return 2 * i + 2

    def _sift_up(self, i: int) -> None:
        while i > 0 and self.data[self._parent(i)] < self.data[i]:
            p = self._parent(i)
            self.data[i], self.data[p] = self.data[p], self.data[i]
            i = p

    def _sift_down(self, i: int) -> None:
        n = len(self.data)
        while True:
            l, r = self._left(i), self._right(i)
            largest = i
            if l < n and self.data[l] > self.data[largest]: largest = l
            if r < n and self.data[r] > self.data[largest]: largest = r
            if largest == i: return
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            i = largest

    def insert(self, x: int) -> None:
        self.data.append(x)
        self._sift_up(len(self.data) - 1)

    def extract_max(self) -> int:
        if not self.data:
            raise IndexError("Heap empty")
        top = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return top


def heap_sort(arr: List[int]) -> None:
    """In-place ascending sort using max-heap construction."""
    n = len(arr)

    def sift_down(start: int, end: int) -> None:
        i = start
        while True:
            l, r = 2*i + 1, 2*i + 2
            largest = i
            if l < end and arr[l] > arr[largest]: largest = l
            if r < end and arr[r] > arr[largest]: largest = r
            if largest == i: return
            arr[i], arr[largest] = arr[largest], arr[i]
            i = largest

    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        sift_down(0, i)


def kth_largest(arr: List[int], k: int) -> int:
    """Maintain a min-heap of size k; root is the kth largest."""
    h: List[int] = []
    for x in arr:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return h[0]


class MedianFinder:
    """Two heaps: lower (max-heap via negation) | upper (min-heap)."""

    def __init__(self) -> None:
        self.lower: List[int] = []  # store as negatives for max-heap behavior
        self.upper: List[int] = []

    def add_num(self, num: int) -> None:
        # 1) push to lower (max-heap) — use -num
        heapq.heappush(self.lower, -num)
        # 2) move the top of lower to upper to maintain ordering
        heapq.heappush(self.upper, -heapq.heappop(self.lower))
        # 3) rebalance sizes so len(lower) >= len(upper)
        if len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def find_median(self) -> float:
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2.0


def main() -> None:
    print("=== Max-Heap ===")
    heap = MaxHeap()
    for x in [5, 3, 7, 1, 9, 2, 8]:
        heap.insert(x)
    out = []
    while not heap.is_empty():
        out.append(heap.extract_max())
    print("Extract in order:", out)  # 9 8 7 5 3 2 1

    print("\n=== Heap Sort ===")
    arr = [12, 11, 13, 5, 6, 7]
    print("Before:", arr)
    heap_sort(arr)
    print("After: ", arr)

    print("\n=== Kth Largest ===")
    arr2 = [3, 2, 1, 5, 6, 4]
    for k in range(1, len(arr2) + 1):
        print(f"k={k} -> {kth_largest(arr2, k)}")

    print("\n=== heapq min-heap demo ===")
    h: List[int] = []
    for x in [5, 1, 3, 2, 4]: heapq.heappush(h, x)
    poll = []
    while h: poll.append(heapq.heappop(h))
    print("Pop order:", poll)  # 1 2 3 4 5

    print("\n=== Median from Stream ===")
    mf = MedianFinder()
    for x in [5, 15, 1, 3, 2, 8, 7, 9, 10, 6, 11, 4]:
        mf.add_num(x)
        print(f"Added {x:2d} -> median = {mf.find_median():.1f}")


if __name__ == "__main__":
    main()


"""
NOTES (vs. Java):
- Java PriorityQueue is a MIN-heap by default; pass Collections.reverseOrder()
  for a max-heap. Python heapq is min-only — negate values for max-heap.
- Java's PriorityQueue<int[]> supports custom Comparator; Python's heapq
  compares tuples lexicographically, so (priority, payload) works naturally.
- buildHeap and sift logic is identical conceptually across languages.
"""
