"""
WEEK 19 - PYTHON DSA
Topic: Greedy Algorithms — Paradigm + Classic Problems
File: 1.GreedyAlgorithms.py

CONCEPT:
    Greedy algorithms commit to the locally optimal choice at every step
    and never reconsider. They work when the problem has:
        1. Greedy choice property -- a global optimum can be assembled by
           making locally optimal choices.
        2. Optimal substructure -- optimal answer contains optimal sub-answers.
    Greedy is fast (often O(n log n)) but only correct on certain problems —
    e.g. 0/1 knapsack needs DP, but FRACTIONAL knapsack is greedy.

KEY POINTS:
    - Sort and sweep is the most common pattern.
    - Proofs use exchange argument: swapping greedy with any alternative
      doesn't improve the answer.
    - Heaps (heapq) often help when the greedy choice is "smallest/largest
      seen so far".

ALGORITHM / APPROACH:
    Five canonical problems (matching the Java reference):
        1. Activity Selection         -- sort by end time; pick non-overlapping.
        2. Fractional Knapsack        -- sort by value/weight desc; take prefixes.
        3. Min Coins (canonical)      -- repeatedly take the largest coin.
        4. Merge Intervals            -- sort by start; merge contiguous overlaps.
        5. Min Meeting Rooms          -- sort + min-heap of end times.

PYTHON-SPECIFIC NOTES:
    - `sorted(items, key=...)` and `list.sort(key=...)` for ergonomic sorting.
    - `heapq` provides a min-heap; for max-heap negate values.
    - `collections.OrderedDict` exists but plain dict already preserves order
      since Python 3.7.
    - Use `tuple` for fixed-shape records or `dataclasses` for clarity.

DRY RUN:
    Activity Selection:
        start = [1, 3, 0, 5, 8, 5]
        end   = [2, 4, 6, 7, 9, 9]
        Sort by end -> indexes [0,1,3,2,4,5] giving end-order [2,4,7,6,9,9]
        Pick idx 0 (1..2). Last end = 2.
        idx 1 starts at 3 >= 2 -> pick (3..4). Last end = 4.
        idx 3 starts at 5 >= 4 -> pick (5..7). Last end = 7.
        idx 2 starts at 0 < 7  -> skip.
        idx 4 starts at 8 >= 7 -> pick (8..9). Last end = 9.
        idx 5 starts at 5 < 9  -> skip. Total = 4.

    Min Meeting Rooms [[0,30],[5,10],[15,20]]:
        sort by start -> same order
        heap = [30]
        meeting (5,10): 5 < 30 -> need extra room; heap=[10,30]
        meeting (15,20): 15 >= 10 -> pop 10; push 20; heap=[20,30]
        Answer = max heap size seen = 2.

COMPLEXITY:
    activity_selection      O(n log n)
    fractional_knapsack     O(n log n)
    min_coins_greedy        O(c log c + answer-magnitude)
    merge_intervals         O(n log n)
    min_meeting_rooms       O(n log n)
"""

from __future__ import annotations
import heapq
from typing import Dict, List, Sequence, Tuple


# 1. ACTIVITY SELECTION
def activity_selection(start: Sequence[int], end: Sequence[int]) -> int:
    """Maximum number of non-overlapping activities. Greedy: pick earliest finish."""
    if not start:
        return 0
    order = sorted(range(len(start)), key=lambda i: end[i])
    count = 1
    last_end = end[order[0]]
    for k in order[1:]:
        if start[k] >= last_end:
            count += 1
            last_end = end[k]
    return count


# 2. FRACTIONAL KNAPSACK
def fractional_knapsack(weights: Sequence[int], values: Sequence[int],
                        capacity: int) -> float:
    """Greedy by value/weight density. Allows taking a fraction of an item."""
    items = sorted(zip(weights, values), key=lambda wv: wv[1] / wv[0], reverse=True)
    total = 0.0
    remaining = capacity
    for w, v in items:
        if remaining <= 0:
            break
        take = min(w, remaining)
        total += take * v / w
        remaining -= take
    return total


# 3. MIN COINS (greedy works only for canonical systems, e.g. USD)
def min_coins_greedy(coins: Sequence[int], target: int) -> Dict[int, int]:
    """Returns mapping coin -> count. Note: not optimal for arbitrary coin sets."""
    result: Dict[int, int] = {}
    for c in sorted(coins, reverse=True):
        if target <= 0:
            break
        if c <= target:
            count = target // c
            result[c] = count
            target -= c * count
    return result


# 4. MERGE INTERVALS
def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """Merge any overlapping intervals. Greedy by start time."""
    if len(intervals) <= 1:
        return [iv[:] for iv in intervals]
    sorted_iv = sorted(intervals, key=lambda iv: iv[0])
    merged: List[List[int]] = [sorted_iv[0][:]]
    for s, e in sorted_iv[1:]:
        last = merged[-1]
        if s <= last[1]:
            last[1] = max(last[1], e)
        else:
            merged.append([s, e])
    return merged


# 5. MIN MEETING ROOMS
def min_meeting_rooms(intervals: List[List[int]]) -> int:
    """Minimum rooms needed; greedy + min-heap of currently busy room end times."""
    if not intervals:
        return 0
    sorted_iv = sorted(intervals, key=lambda iv: iv[0])
    heap: List[int] = [sorted_iv[0][1]]                # end time of first meeting
    for s, e in sorted_iv[1:]:
        if s >= heap[0]:
            heapq.heappop(heap)                        # room frees up
        heapq.heappush(heap, e)
    return len(heap)


def main() -> None:
    print("=== Activity Selection ===")
    start = [1, 3, 0, 5, 8, 5]
    end   = [2, 4, 6, 7, 9, 9]
    print("Max activities:", activity_selection(start, end))   # 4

    print("\n=== Fractional Knapsack ===")
    print(f"Max value: {fractional_knapsack([10,20,30],[60,100,120], 50):.2f}") # 240.00

    print("\n=== Min Coins (US denominations) ===")
    usd = [1, 5, 10, 25, 50, 100]
    print("Change for 87 cents:", min_coins_greedy(usd, 87))
    print("Change for 30 cents:", min_coins_greedy(usd, 30))

    print("\n=== Merge Intervals ===")
    print("Merged:", merge_intervals([[1,3],[2,6],[8,10],[15,18]]))
    # [[1,6],[8,10],[15,18]]

    print("\n=== Min Meeting Rooms ===")
    print("Rooms needed:", min_meeting_rooms([[0,30],[5,10],[15,20]]))   # 2
    print("Rooms needed:", min_meeting_rooms([[7,10],[2,4]]))            # 1


if __name__ == "__main__":
    main()


"""
NOTES (Python vs Java):
    - Java needs `Integer[]` boxed arrays + Comparator for sorting indices;
      Python's `sorted(range(n), key=lambda i: end[i])` is a one-liner.
    - heapq is a min-heap of any comparable; for max-heap, negate values
      or wrap with a (-priority, item) tuple.
    - Java Arrays.sort uses primitive specialisations; Python's Timsort is
      stable and works on any iterable.
    - Greedy correctness PROOFS belong on paper — the implementation here
      assumes the problem really has the greedy-choice property.
"""
