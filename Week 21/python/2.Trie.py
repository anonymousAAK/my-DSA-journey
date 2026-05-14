"""
WEEK 21 - PYTHON ADVANCED DSA
Topic: Trie (Prefix Tree) + Binary Trie for Maximum XOR
File: 2.Trie.py

CONCEPT:
    A trie is a rooted tree where each edge represents a character.
    The path from root to a marked node spells one of the stored words.
    Tries shine for prefix-based operations: search, count-with-prefix,
    autocomplete, longest-prefix-match (IP routing), and a binary trie
    can compute Maximum XOR between two array elements in O(n log V).

KEY POINTS:
    - Each node holds children (dict or fixed-size array of 26) and a flag
      `is_end` plus an optional `word_count` for prefix counting.
    - Insert/search/startsWith all run in O(m) for a word of length m.
    - Delete must clear `is_end` and prune dead branches.
    - Binary trie: insert each integer's bits MSB->LSB; for each query,
      greedily walk to the opposite bit when present to maximise XOR.

ALGORITHM / APPROACH:
    insert(word):
        node = root
        for c in word:
            create child if missing
            node = child
            node.word_count += 1
        node.is_end = True

    search/startsWith: walk from root, return based on terminal flag /
    successful walk.

    autocomplete(prefix):
        walk to prefix node; DFS collecting all words below.

    delete(word):
        recursive helper unsets is_end at the terminal node and prunes
        children whose word_count drops to 0.

    maxXOR(nums):
        determine bit width B from max(nums)
        insert each x's bits into binary trie
        for each x: greedily traverse, choosing opposite bit when possible
        track best XOR seen.

PYTHON-SPECIFIC NOTES vs JAVA:
    - Use a small `class TrieNode` with a dict children for flexibility,
      or a length-26 list to mirror the Java code one-to-one.
    - Use list-of-list for the binary trie to mimic Java's int[][] layout,
      avoiding per-node object allocation overhead.
    - String iteration is direct (`for c in word`), no .toCharArray needed.
    - Recursion is fine for the alphabet sizes used here; very deep
      tries should switch to iterative DFS.

DRY RUN:
    Insert "apple", "app".
        After "apple": path a->p->p->l->e, is_end on the last 'e'.
        After "app":  path a->p->p, is_end on the second 'p'.
    search("app")     -> True   (is_end is set on second 'p').
    search("ap")      -> False  (no is_end on first 'p').
    startsWith("ap")  -> True.

    Max XOR demo on [3,10,5,25,2,8] (5-bit numbers):
        25=11001, 5=00101 -> XOR = 11100 = 28.
        Greedy walk for 5 finds 25 because we can pick bit-4=1
        (opposite of 5's bit-4=0) at the root of the trie.

COMPLEXITY:
    Trie ops:           O(m) per operation.
    Autocomplete:       O(m + total length of words below).
    Delete:             O(m).
    Max XOR (binary):   O(n * B) build + O(n * B) query, B ~ log(max).
"""

from __future__ import annotations
from typing import List, Optional


class TrieNode:
    __slots__ = ("children", "is_end", "word_count")

    def __init__(self) -> None:
        self.children: List[Optional["TrieNode"]] = [None] * 26
        self.is_end: bool = False
        self.word_count: int = 0


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    @staticmethod
    def _idx(ch: str) -> int:
        return ord(ch) - ord("a")

    def insert(self, word: str) -> None:
        node = self.root
        for c in word:
            i = self._idx(c)
            if node.children[i] is None:
                node.children[i] = TrieNode()
            node = node.children[i]  # type: ignore[assignment]
            node.word_count += 1
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for c in word:
            i = self._idx(c)
            if node.children[i] is None:
                return False
            node = node.children[i]  # type: ignore[assignment]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for c in prefix:
            i = self._idx(c)
            if node.children[i] is None:
                return False
            node = node.children[i]  # type: ignore[assignment]
        return True

    def count_with_prefix(self, prefix: str) -> int:
        node = self.root
        for c in prefix:
            i = self._idx(c)
            if node.children[i] is None:
                return 0
            node = node.children[i]  # type: ignore[assignment]
        return node.word_count

    def autocomplete(self, prefix: str) -> List[str]:
        node = self.root
        for c in prefix:
            i = self._idx(c)
            if node.children[i] is None:
                return []
            node = node.children[i]  # type: ignore[assignment]
        out: List[str] = []
        self._dfs_collect(node, list(prefix), out)
        return out

    def _dfs_collect(self, node: TrieNode, current: List[str], out: List[str]) -> None:
        if node.is_end:
            out.append("".join(current))
        for i in range(26):
            child = node.children[i]
            if child is not None:
                current.append(chr(ord("a") + i))
                self._dfs_collect(child, current, out)
                current.pop()

    def delete(self, word: str) -> bool:
        return self._delete(self.root, word, 0)

    def _delete(self, node: TrieNode, word: str, idx: int) -> bool:
        if idx == len(word):
            if not node.is_end:
                return False
            node.is_end = False
            return True
        i = self._idx(word[idx])
        child = node.children[i]
        if child is None:
            return False
        deleted = self._delete(child, word, idx + 1)
        if deleted:
            child.word_count -= 1
            if not any(c is not None for c in child.children) and child.word_count == 0:
                node.children[i] = None
        return deleted


def max_xor(nums: List[int]) -> int:
    """Maximum XOR of any pair via binary trie."""
    if not nums:
        return 0
    bits = max(nums).bit_length() or 1
    # trie[node][0/1] = child index (0 means "absent")
    trie: List[List[int]] = [[0, 0]]

    for x in nums:
        node = 0
        for b in range(bits - 1, -1, -1):
            bit = (x >> b) & 1
            if trie[node][bit] == 0:
                trie.append([0, 0])
                trie[node][bit] = len(trie) - 1
            node = trie[node][bit]

    best = 0
    for x in nums:
        node = 0
        cur = 0
        for b in range(bits - 1, -1, -1):
            bit = (x >> b) & 1
            want = 1 - bit
            if trie[node][want] != 0:
                cur |= (1 << b)
                node = trie[node][want]
            else:
                node = trie[node][bit]
        if cur > best:
            best = cur
    return best


def main() -> None:
    trie = Trie()
    for w in ["apple", "app", "application", "apply", "apt", "banana", "band"]:
        trie.insert(w)

    print("=== Trie ===")
    print("search('apple')     :", trie.search("apple"))    # True
    print("search('app')       :", trie.search("app"))      # True
    print("search('ap')        :", trie.search("ap"))       # False
    print("starts_with('app')  :", trie.starts_with("app")) # True
    print("starts_with('xyz')  :", trie.starts_with("xyz")) # False

    print("\nautocomplete('app'):", sorted(trie.autocomplete("app")))
    print("autocomplete('ban'):", sorted(trie.autocomplete("ban")))
    print("autocomplete('z')  :", trie.autocomplete("z"))

    trie.delete("app")
    print("\nAfter deleting 'app':")
    print("search('app')   :", trie.search("app"))     # False
    print("search('apple') :", trie.search("apple"))   # True

    print("\n=== Maximum XOR ===")
    print("max_xor([3,10,5,25,2,8]) =", max_xor([3, 10, 5, 25, 2, 8]))  # 28
    print("max_xor([0,1,2])         =", max_xor([0, 1, 2]))             # 3


if __name__ == "__main__":
    main()
