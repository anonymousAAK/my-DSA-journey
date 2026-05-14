"""
WEEK 2 - PYTHON CONTROL FLOW
Topic: Data Types Review
File: 1.data_types_review.py

CONCEPT:
A quick refresher of the Java examples in this lesson:
  1. Byte overflow (Java only) — Python has no byte/short/int distinction.
  2. Integer-division pitfall when storing 6/4 in a float.
  3. Modulo on float vs int.
  4. Relational operator returns bool.

Python's behaviour differs from Java in subtle but important ways:
  - `/` is float division, `//` is integer (floor) division.
  - int is arbitrary precision, so there is no overflow.
  - bool is a subtype of int; True == 1, False == 0.

KEY POINTS:
 - 6 / 4   -> 1.5    (Java would give 1; use 6 // 4 to match Java's int /).
 - 55.5 % 10 -> 5.5  (modulo works on floats).
 - 5 > 6    -> False (Python prints the literal `False`).
 - No fixed-width byte type — but Python WOULD let you build one via bytes().

SYNTAX:
 a / b              # float division
 a // b              # floor division
 a % b              # modulo (sign follows divisor!)
 a > b              # -> bool

DRY RUN:
 1) a = 6 / 4         -> 1.5  (float)
    b = 6 // 4         -> 1    (int)
    c = a + b           -> 2.5  (mixed -> float)
 2) 55.5 % 10           -> 5.5
    55   % 10           -> 5
 3) 5 > 6                -> False

COMPLEXITY: O(1) for each example.
"""


def example_1_no_byte_overflow() -> None:
    """Python has no `byte` type, so the Java overflow case does not apply."""
    print("--- Example 1: byte overflow (Java only) ---")
    # In Java: byte b = 50 * 50;  // 2500 doesn't fit in byte; compile error.
    # In Python: int is arbitrary-precision, so 50 * 50 = 2500 just works.
    b = 50 * 50
    print(f"50 * 50 = {b}   # Python int has no fixed width")


def example_2_division() -> None:
    """6/4 in Python differs from Java -- here we get FLOAT, not INT."""
    print("\n--- Example 2: division ---")
    a: float = 6 / 4       # 1.5 (true division)
    b: int = 6 // 4         # 1   (floor division -- matches Java's int /)
    c: float = a + b        # 2.5
    print(f"a (6/4)  = {a}")
    print(f"b (6//4) = {b}")
    print(f"c = a + b = {c}")


def example_3_modulo() -> None:
    """Modulo works for both int and float."""
    print("\n--- Example 3: modulo on float vs int ---")
    a = 55.5
    b = 55
    a = a % 10              # 5.5
    b = b % 10              # 5
    print(f"55.5 % 10 = {a}")
    print(f"55   % 10 = {b}")


def example_4_relational() -> None:
    """A relational operator returns a bool."""
    print("\n--- Example 4: relational returns bool ---")
    var1, var2 = 5, 6
    print(f"5 > 6 -> {var1 > var2}")    # False


def main() -> None:
    example_1_no_byte_overflow()
    example_2_division()
    example_3_modulo()
    example_4_relational()


if __name__ == "__main__":
    main()


# NOTES:
# - Java's primitive integer types overflow silently (or in narrow types, cause a
#   compile error). Python's `int` is unbounded.
# - Java `/` truncates ints, `%` follows the SIGN OF THE DIVIDEND.
#   Python `/` is float division, `%` follows the SIGN OF THE DIVISOR.
# - Bool is a subclass of int in Python; `True + 1 == 2` is legal (Java forbids it).
