"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Data Types in Python
File: 9.data_types.py

CONCEPT:
Java has 8 PRIMITIVE types (byte, short, int, long, float, double, char, boolean)
plus reference types like String. Python has NO primitives — everything is an
object. Its main built-in types are:
  int, float, complex, bool, str, bytes, list, tuple, dict, set, NoneType

KEY POINTS:
- `int`   : arbitrary precision (no overflow). Replaces byte/short/int/long.
- `float` : 64-bit IEEE 754. Replaces both Java float AND double.
- `complex`: a + bj  (no Java equivalent in the standard library)
- `bool`  : True / False; subclass of int — True == 1, False == 0
- `str`   : immutable Unicode string. Replaces both Java String AND char.
- `bytes` : immutable sequence of 0..255 ints (use for binary data)
- `NoneType`: the singleton `None`, similar to Java's null
- `type(x)` returns x's class. `isinstance(x, T)` checks type.

PYTHON-SPECIFIC NOTES vs Java:
- No `char` type — single characters are length-1 strings.
- `str` is immutable, just like Java's String.
- Use `sys.getsizeof(obj)` to inspect runtime size (in bytes).

SYNTAX:
n: int   = 42
x: float = 3.14
b: bool  = True
s: str   = "hello"
none     = None

DRY RUN:
1. type(42)        -> <class 'int'>
2. type(3.14)      -> <class 'float'>
3. type("hi")      -> <class 'str'>
4. type(True)      -> <class 'bool'>
5. 2 ** 100        -> 1267650600228229401496703205376  (no overflow!)
"""

import sys


def show_types() -> None:
    samples = [
        42,
        3.14,
        2 + 3j,
        True,
        False,
        "hello",
        b"bytes",
        [1, 2, 3],
        (1, 2, 3),
        {"a": 1},
        {1, 2, 3},
        None,
    ]
    print(f"{'value':<20} {'type':<20} {'size (bytes)':<15}")
    print("-" * 55)
    for v in samples:
        print(f"{repr(v):<20} {type(v).__name__:<20} {sys.getsizeof(v):<15}")


def show_no_overflow() -> None:
    """Python ints have arbitrary precision — Java int would overflow at 2^31."""
    print("\nLarge integer arithmetic (no overflow!):")
    big = 2 ** 100
    print(f"2^100  = {big}")
    print(f"100!   = {factorial(100)}")


def factorial(n: int) -> int:
    """Iterative factorial; returns Python int (arbitrary precision)."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def show_string_is_char() -> None:
    """Demonstrate that there is no separate `char` type."""
    s = "Z"
    print(f"\nSingle character behaviour:")
    print(f"  s        = {s!r}")
    print(f"  type(s)  = {type(s).__name__}")
    print(f"  len(s)   = {len(s)}")
    print(f"  ord(s)   = {ord(s)}    # Java: (int) 'Z' -> 90")
    print(f"  chr(90)  = {chr(90)!r}  # Java: (char) 90 -> 'Z'")


def main() -> None:
    show_types()
    show_no_overflow()
    show_string_is_char()


if __name__ == "__main__":
    main()


# NOTES:
# - Java ints/floats are PRIMITIVES living on the stack; Python wraps them as
#   objects on the heap (CPython interns small ints for speed).
# - Java's `String` is reference type but immutable; Python's `str` is the same.
# - Java has separate `char` (16-bit Unicode); Python uses 1-character strings.
# - Booleans in Python are ints — `True + True == 2`. Java forbids this.
# - There is no `null` keyword — Python uses `None`. Comparison: `x is None`.
