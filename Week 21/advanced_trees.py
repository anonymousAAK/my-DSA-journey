"""
Week 21: Advanced Trees
========================
This module covers three powerful tree-based data structures used for
range queries, prefix operations, and string problems.

Topics covered:
    1. Segment Tree (build, range sum query, point update)
    2. Binary Indexed Tree / Fenwick Tree (update, prefix sum, range sum)
    3. Trie (insert, search, starts_with, autocomplete, delete)
"""

from __future__ import annotations

from typing import List, Optional


# ---------------------------------------------------------------------------
# 1. Segment Tree — range sum query + point update
# ---------------------------------------------------------------------------
class SegmentTree:
    """
    Segment tree for range sum queries and point updates.

    The tree is stored in a 1-indexed array of size 4*n (to handle all
    levels comfortably).

    Operations:
        build(arr)          — O(n)
        query(l, r)         — O(log n)   range sum [l, r] inclusive
        update(idx, val)    — O(log n)   set arr[idx] = val

    Space: O(n)
    """

    def __init__(self, arr: List[int]) -> None:
        self._n = len(arr)
        self._tree = [0] * (4 * self._n)
        self._arr = arr[:]
        if self._n > 0:
            self._build(1, 0, self._n - 1)

    # --- Build -------------------------------------------------------------
    def _build(self, node: int, start: int, end: int) -> None:
        """
        Recursively build the segment tree.

        Each leaf stores one element.  Each internal node stores the sum
        of its children.

        Time: O(n)
        """
        if start == end:
            self._tree[node] = self._arr[start]
            return
        mid = (start + end) // 2
        self._build(2 * node, start, mid)
        self._build(2 * node + 1, mid + 1, end)
        self._tree[node] = self._tree[2 * node] + self._tree[2 * node + 1]

    # --- Range Sum Query ---------------------------------------------------
    def query(self, l: int, r: int) -> int:
        """
        Return the sum of elements in the range [l, r] (0-indexed, inclusive).

        Strategy: traverse the tree.  At each node:
          - If the node's range is completely inside [l, r], return its value.
          - If completely outside, return 0.
          - Otherwise, recurse into both children and sum the results.

        Time: O(log n)
        """
        return self._query(1, 0, self._n - 1, l, r)

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or end < l:
            return 0  # completely outside
        if l <= start and end <= r:
            return self._tree[node]  # completely inside
        mid = (start + end) // 2
        left_sum = self._query(2 * node, start, mid, l, r)
        right_sum = self._query(2 * node + 1, mid + 1, end, l, r)
        return left_sum + right_sum

    # --- Point Update ------------------------------------------------------
    def update(self, idx: int, val: int) -> None:
        """
        Set arr[idx] = val and update the tree accordingly.

        Strategy: find the leaf corresponding to idx, update it, then
        propagate the change upward.

        Time: O(log n)
        """
        self._arr[idx] = val
        self._update(1, 0, self._n - 1, idx, val)

    def _update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
        if start == end:
            self._tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update(2 * node, start, mid, idx, val)
        else:
            self._update(2 * node + 1, mid + 1, end, idx, val)
        self._tree[node] = self._tree[2 * node] + self._tree[2 * node + 1]


# ---------------------------------------------------------------------------
# 2. Binary Indexed Tree (Fenwick Tree)
# ---------------------------------------------------------------------------
class FenwickTree:
    """
    Binary Indexed Tree (BIT) / Fenwick Tree for prefix sum queries and
    point updates.

    Internally 1-indexed.  The user-facing API is 0-indexed.

    Key idea: each position i (1-indexed) is responsible for a range of
    elements determined by the lowest set bit of i.

    Operations:
        update(idx, delta)  — O(log n)   add delta to arr[idx]
        prefix_sum(idx)     — O(log n)   sum of arr[0..idx]
        range_sum(l, r)     — O(log n)   sum of arr[l..r]

    Space: O(n)
    """

    def __init__(self, n: int) -> None:
        """Create a BIT of size *n*, initialised to all zeros."""
        self._n = n
        self._tree = [0] * (n + 1)  # 1-indexed

    @classmethod
    def from_array(cls, arr: List[int]) -> FenwickTree:
        """
        Build a Fenwick tree from an existing array in O(n).

        Instead of calling update() n times (O(n log n)), we use the
        linear-time construction trick: for each i, add tree[i] to
        tree[i + lowbit(i)] if that index is within bounds.
        """
        bit = cls(len(arr))
        for i in range(len(arr)):
            bit._tree[i + 1] = arr[i]
        for i in range(1, len(arr) + 1):
            j = i + (i & -i)
            if j <= len(arr):
                bit._tree[j] += bit._tree[i]
        return bit

    def update(self, idx: int, delta: int) -> None:
        """
        Add *delta* to the element at position *idx* (0-indexed).

        Propagate the change up through the tree by adding the lowest set bit
        of the current index repeatedly.

        Time: O(log n)
        """
        i = idx + 1  # convert to 1-indexed
        while i <= self._n:
            self._tree[i] += delta
            i += i & (-i)  # move to the next responsible position

    def prefix_sum(self, idx: int) -> int:
        """
        Return the sum of elements arr[0..idx] (inclusive, 0-indexed).

        Walk down by stripping the lowest set bit at each step.

        Time: O(log n)
        """
        s = 0
        i = idx + 1  # 1-indexed
        while i > 0:
            s += self._tree[i]
            i -= i & (-i)
        return s

    def range_sum(self, l: int, r: int) -> int:
        """
        Return sum of arr[l..r] (inclusive, 0-indexed).

        Time: O(log n)
        """
        if l == 0:
            return self.prefix_sum(r)
        return self.prefix_sum(r) - self.prefix_sum(l - 1)


# ---------------------------------------------------------------------------
# 3. Trie (Prefix Tree)
# ---------------------------------------------------------------------------
class _TrieNode:
    """A single node in the Trie."""

    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.is_end: bool = False


class Trie:
    """
    Trie (prefix tree) supporting insert, search, prefix search,
    autocomplete, and delete.

    All operations run in O(L) time where L is the length of the word/prefix.

    Space: O(total characters inserted) in the worst case (no shared prefixes).
    """

    def __init__(self) -> None:
        self._root = _TrieNode()

    # --- Insert ------------------------------------------------------------
    def insert(self, word: str) -> None:
        """
        Insert *word* into the trie.
        Time: O(L) where L = len(word)
        """
        node = self._root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = _TrieNode()
            node = node.children[ch]
        node.is_end = True

    # --- Search ------------------------------------------------------------
    def search(self, word: str) -> bool:
        """
        Return True if *word* is in the trie (exact match).
        Time: O(L)
        """
        node = self._find_node(word)
        return node is not None and node.is_end

    # --- Starts With (prefix search) ---------------------------------------
    def starts_with(self, prefix: str) -> bool:
        """
        Return True if any word in the trie starts with *prefix*.
        Time: O(L)
        """
        return self._find_node(prefix) is not None

    # --- Autocomplete ------------------------------------------------------
    def autocomplete(self, prefix: str) -> List[str]:
        """
        Return all words in the trie that start with *prefix*.

        Strategy: navigate to the prefix node, then DFS to collect all
        words reachable from there.

        Time: O(L + number_of_matching_characters)
        """
        node = self._find_node(prefix)
        if node is None:
            return []
        results: List[str] = []
        self._collect(node, list(prefix), results)
        return results

    def _collect(self, node: _TrieNode, path: List[str], results: List[str]) -> None:
        """DFS helper to collect all complete words from *node*."""
        if node.is_end:
            results.append("".join(path))
        for ch in sorted(node.children):  # sorted for deterministic order
            path.append(ch)
            self._collect(node.children[ch], path, results)
            path.pop()

    # --- Delete ------------------------------------------------------------
    def delete(self, word: str) -> bool:
        """
        Delete *word* from the trie.  Returns True if the word existed.

        Strategy: recursively descend to the end of the word.  On the way
        back up, remove nodes that are no longer needed (no children and
        not end-of-word for another word).

        Time: O(L)
        """
        return self._delete(self._root, word, 0)

    def _delete(self, node: _TrieNode, word: str, depth: int) -> bool:
        if depth == len(word):
            if not node.is_end:
                return False  # word not found
            node.is_end = False
            return True  # signal that we can potentially prune

        ch = word[depth]
        if ch not in node.children:
            return False

        found = self._delete(node.children[ch], word, depth + 1)

        # Prune child if it has no children and is not an end node.
        if found:
            child = node.children[ch]
            if not child.is_end and not child.children:
                del node.children[ch]

        return found

    # --- Internal helper ---------------------------------------------------
    def _find_node(self, prefix: str) -> Optional[_TrieNode]:
        """Navigate to the node corresponding to *prefix*, or None."""
        node = self._root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node


# ===========================================================================
# Test Cases
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Week 21 — Advanced Trees")
    print("=" * 60)

    # --- Segment Tree ------------------------------------------------------
    print("\n--- Segment Tree ---")
    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(arr)
    assert st.query(0, 5) == 36  # sum of entire array
    assert st.query(1, 3) == 15  # 3 + 5 + 7
    assert st.query(2, 4) == 21  # 5 + 7 + 9
    print(f"Array: {arr}")
    print(f"query(0,5) = {st.query(0,5)}, query(1,3) = {st.query(1,3)}")

    st.update(3, 10)  # change 7 -> 10
    assert st.query(1, 3) == 18  # 3 + 5 + 10
    assert st.query(0, 5) == 39  # total increased by 3
    print(f"After update(3, 10): query(1,3) = {st.query(1,3)}, query(0,5) = {st.query(0,5)}")

    # --- Fenwick Tree ------------------------------------------------------
    print("\n--- Fenwick Tree (BIT) ---")
    arr2 = [2, 1, 1, 3, 2, 3, 4, 5, 6, 7, 8, 9]
    bit = FenwickTree.from_array(arr2)
    assert bit.prefix_sum(5) == 12   # 2+1+1+3+2+3
    assert bit.range_sum(2, 5) == 9  # 1+3+2+3
    print(f"Array: {arr2}")
    print(f"prefix_sum(5) = {bit.prefix_sum(5)}, range_sum(2,5) = {bit.range_sum(2,5)}")

    bit.update(3, 5)  # add 5 to arr[3], so arr[3] becomes 8
    assert bit.prefix_sum(5) == 17
    print(f"After update(3, +5): prefix_sum(5) = {bit.prefix_sum(5)}")

    # --- Trie --------------------------------------------------------------
    print("\n--- Trie ---")
    trie = Trie()
    for word in ["apple", "app", "apricot", "banana", "band", "ban"]:
        trie.insert(word)

    assert trie.search("apple") is True
    assert trie.search("app") is True
    assert trie.search("ap") is False
    assert trie.starts_with("ap") is True
    assert trie.starts_with("ban") is True
    assert trie.starts_with("cat") is False
    print(f"search('apple')={trie.search('apple')}, search('ap')={trie.search('ap')}")
    print(f"starts_with('ap')={trie.starts_with('ap')}")

    # Autocomplete
    ac = trie.autocomplete("ap")
    print(f"autocomplete('ap') = {ac}")
    assert "apple" in ac and "app" in ac and "apricot" in ac

    ac_ban = trie.autocomplete("ban")
    print(f"autocomplete('ban') = {ac_ban}")
    assert "banana" in ac_ban and "band" in ac_ban and "ban" in ac_ban

    # Delete
    assert trie.delete("app") is True
    assert trie.search("app") is False
    assert trie.search("apple") is True  # "apple" should still exist
    print(f"After delete('app'): search('app')={trie.search('app')}, search('apple')={trie.search('apple')}")

    assert trie.delete("nonexistent") is False
    print("delete('nonexistent') = False (word not found)")

    print("\nAll tests passed!")
