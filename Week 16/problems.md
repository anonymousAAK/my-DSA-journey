# Week 16 — Practice Problems

Topics covered this week: hashing, HashMap/HashSet, frequency counting, prefix-sum + map, collision concepts.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Two Sum | Easy | Hash map lookup | https://leetcode.com/problems/two-sum/ | Google, Amazon, Meta, Apple |
| 2 | Group Anagrams | Medium | Hashing keys | https://leetcode.com/problems/group-anagrams/ | Amazon, Meta, Microsoft, Uber |
| 3 | Subarray Sum Equals K | Medium | Prefix sum + map | https://leetcode.com/problems/subarray-sum-equals-k/ | Meta, Amazon, Google, Microsoft |
| 4 | Longest Consecutive Sequence | Medium | Hash set | https://leetcode.com/problems/longest-consecutive-sequence/ | Amazon, Meta, Google |
| 5 | Happy Number | Easy | Set-based cycle detection | https://leetcode.com/problems/happy-number/ | Google, Amazon, Microsoft |
| 6 | Intersection of Two Arrays | Easy | Set intersect | https://leetcode.com/problems/intersection-of-two-arrays/ | Common |
| 7 | Intersection of Two Arrays II | Easy | Multiset / count map | https://leetcode.com/problems/intersection-of-two-arrays-ii/ | Common |
| 8 | Isomorphic Strings | Easy | Two-way map | https://leetcode.com/problems/isomorphic-strings/ | Common |
| 9 | First Unique Character in a String | Easy | Frequency map | https://leetcode.com/problems/first-unique-character-in-a-string/ | Amazon, Meta, Microsoft, Bloomberg |
| 10 | LRU Cache | Medium | Hash + DLL | https://leetcode.com/problems/lru-cache/ | Amazon, Meta, Microsoft, Google, Apple |
| 11 | 4Sum II | Medium | Pair-sum hashing | https://leetcode.com/problems/4sum-ii/ | Amazon, Google, Common |
| 12 | Contiguous Array | Medium | Prefix counts | https://leetcode.com/problems/contiguous-array/ | Meta, Amazon, Google |

## Stretch Problems

Bonus problems for deeper practice:

- [Design HashMap](https://leetcode.com/problems/design-hashmap/) — implement from scratch.
- [Design HashSet](https://leetcode.com/problems/design-hashset/) — same exercise, simpler.
- [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) — map + array combo.

## Patterns to Master This Week

- "Seen-before" map: store value→index/count to enable O(1) lookup. Pitfall: collisions when keys can repeat; use list buckets.
- Prefix sum + map: complement key is `prefix - k`. Pitfall: seed the map with `(0, 1)` to capture subarrays starting at 0.
- Hashable canonical form (e.g., sorted string for anagram): O(L log L) per key. Pitfall: prefer 26-count tuple for speed.
