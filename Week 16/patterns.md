# Week 16 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which hashing pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given an unsorted array of n ≤ 10^5 integers and a target sum `T`, return indices of two distinct elements summing to `T`.
Pattern: ______
Why: ______

### 2. Given an array, find the length of the longest sequence of consecutive integers (in value, regardless of order). n ≤ 10^5.
Pattern: ______
Why: ______

### 3. Group a list of strings by anagram class. n ≤ 10^4, each string length ≤ 100.
Pattern: ______
Why: ______

### 4. Given an array and integer k, count the number of contiguous subarrays whose sum equals k. n ≤ 10^5.
Pattern: ______
Why: ______

### 5. Given a list of (key, timestamp, value) update events and queries `(key, t)`, return the value of `key` as of time `t`. 10^5 of each.
Pattern: ______
Why: ______

### 6. Distractor: Given a *sorted* array and a target sum, find a pair summing to T. (Should you use a hash set?)
Pattern: ______
Why: ______

### 7. Given a stream of (userId, timestamp) login events, report the number of distinct users that logged in during any 10-minute window.
Pattern: ______
Why: ______

### 8. Given a list of `[from, to]` ticket pairs, reconstruct the itinerary that uses every ticket exactly once. (Distractor flavor.)
Pattern: ______
Why: ______

### 9. Given a string and a fixed pattern, find all anagrams of the pattern occurring in the string. Lengths up to 10^5 and 100.
Pattern: ______
Why: ______

### 10. Given a list of n integers possibly containing duplicates, decide whether any value appears more than once. n ≤ 10^6.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: HashMap of `value → index`. **Why**: for each x, look up `T-x` — O(n).
2. **Pattern**: HashSet membership + start-of-run check. **Why**: only start counting at values without `v-1` in the set; walk forward.
3. **Pattern**: HashMap keyed on sorted-string (or char-count tuple). **Why**: anagrams share canonical key.
4. **Pattern**: Prefix sum + HashMap of `prefix → count`. **Why**: subarray sum = k ↔ `P[j] - P[i] = k`; count matching `P[i]` values.
5. **Pattern**: HashMap of key → sorted timestamp list, binary search per query. **Why**: hash for grouping, binary search inside the time series.
6. **Pattern**: Distractor — two pointers (Week 6/8). **Why**: sorted input makes two pointers O(n) with O(1) space; hashing is unnecessary.
7. **Pattern**: HashMap of userId → last-login + sliding count. **Why**: skip stale entries; cardinality of active map is the answer.
8. **Pattern**: Hierholzer's algorithm — Eulerian path (Week 17). **Why**: hash structure stores adjacency, but the *algorithm* is graph-based, not pure hashing.
9. **Pattern**: Sliding window of size m + frequency comparison (array[26]). **Why**: maintain rolling count, compare against pattern's count.
10. **Pattern**: HashSet of seen values. **Why**: classic O(n) duplicate detection.

</details>
