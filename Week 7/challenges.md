# Week 7 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Longest Palindromic Substring in O(n) — Manacher's

**Spec**:
Read a string `s`. Print the longest palindromic substring (any if ties). Required complexity is O(n). The naive O(n^2) "expand around center" approach is forbidden — use Manacher's algorithm.

**Constraints**:
- Input size: `1 <= |s| <= 10^6`, ASCII characters
- Time: O(n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `babad` | `bab` or `aba` |
| `cbbd` | `bb` |
| `a` | `a` |
| `forgeeksskeegfor` | `geeksskeeg` |
| `abacdfgdcaba` | `aba` (note: full string not a palindrome) |

**Stretch**: Count the total number of distinct palindromic substrings using an eertree (palindromic tree).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: All Anagram Group Indices

**Spec**:
Read a text `t` and a pattern `p`. Print all starting indices in `t` where some anagram of `p` occurs as a substring. Use a sliding window of size `|p|` with a fixed-size count array — do not re-sort or re-hash the window every step.

**Constraints**:
- Input size: `1 <= |p| <= |t| <= 10^6`, lowercase ASCII
- Time: O(|t| + |p|)
- Memory: O(1) (only 26 counters)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `t=cbaebabacd p=abc` | `0 6` |
| `t=abab p=ab` | `0 1 2` |
| `t=aaaaaa p=aa` | `0 1 2 3 4` |
| `t=hello p=xyz` | (empty) |

**Stretch**: Now `|p|` can vary per query and you have `q` queries on the same `t`. Preprocess `t` so each query runs in O(|p| + answers).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: KMP With Multiple Patterns at Once

**Spec**:
Read a text `t` followed by `k` patterns `p_1..p_k`. For each pattern, print on one line: the pattern, a colon, and a space-separated list of all starting indices where it occurs in `t`. You may not run KMP separately `k` times — implement Aho–Corasick (a multi-pattern generalization that builds a trie + failure links analogous to KMP's failure function).

**Constraints**:
- Input size: `|t| <= 10^6`, total pattern length `<= 10^5`, `k <= 10^4`
- Time: O(|t| + total pattern length + total occurrences)
- Memory: O(total pattern length)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `t=ahishers / he, she, his, hers` | `he: 1 4` / `she: 3` / `his: 1` / `hers: 4` |
| `t=aaaa / aa, aaa` | `aa: 0 1 2` / `aaa: 0 1` |

**Stretch**: Build the automaton so that a single linear scan of `t` reports every match for every pattern in true linear total time (use dictionary suffix links).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Smallest String Rotation

**Spec**:
Read a string `s`. Print its lexicographically smallest rotation. Required: Booth's algorithm in O(n) (or duplicate `s` to `s+s` and run Lyndon decomposition — also O(n)). The O(n^2) naive approach of generating all rotations and sorting is forbidden.

**Constraints**:
- Input size: `1 <= |s| <= 10^6`
- Time: O(n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `bca` | `abc` |
| `cba` | `acb` |
| `aaa` | `aaa` |
| `bbaa` | `aabb` |
| `baabaa` | `aabaab` |

**Stretch**: Also print the starting index in the original string at which the smallest rotation begins.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
