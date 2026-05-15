# Week 12 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Largest Rectangle in a Histogram (Monotonic Stack)

**Spec**:
Read `n` and `n` non-negative bar heights. Print the area of the largest axis-aligned rectangle that fits within the histogram. Required complexity O(n) using a monotonic-increasing stack of indices. The O(n^2) "for each bar, expand left/right" approach is forbidden.

**Constraints**:
- `1 <= n <= 10^6`, heights up to `10^9`
- Time: O(n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=6 / 2 1 5 6 2 3` | `10` |
| `n=1 / 7` | `7` |
| `n=4 / 4 4 4 4` | `16` |
| `n=5 / 1 2 3 4 5` | `9` (rectangle 3x3 from bars 3..5) |
| `n=5 / 5 4 3 2 1` | `9` |

**Stretch**: Output also the (left, right) indices of the maximum rectangle.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Min Stack — O(1) `getMin`

**Spec**:
Implement a stack supporting `push x`, `pop`, `top`, and `getMin`, all in O(1). You may not scan the stack on `getMin`. Two acceptable approaches: a parallel "min stack" pushing the running min, or storing `(value, currentMin)` pairs. Pick one.

Read a sequence of operations from stdin and print the output of each `top` / `getMin`.

**Constraints**:
- Up to `10^6` ops
- Time: O(1) per op
- Memory: O(stack size)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `push 3 / push 5 / getMin / push 2 / push 1 / getMin / pop / getMin / top` | `3 1 2 5` |
| `push 1 / getMin / pop / push 2 / getMin` | `1 2` |

**Stretch**: Same problem with `getMax` and `getMin` both in O(1), with arbitrary push/pop.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Evaluate Reverse Polish Notation With Error Handling

**Spec**:
Read a sequence of tokens (postfix). Each token is either an integer literal or one of `+ - * /`. Evaluate and print the integer result. Division truncates toward zero. If the input is malformed (operator with insufficient operands, leftover operands at end, division by zero), print `ERROR` and stop.

**Constraints**:
- Up to `10^6` tokens, intermediate values fit in `long`
- Time: O(n)
- Memory: O(n) worst case

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `2 1 + 3 *` | `9` |
| `4 13 5 / +` | `6` |
| `10 0 /` | `ERROR` |
| `1 +` | `ERROR` (operator needs 2 operands) |
| `1 2` | `ERROR` (leftover operands) |

**Stretch**: Add unary `~` (negate) and modulo `%`. Then add power `**` (warn about overflow).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Next Greater Element — Circular Array Variant

**Spec**:
Read `n` and `n` integers viewed as a **circular** array (after the last element comes the first). For each index `i`, find the next greater element when scanning forward (with wrap-around). If none exists, output `-1`. Required complexity O(n) using a monotonic stack on a "doubled" iteration of indices.

**Constraints**:
- `1 <= n <= 10^6`, values in `[-10^9, 10^9]`
- Time: O(n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=3 / 1 2 1` | `2 -1 2` |
| `n=4 / 5 4 3 2` | `-1 5 5 5` |
| `n=1 / 7` | `-1` |
| `n=5 / 1 2 3 4 3` | `2 3 4 -1 4` |

**Stretch**: Same problem but find the next *smaller* element to the *left* (also circular).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
