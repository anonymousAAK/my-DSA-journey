"""
Week 19: Greedy Algorithms
===========================
A greedy algorithm makes the locally optimal choice at each step, hoping to
arrive at a globally optimal solution.  Greedy works when the problem exhibits
the *greedy-choice property* and *optimal substructure*.

Topics covered:
    1. Activity selection
    2. Fractional knapsack
    3. Minimum coins (greedy, valid for canonical coin systems)
    4. Merge intervals
    5. Minimum meeting rooms (using heapq)
    6. Job sequencing with deadlines
    7. Huffman coding (build tree, encode, decode)
"""

from __future__ import annotations

import heapq
from collections import Counter
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# 1. Activity Selection
# ---------------------------------------------------------------------------
def activity_selection(activities: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Select the maximum number of non-overlapping activities.

    Each activity is (start, finish).

    Greedy strategy: always pick the activity that finishes earliest and
    doesn't conflict with the previously selected activity.

    Proof sketch: the earliest-finishing activity leaves the most room for
    remaining activities, so choosing it is never worse than any alternative.

    Time:  O(n log n) — dominated by sorting
    Space: O(n) for the result
    """
    # Sort by finish time
    sorted_acts = sorted(activities, key=lambda x: x[1])
    selected: List[Tuple[int, int]] = []
    last_finish = -1

    for start, finish in sorted_acts:
        if start >= last_finish:
            selected.append((start, finish))
            last_finish = finish

    return selected


# ---------------------------------------------------------------------------
# 2. Fractional Knapsack
# ---------------------------------------------------------------------------
def fractional_knapsack(
    items: List[Tuple[float, float]], capacity: float
) -> float:
    """
    Fractional knapsack: items can be broken into fractions.

    Each item is (weight, value).

    Greedy strategy: sort by value-to-weight ratio descending; take as much
    as possible of the most valuable-per-unit item first.

    This is optimal because we can always improve by replacing a lower-ratio
    fraction with a higher-ratio one.

    Time:  O(n log n)
    Space: O(n)
    """
    # Sort by value/weight ratio, descending
    sorted_items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)
    total_value = 0.0
    remaining = capacity

    for weight, value in sorted_items:
        if remaining <= 0:
            break
        take = min(weight, remaining)
        total_value += take * (value / weight)
        remaining -= take

    return total_value


# ---------------------------------------------------------------------------
# 3. Minimum Coins — greedy (for canonical coin systems only)
# ---------------------------------------------------------------------------
def minimum_coins_greedy(coins: List[int], amount: int) -> List[int]:
    """
    Find coins that sum to *amount* using as few coins as possible.

    Greedy strategy: always take the largest denomination that fits.

    WARNING: This only produces optimal results for *canonical* coin systems
    (e.g. US coins: 1, 5, 10, 25).  For arbitrary denominations, use DP
    (see Week 18: coin_change).

    Time:  O(n log n + amount/min_coin)
    Space: O(amount/min_coin)
    """
    sorted_coins = sorted(coins, reverse=True)
    result: List[int] = []
    remaining = amount

    for coin in sorted_coins:
        while remaining >= coin:
            result.append(coin)
            remaining -= coin

    if remaining != 0:
        return []  # not possible with greedy
    return result


# ---------------------------------------------------------------------------
# 4. Merge Intervals
# ---------------------------------------------------------------------------
def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merge all overlapping intervals.

    Greedy strategy: sort by start time; merge consecutive intervals that
    overlap (current start <= previous end).

    Time:  O(n log n)
    Space: O(n) for the result
    """
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged: List[List[int]] = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            # Overlapping — extend the current interval.
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


# ---------------------------------------------------------------------------
# 5. Minimum Meeting Rooms (using heapq)
# ---------------------------------------------------------------------------
def min_meeting_rooms(intervals: List[List[int]]) -> int:
    """
    Find the minimum number of meeting rooms required.

    Strategy:
        1. Sort meetings by start time.
        2. Use a min-heap to track the earliest ending meeting in use.
        3. For each meeting:
           - If it starts after the earliest ending meeting, reuse that room
             (pop from heap).
           - Push the current meeting's end time onto the heap.
        4. The heap size at the end is the answer.

    Time:  O(n log n)
    Space: O(n)
    """
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])
    # Min-heap of end times of meetings currently using a room.
    rooms: List[int] = []

    for start, end in intervals:
        # If the earliest-ending meeting has finished, free that room.
        if rooms and rooms[0] <= start:
            heapq.heappop(rooms)
        heapq.heappush(rooms, end)

    return len(rooms)


# ---------------------------------------------------------------------------
# 6. Job Sequencing with Deadlines
# ---------------------------------------------------------------------------
def job_sequencing(
    jobs: List[Tuple[str, int, int]]
) -> Tuple[int, List[str]]:
    """
    Schedule jobs to maximise total profit.  Each job takes 1 unit of time
    and has a deadline.

    Each job is (job_id, deadline, profit).

    Greedy strategy:
        1. Sort jobs by profit descending.
        2. For each job, schedule it in the latest available slot <= its deadline.

    Time:  O(n^2)  (can be improved to O(n log n) with a Union-Find)
    Space: O(max_deadline)
    """
    # Sort by profit descending
    sorted_jobs = sorted(jobs, key=lambda x: x[2], reverse=True)
    max_deadline = max(job[1] for job in jobs) if jobs else 0

    # slots[i] = job_id scheduled at time slot i (1-indexed), None if free.
    slots: List[Optional[str]] = [None] * (max_deadline + 1)
    total_profit = 0
    scheduled: List[str] = []

    for job_id, deadline, profit in sorted_jobs:
        # Find the latest available slot <= deadline.
        for t in range(deadline, 0, -1):
            if slots[t] is None:
                slots[t] = job_id
                total_profit += profit
                scheduled.append(job_id)
                break

    return total_profit, scheduled


# ---------------------------------------------------------------------------
# 7. Huffman Coding
# ---------------------------------------------------------------------------
class _HuffmanNode:
    """Internal node for the Huffman tree."""

    def __init__(
        self,
        char: Optional[str],
        freq: int,
        left: Optional[_HuffmanNode] = None,
        right: Optional[_HuffmanNode] = None,
    ) -> None:
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    # Comparison operators for heapq (break ties deterministically).
    def __lt__(self, other: _HuffmanNode) -> bool:
        return self.freq < other.freq


def huffman_build_tree(text: str) -> Optional[_HuffmanNode]:
    """
    Build a Huffman tree from *text*.

    Algorithm:
        1. Count character frequencies.
        2. Create a leaf node for each character and push onto a min-heap.
        3. Repeatedly pop two smallest nodes, merge into a new internal node,
           and push back, until one node remains (the root).

    Time:  O(n + k log k)  where n = len(text), k = number of unique chars
    Space: O(k)
    """
    freq = Counter(text)
    if not freq:
        return None

    heap: List[_HuffmanNode] = [_HuffmanNode(ch, f) for ch, f in freq.items()]
    heapq.heapify(heap)

    # Special case: only one unique character.
    if len(heap) == 1:
        node = heapq.heappop(heap)
        return _HuffmanNode(None, node.freq, left=node)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = _HuffmanNode(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)

    return heap[0]


def huffman_build_codes(root: Optional[_HuffmanNode]) -> Dict[str, str]:
    """
    Traverse the Huffman tree to produce a mapping char -> binary code.

    Left edge = '0', right edge = '1'.

    Time:  O(k)  where k = number of unique characters
    """
    codes: Dict[str, str] = {}
    if root is None:
        return codes

    def _traverse(node: _HuffmanNode, code: str) -> None:
        if node.char is not None:
            codes[node.char] = code if code else "0"
            return
        if node.left:
            _traverse(node.left, code + "0")
        if node.right:
            _traverse(node.right, code + "1")

    _traverse(root, "")
    return codes


def huffman_encode(text: str, codes: Dict[str, str]) -> str:
    """Encode *text* using pre-built Huffman codes.  O(n)."""
    return "".join(codes[ch] for ch in text)


def huffman_decode(encoded: str, root: Optional[_HuffmanNode]) -> str:
    """
    Decode a Huffman-encoded bit string using the tree.

    Walk down the tree bit by bit; when a leaf is reached, emit its character
    and restart from the root.

    Time:  O(len(encoded))
    """
    if root is None:
        return ""

    result: List[str] = []
    node = root
    for bit in encoded:
        node = node.left if bit == "0" else node.right
        if node is None:
            break
        if node.char is not None:
            result.append(node.char)
            node = root

    return "".join(result)


# ===========================================================================
# Test Cases
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Week 19 — Greedy Algorithms")
    print("=" * 60)

    # --- Activity Selection ------------------------------------------------
    print("\n--- Activity Selection ---")
    activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9),
                  (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    selected = activity_selection(activities)
    print(f"Selected {len(selected)} activities: {selected}")
    assert len(selected) == 4  # (1,4), (5,7), (8,11), (12,16)

    # --- Fractional Knapsack -----------------------------------------------
    print("\n--- Fractional Knapsack ---")
    items = [(10, 60), (20, 100), (30, 120)]  # (weight, value)
    result = fractional_knapsack(items, 50)
    print(f"Max value with capacity 50: {result:.2f}")
    assert abs(result - 240.0) < 1e-9

    # --- Minimum Coins (greedy) --------------------------------------------
    print("\n--- Minimum Coins (Greedy) ---")
    coins_used = minimum_coins_greedy([1, 5, 10, 25], 63)
    print(f"Coins for 63 cents: {coins_used} ({len(coins_used)} coins)")
    assert sum(coins_used) == 63

    # --- Merge Intervals ---------------------------------------------------
    print("\n--- Merge Intervals ---")
    merged = merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])
    assert merged == [[1, 6], [8, 10], [15, 18]]
    print(f"Merged: {merged}")

    merged2 = merge_intervals([[1, 4], [4, 5]])
    assert merged2 == [[1, 5]]
    print(f"Merged: {merged2}")

    # --- Minimum Meeting Rooms ---------------------------------------------
    print("\n--- Minimum Meeting Rooms ---")
    rooms = min_meeting_rooms([[0, 30], [5, 10], [15, 20]])
    assert rooms == 2
    print(f"Meeting rooms needed: {rooms}")

    rooms2 = min_meeting_rooms([[7, 10], [2, 4]])
    assert rooms2 == 1
    print(f"Meeting rooms needed: {rooms2}")

    # --- Job Sequencing ----------------------------------------------------
    print("\n--- Job Sequencing with Deadlines ---")
    jobs = [("a", 2, 100), ("b", 1, 19), ("c", 2, 27),
            ("d", 1, 25), ("e", 3, 15)]
    profit, scheduled = job_sequencing(jobs)
    print(f"Total profit: {profit}, Scheduled: {scheduled}")
    assert profit == 142  # jobs a, c, e

    # --- Huffman Coding ----------------------------------------------------
    print("\n--- Huffman Coding ---")
    text = "abracadabra"
    tree = huffman_build_tree(text)
    codes = huffman_build_codes(tree)
    print(f"Text: '{text}'")
    print(f"Huffman codes: {codes}")

    encoded = huffman_encode(text, codes)
    print(f"Encoded: {encoded}  ({len(encoded)} bits vs {len(text)*8} bits uncompressed)")

    decoded = huffman_decode(encoded, tree)
    assert decoded == text, f"Decoded '{decoded}' != original '{text}'"
    print(f"Decoded: '{decoded}'  [matches original: {decoded == text}]")

    # Test with single character
    tree1 = huffman_build_tree("aaaa")
    codes1 = huffman_build_codes(tree1)
    enc1 = huffman_encode("aaaa", codes1)
    dec1 = huffman_decode(enc1, tree1)
    assert dec1 == "aaaa"
    print(f"Single-char test: encode('aaaa') = '{enc1}', decode = '{dec1}'")

    print("\nAll tests passed!")
