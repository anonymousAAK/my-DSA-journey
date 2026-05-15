"""
WEEK 30 - PYTHON ADVANCED TOPICS
Topic: Top-K Elements Pattern
File: top_k_elements.py

CONCEPT:
    Many interview problems reduce to "find the K largest / smallest /
    most-frequent elements". Three idiomatic solutions:
      1. Min-heap of size K (keeps largest): O(n log K), O(K) space.
      2. Bucket sort by frequency: O(n) time, O(n) space (when input is
         integer or hashable with bounded counts).
      3. Quickselect partition: O(n) expected time, O(1) extra space.

KEY POINTS:
    - Min-heap of size K is the safe default when K << n.
    - Bucket sort works for top-K frequent because counts are bounded by n.
    - Quickselect (Hoare partitioning) is the fastest but has O(n^2) worst
      case unless you randomise or use median-of-medians.

ALGORITHM / APPROACH:
    KTH LARGEST (heap):
        push x into heap; if size > K: pop. top = K-th largest.
    TOP K FREQUENT (heap):
        count freq; min-heap on freq with size K.
    TOP K FREQUENT (bucket):
        count freq; buckets[freq].append(item); collect from highest bucket.
    QUICKSELECT:
        pivot partition; recurse into the side containing K.

PYTHON-SPECIFIC NOTES:
    - `heapq` is a min-heap; for max-heap behaviour negate keys.
    - `collections.Counter` for frequency tally.

DRY RUN / EXAMPLE:
    find_kth_largest [3,2,1,5,6,4], k=2 -> 5
    top_k_frequent  [1,1,1,2,2,3], k=2 -> [1, 2]
    quickselect_kth [3,2,1,5,6,4], k=2 -> 5

COMPLEXITY:
    Heap-based:    O(n log K) time, O(K) space
    Bucket:        O(n) time, O(n) space
    Quickselect:   O(n) expected time, O(1) extra space
"""

from __future__ import annotations

import heapq
import random
from collections import Counter
from typing import List


def find_kth_largest(nums: List[int], k: int) -> int:
    heap: List[int] = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


def top_k_frequent_heap(nums: List[int], k: int) -> List[int]:
    freq = Counter(nums)
    heap: List[tuple] = []
    for v, c in freq.items():
        heapq.heappush(heap, (c, v))
        if len(heap) > k:
            heapq.heappop(heap)
    return [v for _, v in heap]


def top_k_frequent_bucket(nums: List[int], k: int) -> List[int]:
    freq = Counter(nums)
    buckets: List[List[int]] = [[] for _ in range(len(nums) + 1)]
    for v, c in freq.items():
        buckets[c].append(v)
    out: List[int] = []
    for i in range(len(buckets) - 1, -1, -1):
        for v in buckets[i]:
            out.append(v)
            if len(out) == k:
                return out
    return out


def quickselect_kth_largest(nums: List[int], k: int) -> int:
    """Hoare-partition quickselect (expected O(n))."""
    nums = nums[:]  # don't mutate caller
    target = len(nums) - k

    def partition(lo: int, hi: int) -> int:
        pivot = nums[random.randint(lo, hi)]
        i, j = lo, hi
        while i <= j:
            while nums[i] < pivot: i += 1
            while nums[j] > pivot: j -= 1
            if i <= j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1; j -= 1
        return i

    lo, hi = 0, len(nums) - 1
    while lo < hi:
        idx = partition(lo, hi)
        if idx <= target:
            lo = idx
        else:
            hi = idx - 1
    return nums[target]


def _demo() -> None:
    print(f"Kth largest [3,2,1,5,6,4] k=2: {find_kth_largest([3,2,1,5,6,4], 2)}")
    print(f"Top 2 frequent (heap):   {sorted(top_k_frequent_heap([1,1,1,2,2,3], 2))}")
    print(f"Top 2 frequent (bucket): {sorted(top_k_frequent_bucket([1,1,1,2,2,3], 2))}")
    print(f"Quickselect kth=2: {quickselect_kth_largest([3,2,1,5,6,4], 2)}")


if __name__ == "__main__":
    _demo()


# NOTES
# -----
# Differences from Java:
#   * heapq is a min-heap; use tuples for composite priorities.
#   * Counter / Counter.most_common(k) are sometimes simpler than the
#     manual heap / bucket approaches; we keep both for didactic value.
