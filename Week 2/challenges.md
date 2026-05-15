# Week 2 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Collatz Trajectory With Cycle Guard

**Spec**:
Given a positive integer `n`, repeatedly apply the Collatz rule (`n -> n/2` if even, `n -> 3n+1` if odd) until you reach 1, then stop. Print the length of the sequence (number of steps to reach 1) and the maximum value encountered along the way. Also guard against runaway: if you exceed 10,000 steps without reaching 1, print `DIVERGED` and stop. Use only `while`/`if-else` — no recursion, no library functions for arithmetic.

**Constraints**:
- Input size: `1 <= n <= 10^7`
- Time: O(steps)
- Memory: O(1)

**Test inputs**:
| Input | Expected output (two values on one line) |
|-------|------------------------------------------|
| `1` | `0 1` |
| `6` | `8 16` |
| `27` | `111 9232` |
| `97` | `118 9232` |

**Stretch**: For all `n` in `[1, 10^6]`, report the `n` whose trajectory is longest. Cache previously-seen tails to avoid recomputation.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Tax Bracket Salary Computer

**Spec**:
Read a non-negative integer gross annual salary in USD. Compute the take-home pay using these progressive brackets (in order):
- 0% on the first 10,000
- 10% on the next 30,000 (i.e., income from 10,001 to 40,000)
- 20% on the next 60,000 (40,001 to 100,000)
- 30% on the next 150,000 (100,001 to 250,000)
- 40% on everything above 250,000

Print the net salary as an integer (round half-to-even). Use only `if/else` control flow — no arrays, no maps. The challenge is to compose the conditional structure cleanly.

**Constraints**:
- Input size: salary in `[0, 10^9]`
- Time: O(1)
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `5000` | `5000` |
| `40000` | `37000` |
| `100000` | `85000` |
| `250000` | `190000` |
| `1000000` | `640000` |

**Stretch**: Print the marginal and effective tax rates as percentages with one decimal.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Power Without Multiplication

**Spec**:
Read two non-negative integers `a` and `b`. Compute `a^b` using **only addition, subtraction, comparison, and loops** — no `*`, `/`, `%`, `Math.pow`, or shifts. Print the result. Assume the result fits in a signed 64-bit integer. Aim for better than O(a^b) additions: use repeated-doubling to multiply, and exponentiation-by-squaring to power.

**Constraints**:
- Input size: `0 <= a, b <= 60`, result fits in `long`
- Time: target O(log a * log b * log result) additions
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `2 10` | `1024` |
| `0 0` | `1` (by convention) |
| `5 0` | `1` |
| `0 5` | `0` |
| `3 20` | `3486784401` |
| `7 15` | `4747561509943` |

**Stretch**: Modular variant — read a third number `m` and output `(a^b) mod m`, still without using `*` or `%`.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
