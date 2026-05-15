# Week 25 — Hard Mode Challenges (Boss Level)

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Longest Periodic Substring

**Spec**:
Read a string `s`. A string is `k`-periodic if it equals `t` repeated `k` times for some `t` and `k >= 2`. Find the longest substring of `s` that is `k`-periodic for some `k >= 2`. Print its length and one starting index. Required: use the KMP failure function on each suffix (or Z-algorithm) cleverly, achieving O(n^2) or better.

**Constraints**:
- `1 <= |s| <= 10^4`
- Time: O(n^2)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `aababab` | length `6`, substring `ababab` |
| `abcabc` | length `6`, substring `abcabc` |
| `aaaa` | length `4`, substring `aaaa` |
| `abc` | length `0` (no periodic substring with k >= 2) |

**Stretch**: Find the substring whose period is "most periodic" by some metric (largest `k`).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Suffix Array Construction in O(n log n)

**Spec**:
Read a string `s`. Build its suffix array (sorted starting indices of all suffixes) in O(n log n) using doubling + radix/counting sort. The O(n log^2 n) sort-with-comparator approach is acceptable for partial credit. Print the array.

**Constraints**:
- `1 <= |s| <= 10^6`
- Time: O(n log n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `banana` | `5 3 1 0 4 2` (suffixes a, ana, anana, banana, na, nana) |
| `abracadabra` | suffix array of length 11 |
| `aaaa` | `3 2 1 0` |
| `a` | `0` |

**Stretch**: Build the LCP array (longest common prefix between consecutive suffixes) in O(n) using Kasai's algorithm.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Longest Common Substring of Two Strings via Generalized SA

**Spec**:
Read two strings `a` and `b`. Find their longest common substring. Required: build a generalized suffix array (or suffix automaton) of `a + '#' + b + '$'` and look for adjacent suffixes in the SA that come from different sources, maximizing LCP. O(n log n) where `n = |a| + |b|`.

**Constraints**:
- `1 <= |a|, |b| <= 10^5`
- Time: O(n log n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `a=abcdxyz b=xyzabcd` | length `4`, `abcd` (or `xyz`) — pick the longest; if tie, either valid |
| `a=hello b=world` | length `1`, `l` or `o` |
| `a=same b=same` | length `4`, `same` |
| `a=abc b=xyz` | length `0` |

**Stretch**: Longest common substring of *k* strings (extra source markers).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Rabin–Karp Multi-Pattern With Rolling Hash Collisions Handled

**Spec**:
Implement Rabin–Karp to find all occurrences of `k` patterns (all same length `m`) in a text `t`. Use polynomial rolling hash with TWO different moduli (double hashing) to minimize collisions. On hash match, verify the substring char-by-char (because hashes can lie).

**Constraints**:
- `|t| <= 10^6`, `k <= 10^5`, all patterns same length `m <= 100`
- Time: O((|t| + k) + total occurrences * m)
- Memory: O(k)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `t=ababab patterns=ab ba` | `ab: 0 2 4 / ba: 1 3` |
| `t=aaaa patterns=aa` | `aa: 0 1 2` |
| `t=mississippi patterns=iss ssi` | `iss: 1 4 / ssi: 2 5` |

**Stretch**: Patterns of *different* lengths — group by length and run one R–K pass per length group.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: Palindromic Tree (Eertree)

**Spec**:
Build the palindromic tree for string `s` and output:
- The number of distinct palindromic substrings of `s`.
- The longest palindromic substring.
- For each position `i`, the number of palindromes ending at `i`.

Eertree construction: each node represents a distinct palindrome; suffix links point to the longest proper palindromic suffix.

**Constraints**:
- `1 <= |s| <= 10^6`
- Time: O(n * alphabet) or O(n log alphabet)
- Memory: O(n)

**Test inputs**:
| Input | Distinct palindromic substrings | Longest |
|-------|---------------------------------|---------|
| `aaaa` | `4` (a, aa, aaa, aaaa) | `aaaa` |
| `abba` | `4` (a, b, bb, abba) | `abba` |
| `abcbab` | `5` (a, b, c, bcb, bab) | `bcb` (length 3) |
| `a` | `1` | `a` |

**Stretch**: Count palindromic *subsequences* (different problem; classic O(n^2) DP).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
