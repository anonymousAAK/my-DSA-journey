"""
WEEK 24 - PYTHON ADVANCED DSA
Topic: Research-Level Topics (Amortized Analysis, Skip List, Bloom Filter,
       Reservoir Sampling, Count-Min Sketch)
File: 1.ResearchLevelTopics.py

CONCEPT:
    Five techniques bridging classical DSA and research:
        1. Amortized analysis: dynamic-array doubling has O(1) amortized push.
        2. Skip List: probabilistic sorted list with expected O(log n) ops.
        3. Bloom filter: space-efficient probabilistic set with no false negatives.
        4. Reservoir sampling: uniform k-sample from a stream of unknown size.
        5. Count-Min sketch: approximate frequency counting with d hashes.

KEY POINTS:
    - Doubling capacity ensures total copies after n pushes <= 2n -> amortized O(1).
    - Skip list level promotion via geometric coin flips (p ~ 0.5).
    - Bloom filter false-positive rate decreases with more bits / hashes; never has
      false negatives.
    - Reservoir step: keep stream[i] with probability k / (i+1).
    - Count-Min: estimate(x) = min over rows of table[r][hash_r(x)].

ALGORITHM / APPROACH:
    DynamicArray.push: if size==cap, allocate 2*cap and copy; insert.
    SkipList.insert: walk top->bottom collecting `update[]`, then splice at random level.
    BloomFilter: for each hash i, set bits[hash_i(x) % m] = 1.
    Reservoir: for i in [k..n): pick j uniformly in [0..i]; if j<k replace.
    CountMinSketch.add: for each row r, table[r][hash_r(x)] += 1.

PYTHON-SPECIFIC NOTES vs JAVA:
    - Lists already double under the hood; we still illustrate the doubling
      logic explicitly for the amortized-analysis demo.
    - random.Random(seed) for reproducibility.
    - hashlib gives good cross-platform hashes; we use Python's hash() for speed.

DRY RUN:
    DynamicArray with 100 pushes:
        capacities go 1->2->4->...->128; total copies = 1+2+4+...+64 = 127.
        Amortized = 127/100 ~ 1.27 (< 2), demonstrating O(1) per op.

    SkipList: insert sorted output, support range search.
    BloomFilter on {apple, banana, cherry}: 'apple' yes, 'mango' usually no.
    Reservoir: k=5 from 1..20: outputs a uniformly-likely 5-subset.
    Count-Min on stream [1,1,1,2,2,3,...]: estimate(1) ~ 6.

COMPLEXITY:
    DynamicArray.push: amortized O(1).
    SkipList: expected O(log n) per op.
    BloomFilter: O(k) per op, constant memory.
    Reservoir: O(N) total, O(k) memory.
    Count-Min: O(d) per op, O(d*w) memory.
"""

from __future__ import annotations
import random
from typing import List, Optional


# ---------- Amortized Analysis: Dynamic Array ----------
class DynamicArray:
    def __init__(self) -> None:
        self.data: List[int] = [0] * 1
        self.size = 0
        self.capacity = 1
        self.total_copies = 0

    def push(self, x: int) -> None:
        if self.size == self.capacity:
            new_data = [0] * (self.capacity * 2)
            for i in range(self.size):
                new_data[i] = self.data[i]
                self.total_copies += 1
            self.data = new_data
            self.capacity *= 2
        self.data[self.size] = x
        self.size += 1

    def amortized_per_op(self) -> float:
        return self.total_copies / max(self.size, 1)


# ---------- Skip List ----------
class SkipNode:
    __slots__ = ("val", "next")

    def __init__(self, val: int, level: int) -> None:
        self.val = val
        self.next: List[Optional["SkipNode"]] = [None] * (level + 1)


class SkipList:
    MAX_LEVEL = 16
    P = 0.5

    def __init__(self, seed: int = 42) -> None:
        self.head = SkipNode(-(10 ** 18), self.MAX_LEVEL)
        self.level = 0
        self.rng = random.Random(seed)

    def _random_level(self) -> int:
        lvl = 0
        while self.rng.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, val: int) -> None:
        update: List[Optional[SkipNode]] = [None] * (self.MAX_LEVEL + 1)
        cur = self.head
        for i in range(self.level, -1, -1):
            while cur.next[i] is not None and cur.next[i].val < val:  # type: ignore[union-attr]
                cur = cur.next[i]  # type: ignore[assignment]
            update[i] = cur
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.head
            self.level = lvl
        node = SkipNode(val, lvl)
        for i in range(lvl + 1):
            node.next[i] = update[i].next[i]  # type: ignore[union-attr]
            update[i].next[i] = node          # type: ignore[union-attr]

    def search(self, val: int) -> bool:
        cur = self.head
        for i in range(self.level, -1, -1):
            while cur.next[i] is not None and cur.next[i].val < val:  # type: ignore[union-attr]
                cur = cur.next[i]  # type: ignore[assignment]
        nxt = cur.next[0]
        return nxt is not None and nxt.val == val

    def to_list(self) -> List[int]:
        out: List[int] = []
        cur = self.head.next[0]
        while cur is not None:
            out.append(cur.val)
            cur = cur.next[0]
        return out


# ---------- Bloom Filter ----------
class BloomFilter:
    def __init__(self, size: int) -> None:
        self.size = size
        self.bits = [False] * size

    @staticmethod
    def _h1(s: str) -> int:
        return abs(hash(s))

    @staticmethod
    def _h2(s: str) -> int:
        return abs(hash(s) * 31 + 17)

    def add(self, s: str) -> None:
        self.bits[self._h1(s) % self.size] = True
        self.bits[self._h2(s) % self.size] = True

    def might_contain(self, s: str) -> bool:
        return self.bits[self._h1(s) % self.size] and self.bits[self._h2(s) % self.size]


# ---------- Reservoir Sampling ----------
def reservoir_sample(stream: List[int], k: int, seed: int = 42) -> List[int]:
    rng = random.Random(seed)
    reservoir = stream[:k]
    for i in range(k, len(stream)):
        j = rng.randint(0, i)
        if j < k:
            reservoir[j] = stream[i]
    return reservoir


# ---------- Count-Min Sketch ----------
class CountMinSketch:
    def __init__(self, d: int, w: int, seed: int = 42) -> None:
        self.d = d
        self.w = w
        self.table = [[0] * w for _ in range(d)]
        rng = random.Random(seed)
        self.seeds = [rng.randint(0, 2 ** 31 - 1) for _ in range(d)]

    def _idx(self, x: int, row: int) -> int:
        return abs((x ^ self.seeds[row])) % self.w

    def add(self, x: int) -> None:
        for r in range(self.d):
            self.table[r][self._idx(x, r)] += 1

    def estimate(self, x: int) -> int:
        return min(self.table[r][self._idx(x, r)] for r in range(self.d))


def main() -> None:
    print("=== Amortized Analysis: Dynamic Array ===")
    da = DynamicArray()
    for i in range(100):
        da.push(i)
    print(f"After 100 pushes: total copies = {da.total_copies}, amortized = {da.amortized_per_op():.2f} per op")

    print("\n=== Skip List ===")
    sl = SkipList()
    for x in [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]:
        sl.insert(x)
    print("SkipList:", sl.to_list())
    print("search(19):", sl.search(19))
    print("search(15):", sl.search(15))

    print("\n=== Bloom Filter ===")
    bf = BloomFilter(1000)
    for w in ["apple", "banana", "cherry", "date", "elderberry"]:
        bf.add(w)
    print("'apple' in filter:", bf.might_contain("apple"))
    print("'cherry' in filter:", bf.might_contain("cherry"))
    print("'mango' in filter:", bf.might_contain("mango"))
    print("'xyz' in filter:", bf.might_contain("xyz"))

    print("\n=== Reservoir Sampling ===")
    stream = list(range(1, 21))
    print("Sample of 5 from stream [1..20]:", reservoir_sample(stream, 5))

    print("\n=== Count-Min Sketch ===")
    cms = CountMinSketch(3, 100)
    data = [1, 1, 1, 2, 2, 3, 4, 1, 2, 1, 5, 1, 2, 3, 3, 3]
    for x in data:
        cms.add(x)
    for v in [1, 2, 3, 5, 9]:
        print(f"Estimated frequency of {v}: {cms.estimate(v)}")


if __name__ == "__main__":
    main()
