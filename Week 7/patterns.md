# Week 7 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which string pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given a string of length up to 10^5, decide whether it is a palindrome, ignoring case and non-alphanumeric characters.
Pattern: ______
Why: ______

### 2. Given two strings `s` and `t` of length up to 10^5, decide whether `t` is an anagram of `s`.
Pattern: ______
Why: ______

### 3. Given a text `T` of length n ≤ 10^4 and a pattern `P` of length m ≤ 100, find all occurrences of `P` in `T`. Naïve O(nm) is acceptable.
Pattern: ______
Why: ______

### 4. Given a string, find the length of the longest substring without repeating characters. Length up to 10^5.
Pattern: ______
Why: ______

### 5. Given a string, find the longest palindromic substring. Length up to 10^3 (so O(n^2) is fine).
Pattern: ______
Why: ______

### 6. Given a string of parentheses `()[]{}`, decide if it is balanced. Length up to 10^5.
Pattern: ______
Why: ______

### 7. Distractor: Given two strings `s` and `t` of length up to 10^6, decide whether `t` occurs in `s`. (Naïve is too slow — what now?)
Pattern: ______
Why: ______

### 8. Given a string, count the number of distinct characters. Input ASCII only.
Pattern: ______
Why: ______

### 9. Given a string of words separated by single spaces, reverse the order of words. In place if possible. Length up to 10^5.
Pattern: ______
Why: ______

### 10. Given a string, return the first non-repeating character. Length up to 10^5.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Two pointers (left/right converging). **Why**: skip non-alphanumeric, compare lowercase — O(n).
2. **Pattern**: Frequency count (array[26] or hashmap). **Why**: anagrams have identical character multisets.
3. **Pattern**: Naïve substring search. **Why**: small `m` means O(nm) ≈ 10^6 is fine; KMP overkill here.
4. **Pattern**: Sliding window with last-seen map. **Why**: expand right, jump `left` past previous occurrence — O(n).
5. **Pattern**: Expand-around-center. **Why**: every palindrome has a center; try 2n−1 centers, expand outward — O(n^2).
6. **Pattern**: Stack of openers. **Why**: each closer must match the top — Week 12 preview, but a string drill at heart.
7. **Pattern**: KMP or Z-algorithm or Rabin-Karp (Week 25 territory). **Why**: lengths 10^6 force linear-time exact matching; this is the distractor that hints at advanced string algorithms.
8. **Pattern**: Boolean array of size 128 or HashSet. **Why**: O(n) with O(1) (alphabet-size) space.
9. **Pattern**: Reverse whole string, then reverse each word (or split and reverse list). **Why**: two-pass in-place trick mirrors the rotate-array idea.
10. **Pattern**: Two-pass frequency count. **Why**: count chars first, then scan again returning first with count 1.

</details>
