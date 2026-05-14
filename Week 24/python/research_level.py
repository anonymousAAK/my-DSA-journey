"""
Week 24: Research-Level Data Structures & Algorithms
=====================================================
This module covers probabilistic data structures, randomised algorithms,
and approximation algorithms for NP-hard problems.

Topics covered:
    1. Skip List (insert, search, display)
    2. Bloom Filter (add, might_contain, false positive demo)
    3. Reservoir Sampling
    4. Count-Min Sketch (add, estimate)
    5. Vertex Cover 2-Approximation
    6. Greedy Set Cover
"""

from __future__ import annotations

import hashlib
import math
import random
from typing import Any, Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# 1. Skip List
# ---------------------------------------------------------------------------
class _SkipNode:
    """A node in the skip list with multiple forward pointers."""

    __slots__ = ("key", "forward")

    def __init__(self, key: float, level: int) -> None:
        self.key = key
        # forward[i] points to the next node at level i.
        self.forward: List[Optional[_SkipNode]] = [None] * (level + 1)

    def __repr__(self) -> str:
        return f"SkipNode({self.key}, levels={len(self.forward)})"


class SkipList:
    """
    Skip list: a probabilistic alternative to balanced BSTs.

    A skip list is a layered linked list where each level is a subsequence
    of the level below.  Searching is O(log n) expected time by "express
    lanes" at higher levels.

    Operations (expected time):
        insert  : O(log n)
        search  : O(log n)
        delete  : O(log n)

    Space: O(n) expected (each node has ~2 forward pointers on average).

    The maximum level is capped at O(log n) for practical purposes.
    """

    def __init__(self, max_level: int = 16, p: float = 0.5) -> None:
        """
        Create an empty skip list.

        Args:
            max_level: maximum number of levels (height of the list).
            p: probability of promoting a node to the next level.
        """
        self._max_level = max_level
        self._p = p
        self._level = 0  # current highest level in use
        # Header node with key -inf acts as a sentinel.
        self._header = _SkipNode(float("-inf"), max_level)

    def _random_level(self) -> int:
        """Generate a random level for a new node using geometric distribution."""
        lvl = 0
        while random.random() < self._p and lvl < self._max_level:
            lvl += 1
        return lvl

    def search(self, key: float) -> bool:
        """
        Search for *key* in the skip list.

        Start at the highest level and move right while the next node's key
        is less than *key*.  Drop down a level when stuck.  At level 0,
        check if the next node matches.

        Time: O(log n) expected
        """
        current = self._header
        for i in range(self._level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        return current is not None and current.key == key

    def insert(self, key: float) -> None:
        """
        Insert *key* into the skip list.

        1. Find the position at each level where the new node should go
           (same traversal as search, recording "update" pointers).
        2. Generate a random level for the new node.
        3. Splice the new node into each level up to its random level.

        Time: O(log n) expected
        """
        update: List[_SkipNode] = [self._header] * (self._max_level + 1)
        current = self._header

        for i in range(self._level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        # If key already exists, we could update value; here we just skip.
        if current and current.key == key:
            return

        new_level = self._random_level()
        if new_level > self._level:
            for i in range(self._level + 1, new_level + 1):
                update[i] = self._header
            self._level = new_level

        new_node = _SkipNode(key, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def display(self) -> str:
        """Return a string representation of all levels."""
        lines: List[str] = []
        for lvl in range(self._level + 1):
            line = f"Level {lvl}: "
            node = self._header.forward[lvl]
            elements: List[str] = []
            while node:
                elements.append(str(node.key))
                node = node.forward[lvl]
            line += " -> ".join(elements) if elements else "(empty)"
            lines.append(line)
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# 2. Bloom Filter
# ---------------------------------------------------------------------------
class BloomFilter:
    """
    Bloom filter: a space-efficient probabilistic set membership test.

    - add(item):          mark item as present (no false negatives)
    - might_contain(item): returns True if item *might* be present
                           (possible false positives)

    False positive probability ~ (1 - e^(-kn/m))^k
    where m = bit array size, k = number of hash functions, n = items inserted.

    Optimal k = (m/n) * ln(2).

    Space: O(m) bits
    Time:  O(k) per add/query
    """

    def __init__(self, expected_items: int, fp_rate: float = 0.01) -> None:
        """
        Create a Bloom filter sized for *expected_items* with false positive
        rate *fp_rate*.
        """
        # Calculate optimal bit array size: m = -n*ln(p) / (ln(2))^2
        self._m = max(1, int(-expected_items * math.log(fp_rate) / (math.log(2) ** 2)))
        # Calculate optimal number of hash functions: k = (m/n) * ln(2)
        self._k = max(1, int((self._m / expected_items) * math.log(2)))
        self._bit_array = [False] * self._m
        self._count = 0

    @property
    def size(self) -> int:
        return self._m

    @property
    def num_hashes(self) -> int:
        return self._k

    def _hashes(self, item: str) -> List[int]:
        """
        Generate k hash positions using double hashing:
            h_i(x) = (h1(x) + i * h2(x)) mod m

        This avoids computing k independent hash functions.
        """
        h1 = int(hashlib.md5(item.encode()).hexdigest(), 16)
        h2 = int(hashlib.sha256(item.encode()).hexdigest(), 16)
        return [(h1 + i * h2) % self._m for i in range(self._k)]

    def add(self, item: str) -> None:
        """Add *item* to the Bloom filter.  O(k)."""
        for pos in self._hashes(item):
            self._bit_array[pos] = True
        self._count += 1

    def might_contain(self, item: str) -> bool:
        """
        Check if *item* might be in the set.

        Returns False  -> item is DEFINITELY not in the set.
        Returns True   -> item is PROBABLY in the set (possible false positive).

        O(k)
        """
        return all(self._bit_array[pos] for pos in self._hashes(item))


# ---------------------------------------------------------------------------
# 3. Reservoir Sampling
# ---------------------------------------------------------------------------
def reservoir_sampling(stream: List[Any], k: int) -> List[Any]:
    """
    Select k items uniformly at random from a stream of unknown length.

    Algorithm R (Vitter, 1985):
        1. Fill the reservoir with the first k items.
        2. For each subsequent item at index i (0-indexed):
           - Pick a random integer j in [0, i].
           - If j < k, replace reservoir[j] with stream[i].

    Proof of uniformity: after processing i items, each item is in the
    reservoir with probability k/i.

    Time:  O(n)
    Space: O(k)
    """
    if k <= 0:
        return []
    if k >= len(stream):
        return list(stream)

    reservoir = list(stream[:k])

    for i in range(k, len(stream)):
        j = random.randint(0, i)
        if j < k:
            reservoir[j] = stream[i]

    return reservoir


# ---------------------------------------------------------------------------
# 4. Count-Min Sketch
# ---------------------------------------------------------------------------
class CountMinSketch:
    """
    Count-Min Sketch: a probabilistic frequency estimation data structure.

    - add(item, count): increment the count of *item*
    - estimate(item):   return an estimate of item's count (may overcount)

    Guarantees: estimate(item) >= true_count(item)
                P(estimate - true_count > epsilon * N) < delta
    where N = total count, epsilon = e/width, delta = 1/e^depth.

    Time:  O(depth) per add/estimate
    Space: O(width * depth)
    """

    def __init__(self, width: int = 1000, depth: int = 5) -> None:
        """
        Create a Count-Min Sketch.

        Args:
            width:  number of counters per row (controls accuracy).
            depth:  number of hash functions / rows (controls confidence).
        """
        self._width = width
        self._depth = depth
        self._table = [[0] * width for _ in range(depth)]
        # Use random seeds for each hash function.
        self._seeds = [random.randint(0, 2**31) for _ in range(depth)]

    def _hash(self, item: str, seed: int) -> int:
        """Compute a hash for *item* with the given *seed*."""
        h = hashlib.md5(f"{seed}:{item}".encode()).hexdigest()
        return int(h, 16) % self._width

    def add(self, item: str, count: int = 1) -> None:
        """Add *count* occurrences of *item*.  O(depth)."""
        for i in range(self._depth):
            col = self._hash(item, self._seeds[i])
            self._table[i][col] += count

    def estimate(self, item: str) -> int:
        """
        Estimate the count of *item*.

        Returns the minimum across all rows (minimises overcounting).
        O(depth).
        """
        return min(
            self._table[i][self._hash(item, self._seeds[i])]
            for i in range(self._depth)
        )


# ---------------------------------------------------------------------------
# 5. Vertex Cover — 2-Approximation
# ---------------------------------------------------------------------------
def vertex_cover_2approx(
    n: int, edges: List[Tuple[int, int]]
) -> Set[int]:
    """
    Find a vertex cover of at most 2x the optimal size.

    A vertex cover is a set of vertices such that every edge has at least
    one endpoint in the set.

    Algorithm (2-approximation):
        1. Pick any uncovered edge (u, v).
        2. Add BOTH u and v to the cover.
        3. Remove all edges incident to u or v.
        4. Repeat until all edges are covered.

    This guarantees |cover| <= 2 * |OPT| because the optimal cover must
    include at least one endpoint of each edge we picked, and we added two.

    Time:  O(V + E)
    Space: O(V + E)
    """
    cover: Set[int] = set()
    covered = [False] * len(edges)

    # Build adjacency: edge_index -> (u, v)
    # Also track which edges are incident to each vertex.
    incident: Dict[int, List[int]] = {i: [] for i in range(n)}
    for idx, (u, v) in enumerate(edges):
        incident[u].append(idx)
        incident[v].append(idx)

    for idx, (u, v) in enumerate(edges):
        if covered[idx]:
            continue
        # Add both endpoints
        cover.add(u)
        cover.add(v)
        # Mark all incident edges as covered
        for ei in incident[u]:
            covered[ei] = True
        for ei in incident[v]:
            covered[ei] = True

    return cover


# ---------------------------------------------------------------------------
# 6. Greedy Set Cover
# ---------------------------------------------------------------------------
def greedy_set_cover(
    universe: Set[int], subsets: List[Set[int]]
) -> List[int]:
    """
    Greedy approximation for the Set Cover problem.

    Given a universe U and a collection S of subsets of U, find the
    smallest sub-collection whose union equals U.  This is NP-hard.

    Greedy algorithm:
        Repeatedly pick the subset that covers the most uncovered elements.

    Approximation ratio: O(ln n) where n = |universe|.
    This is essentially the best possible unless P = NP.

    Returns a list of indices (into *subsets*) of the chosen subsets.

    Time:  O(|universe| * |subsets| * max_subset_size)
    Space: O(|universe|)
    """
    uncovered = set(universe)
    chosen: List[int] = []
    used = [False] * len(subsets)

    while uncovered:
        # Pick the subset that covers the most uncovered elements.
        best_idx = -1
        best_count = 0
        for i, s in enumerate(subsets):
            if used[i]:
                continue
            covered = len(s & uncovered)
            if covered > best_count:
                best_count = covered
                best_idx = i

        if best_idx == -1 or best_count == 0:
            break  # can't cover any more elements

        used[best_idx] = True
        chosen.append(best_idx)
        uncovered -= subsets[best_idx]

    return chosen


# ===========================================================================
# Test Cases
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Week 24 — Research-Level Data Structures & Algorithms")
    print("=" * 60)

    random.seed(42)  # reproducible tests

    # --- Skip List ---------------------------------------------------------
    print("\n--- Skip List ---")
    sl = SkipList(max_level=4, p=0.5)
    for val in [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]:
        sl.insert(val)
    print(sl.display())
    assert sl.search(19) is True
    assert sl.search(20) is False
    print(f"search(19)={sl.search(19)}, search(20)={sl.search(20)}")

    # Test duplicate insert (should be no-op)
    sl.insert(19)
    assert sl.search(19) is True

    # --- Bloom Filter ------------------------------------------------------
    print("\n--- Bloom Filter ---")
    bf = BloomFilter(expected_items=1000, fp_rate=0.01)
    print(f"Bloom filter: {bf.size} bits, {bf.num_hashes} hash functions")

    words = ["apple", "banana", "cherry", "date", "elderberry"]
    for w in words:
        bf.add(w)

    for w in words:
        assert bf.might_contain(w) is True
    print(f"All inserted words found: True")

    # False positive test
    test_words = [f"word_{i}" for i in range(10000)]
    false_positives = sum(1 for w in test_words if bf.might_contain(w))
    fp_rate = false_positives / len(test_words)
    print(f"False positive rate on {len(test_words)} random words: {fp_rate:.4f}")

    # --- Reservoir Sampling ------------------------------------------------
    print("\n--- Reservoir Sampling ---")
    stream = list(range(1, 10001))  # 1 to 10000
    k = 10
    sample = reservoir_sampling(stream, k)
    print(f"Reservoir sample (k={k}) from [1..10000]: {sample}")
    assert len(sample) == k
    assert all(1 <= x <= 10000 for x in sample)

    # Statistical test: run many times and check distribution is roughly uniform.
    counts = [0] * 10001
    num_trials = 10000
    for _ in range(num_trials):
        for x in reservoir_sampling(stream, k):
            counts[x] += 1
    # Expected count per element = k * num_trials / 10000 = 10
    avg = sum(counts[1:]) / 10000
    print(f"Average selection count per element over {num_trials} trials: {avg:.2f} (expected ~{k*num_trials/10000:.1f})")

    # --- Count-Min Sketch --------------------------------------------------
    print("\n--- Count-Min Sketch ---")
    cms = CountMinSketch(width=1000, depth=7)
    true_counts = {"apple": 100, "banana": 50, "cherry": 30, "date": 10}
    for item, count in true_counts.items():
        cms.add(item, count)

    for item, true_count in true_counts.items():
        est = cms.estimate(item)
        print(f"  {item}: true={true_count}, estimate={est}")
        assert est >= true_count  # CMS never undercounts

    absent_est = cms.estimate("fig")
    print(f"  fig (never added): estimate={absent_est}")

    # --- Vertex Cover 2-Approximation -------------------------------------
    print("\n--- Vertex Cover (2-Approximation) ---")
    # Graph:
    #   0 -- 1 -- 2
    #   |    |
    #   3 -- 4
    vc_edges = [(0, 1), (1, 2), (0, 3), (3, 4), (1, 4)]
    cover = vertex_cover_2approx(5, vc_edges)
    print(f"Vertex cover: {cover}")
    # Verify it's a valid cover: every edge has at least one endpoint in cover.
    for u, v in vc_edges:
        assert u in cover or v in cover, f"Edge ({u},{v}) not covered!"
    print(f"Cover size: {len(cover)} (optimal is likely 2-3)")

    # --- Greedy Set Cover --------------------------------------------------
    print("\n--- Greedy Set Cover ---")
    universe = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    subsets = [
        {1, 2, 3, 4},       # 0
        {3, 4, 5, 6},       # 1
        {5, 6, 7, 8},       # 2
        {7, 8, 9, 10},      # 3
        {1, 5, 9},          # 4
        {2, 6, 10},         # 5
    ]
    chosen = greedy_set_cover(universe, subsets)
    covered = set()
    for idx in chosen:
        covered |= subsets[idx]
    print(f"Chosen subsets (indices): {chosen}")
    print(f"Union covers: {covered}")
    assert covered == universe
    print(f"Number of subsets used: {len(chosen)}")

    # Another test: exact cover possible with 2 subsets
    universe2 = {1, 2, 3, 4}
    subsets2 = [{1, 2}, {3, 4}, {1, 3}, {2, 4}, {1, 2, 3, 4}]
    chosen2 = greedy_set_cover(universe2, subsets2)
    covered2 = set()
    for idx in chosen2:
        covered2 |= subsets2[idx]
    assert covered2 == universe2
    print(f"\nSecond test — chosen: {chosen2}, sets used: {len(chosen2)}")

    print("\nAll tests passed!")
