# Week 7 — Practice Problems

Topics covered this week: strings, StringBuilder, character arrays, palindrome/anagram checks, substring search, common prefix.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Valid Palindrome | Easy | Two pointers | https://leetcode.com/problems/valid-palindrome/ |
| 2 | Valid Anagram | Easy | Counting | https://leetcode.com/problems/valid-anagram/ |
| 3 | Longest Common Prefix | Easy | Vertical scan | https://leetcode.com/problems/longest-common-prefix/ |
| 4 | Implement strStr() | Easy | Substring search | https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/ |
| 5 | Reverse Words in a String | Medium | Tokenize / reverse | https://leetcode.com/problems/reverse-words-in-a-string/ |
| 6 | Group Anagrams | Medium | Hashing keys | https://leetcode.com/problems/group-anagrams/ |
| 7 | Longest Palindromic Substring | Medium | Expand around center | https://leetcode.com/problems/longest-palindromic-substring/ |
| 8 | Valid Parentheses | Easy | Stack basics | https://leetcode.com/problems/valid-parentheses/ |
| 9 | Roman to Integer | Easy | Lookup + scan | https://leetcode.com/problems/roman-to-integer/ |
| 10 | String to Integer (atoi) | Medium | Careful parsing | https://leetcode.com/problems/string-to-integer-atoi/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Repeated String Match](https://leetcode.com/problems/repeated-string-match/) — bridges to KMP later.
- [Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/) — length-prefix framing.
- [Decode Ways](https://leetcode.com/problems/decode-ways/) — preview of string DP.

## Patterns to Master This Week

- Two-pointer palindrome: skip non-alphanumeric, lowercase compare. O(n) time. Pitfall: forgetting Unicode/locale rules.
- Anagram via 26-length count array (ASCII lowercase) — O(n) time, O(1) extra space. Pitfall: use sorting (O(n log n)) only if input has unicode/punctuation.
- StringBuilder over `+=` for repeated concatenation: avoids accidental O(n^2) string building.
