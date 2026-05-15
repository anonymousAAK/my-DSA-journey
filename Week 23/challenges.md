# Week 23 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Bitmask TSP With a Mandatory Waypoint Order

**Spec**:
Read `n`, the `n x n` distance matrix, and a sequence `p_1, p_2, ..., p_k` of waypoint indices that **must be visited in this relative order** (other cities may be visited between them, in any order). Start and end at city 0. Find the minimum-cost Hamiltonian cycle satisfying the constraint. Use bitmask DP with `dp[mask][v]` plus a per-state "next required waypoint index" counter.

**Constraints**:
- `1 <= n <= 18`, `0 <= k <= n`
- Time: O(2^n * n^2)
- Memory: O(2^n * n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=4 mandatory=(1,2,3) matrix=fully connected with cost = i+j` | minimum tour with relative order 0 -> ... -> 1 -> ... -> 2 -> ... -> 3 -> ... -> 0 |
| `n=3 mandatory=(1,2) matrix=symmetric with distinct costs` | minimum 0-1-2-0 |
| `n=1 mandatory=()` | `0` |

**Stretch**: Multiple "must-visit-before" pairs (partial order), encoded as a precedence DAG.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Digit DP — Count Numbers in Range with Property

**Spec**:
Print the count of integers in `[L, R]` whose digit sum is divisible by `m`. Required: digit DP on the decimal representation, with state `(position, sum mod m, tight)`. Compute `f(R) - f(L-1)`.

**Constraints**:
- `1 <= L <= R <= 10^18`, `1 <= m <= 100`
- Time: O(18 * m * 2)
- Memory: same

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `L=1 R=10 m=3` | `3` (3, 6, 9) |
| `L=1 R=100 m=5` | `19` |
| `L=1 R=1 m=1` | `1` |
| `L=10 R=10 m=2` | `0` (digit sum 1) |

**Stretch**: Count numbers in `[L, R]` whose digits are non-decreasing.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: SOS DP — Sum Over Subsets

**Spec**:
Read `n` and `2^n` values `f(S)` indexed by subset `S` of `[0..n-1]`. Compute `g(S) = sum over T subset of S of f(T)`. Required: O(n * 2^n) using the SOS DP recurrence (iterate over each bit; for each subset that includes the bit, add the value at the subset with that bit removed).

**Constraints**:
- `1 <= n <= 20`
- Time: O(n * 2^n)
- Memory: O(2^n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=2 f=[1, 2, 3, 4]` (indices 00, 01, 10, 11) | `g=[1, 3, 4, 10]` |
| `n=1 f=[5, 7]` | `g=[5, 12]` |
| `n=3 f=[1,1,1,1,1,1,1,1]` | `g=[1,2,2,4,2,4,4,8]` |

**Stretch**: Inverse SOS (Möbius transform on the subset lattice) — recovers `f` from `g`.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Convex Hull Trick / Li Chao Tree

**Spec**:
Maintain a set of lines `y = m*x + b`. Support two operations: `addLine(m, b)` and `query(x)` returns the minimum `y` over all lines at `x`. Required O(log n) per op using a Li Chao tree on a discrete domain of `x` values, OR amortized O(1) using a deque of lines if queries are monotonic.

**Constraints**:
- `1 <= q <= 10^5`, `x` in `[-10^9, 10^9]`
- Time: O(log n) per op
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `addLine 1 0 / addLine -1 5 / query 0 / query 5 / query 2` | `0 -0 1` (min of x and 5-x at x=0,5,2) |
| `addLine 0 7 / query -100 / query 100` | `7 7` |

**Stretch**: Support maximum-Y queries by negating all `m, b` and querying the minimum, then negating the answer.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: Matrix Exponentiation for Linear Recurrence

**Spec**:
Read `k` (recurrence order), `c_1, c_2, ..., c_k` (coefficients), `a_0, a_1, ..., a_{k-1}` (base cases), `n`, and modulus `M`. The recurrence is `a_i = c_1 * a_{i-1} + c_2 * a_{i-2} + ... + c_k * a_{i-k}`. Print `a_n mod M`. Required: build the `k x k` companion matrix, exponentiate to the `n`-th power in O(k^3 log n) with all arithmetic mod `M`.

**Constraints**:
- `1 <= k <= 50`, `0 <= n <= 10^18`, `M <= 10^9 + 7`
- Time: O(k^3 log n)
- Memory: O(k^2)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `k=2 c=[1,1] a=[0,1] n=10 M=10^9+7` | `55` (Fibonacci) |
| `k=1 c=[2] a=[1] n=10 M=10^9+7` | `1024` |
| `k=2 c=[1,1] a=[0,1] n=10^18 M=10^9+7` | `(F(10^18) mod M)` |
| `k=3 c=[1,1,1] a=[0,1,1] n=15 M=1000` | (Tribonacci-like, verify) |

**Stretch**: Replace matrix exponentiation with Kitamasa's algorithm (O(k^2 log n) — faster for large k).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
