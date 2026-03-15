"""
WEEK 24 — Python: Research-Level Topics
Skip list, Bloom filter, reservoir sampling, count-min sketch,
NP-completeness concepts, approximation algorithms.
"""
import random
import math
from typing import List, Set, Optional

# === BLOOM FILTER ===
class BloomFilter:
    """
    Space-efficient probabilistic set.
    - False positives possible
    - No false negatives
    Space: O(m) bits, Time: O(k) per operation where k = number of hash functions.
    """
    def __init__(self, size: int = 1000, num_hashes: int = 3):
        self.size = size
        self.num_hashes = num_hashes
        self.bits = [False] * size

    def _hashes(self, item: str) -> List[int]:
        """Generate k hash positions."""
        positions = []
        for i in range(self.num_hashes):
            h = hash(item + str(i)) % self.size
            positions.append(abs(h))
        return positions

    def add(self, item: str):
        for pos in self._hashes(item):
            self.bits[pos] = True

    def might_contain(self, item: str) -> bool:
        return all(self.bits[pos] for pos in self._hashes(item))


# === RESERVOIR SAMPLING ===
def reservoir_sample(stream: List[int], k: int) -> List[int]:
    """
    Randomly sample k items from a stream of unknown size.
    Each item has equal probability k/N of being selected.
    Time: O(N), Space: O(k)
    """
    reservoir = stream[:k]
    for i in range(k, len(stream)):
        j = random.randint(0, i)
        if j < k:
            reservoir[j] = stream[i]
    return reservoir


# === COUNT-MIN SKETCH ===
class CountMinSketch:
    """
    Approximate frequency counting.
    Space: O(d * w) instead of O(distinct elements).
    Estimate >= true count (overestimates due to collisions).
    """
    def __init__(self, d: int = 3, w: int = 100):
        self.d = d
        self.w = w
        self.table = [[0] * w for _ in range(d)]
        self.seeds = [random.randint(0, 10**9) for _ in range(d)]

    def add(self, x: int, count: int = 1):
        for i in range(self.d):
            pos = abs(hash((x, self.seeds[i]))) % self.w
            self.table[i][pos] += count

    def estimate(self, x: int) -> int:
        return min(
            self.table[i][abs(hash((x, self.seeds[i]))) % self.w]
            for i in range(self.d)
        )


# === SKIP LIST (Simplified) ===
class SkipListNode:
    def __init__(self, val: int = -math.inf, level: int = 0):
        self.val = val
        self.next = [None] * (level + 1)

class SkipList:
    """
    Probabilistic sorted list. Expected O(log n) search/insert/delete.
    """
    MAX_LEVEL = 16
    P = 0.5

    def __init__(self):
        self.head = SkipListNode(level=self.MAX_LEVEL)
        self.level = 0

    def _random_level(self) -> int:
        lvl = 0
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, val: int):
        update = [None] * (self.MAX_LEVEL + 1)
        curr = self.head
        for i in range(self.level, -1, -1):
            while curr.next[i] and curr.next[i].val < val:
                curr = curr.next[i]
            update[i] = curr

        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.head
            self.level = lvl

        node = SkipListNode(val, lvl)
        for i in range(lvl + 1):
            node.next[i] = update[i].next[i]
            update[i].next[i] = node

    def search(self, val: int) -> bool:
        curr = self.head
        for i in range(self.level, -1, -1):
            while curr.next[i] and curr.next[i].val < val:
                curr = curr.next[i]
        curr = curr.next[0]
        return curr is not None and curr.val == val

    def display(self) -> List[int]:
        result = []
        curr = self.head.next[0]
        while curr:
            result.append(curr.val)
            curr = curr.next[0]
        return result


# === APPROXIMATION ALGORITHMS ===

def vertex_cover_2approx(V: int, edges: List[tuple]) -> Set[int]:
    """
    2-approximation for Minimum Vertex Cover.
    |result| <= 2 * |optimal|.
    Time: O(V + E)
    """
    covered = set()
    result = set()
    for u, v in edges:
        if u not in covered and v not in covered:
            result.add(u)
            result.add(v)
            covered.add(u)
            covered.add(v)
    return result

def greedy_set_cover(universe: Set[int], sets: List[Set[int]]) -> List[int]:
    """
    Greedy O(log n)-approximation for Set Cover.
    At each step, pick the set covering the most uncovered elements.
    """
    uncovered = set(universe)
    chosen = []
    while uncovered:
        best_idx = max(range(len(sets)), key=lambda i: len(sets[i] & uncovered))
        if not (sets[best_idx] & uncovered):
            break
        chosen.append(best_idx)
        uncovered -= sets[best_idx]
    return chosen


if __name__ == "__main__":
    # Bloom Filter
    print("=== Bloom Filter ===")
    bf = BloomFilter(size=1000, num_hashes=3)
    words = ["apple", "banana", "cherry", "date"]
    for w in words:
        bf.add(w)
    for test in ["apple", "cherry", "mango", "xyz"]:
        print(f"  '{test}': {bf.might_contain(test)}")

    # Reservoir Sampling
    print("\n=== Reservoir Sampling ===")
    random.seed(42)
    stream = list(range(1, 101))
    sample = reservoir_sample(stream, 5)
    print(f"  5 from [1..100]: {sample}")

    # Count-Min Sketch
    print("\n=== Count-Min Sketch ===")
    cms = CountMinSketch(d=3, w=100)
    data = [1,1,1,2,2,3,4,1,2,1,5,1,2,3,3,3]
    for x in data:
        cms.add(x)
    for x in [1, 2, 3, 5, 9]:
        print(f"  freq({x}) ≈ {cms.estimate(x)}")

    # Skip List
    print("\n=== Skip List ===")
    sl = SkipList()
    for x in [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]:
        sl.insert(x)
    print(f"  Elements: {sl.display()}")
    print(f"  search(19): {sl.search(19)}")
    print(f"  search(15): {sl.search(15)}")

    # Vertex Cover
    print("\n=== Vertex Cover (2-approx) ===")
    edges = [(0,1), (0,2), (1,3), (2,3), (3,4)]
    cover = vertex_cover_2approx(5, edges)
    print(f"  Cover: {cover}, size: {len(cover)}")

    # Set Cover
    print("\n=== Greedy Set Cover ===")
    universe = set(range(10))
    sets = [{0,1,2}, {3,4,5}, {4,5,6,7}, {0,3,8}, {2,7,9}]
    chosen = greedy_set_cover(universe, sets)
    covered = set()
    for i in chosen:
        covered |= sets[i]
    print(f"  Chosen sets: {chosen}")
    print(f"  Covered: {covered}")
