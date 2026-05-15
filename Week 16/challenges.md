# Week 16 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Custom Open-Addressing HashMap

**Spec**:
Implement a hashmap from scratch using **open addressing with linear probing** (or quadratic — pick one). No `HashMap` library. Support `put`, `get`, `remove`. Use a tombstone marker for deletions. Resize (double + rehash) when load factor exceeds 0.7. Implement your own hash function for integer or string keys.

**Constraints**:
- Up to `10^6` ops
- Time: O(1) amortized per op
- Memory: O(capacity)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `put a 1 / put b 2 / get a / get c / remove a / get a / put a 3 / get a` | `1 -1 -1 3` |
| 1M inserts of distinct keys then 1M lookups | all hits, no false misses |
| `put a 1 / put a 2 / get a` | `2` (overwrite) |

**Stretch**: Implement with Robin Hood hashing — track probe distances and rebalance. Compare collision behavior.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Longest Consecutive Sequence

**Spec**:
Read `n` and `n` integers. Find the length of the longest sequence of consecutive integers (in value, not position) that appear in the array. Required complexity O(n) average — use a hashset. The O(n log n) sort approach is forbidden.

Trick: only start counting from values whose `v-1` is NOT in the set (so each sequence is counted exactly once).

**Constraints**:
- `1 <= n <= 10^6`, values in `[-10^9, 10^9]`
- Time: O(n) expected
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=6 / 100 4 200 1 3 2` | `4` (1,2,3,4) |
| `n=1 / 5` | `1` |
| `n=0 / (empty)` | `0` |
| `n=9 / 0 3 7 2 5 8 4 6 0` | `9` (0..8) |

**Stretch**: Also output the actual range `[lo, hi]` of the longest run.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Subarray Sum Equals K

**Spec**:
Read `n`, `k`, and `n` integers (may be negative). Count the number of contiguous subarrays whose sum equals `k`. Required O(n) using a hashmap of prefix-sum counts: at each index, if `(prefix - k)` has been seen `c` times, add `c` to the answer.

**Constraints**:
- `1 <= n <= 10^6`, values in `[-10^4, 10^4]`, `k` in `[-10^9, 10^9]`
- Time: O(n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=4 k=2 / 1 1 1 1` | `3` |
| `n=2 k=3 / 1 2` | `1` |
| `n=6 k=0 / 1 -1 1 -1 1 -1` | `9` |
| `n=5 k=7 / 1 2 3 4 5` | `1` |

**Stretch**: Subarray sum **divisible by k** (different trick: bucket by `prefix mod k`).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Group Anagrams With Custom Key Encoding

**Spec**:
Read `n` strings. Group anagrams together and print each group on one line (any order within group, any order across groups). Required O(N L) where N = number of strings and L = max string length, **not** O(N L log L). Don't sort each string; use a fixed-size 26-character count array as the group key, encoded as a string.

**Constraints**:
- `1 <= n <= 10^5`, total length `<= 10^7`
- Time: O(N L)
- Memory: O(N L)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `eat tea tan ate nat bat` | `[eat tea ate] [tan nat] [bat]` |
| `(empty)` | `(empty)` |
| `a` | `[a]` |
| `abc cba xyz` | `[abc cba] [xyz]` |

**Stretch**: Same problem but unicode strings (variable byte length per character).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: Two Sum — All Distinct Pairs

**Spec**:
Read `n`, `target`, and `n` integers (may include duplicates). Print all **distinct** pairs `(a, b)` with `a <= b` and `a + b == target`. Each value pair appears at most once in the output. Required O(n) using a hashmap of counts.

**Constraints**:
- `1 <= n <= 10^6`
- Time: O(n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=8 target=6 / 1 5 7 -1 5 2 4 3` | `(1,5) (-1,7) (2,4) (3,3) no — 3 only appears once → (3,3) excluded` |
| `n=5 target=4 / 2 2 2 2 2` | `(2,2)` |
| `n=3 target=10 / 1 2 3` | (empty) |
| `n=4 target=0 / -1 1 -1 1` | `(-1,1)` |

**Stretch**: Three-sum: all distinct triples `(a, b, c)` with `a + b + c == target` in O(n^2).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
