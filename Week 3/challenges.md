# Week 3 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Base-K Conversion Round Trip

**Spec**:
Read three values on one line: an integer `n` (`0 <= n <= 10^18`), a source base `s`, and a target base `t` (both in `[2, 36]`). Convert `n` from base `s` to base `t` and print the result. Treat `n` as a string of digits/letters in base `s` (digits `0-9`, then letters `a-z` for values 10–35), case-insensitive on input, lowercase on output. Don't use library base-conversion calls.

**Constraints**:
- Input size: number string up to 64 digits, bases in `[2, 36]`
- Time: O(L) where L = length of input number
- Memory: O(L)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `1010 2 10` | `10` |
| `255 10 16` | `ff` |
| `zz 36 10` | `1295` |
| `0 10 16` | `0` |
| `1a 16 2` | `11010` |

**Stretch**: Support negative numbers (leading `-`) and arbitrary precision (no `long` ceiling) using string arithmetic.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Streaming Prime Sieve

**Spec**:
Print the first `k` prime numbers, one per line. `k` is read from stdin. You may not allocate an array sized by an upper bound on the k-th prime — instead, grow your data structure dynamically as you discover primes, or use a wheel + trial-division by previously-discovered primes only.

**Constraints**:
- Input size: `1 <= k <= 10^5`
- Time: roughly O(k * sqrt(p_k) / log p_k)
- Memory: O(k)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `1` | `2` |
| `5` | `2`, `3`, `5`, `7`, `11` (one per line) |
| `10` | first 10 primes ending in `29` |
| `100` | 100th prime = `541` |

**Stretch**: Same problem but print only primes whose digit sum is itself prime.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Generalized Fibonacci (Pisano Period)

**Spec**:
Read two non-negative integers `n` and `m`. Print the `n`-th Fibonacci number modulo `m`. `n` can be astronomically large, so you may not iterate `n` times; exploit the **Pisano period**: the sequence `F(i) mod m` is periodic with some period `π(m)`. Find `π(m)` by iterating until you see the pair `(0, 1)` repeat, then reduce `n mod π(m)` and print `F(n mod π(m)) mod m`.

**Constraints**:
- Input size: `n` up to `10^18`, `m` up to `10^4`
- Time: O(π(m)), which is at most ~6m
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `0 2` | `0` |
| `10 5` | `0` (F(10) = 55) |
| `239 1000` | `161` |
| `2816213588 30524` | `28366` |
| `1000000000000 1234` | (compute via Pisano) |

**Stretch**: Solve without Pisano using fast doubling (`F(2k) = F(k)(2F(k+1)-F(k))`, `F(2k+1) = F(k)^2 + F(k+1)^2`), still in O(log n) modular operations.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
