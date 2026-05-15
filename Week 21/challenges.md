# Week 21 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Segment Tree With Lazy Propagation (Range Add, Range Sum)

**Spec**:
Build a segment tree over an array of size `n`. Support two operations in O(log n):
- `update l r v`: add `v` to every element in `[l, r]`.
- `query l r`: return the sum of `[l, r]`.

Use lazy propagation: a `lazy[v]` array holds pending updates to push down on traversal.

**Constraints**:
- `1 <= n, q <= 10^5`, values in `[-10^9, 10^9]`
- Time: O(log n) per op
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=5 arr=1 2 3 4 5 / query 0 4 / update 1 3 10 / query 0 4 / query 2 2` | `15 45 13` |
| `n=1 arr=7 / update 0 0 3 / query 0 0` | `10` |
| `n=4 arr=0 0 0 0 / update 0 3 5 / update 0 1 -5 / query 0 3` | `10` |

**Stretch**: Range *assignment* (not add) + range sum — needs different lazy semantics (assignment overrides additions).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Persistent Segment Tree (K-th Smallest in Range)

**Spec**:
Read an array and `q` queries `(l, r, k)`: return the k-th smallest element in subarray `a[l..r]`. Required: build a persistent segment tree indexed by value, where version `i` represents the multiset of `a[0..i]`. Each query subtracts version `l-1` from version `r` to get the multiset of `a[l..r]` and walks the tree.

**Constraints**:
- `1 <= n, q <= 10^5`
- Time: O((n + q) log n)
- Memory: O(n log n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=7 arr=1 5 2 6 3 7 4 / query (0, 6, 1) (0, 6, 4) (1, 3, 2)` | `1 4 5` |
| `n=3 arr=2 2 2 / query (0, 2, 1) (0, 2, 3)` | `2 2` |

**Stretch**: Also support a point update (set `a[i] = v`); now you need a BIT-of-segment-trees for O(log^2 n).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Trie + Maximum XOR Pair

**Spec**:
Read `n` and `n` non-negative integers (fits in 32 bits). Find the maximum value of `a[i] XOR a[j]` over all pairs `i < j`. Required: O(n * 32) using a binary trie: insert each number into the trie bit-by-bit (MSB first); for each number, walk the trie greedily choosing the opposite bit when possible.

**Constraints**:
- `1 <= n <= 10^6`
- Time: O(n * 32)
- Memory: O(n * 32)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=5 / 3 10 5 25 2` | `28` (5 XOR 25) |
| `n=1 / 7` | `0` (or undefined; pick a rule) |
| `n=2 / 0 0` | `0` |
| `n=4 / 8 1 2 12` | `13` |

**Stretch**: For each `i`, find the `j` maximizing `a[i] XOR a[j]` and output both indices.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: BIT Supporting Range Update + Range Sum (Two BITs)

**Spec**:
Implement a Binary Indexed Tree pair that supports:
- `update l r v`: add `v` to every element in `[l, r]`.
- `query l r`: sum of `[l, r]`.

In O(log n) per op using **two** BITs (the standard `B1, B2` trick): one for `v` and one for `v * (l-1)`.

**Constraints**:
- `1 <= n, q <= 10^6`
- Time: O(log n) per op
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=5 / update 1 3 2 / query 1 3 / query 0 4 / update 0 4 1 / query 0 4` | `6 6 11` |
| `n=1 / update 0 0 5 / query 0 0` | `5` |

**Stretch**: Add a `set` (assignment) operation in addition to range-add. This breaks the BIT trick; explain why and consider segment tree with lazy.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: Trie-Based Autocomplete With Top-K Suggestions

**Spec**:
Maintain a dictionary of `(word, weight)` pairs (insertable). For a query prefix `p`, return up to `k` words sharing prefix `p` with the highest weights, ties broken lexicographically.

Required: at each trie node, store a top-`k` max-heap (or sorted list) of suggestions cached. Update on insert.

**Constraints**:
- Up to `10^5` words, total length `10^6`, `k <= 10`
- Time: O(|p| + k log k) per query; O(|word| * k) per insert
- Memory: O(total length * k)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| insert `apple 5, app 4, apply 7, apricot 3 / query app 2` | `apply apple` |
| insert + query `a` for `k=3` | `apply apple app` |

**Stretch**: Support deletion of words (refresh the cached top-k along the path).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
