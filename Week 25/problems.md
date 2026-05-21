# Week 25 — Practice Problems

Topics covered this week: advanced string algorithms — KMP, Z-algorithm, Rabin-Karp, Manacher's, suffix arrays.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Find the Index of the First Occurrence in a String | Easy | KMP / naive | https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/ | Amazon, Microsoft, Apple |
| 2 | Repeated Substring Pattern | Easy | KMP failure function | https://leetcode.com/problems/repeated-substring-pattern/ | Amazon, Google, Common |
| 3 | Rotate String | Easy | Concatenation trick | https://leetcode.com/problems/rotate-string/ | Amazon, Google, Common |
| 4 | Longest Happy Prefix | Hard | KMP failure | https://leetcode.com/problems/longest-happy-prefix/ | Google, Common |
| 5 | Shortest Palindrome | Hard | KMP on reversed concat | https://leetcode.com/problems/shortest-palindrome/ | Google, Pocket Gems, Common |
| 6 | Longest Palindromic Substring | Medium | Expand around center / Manacher | https://leetcode.com/problems/longest-palindromic-substring/ | Amazon, Microsoft, Meta, Apple |
| 7 | Palindromic Substrings | Medium | Expand around center | https://leetcode.com/problems/palindromic-substrings/ | Meta, Amazon, Google |
| 8 | Distinct Echo Substrings | Hard | Rabin-Karp | https://leetcode.com/problems/distinct-echo-substrings/ | Common |
| 9 | Longest Duplicate Substring | Hard | Binary search + Rabin-Karp | https://leetcode.com/problems/longest-duplicate-substring/ | Google, Amazon, Common |
| 10 | Sum of Scores of Built Strings | Hard | Z-function | https://leetcode.com/problems/sum-of-scores-of-built-strings/ | Common |
| 11 | Find All Anagrams in a String | Medium | Sliding window | https://leetcode.com/problems/find-all-anagrams-in-a-string/ | Amazon, Meta, Google |

## Stretch Problems

Bonus problems for deeper practice:

- [Strong Password Checker](https://leetcode.com/problems/strong-password-checker/) — tricky string casework.
- [Number of Distinct Substrings in a String](https://leetcode.com/problems/distinct-substrings/) — suffix array / trie.
- [Smallest String With Swaps](https://leetcode.com/problems/smallest-string-with-swaps/) — UF + sorted groups.

## Patterns to Master This Week

- KMP failure (`lps`) array: longest proper prefix that is also suffix; pattern match in O(n+m). Pitfall: building `lps` correctly — re-read carefully.
- Rabin-Karp rolling hash: O(n+m) average, but worst case is O(nm) on hash collisions. Pitfall: pick two prime moduli to avoid hash attacks.
- Manacher's algorithm: O(n) palindrome lengths via mirror property. Pitfall: insert separators (`#`) to unify odd/even cases.
