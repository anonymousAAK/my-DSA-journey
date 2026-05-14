"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Variables and Addition
File: 4.add_two_numbers.py

CONCEPT:
A variable in Python is just a name bound to an object. There is NO type
declaration — the type is whatever the right-hand side evaluates to. You may
optionally annotate the type for documentation / static analysis purposes.

KEY POINTS:
- No `int a;` declaration step — `a = 10` both creates and initialises in one go
- Python integers have ARBITRARY precision (no overflow at 2^31-1 like Java's int)
- Names follow rules similar to Java: letters, digits, _; cannot start with a digit;
  cannot be a Python reserved keyword; case-sensitive
- The walrus operator `:=` (Python 3.8+) lets you assign inside an expression
- Multiple assignment is supported: `a, b = 10, 25`
- Type hints (PEP 484): `a: int = 10` — purely informational; not enforced at runtime

SYNTAX:
a = 10                  # bind name `a` to int object 10
a: int = 10             # same, with optional type annotation
a, b = 10, 25           # tuple unpacking — assign two names at once
c = a + b               # rebind `c` to result of a + b

DRY RUN:
1. a = 10, b = 25
   c = a + b  -> 10 + 25 = 35
   print(c)   -> "35"
2. With type hints:
   x: int = 7; y: int = -3
   z = x + y -> 4
"""


def main() -> None:
    # --- Plain assignment (no type declaration needed) ---
    a = 10            # Python infers int
    b = 25            # int
    c = a + b         # int (35)
    print(c)          # 35

    # --- Same, with type annotations (optional, recommended for clarity) ---
    x: int = 10
    y: int = 25
    z: int = x + y
    print(f"x + y = {z}")

    # --- Tuple unpacking: assign multiple variables on one line ---
    p, q = 7, -3
    print(f"p + q = {p + q}")

    # --- Big integers — Python has no overflow (unlike Java's int) ---
    huge = 10 ** 30
    print(f"10^30 = {huge}")        # works fine; Java's int would overflow

    # --- Variable naming rules (same idea as Java) ---
    valid_name = 1
    _private = 2
    camelCase = 3            # legal but PEP 8 prefers snake_case
    # 1bad = 4              # SyntaxError: cannot start with a digit
    # class = 5             # SyntaxError: 'class' is a reserved keyword
    print(valid_name, _private, camelCase)


if __name__ == "__main__":
    main()


# NOTES:
# - Java requires you to declare a type before use; Python does not.
# - Java's int is 32-bit (overflows past ~2.1B); Python's int is unbounded.
# - In Python every value is an OBJECT (even `1`); in Java primitives like int
#   are not objects (their boxed form Integer is).
# - Unused variables are not an error in Python (Java's compiler may warn).
# - `final int x = 10;` in Java has no built-in Python equivalent — convention
#   is `UPPER_SNAKE_CASE` for "constants" (still mutable in practice).
