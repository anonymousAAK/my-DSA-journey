# Week 25 — Practice Problems

Topics covered this week: advanced string algorithms — KMP, Z-algorithm, Rabin-Karp, Manacher's, suffix arrays.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Find the Index of the First Occurrence in a String | Easy | KMP / naive | https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/ |
| 2 | Repeated Substring Pattern | Easy | KMP failure function | https://leetcode.com/problems/repeated-substring-pattern/ |
| 3 | Rotate String | Easy | Concatenation trick | https://leetcode.com/problems/rotate-string/ |
| 4 | Longest Happy Prefix | Hard | KMP failure | https://leetcode.com/problems/longest-happy-prefix/ |
| 5 | Shortest Palindrome | Hard | KMP on reversed concat | https://leetcode.com/problems/shortest-palindrome/ |
| 6 | Longest Palindromic Substring | Medium | Expand around center / Manacher | https://leetcode.com/problems/longest-palindromic-substring/ |
| 7 | Palindromic Substrings | Medium | Expand around center | https://leetcode.com/problems/palindromic-substrings/ |
| 8 | Distinct Echo Substrings | Hard | Rabin-Karp | https://leetcode.com/problems/distinct-echo-substrings/ |
| 9 | Longest Duplicate Substring | Hard | Binary search + Rabin-Karp | https://leetcode.com/problems/longest-duplicate-substring/ |
| 10 | Sum of Scores of Built Strings | Hard | Z-function | https://leetcode.com/problems/sum-of-scores-of-built-strings/ |
| 11 | Find All Anagrams in a String | Medium | Sliding window | https://leetcode.com/problems/find-all-anagrams-in-a-string/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Strong Password Checker](https://leetcode.com/problems/strong-password-checker/) — tricky string casework.
- [Number of Distinct Substrings in a String](https://leetcode.com/problems/distinct-substrings/) — suffix array / trie.
- [Smallest String With Swaps](https://leetcode.com/problems/smallest-string-with-swaps/) — UF + sorted groups.

## Patterns to Master This Week

- KMP failure (`lps`) array: longest proper prefix that is also suffix; pattern match in O(n+m). Pitfall: building `lps` correctly — re-read carefully.
- Rabin-Karp rolling hash: O(n+m) average, but worst case is O(nm) on hash collisions. Pitfall: pick two prime moduli to avoid hash attacks.
- Manacher's algorithm: O(n) palindrome lengths via mirror property. Pitfall: insert separators (`#`) to unify odd/even cases.
