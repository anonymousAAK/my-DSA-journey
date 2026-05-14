"""
WEEK 21 - PYTHON ADVANCED DSA
Topic: Segment Tree & Binary Indexed Tree (Fenwick Tree)
File: 1.SegmentTreeAndBIT.py

CONCEPT:
    Segment Tree: a binary tree of array intervals. Each node stores an
    aggregate (sum / min / max / xor ...) over its interval. It enables
    O(log n) RANGE queries and O(log n) POINT updates.

    Binary Indexed Tree (BIT / Fenwick Tree): a flat array that uses each
    index's lowest-set-bit to encode an implicit tree. Simpler and faster in
    practice than a segment tree, but limited to operations whose inverse
    exists (sum / xor) for range queries.

KEY POINTS:
    - Segment tree is stored in an array of size ~4n (worst-case tree height
      makes the safe upper bound 4n for a flat array layout).
    - Each segment-tree node has children at indices 2*node+1 and 2*node+2.
    - Build is bottom-up via post-order recursion: O(n).
    - BIT is 1-indexed; the trick "i & -i" isolates the lowest set bit and
      moves to the parent (for prefix sum) or next responsible index
      (for update).
    - BIT range sum uses prefix(r) - prefix(l-1).

ALGORITHM / APPROACH:
    Segment Tree (sum):
        build(node, lo, hi):
            if lo == hi: tree[node] = arr[lo]; return
            mid = (lo+hi)//2
            build left, build right
            tree[node] = tree[left] + tree[right]
        update(node, lo, hi, idx, val):
            if lo == hi: tree[node] = val; return
            recurse into the child containing idx
            recombine
        query(node, lo, hi, l, r):
            no overlap   -> 0
            full overlap -> tree[node]
            partial      -> sum of recursive child queries

    BIT:
        update(i, delta): while i <= n: bit[i] += delta; i += i & -i
        prefix(i):        s=0; while i > 0: s += bit[i]; i -= i & -i; return s

PYTHON-SPECIFIC NOTES vs JAVA:
    - Use plain lists; no need to size at "4*n" exactly, but doing so
      keeps complexity tight and matches the Java reference.
    - Recursion depth in Python is limited (default 1000) — bump
      sys.setrecursionlimit for big arrays, or use an iterative segment tree.
    - Negative indexing on lists is convenient but avoid it inside BIT to
      keep the bit-manipulation trick clear.
    - Use type hints (List[int]) for clarity.

DRY RUN:
    arr = [1, 3, 5, 7, 9, 11], n=6
    Segment tree (sums) for [0..5]:
        build(0, 0, 5) -> mid=2
            build(1, 0, 2): -> 1+3+5 = 9
            build(2, 3, 5): -> 7+9+11 = 27
        tree[0] = 36
    query(1, 3) walks: full overlap on right of left subtree (3+5)=8 plus
    full overlap on left of right subtree (7) -> 15.
    update(3, 10): set leaf for index 3 to 10, propagate: tree[0]=39.

    BIT for the same array (1-indexed):
        bit[1]=1, bit[2]=1+3=4, bit[3]=5, bit[4]=1+3+5+7=16,
        bit[5]=9, bit[6]=9+11=20
        prefix(4) = bit[4] = 16 (1+3+5+7).
        rangeSum(2,5) = prefix(5) - prefix(1) = 25 - 1 = 24.

COMPLEXITY:
    Segment Tree: build O(n); query/update O(log n); space O(4n).
    BIT:          build O(n log n); query/update O(log n); space O(n).
"""

from __future__ import annotations
from typing import List


class SegmentTree:
    """Sum segment tree with point updates and range sum queries."""

    def __init__(self, arr: List[int]) -> None:
        self.n = len(arr)
        self.tree: List[int] = [0] * (4 * max(self.n, 1))
        if self.n:
            self._build(arr, 0, 0, self.n - 1)

    def _build(self, arr: List[int], node: int, lo: int, hi: int) -> None:
        if lo == hi:
            self.tree[node] = arr[lo]
            return
        mid = (lo + hi) // 2
        self._build(arr, 2 * node + 1, lo, mid)
        self._build(arr, 2 * node + 2, mid + 1, hi)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def update(self, idx: int, val: int) -> None:
        self._update(0, 0, self.n - 1, idx, val)

    def _update(self, node: int, lo: int, hi: int, idx: int, val: int) -> None:
        if lo == hi:
            self.tree[node] = val
            return
        mid = (lo + hi) // 2
        if idx <= mid:
            self._update(2 * node + 1, lo, mid, idx, val)
        else:
            self._update(2 * node + 2, mid + 1, hi, idx, val)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query(self, l: int, r: int) -> int:
        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, node: int, lo: int, hi: int, l: int, r: int) -> int:
        if r < lo or hi < l:        # disjoint
            return 0
        if l <= lo and hi <= r:     # fully contained
            return self.tree[node]
        mid = (lo + hi) // 2
        return (self._query(2 * node + 1, lo, mid, l, r)
                + self._query(2 * node + 2, mid + 1, hi, l, r))


class BIT:
    """Fenwick Tree: 1-indexed prefix-sum structure."""

    def __init__(self, arr_or_size) -> None:
        if isinstance(arr_or_size, int):
            self.n = arr_or_size
            self.bit: List[int] = [0] * (self.n + 1)
        else:
            self.n = len(arr_or_size)
            self.bit = [0] * (self.n + 1)
            for i, v in enumerate(arr_or_size):
                self.update(i + 1, v)

    def update(self, i: int, delta: int) -> None:
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def prefix_sum(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, l: int, r: int) -> int:
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

    def point_set(self, i: int, old_val: int, new_val: int) -> None:
        self.update(i, new_val - old_val)


def main() -> None:
    arr = [1, 3, 5, 7, 9, 11]
    print("Array: [1, 3, 5, 7, 9, 11]")

    print("\n=== Segment Tree ===")
    st = SegmentTree(arr)
    print("sum(0,5) =", st.query(0, 5))   # 36
    print("sum(1,3) =", st.query(1, 3))   # 15
    print("sum(2,4) =", st.query(2, 4))   # 21

    st.update(3, 10)
    print("\nAfter update arr[3]=10:")
    print("sum(0,5) =", st.query(0, 5))   # 39
    print("sum(1,3) =", st.query(1, 3))   # 18

    print("\n=== Binary Indexed Tree (Fenwick Tree) ===")
    bit = BIT(arr)
    print("prefix_sum(4) =", bit.prefix_sum(4))      # 16
    print("range_sum(2,5) =", bit.range_sum(2, 5))   # 24
    print("range_sum(1,6) =", bit.range_sum(1, 6))   # 36

    bit.update(4, 3)  # add 3 to index 4 (logical arr[3] becomes 10)
    print("\nAfter adding 3 to index 4:")
    print("prefix_sum(6) =", bit.prefix_sum(6))      # 39
    print("range_sum(3,5) =", bit.range_sum(3, 5))   # 5+10+9 = 24


if __name__ == "__main__":
    main()
