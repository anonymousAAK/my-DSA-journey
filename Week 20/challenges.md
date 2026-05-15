# Week 20 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Sudoku Solver With Bitmask Pruning

**Spec**:
Read a 9x9 Sudoku grid (`.` for empty). Solve and print the completed grid. Use backtracking with three bitmasks (`rows[9]`, `cols[9]`, `boxes[9]`) so that "is digit d valid at (r,c)" is an O(1) bit check, not an O(9) scan. Always pick the empty cell with the **fewest legal candidates** to branch on (MRV heuristic).

**Constraints**:
- Single 9x9 puzzle, guaranteed solvable
- Time: well under 100 ms for hard puzzles
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| classic "world's hardest Sudoku" | completed grid |
| empty grid (all `.`) | any valid completion |
| nearly-full grid (1 cell empty) | filled |

**Stretch**: Solve N-Queens for `N` up to 14 using bitmasks for column/diagonal occupancy and count all solutions.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Word Break II — Return All Sentences

**Spec**:
Read a string `s` and a dictionary of words. Return all possible sentences (space-separated) that segment `s` into dictionary words. Each word may be reused. Use backtracking + memoization on suffix start indices (DP map from index → list of sentences). Pruning: precompute for each index whether *any* segmentation exists, to avoid exploring dead ends.

**Constraints**:
- `|s| <= 100`, dictionary up to 1000 words
- Time: worst-case exponential in number of segmentations, but with memoization much better in practice
- Memory: O(|s| * number of sentences)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `s=catsanddog dict=cat cats and sand dog` | `cat sand dog`, `cats and dog` |
| `s=pineapplepenapple dict=apple pen applepen pine pineapple` | 3 sentences |
| `s=catsandog dict=cats dog sand and cat` | (empty list) |
| `s=a dict=a` | `a` |

**Stretch**: Output only the *shortest* (fewest-word) sentence; ties broken lexicographically.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Permutations With Duplicates

**Spec**:
Read `n` and `n` integers (may have duplicates). Print all distinct permutations exactly once. Use backtracking with this trick: sort the input, then in the recursive step skip choosing a duplicate at the same level (`if i > 0 && a[i] == a[i-1] && !used[i-1] continue`).

**Constraints**:
- `1 <= n <= 8`
- Time: O(n! * n) worst case
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=3 / 1 1 2` | `1 1 2`, `1 2 1`, `2 1 1` |
| `n=3 / 1 2 3` | `6` permutations |
| `n=4 / 1 1 2 2` | `6` distinct permutations |
| `n=1 / 7` | `7` |

**Stretch**: Same but as a generator that yields the next permutation in lex order (use `std::next_permutation`-style algorithm — without library help).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Hamiltonian Path Existence (Backtracking + Pruning)

**Spec**:
Read an undirected graph (n up to 20). Determine whether a Hamiltonian path (visits every vertex exactly once) exists. Print `YES` and a path if so, else `NO`. Use backtracking with pruning: connectivity check at each step, degree check, and Warnsdorff-style heuristic for ordering neighbor exploration.

**Constraints**:
- `1 <= n <= 20`, `m <= n*(n-1)/2`
- Time: exponential worst case, fast for sparse graphs
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=4 edges=(1,2)(2,3)(3,4)(4,1)` (cycle) | `YES`, e.g. `1 2 3 4` |
| `n=3 edges=(1,2)` | `NO` |
| `n=5 K_5 (complete)` | `YES` |
| `n=4 edges=(1,2)(3,4)` | `NO` |

**Stretch**: Find a Hamiltonian *cycle* (returns to start). Solve via Held–Karp DP in O(2^n * n^2) for `n <= 20`.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: Generate All Valid Parentheses Combinations

**Spec**:
Read `n`. Print all distinct strings of `n` pairs of matched parentheses (so length `2n`). Use backtracking constrained by two counters: `open < n` allows adding `(`; `close < open` allows adding `)`. Print in lex order.

**Constraints**:
- `0 <= n <= 12` (Catalan number explosion)
- Time: O(C_n * n) where `C_n` is the n-th Catalan number
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=0` | (single empty string) |
| `n=1` | `()` |
| `n=2` | `(())`, `()()` |
| `n=3` | `((()))`, `(()())`, `(())()`, `()(())`, `()()()` |

**Stretch**: Two kinds of brackets `()` and `[]`. Generate all balanced strings of length `2n`.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
