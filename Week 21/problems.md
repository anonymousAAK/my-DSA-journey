# Week 21 — Practice Problems

Topics covered this week: segment trees, Fenwick (BIT) trees, range queries, point/range updates, tries (prefix trees).

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Range Sum Query - Mutable | Medium | Segment tree / BIT | https://leetcode.com/problems/range-sum-query-mutable/ | Amazon, Google, Common |
| 2 | Count of Smaller Numbers After Self | Hard | BIT / merge sort | https://leetcode.com/problems/count-of-smaller-numbers-after-self/ | Amazon, Google, Microsoft |
| 3 | Range Sum Query 2D - Mutable | Hard | 2D BIT | https://leetcode.com/problems/range-sum-query-2d-mutable/ | Common |
| 4 | Implement Trie (Prefix Tree) | Medium | Trie basics | https://leetcode.com/problems/implement-trie-prefix-tree/ | Amazon, Google, Microsoft, Meta |
| 5 | Design Add and Search Words Data Structure | Medium | Trie with wildcards | https://leetcode.com/problems/design-add-and-search-words-data-structure/ | Amazon, Meta, Google |
| 6 | Word Search II | Hard | Trie + backtracking | https://leetcode.com/problems/word-search-ii/ | Amazon, Meta, Microsoft, Google |
| 7 | Maximum XOR of Two Numbers in an Array | Medium | Binary trie | https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/ | Common |
| 8 | Replace Words | Medium | Trie root match | https://leetcode.com/problems/replace-words/ | Common |
| 9 | Longest Word in Dictionary | Medium | Trie / sort | https://leetcode.com/problems/longest-word-in-dictionary/ | Common |
| 10 | Map Sum Pairs | Medium | Trie with sum | https://leetcode.com/problems/map-sum-pairs/ | Common |
| 11 | The Skyline Problem | Hard | Segment tree / heap | https://leetcode.com/problems/the-skyline-problem/ | Amazon, Meta, Google, Microsoft |

## Stretch Problems

Bonus problems for deeper practice:

- [Range Module](https://leetcode.com/problems/range-module/) — interval segment tree.
- [Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) — BIT or merge-sort.
- [Stream of Characters](https://leetcode.com/problems/stream-of-characters/) — reversed trie for streaming match.

## Patterns to Master This Week

- Segment tree: recursive build + range query with lazy propagation when needed. Pitfall: index 1-based vs 0-based confusion.
- BIT (Fenwick): use `i += i & -i` to walk parents in O(log n). Pitfall: BIT supports prefix queries; range = prefix(r) - prefix(l-1).
- Trie node = `Node[26]` (or HashMap) + terminal flag. Pitfall: forgetting to mark end-of-word leads to false positives.
