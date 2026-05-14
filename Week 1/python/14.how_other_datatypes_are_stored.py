"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: How Float and Character Data Are Stored
File: 14.how_other_datatypes_are_stored.py

CONCEPT:
Python's `float` is always a 64-bit IEEE 754 double — there is NO separate
single-precision float by default (numpy provides one). Python has NO `char`
type; characters are length-1 `str` values whose Unicode code point is
returned by `ord()` and the inverse is `chr()`.

KEY POINTS:
- float is 8 bytes (IEEE 754 double); use `struct.pack('!f', x)` for 32-bit form
- No 'f' suffix needed — `1.5` is a float; `1.5e10` is scientific notation
- `Decimal` (decimal module) gives exact base-10 arithmetic when needed
- A character is just `str` of length 1 — `ord('A') == 65`, `chr(65) == 'A'`
- Adding an int to a character requires `chr(ord(ch) + n)` — Python does NOT
  silently coerce char + int to int the way Java does

SYNTAX:
x = 10.4               # float (always double precision)
ord('A')               # 65
chr(65)                # 'A'
chr(ord('a') + 1)      # 'b'

DRY RUN:
1. ord('X') -> 88, ord('Y') -> 89
   print(chr(88), chr(89)) -> "X Y"
2. chr(ord('a') + 1) -> 'b'   (Java prints int 98)
3. ord('a') + ord('b') -> 195  (Java would also produce 195 because chars are ints)

COMPLEXITY: O(1) for ord/chr.
"""

import struct
from decimal import Decimal


def show_float_storage() -> None:
    print("=== Float storage ===")
    x = 10.4
    print(f"x          = {x}")
    print(f"size (sys) = {struct.calcsize('d')} bytes  (double precision)")
    print(f"hex repr   = {x.hex()}")                     # IEEE 754 hex
    # Single-precision form via struct.pack
    single = struct.pack("!f", x)
    print(f"32-bit IEEE = {single.hex()}  (lossy: rounds to nearest float32)")
    print(f"Decimal    = {Decimal('10.4')}  (exact base-10 representation)")


def show_char_storage() -> None:
    print("\n=== Character storage (no `char` type — strings of length 1) ===")
    ch1 = chr(88)            # 'X'  (Java: char ch1 = 88;)
    ch2 = "Y"
    print(f"ch1, ch2 = {ch1}, {ch2}")

    # Adding int to a "char": MUST use ord/chr explicitly in Python
    print(f"chr(ord('a') + 1) = {chr(ord('a') + 1)}     # 'b'")

    # Java prints `'a' + 1` as 98; Python equivalent:
    print(f"ord('a') + 1      = {ord('a') + 1}        # 98 (int)")
    print(f"ord('a') + ord('b') = {ord('a') + ord('b')}      # 195 (Java behaviour)")

    # Concatenation behaviour
    # In Java: 'a' + 'b' (chars) -> 195 (int); ('a'+'b' as Strings) -> "ab"
    # In Python: 'a' + 'b' (strs) -> "ab"
    print(f"'a' + 'b'         = {'a' + 'b'}        # 'ab' (string concat)")


def main() -> None:
    show_float_storage()
    show_char_storage()


if __name__ == "__main__":
    main()


# NOTES:
# - Java needs the 'f' suffix to declare a float literal (`10.4f`); Python has
#   no separate single-precision literal — every `1.5` is a 64-bit double.
# - For exact decimal math (e.g. money), use `decimal.Decimal` in Python.
# - For arrays of fixed-width numerics, use `array.array` or numpy.
# - Characters in Python are NEVER implicitly numeric — `'a' + 1` is a TypeError.
