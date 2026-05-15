# Week 21 — Practice Problems

Topics covered this week: segment trees, Fenwick (BIT) trees, range queries, point/range updates, tries (prefix trees).

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Range Sum Query - Mutable | Medium | Segment tree / BIT | https://leetcode.com/problems/range-sum-query-mutable/ |
| 2 | Count of Smaller Numbers After Self | Hard | BIT / merge sort | https://leetcode.com/problems/count-of-smaller-numbers-after-self/ |
| 3 | Range Sum Query 2D - Mutable | Hard | 2D BIT | https://leetcode.com/problems/range-sum-query-2d-mutable/ |
| 4 | Implement Trie (Prefix Tree) | Medium | Trie basics | https://leetcode.com/problems/implement-trie-prefix-tree/ |
| 5 | Design Add and Search Words Data Structure | Medium | Trie with wildcards | https://leetcode.com/problems/design-add-and-search-words-data-structure/ |
| 6 | Word Search II | Hard | Trie + backtracking | https://leetcode.com/problems/word-search-ii/ |
| 7 | Maximum XOR of Two Numbers in an Array | Medium | Binary trie | https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/ |
| 8 | Replace Words | Medium | Trie root match | https://leetcode.com/problems/replace-words/ |
| 9 | Longest Word in Dictionary | Medium | Trie / sort | https://leetcode.com/problems/longest-word-in-dictionary/ |
| 10 | Map Sum Pairs | Medium | Trie with sum | https://leetcode.com/problems/map-sum-pairs/ |
| 11 | The Skyline Problem | Hard | Segment tree / heap | https://leetcode.com/problems/the-skyline-problem/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Range Module](https://leetcode.com/problems/range-module/) — interval segment tree.
- [Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) — BIT or merge-sort.
- [Stream of Characters](https://leetcode.com/problems/stream-of-characters/) — reversed trie for streaming match.

## Patterns to Master This Week

- Segment tree: recursive build + range query with lazy propagation when needed. Pitfall: index 1-based vs 0-based confusion.
- BIT (Fenwick): use `i += i & -i` to walk parents in O(log n). Pitfall: BIT supports prefix queries; range = prefix(r) - prefix(l-1).
- Trie node = `Node[26]` (or HashMap) + terminal flag. Pitfall: forgetting to mark end-of-word leads to false positives.
