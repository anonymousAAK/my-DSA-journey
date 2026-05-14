"""
Week 15: Heaps & Priority Queues
=================================
A heap is a complete binary tree stored in an array where every parent
satisfies the heap property (max-heap: parent >= children, min-heap:
parent <= children).

Key properties (0-indexed array):
    parent(i)      = (i - 1) // 2
    left_child(i)  = 2 * i + 1
    right_child(i) = 2 * i + 2

Topics covered:
    1. MaxHeap class from scratch (insert, extract_max, sift_up, sift_down, build_heap)
    2. Heap sort (in-place)
    3. Kth largest element using heapq
    4. Merge k sorted lists using heapq
    5. MedianFinder class (two-heap approach)
"""

from __future__ import annotations

import heapq
from typing import List, Optional


# ---------------------------------------------------------------------------
# 1. MaxHeap Class — built from scratch
# ---------------------------------------------------------------------------
class MaxHeap:
    """
    A max-heap backed by a Python list.

    Internally the largest element is always at index 0.

    Time complexities:
        insert       : O(log n)
        extract_max  : O(log n)
        peek         : O(1)
        build_heap   : O(n)   — via Floyd's algorithm
    Space: O(n) for the underlying list.
    """

    def __init__(self, items: Optional[List[int]] = None) -> None:
        """Initialise the heap, optionally building from *items* in O(n)."""
        if items is None:
            self._data: List[int] = []
        else:
            self._data = list(items)  # copy so we don't mutate the caller's list
            self._build_heap()

    # ---- public API -------------------------------------------------------

    def insert(self, value: int) -> None:
        """
        Append *value* to the end and bubble it up to restore the heap property.
        Time: O(log n)
        """
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    def extract_max(self) -> int:
        """
        Remove and return the maximum element (root).
        Swap root with last element, pop, then sift the new root down.
        Time: O(log n)
        Raises IndexError if the heap is empty.
        """
        if not self._data:
            raise IndexError("extract_max from an empty heap")
        # Swap root with the last element
        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        max_val = self._data.pop()
        if self._data:
            self._sift_down(0)
        return max_val

    def peek(self) -> int:
        """Return the maximum element without removing it.  O(1)."""
        if not self._data:
            raise IndexError("peek on an empty heap")
        return self._data[0]

    @property
    def size(self) -> int:
        return len(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __repr__(self) -> str:
        return f"MaxHeap({self._data})"

    # ---- internal helpers -------------------------------------------------

    def _sift_up(self, idx: int) -> None:
        """
        Move element at *idx* upward while it is greater than its parent.
        Time: O(log n) — at most the height of the tree.
        """
        while idx > 0:
            parent = (idx - 1) // 2
            if self._data[idx] > self._data[parent]:
                self._data[idx], self._data[parent] = self._data[parent], self._data[idx]
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        """
        Move element at *idx* downward while it is smaller than a child.
        Always swap with the *larger* child to maintain max-heap property.
        Time: O(log n)
        """
        n = len(self._data)
        while True:
            largest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self._data[left] > self._data[largest]:
                largest = left
            if right < n and self._data[right] > self._data[largest]:
                largest = right

            if largest != idx:
                self._data[idx], self._data[largest] = self._data[largest], self._data[idx]
                idx = largest
            else:
                break

    def _build_heap(self) -> None:
        """
        Floyd's build-heap: sift down every non-leaf starting from the last
        internal node.  This is O(n) — *not* O(n log n) — because most nodes
        are near the bottom of the tree and sift down only a short distance.
        """
        n = len(self._data)
        # Last internal node is the parent of the last element.
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)


# ---------------------------------------------------------------------------
# 2. Heap Sort (in-place, ascending order)
# ---------------------------------------------------------------------------
def heap_sort(arr: List[int]) -> List[int]:
    """
    Sort *arr* in-place in ascending order using heap sort.

    Algorithm:
        1. Build a max-heap from the array                     — O(n)
        2. Repeatedly swap root (max) with the last unsorted
           element and shrink the heap region, sifting down     — O(n log n)

    Time:  O(n log n) — all cases
    Space: O(1) — in-place (no auxiliary array)

    Returns *arr* for convenience (it is sorted in-place).
    """
    n = len(arr)

    # --- Phase 1: build max-heap in-place ---
    def sift_down(start: int, end: int) -> None:
        """Sift element at *start* down within arr[0..end]."""
        idx = start
        while True:
            largest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            if left <= end and arr[left] > arr[largest]:
                largest = left
            if right <= end and arr[right] > arr[largest]:
                largest = right
            if largest != idx:
                arr[idx], arr[largest] = arr[largest], arr[idx]
                idx = largest
            else:
                break

    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n - 1)

    # --- Phase 2: extract max repeatedly ---
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]  # move current max to sorted region
        sift_down(0, end - 1)

    return arr


# ---------------------------------------------------------------------------
# 3. Kth Largest Element using heapq
# ---------------------------------------------------------------------------
def kth_largest(nums: List[int], k: int) -> int:
    """
    Return the k-th largest element in *nums*.

    Strategy: maintain a min-heap of size k.
    - Push every element onto the heap.
    - If the heap grows beyond k, pop the smallest.
    After processing all elements the root of the heap is the k-th largest.

    Time:  O(n log k)
    Space: O(k)
    """
    # heapq is a min-heap; we keep the k largest seen so far.
    min_heap: List[int] = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)  # discard the smallest of the k+1 elements
    return min_heap[0]


def kth_largest_quickselect(nums: List[int], k: int) -> int:
    """
    Alternative O(n) average approach using heapq.nlargest (internally uses
    a heap of size k, identical complexity to the manual version above).

    Time:  O(n log k)  (heapq.nlargest is implemented efficiently in C)
    Space: O(k)
    """
    return heapq.nlargest(k, nums)[-1]


# ---------------------------------------------------------------------------
# 4. Merge k Sorted Lists using heapq
# ---------------------------------------------------------------------------
def merge_k_sorted_lists(lists: List[List[int]]) -> List[int]:
    """
    Merge *k* sorted lists into a single sorted list.

    Uses a min-heap of size k.  Each heap entry is (value, list_index, element_index)
    so we always extract the globally smallest element next.

    Let N = total number of elements across all lists.
    Time:  O(N log k)  — each of the N elements is pushed/popped once on a
                          heap of size at most k.
    Space: O(N) for the result + O(k) for the heap.
    """
    result: List[int] = []
    # Seed the heap with the first element of each non-empty list.
    # Tuple: (value, list_index, element_index)
    heap: List[tuple[int, int, int]] = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    while heap:
        val, li, ei = heapq.heappop(heap)
        result.append(val)
        # If this list has more elements, push the next one.
        if ei + 1 < len(lists[li]):
            heapq.heappush(heap, (lists[li][ei + 1], li, ei + 1))

    return result


# ---------------------------------------------------------------------------
# 5. MedianFinder — two-heap approach
# ---------------------------------------------------------------------------
class MedianFinder:
    """
    Efficiently find the median of a growing stream of numbers.

    Idea — partition numbers into two halves:
        max_heap (lower half)  — stores the smaller half; we want quick access
                                 to the *largest* of them, hence max-heap.
        min_heap (upper half)  — stores the larger half; we want the *smallest*
                                 of them, hence min-heap.

    Invariants maintained after every insertion:
        1. len(max_heap) == len(min_heap)   OR   len(max_heap) == len(min_heap) + 1
        2. Every element in max_heap <= every element in min_heap

    Python's heapq is a min-heap, so we store negated values in max_heap.

    Time:
        add_num     : O(log n)
        find_median : O(1)
    Space: O(n)
    """

    def __init__(self) -> None:
        # max_heap stores negated values so heapq (min-heap) acts as a max-heap.
        self._max_heap: List[int] = []  # lower half
        self._min_heap: List[int] = []  # upper half

    def add_num(self, num: int) -> None:
        """Add a number to the data structure.  O(log n)."""
        # Step 1: push to max_heap (lower half)
        heapq.heappush(self._max_heap, -num)

        # Step 2: ensure max_heap's root <= min_heap's root
        if self._min_heap and (-self._max_heap[0] > self._min_heap[0]):
            val = -heapq.heappop(self._max_heap)
            heapq.heappush(self._min_heap, val)

        # Step 3: balance sizes — max_heap may be at most 1 larger
        if len(self._max_heap) > len(self._min_heap) + 1:
            val = -heapq.heappop(self._max_heap)
            heapq.heappush(self._min_heap, val)
        elif len(self._min_heap) > len(self._max_heap):
            val = heapq.heappop(self._min_heap)
            heapq.heappush(self._max_heap, -val)

    def find_median(self) -> float:
        """
        Return the median of all elements added so far.  O(1).
        Raises IndexError if no elements have been added.
        """
        if not self._max_heap:
            raise IndexError("find_median on empty MedianFinder")

        if len(self._max_heap) > len(self._min_heap):
            # Odd total count — median is the root of the larger (lower) heap.
            return float(-self._max_heap[0])
        else:
            # Even total count — median is the average of the two roots.
            return (-self._max_heap[0] + self._min_heap[0]) / 2.0


# ===========================================================================
# Test Cases
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Week 15 — Heaps & Priority Queues")
    print("=" * 60)

    # --- MaxHeap -----------------------------------------------------------
    print("\n--- MaxHeap ---")
    h = MaxHeap()
    for v in [3, 1, 6, 5, 2, 4]:
        h.insert(v)
    print(f"Heap after inserts: {h}")
    assert h.peek() == 6
    assert h.extract_max() == 6
    assert h.extract_max() == 5
    print(f"After two extract_max calls: {h}")

    # build_heap from list
    h2 = MaxHeap([10, 20, 5, 7, 15])
    assert h2.peek() == 20
    print(f"build_heap from [10,20,5,7,15]: {h2}")

    # --- Heap Sort ---------------------------------------------------------
    print("\n--- Heap Sort ---")
    data = [12, 11, 13, 5, 6, 7]
    print(f"Before: {data}")
    heap_sort(data)
    print(f"After:  {data}")
    assert data == sorted(data)

    data2 = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
    heap_sort(data2)
    assert data2 == sorted(data2)
    print(f"Sorted: {data2}")

    # --- Kth Largest -------------------------------------------------------
    print("\n--- Kth Largest Element ---")
    nums = [3, 2, 1, 5, 6, 4]
    assert kth_largest(nums, 2) == 5
    print(f"2nd largest in {nums}: {kth_largest(nums, 2)}")
    assert kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    print(f"4th largest in [3,2,3,1,2,4,5,5,6]: {kth_largest([3,2,3,1,2,4,5,5,6], 4)}")

    # --- Merge k Sorted Lists ----------------------------------------------
    print("\n--- Merge k Sorted Lists ---")
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    merged = merge_k_sorted_lists(lists)
    print(f"Merged {lists} -> {merged}")
    assert merged == [1, 1, 2, 3, 4, 4, 5, 6]

    empty_test = merge_k_sorted_lists([[], [1], []])
    assert empty_test == [1]
    print(f"Merged [[], [1], []] -> {empty_test}")

    # --- MedianFinder ------------------------------------------------------
    print("\n--- MedianFinder ---")
    mf = MedianFinder()
    mf.add_num(1)
    assert mf.find_median() == 1.0
    mf.add_num(2)
    assert mf.find_median() == 1.5
    mf.add_num(3)
    assert mf.find_median() == 2.0
    mf.add_num(4)
    assert mf.find_median() == 2.5
    mf.add_num(5)
    assert mf.find_median() == 3.0
    print(f"Stream [1,2,3,4,5] — medians: 1.0, 1.5, 2.0, 2.5, 3.0  [PASS]")

    mf2 = MedianFinder()
    for v in [5, 15, 1, 3]:
        mf2.add_num(v)
    assert mf2.find_median() == 4.0
    print(f"Stream [5,15,1,3] — median = {mf2.find_median()}  [PASS]")

    print("\nAll tests passed!")
