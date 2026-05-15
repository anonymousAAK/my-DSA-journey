"""
WEEK 2 - PYTHON CONTROL FLOW
Topic: If-Else Conditional Statements
File: 2.if_else.py

CONCEPT:
`if` / `elif` / `else` direct execution based on a boolean expression.
Python uses indentation (not braces) to delimit blocks. There is no `else if`
keyword pair — it is contracted to `elif`.

KEY POINTS:
 - Indentation (commonly 4 spaces) defines the block.
 - The condition must be a bool OR a "truthy"/"falsy" value (empty containers,
   0, None, "" are falsy; everything else is truthy).
 - Python has a CONDITIONAL EXPRESSION (ternary): `a if cond else b`.
 - No `switch` statement until 3.10's `match` / `case` (structural pattern matching).
 - Multiple conditions: `and`, `or`, `not` (Java: `&&`, `||`, `!`).

SYNTAX:
 if cond:
     ...
 elif other_cond:
     ...
 else:
     ...

 x = "big" if n > 10 else "small"

DRY RUN:
 a, b = 10, 15
 a > b  -> False  -> print "b "
 then print "is greater"
 -> "b is greater"

COMPLEXITY: O(1) per check.
"""


def main() -> None:
    a, b = 10, 15

    if a > b:
        print("a ", end="")
    else:
        print("b ", end="")
    print("is greater")     # always prints — outside the if/else

    # Ternary expression — Python's equivalent of Java's `a > b ? "a" : "b"`
    print("a is bigger" if a > b else "b is bigger")

    # Chained elif: classify a number
    n = 0
    if n > 0:
        print("positive")
    elif n < 0:
        print("negative")
    else:
        print("zero")

    # `match` statement (Python 3.10+) — closest to Java's `switch`
    grade = "B"
    match grade:
        case "A":
            print("Excellent")
        case "B" | "C":
            print("Good")
        case _:
            print("Try harder")

    # Truthy / falsy values
    for v in (0, 1, "", "hi", None, [], [0], {}):
        print(f"bool({v!r}) = {bool(v)}")


if __name__ == "__main__":
    main()


# NOTES:
# - Java requires curly braces; Python uses indentation (PEP 8 -> 4 spaces).
# - Python's truthiness lets you write `if my_list:` instead of `if len(my_list) > 0`.
# - `match` / `case` is structural; far more powerful than Java's `switch`.
# - There is no `do { } while ();` in Python — emulate with `while True: ... if cond: break`.
