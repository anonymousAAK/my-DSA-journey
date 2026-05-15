"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Typecasting (Type Conversion)
File: 15.typecasting.py

CONCEPT:
Type conversion in Python is done with the constructor of the target type:
`int(x)`, `float(x)`, `str(x)`, `bool(x)`, etc. Python does NOT distinguish
"widening" vs "narrowing" the way Java does — every conversion is explicit
and uses the same syntax.

KEY POINTS:
- `int(3.7)`     -> 3   (truncates toward zero, matches Java's `(int) 3.7`)
- `int(-3.7)`    -> -3  (truncate toward zero, NOT floor)
- `float(5)`     -> 5.0 (Java: `(double) 5` or implicit widening)
- `str(42)`      -> "42" (Java: `Integer.toString(42)` or `"" + 42`)
- `int("123")`   -> 123 (Java: `Integer.parseInt("123")`)
- `bool(0)`      -> False; `bool(1)` -> True; `bool("")` -> False
- Implicit "widening" int -> float happens only inside arithmetic (1 + 2.0 -> 3.0)

PYTHON-SPECIFIC NOTES vs Java:
- No casting syntax `(type)value` — always a function call
- `int(s)` raises `ValueError` for bad strings (Java throws NumberFormatException)
- `int(x, base)` parses strings in any base 2..36

DRY RUN:
1. i = 100;  l1 = i             -> 100   (already int)
2. d = 100.04; l2 = int(d)       -> 100   (truncates)
3. int("1010", 2)                -> 10    (binary parse)
4. float("3.14e2")               -> 314.0
"""


def main() -> None:
    # --- "Widening" int -> float (implicit during arithmetic) ---
    i = 100
    f = i + 0.0          # implicit promotion to float
    print(f"i + 0.0 = {f}  ({type(f).__name__})")

    # --- "Narrowing" float -> int (explicit, truncates toward zero) ---
    d = 100.04
    truncated = int(d)
    print(f"int({d}) = {truncated}        # truncates the decimal part")

    print(f"int(-100.99) = {int(-100.99)}  # -100, NOT -101 (truncates toward zero)")
    print(f"floor(-100.99) = {-101}        # use math.floor for floor semantics")

    # --- str <-> numeric ---
    print(f"str(42)       = {str(42)!r}")
    print(f"int('123')    = {int('123')}")
    print(f"float('3.14') = {float('3.14')}")
    # Bases — handy for binary, octal, hex
    print(f"int('1010', 2) = {int('1010', 2)}    # binary")
    print(f"int('1A', 16) = {int('1A', 16)}     # hex")

    # --- bool conversions ---
    print(f"bool(0)   = {bool(0)}")
    print(f"bool(1)   = {bool(1)}")
    print(f"bool('')  = {bool('')}")
    print(f"bool([])  = {bool([])}")
    print(f"bool('x') = {bool('x')}")

    # --- Java demo equivalent ---
    print("\n=== Java demo equivalent ===")
    java_i = 100
    java_l1 = java_i              # widening (int -> long is automatic in Java; here just int)
    java_d = 100.04
    java_l2 = int(java_d)         # explicit narrowing
    print(java_i)                # 100
    print(java_l1)               # 100
    print(java_d)                # 100.04
    print(java_l2)               # 100


if __name__ == "__main__":
    main()


# NOTES:
# - Java has TWO categories: widening (automatic) and narrowing (explicit cast).
#   Python ALWAYS requires explicit conversion via constructor functions.
# - `int(x)` truncates toward zero; `math.floor(x)` floors toward -infinity.
# - Strings -> int: invalid input raises ValueError. Wrap with try/except for safety.
# - Python's `bool` is a subclass of int — `True == 1`, `False == 0`.
