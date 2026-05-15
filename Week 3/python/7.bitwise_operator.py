"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: Bitwise Operators
File: 7.bitwise_operator.py

CONCEPT:
Python supports & | ^ ~ << >> on int. Because int is arbitrary precision,
there is NO unsigned-right-shift operator (`>>>` in Java) — there is no
fixed bit-width to fill on the left. To emulate Java's `n >>> p`, mask to
32 bits first: `(n & 0xFFFFFFFF) >> p`.

KEY POINTS:
 - `&` AND, `|` OR, `^` XOR, `~` NOT, `<<` left shift, `>>` arithmetic right shift
 - `~n` == `-(n+1)`  (two's-complement negation)
 - `n << k` == n * 2^k; `n >> k` == n // 2^k (floor)
 - Use `bin(n)` to inspect binary form (returns str like "0b10011")
 - Use `format(n, 'b')` to print without the "0b" prefix

SYNTAX:
 a & b; a | b; a ^ b; ~a; a << k; a >> k

DRY RUN:
 a=19 (10011), b=28 (11100)
   a & b = 16 (10000)
   a | b = 31 (11111)
   a ^ b = 15 (01111)
   ~a    = -20
   a<<2  = 76
   a>>2  = 4

COMPLEXITY: O(width) for very large ints; O(1) for normal ints.
"""


def main() -> None:
    a = 19   # 10011
    b = 28   # 11100

    print(f"a       = {a:>5b}  ({a})")
    print(f"b       = {b:>5b}  ({b})")
    print(f"a & b   = {a & b:>5b}  ({a & b})")
    print(f"a | b   = {a | b:>5b}  ({a | b})")
    print(f"a ^ b   = {a ^ b:>5b}  ({a ^ b})")
    print(f"~a      = {~a}        # -(a+1)")
    print(f"a << 2  = {a << 2}")
    print(f"a >> 2  = {a >> 2}")

    # Java's >>> emulation: mask to 32 bits then shift
    n = -4
    print(f"\nJava's -4 >>> 28 (32-bit emulated) = {(n & 0xFFFFFFFF) >> 28}")

    # Bit tricks
    print("\n--- common bit tricks ---")
    x = 0b10110
    print(f"is bit 1 set in {x:b}? -> {(x >> 1) & 1}")     # extract bit
    print(f"set   bit 0    in {x:b} -> {(x | (1 << 0)):b}")
    print(f"clear bit 1    in {x:b} -> {(x & ~(1 << 1)):b}")
    print(f"flip  bit 4    in {x:b} -> {(x ^ (1 << 4)):b}")
    print(f"x is even? {x & 1 == 0}")


if __name__ == "__main__":
    main()


# NOTES:
# - Python int is arbitrary precision; there's no fixed-width "high bit" to fill.
# - There is NO `>>>` operator in Python; mask explicitly: `(n & 0xFFFFFFFF) >> p`.
# - The format spec `{n:b}` prints binary; `{n:08b}` zero-pads to 8 bits.
# - For really fast bit ops over many integers, use the `numpy` library (vectorised).
