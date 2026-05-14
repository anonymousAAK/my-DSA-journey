"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Arithmetic Operations & Operator Precedence
File: 5.arithmetic_operation.py

CONCEPT:
Python provides the standard arithmetic operators plus a few extras Java
lacks: `**` for exponentiation and `//` for floor (integer) division.
Importantly `/` ALWAYS performs true (float) division — even between two
integers — which is the opposite of Java's integer-division behaviour.

KEY POINTS:
- `+ - * /`  : addition, subtraction, multiplication, TRUE division (float result)
- `//`       : floor division (truncates toward negative infinity, not toward zero!)
- `%`        : modulus (sign follows the divisor in Python; differs from Java for negatives)
- `**`       : exponentiation (Java: Math.pow)
- Parentheses override default precedence
- Precedence high -> low (selected): `**` > unary `+ -` > `* / // %` > `+ -`
- Booleans are a subtype of int: `True + 1 == 2`

SYNTAX:
10 / 6           # 1.6666666666666667  (Java would give 1)
10 // 6          # 1                  (Java's int division)
10 % 6           # 4
2 ** 10          # 1024
(-7) // 2        # -4   (Python floors toward -inf)
(-7) % 2         # 1    (sign follows divisor)

DRY RUN:
1. a=3, b=10
   c = b / (2*a)  ->  10 / 6 = 1.6666... (float, NOT 1 like Java)
2. c = b // (2*a) ->  10 // 6 = 1        (matches Java's int division)
3. (-7) % 2       ->  1                  (Java would give -1)

COMPLEXITY: O(1) per operation.
"""


def main() -> None:
    a = 3
    b = 10

    # True division — ALWAYS produces a float in Python 3
    print(f"b / (2*a) = {b / (2 * a)}")        # 1.6666666666666667

    # Floor division — equivalent to Java's int / int
    print(f"b // (2*a) = {b // (2 * a)}")      # 1

    # Modulus
    print(f"b % (2*a)  = {b % (2 * a)}")       # 4

    # Exponentiation operator (Java has no built-in operator; uses Math.pow)
    print(f"2 ** 10 = {2 ** 10}")              # 1024

    # Floor-vs-Java behaviour with negatives:
    print(f"-7 // 2  = {-7 // 2}    (Java truncates -> -3, Python floors -> -4)")
    print(f"-7 %  2  = {-7 % 2}    (Java -> -1, Python -> 1; sign follows divisor)")

    # Operator precedence
    expr = 10 + 20 * 30          # = 10 + 600 = 610
    print(f"10 + 20 * 30 = {expr}")

    # Parentheses to force a different order
    expr = (10 + 20) * 30        # = 30 * 30 = 900
    print(f"(10 + 20) * 30 = {expr}")

    # Boolean is a subtype of int
    print(f"True + 1 = {True + 1}")            # 2
    print(f"sum([True, False, True]) = {sum([True, False, True])}")  # 2


if __name__ == "__main__":
    main()


# NOTES:
# - Java's `/` between ints truncates; Python's `/` always returns a float.
#   Use `//` in Python to match Java's int-division behaviour.
# - Python's `%` follows the SIGN OF THE DIVISOR (mathematical modulo).
#   Java's `%` follows the SIGN OF THE DIVIDEND.
# - Python adds `**` for exponentiation; Java requires `Math.pow(base, exp)`.
# - Python booleans (`True`, `False`) ARE ints — Java's `boolean` is its own type.
