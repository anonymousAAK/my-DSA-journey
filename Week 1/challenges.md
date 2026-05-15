# Week 1 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Safe Integer Average

**Spec**:
Read two integers from standard input (each can be any value in the 32-bit signed range) and print their integer average truncated toward zero. Your program must not overflow, even when both inputs are near `Integer.MAX_VALUE` or `Integer.MIN_VALUE`. Do not promote the inputs to a wider type as your only defense — explain in your journal why a naive `(a+b)/2` is wrong and demonstrate a safe formula.

**Constraints**:
- Input size: two integers, each in `[-2^31, 2^31 - 1]`
- Time: O(1)
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `4 6` | `5` |
| `-3 3` | `0` |
| `2147483647 2147483647` | `2147483647` |
| `-2147483648 -2147483647` | `-2147483647` (truncated toward zero from -2147483647.5) |
| `7 -2` | `2` (truncated toward zero from 2.5) |

**Stretch**: Extend to averaging *N* integers given on stdin one per line, still without overflow and without using floating point.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Manual Typecast Round-Trip

**Spec**:
Write a program that reads a `double` and prints (a) its truncated `int` value, (b) the `int` value bitwise-reinterpreted from the same 8 bytes the double occupies, and (c) the difference between the original double and the truncated int as a string with exactly 6 digits after the decimal point. You may not use any high-level formatting helper that masks the typecast — do the formatting manually (compute integer and fractional parts yourself).

**Constraints**:
- Input size: one double in `[-1e9, 1e9]`
- Time: O(1)
- Memory: O(1)

**Test inputs**:
| Input | Expected output (3 lines) |
|-------|---------------------------|
| `3.75` | `3` / (bit pattern of 3.75 as long, e.g. `4615288898129526784`) / `0.750000` |
| `-2.5` | `-2` / (long bits of -2.5) / `-0.500000` |
| `0.1` | `0` / (long bits of 0.1) / `0.100000` |

**Stretch**: Also print which IEEE-754 components (sign / exponent / mantissa) you can recover from the bit pattern, and confirm that two doubles with the same printed decimal can have *different* bit patterns.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Operator Precedence Quiz Engine

**Spec**:
Read a single line containing an arithmetic expression with only non-negative integer literals, the operators `+ - * / %`, and the parentheses `(` and `)`. No spaces guaranteed in input. Evaluate it using standard integer precedence (no exponentiation). Division is integer division truncated toward zero; modulo follows the sign of the dividend. Print the integer result.

You may NOT use a built-in expression evaluator (no `eval`, no scripting engine). Build a small parser yourself.

**Constraints**:
- Input size: expression up to 200 characters, nesting depth up to 20
- Time: O(N) where N is the expression length
- Memory: O(N)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `2+3*4` | `14` |
| `(2+3)*4` | `20` |
| `100/3` | `33` |
| `7%3+2*(5-1)` | `9` |
| `((1+2)*(3+4))/((2+3))` | `4` |

**Stretch**: Support unary minus (`-3*2` should give `-6`).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
