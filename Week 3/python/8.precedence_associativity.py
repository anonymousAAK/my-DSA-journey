"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: Operator Precedence and Associativity
File: 8.precedence_associativity.py

CONCEPT:
Operator precedence determines which operator binds tighter in an expression
with multiple operators. Associativity decides the order when several
operators of EQUAL precedence appear. Most binary operators are left-to-right
associative; assignment and `**` are right-to-left.

PYTHON-SPECIFIC NOTES:
 - `**` (exponentiation) has HIGHER precedence than unary minus on its right
   side: `-2 ** 2 == -4`, NOT 4. Use `(-2) ** 2`.
 - Comparison operators CHAIN naturally: `1 < x < 10` works mathematically
   (in Java this would be a compile error).
 - `and` / `or` are short-circuit and return one of the operand values.

KEY POINTS:
 - High -> low precedence (selected): `**` > unary `+ -` > `* / // %` > `+ -`
   > `<< >>` > `&` > `^` > `|` > comparisons > `not` > `and` > `or` > `if/else` (ternary)
 - Use parentheses liberally for clarity.

SYNTAX:
 result = 10 + 20 * 30        # 610  (mul before add)
 result = (10 + 20) * 30       # 900
 result = -2 ** 2              # -4   (** binds tighter than unary -)
 result = 1 < 5 < 10            # True (chained)

DRY RUN:
 1) 10 + 20 * 30 -> 10 + 600 -> 610
 2) (10 + 20) * 30 -> 30 * 30 -> 900
 3) -2 ** 2 -> -(2 ** 2) -> -4
 4) (1 < 5) < 10 -> True < 10 -> 1 < 10 -> True   # NOT chained interpretation
    1 < 5 < 10 (chained) -> True
"""


def show_precedence() -> None:
    print("--- precedence ---")
    print(f"10 + 20 * 30   = {10 + 20 * 30}")        # 610
    print(f"(10+20) * 30   = {(10 + 20) * 30}")      # 900
    print(f"2 ** 3 ** 2    = {2 ** 3 ** 2}")          # 512 (right-assoc: 2**(3**2)=2**9)
    print(f"(2 ** 3) ** 2 = {(2 ** 3) ** 2}")         # 64

    # ** vs unary minus
    print(f"\n-2 ** 2  = {-2 ** 2}    # -(2**2) = -4")
    print(f"(-2) ** 2 = {(-2) ** 2}    # 4")


def order_of_evaluation_warning() -> None:
    """Side-effect order is well-defined (left to right) in Python."""
    print("\n--- order of evaluation ---")
    log = []
    def f(name, val):
        log.append(name)
        return val
    result = f("F1", 5) + f("F2", 10)
    print(f"f(F1) + f(F2) = {result}; call order = {log}")


def chained_comparisons() -> None:
    """Java forbids a > b > c; Python allows it."""
    print("\n--- chained comparisons ---")
    x = 7
    print(f"1 < x < 10 -> {1 < x < 10}")            # True
    print(f"0 == 0 == 0 -> {0 == 0 == 0}")          # True
    print(f"1 < 2 > 0 -> {1 < 2 > 0}")              # True (1<2 and 2>0)
    # Equivalent to: (1 < x) and (x < 10), short-circuits


def short_circuit() -> None:
    print("\n--- short-circuit and / or ---")
    print(f"True or (1/0) = {True or (1/0)}")  # short-circuits BEFORE 1/0
    print(f"'' or 'fallback' = {'' or 'fallback'}")
    print(f"'first' and 'second' = {'first' and 'second'}")


def main() -> None:
    show_precedence()
    order_of_evaluation_warning()
    chained_comparisons()
    short_circuit()


if __name__ == "__main__":
    main()


# NOTES:
# - Python guarantees LEFT-TO-RIGHT evaluation of operands (Java's order is
#   guaranteed for + and similar; C++ leaves it largely undefined).
# - `**` is RIGHT-associative: `a ** b ** c` == `a ** (b ** c)`.
# - Chained comparisons are mathematically intuitive and short-circuit.
# - Always prefer parentheses for non-obvious expressions.
