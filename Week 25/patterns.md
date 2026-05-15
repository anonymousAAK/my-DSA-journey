# Week 25 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which string algorithm applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given a text `T` (length 10^6) and a pattern `P` (length 10^5), find all occurrences of `P` in `T` in linear total time.
Pattern: ______
Why: ______

### 2. Given a string `S` of length 10^6, for each prefix find the longest proper prefix that is also a suffix of that prefix.
Pattern: ______
Why: ______

### 3. Given a string `S` of length 10^6, compute for every position `i` the length of the longest substring starting at `i` that matches a prefix of `S`.
Pattern: ______
Why: ______

### 4. Given a text `T` and `k` patterns of total length 10^5, find all occurrences of any pattern in `T` (length 10^6) in linear time.
Pattern: ______
Why: ______

### 5. Given two strings of equal length n, decide whether one is a rotation of the other in O(n).
Pattern: ______
Why: ______

### 6. Given a string of length 10^6, compute the length of the longest palindromic substring in linear time.
Pattern: ______
Why: ______

### 7. Distractor: Given a short text (length 100) and a short pattern (length 10), find all occurrences. (KMP?)
Pattern: ______
Why: ______

### 8. Given a stream of incoming characters, maintain a rolling fingerprint that can detect when the last `m` characters match a known pattern.
Pattern: ______
Why: ______

### 9. Given a string and many queries asking "is `S[i..j]` a palindrome?", answer each in O(1) after O(n) preprocessing.
Pattern: ______
Why: ______

### 10. Given a string, count the number of distinct substrings. n ≤ 10^5.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: KMP. **Why**: failure function precompute lets the search never backtrack — O(n+m).
2. **Pattern**: KMP failure function (`pi[]`). **Why**: that's literally the definition.
3. **Pattern**: Z-algorithm. **Why**: Z[i] = LCP(S, S[i..]) — linear.
4. **Pattern**: Aho–Corasick automaton. **Why**: multi-pattern KMP — trie + failure links.
5. **Pattern**: Concatenate `S+S` and search for the other string with KMP. **Why**: every rotation is a substring of `S+S`.
6. **Pattern**: Manacher's algorithm. **Why**: linear-time longest palindromic substring via mirror-based expansion.
7. **Pattern**: Distractor — naïve substring match is fine. **Why**: O(n·m) ≈ 1000; KMP is correct but overkill.
8. **Pattern**: Rabin–Karp rolling hash. **Why**: O(1) hash update per character with polynomial hash.
9. **Pattern**: Manacher precompute + array indexing. **Why**: store palindrome radii at each center; query is a constant-time lookup.
10. **Pattern**: Suffix automaton / suffix array + LCP. **Why**: count = Σ (len − lcp) — advanced string structures.

</details>
