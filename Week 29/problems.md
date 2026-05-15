# Week 29 — Practice Problems

Topics covered this week: object-oriented system design, building data structures from scratch, designing APIs around classic DS patterns.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Design HashMap | Easy | Buckets + chaining | https://leetcode.com/problems/design-hashmap/ |
| 2 | Design HashSet | Easy | Bucket design | https://leetcode.com/problems/design-hashset/ |
| 3 | LRU Cache | Medium | HashMap + DLL | https://leetcode.com/problems/lru-cache/ |
| 4 | LFU Cache | Hard | Two-level maps | https://leetcode.com/problems/lfu-cache/ |
| 5 | Design Twitter | Medium | Feed merge + heap | https://leetcode.com/problems/design-twitter/ |
| 6 | Design Snake Game | Medium | Deque + set | https://leetcode.com/problems/design-snake-game/ |
| 7 | Design Underground System | Medium | Two maps | https://leetcode.com/problems/design-underground-system/ |
| 8 | Insert Delete GetRandom O(1) | Medium | Map + array | https://leetcode.com/problems/insert-delete-getrandom-o1/ |
| 9 | Design Tic-Tac-Toe | Medium | Row/col/diag counters | https://leetcode.com/problems/design-tic-tac-toe/ |
| 10 | Design Browser History | Medium | Stacks or doubly-linked list | https://leetcode.com/problems/design-browser-history/ |
| 11 | Design Add and Search Words Data Structure | Medium | Trie with wildcards | https://leetcode.com/problems/design-add-and-search-words-data-structure/ |
| 12 | Design Authentication Manager | Medium | Map + lazy expiry | https://leetcode.com/problems/design-authentication-manager/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Design In-Memory File System](https://leetcode.com/problems/design-in-memory-file-system/) — tree of directories.
- [Design Search Autocomplete System](https://leetcode.com/problems/design-search-autocomplete-system/) — trie + ranked top-k.
- [All O`one Data Structure](https://leetcode.com/problems/all-oone-data-structure/) — buckets of counts linked together.

## Patterns to Master This Week

- HashMap + DLL = the LRU/LFU/sliding-recency archetype. Pitfall: maintain DLL invariants on both ends; remember to update map keys when evicting.
- Compose by responsibility: one class per concept (User, Tweet, Feed). Pitfall: god-class anti-pattern; clean OO scales better.
- Lazy expiry beats eager scans for token/rate-limit/expiry tables. Pitfall: validate freshness on read paths, not via a background sweep.
