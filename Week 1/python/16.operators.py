"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Operators in Python (Arithmetic, Relational, Logical, Bitwise)
File: 16.operators.py

CONCEPT:
Python supports the same operator categories as Java with a few notable
differences. The biggest changes are:
  - Logical operators are SPELLED OUT: `and`, `or`, `not` (Java uses `&&`, `||`, `!`)
  - `/` is true division; use `//` for floor division
  - `**` is exponentiation
  - Chained comparisons are supported: `a < b < c`

KEY POINTS:
- Arithmetic: + - * / // % **
- Relational: == != > < >= <=
- Logical:    and or not (with short-circuit evaluation)
- Bitwise:    & | ^ ~ << >>
- Identity:   is, is not  (compare object identity, NOT equality)
- Membership: in, not in  (`x in [1,2,3]`)
- Assignment: = += -= *= /= //= %= **= &= |= ^= <<= >>=

PYTHON-SPECIFIC NOTES vs Java:
- `==` compares VALUES; `is` compares IDENTITY (Java's `==` is identity for objects).
- `and` / `or` return the OPERAND VALUE, not a boolean ("hi" or "" -> "hi").
- Chained comparisons: `1 < x < 10` is mathematically what you'd expect (Java
  forbids this — would parse as (1<x)<10 with type errors).
- No unsigned-right-shift (`>>>`) — Python ints have no fixed width.

DRY RUN:
1. a, b = True, False
   a and b -> False
   a or  b -> True
   not a    -> False
2. 19 & 28 -> 16; 19 | 28 -> 31; 19 ^ 28 -> 15
3. 1 < 5 < 10 -> True (chained)
"""


def show_arithmetic() -> None:
    print("=== Arithmetic ===")
    print(f"  10 + 3 = {10 + 3}")
    print(f"  10 - 3 = {10 - 3}")
    print(f"  10 * 3 = {10 * 3}")
    print(f"  10 / 3 = {10 / 3}      # true division -> float")
    print(f"  10 // 3 = {10 // 3}      # floor division -> int")
    print(f"  10 % 3 = {10 % 3}")
    print(f"  2 ** 10 = {2 ** 10}    # exponentiation")


def show_relational() -> None:
    print("\n=== Relational (each returns bool) ===")
    a, b = 5, 6
    print(f"  a == b: {a == b}")
    print(f"  a != b: {a != b}")
    print(f"  a >  b: {a > b}")
    print(f"  a <  b: {a < b}")
    print(f"  a >= b: {a >= b}")
    print(f"  a <= b: {a <= b}")
    # Chained comparisons — illegal in Java
    x = 7
    print(f"  1 < {x} < 10: {1 < x < 10}    # chained, evaluates as (1<x) and (x<10)")


def show_logical() -> None:
    print("\n=== Logical (and / or / not) ===")
    a, b = True, False
    print(f"  a and b: {a and b}")
    print(f"  a or  b: {a or b}")
    print(f"  not a  : {not a}")
    # Short-circuit value pass-through
    print(f"  '' or 'fallback': {'' or 'fallback'!r}    # returns first truthy operand")
    print(f"  'hi' and 42: {'hi' and 42!r}              # returns last operand if all truthy")


def show_bitwise() -> None:
    print("\n=== Bitwise ===")
    a, b = 19, 28          # 19 = 10011, 28 = 11100
    print(f"  a & b  = {a & b}    # AND -> 16")
    print(f"  a | b  = {a | b}    # OR  -> 31")
    print(f"  a ^ b  = {a ^ b}    # XOR -> 15")
    print(f"  ~a     = {~a}     # NOT -> -(a+1) = -20")
    print(f"  a << 2 = {a << 2}    # left shift -> 76")
    print(f"  a >> 2 = {a >> 2}    # right shift -> 4")
    # No `>>>` in Python; emulate with mask
    n = -4
    print(f"  unsigned-right-shift of -4 by 28 (32-bit emulation) = {(n & 0xFFFFFFFF) >> 28}")


def show_identity_membership() -> None:
    print("\n=== Identity / Membership ===")
    a = [1, 2, 3]
    b = a
    c = [1, 2, 3]
    print(f"  a is b: {a is b}    # same object -> True")
    print(f"  a is c: {a is c}    # different objects, same value -> False")
    print(f"  a == c: {a == c}    # value comparison -> True")
    print(f"  2 in a: {2 in a}")
    print(f"  9 not in a: {9 not in a}")


def main() -> None:
    show_arithmetic()
    show_relational()
    show_logical()
    show_bitwise()
    show_identity_membership()


if __name__ == "__main__":
    main()


# NOTES:
# - Java's `&&`/`||`/`!` are spelled `and`/`or`/`not` in Python.
# - Java uses `==` for both primitive equality AND reference identity.
#   Python uses `==` for VALUE equality and `is` for IDENTITY.
# - Python lacks `>>>` (unsigned right shift) because ints aren't fixed width.
# - `and` / `or` return one of the operands (not strictly bool); convenient idiom.
# - Chained comparisons like `0 <= x < n` make range checks easy.
