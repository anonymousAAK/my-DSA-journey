"""
WEEK 2 - PYTHON CONTROL FLOW
Topic: Total Salary Calculation using If-Else
File: 7.total_salary.py

PROBLEM:
Given a basic salary (int) and a grade (A/B/C), compute and print the
rounded total salary:
   total = basic + hra + da + allowance - pf
   hra   = 20% of basic
   da    = 50% of basic
   pf    = 11% of basic
   allowance = 1700 (A) / 1500 (B) / 1300 (C or other)

CONCEPT:
Demonstrates an if/elif/else cascade combined with arithmetic and rounding.
`round(x)` in Python uses BANKER'S rounding (round half to even) — to match
Java's `Math.round` (round half up) we use `math.floor(x + 0.5)`.

KEY POINTS:
 - Multiple percentages with `*` and `/`.
 - `round()` -- bankers rounding; `math.floor(x+0.5)` -- half-up like Java.
 - Match-case (3.10+) is an alternative to if/elif/else.

SYNTAX:
 if grade == 'A': allow = 1700
 elif grade == 'B': allow = 1500
 else: allow = 1300

DRY RUN:
 basic=10000, grade='A'
   hra=2000, da=5000, allow=1700, pf=1100
   total = 10000 + 2000 + 5000 + 1700 - 1100 = 17600

COMPLEXITY: O(1).
"""

import sys
import math


def total_salary(basic: int, grade: str) -> int:
    hra = 0.2 * basic
    da  = 0.5 * basic
    pf  = 0.11 * basic
    if grade == 'A':
        allowance = 1700
    elif grade == 'B':
        allowance = 1500
    else:
        allowance = 1300
    total = basic + hra + da + allowance - pf
    return math.floor(total + 0.5)        # half-up rounding (matches Java's Math.round)


def main() -> None:
    if sys.stdin.isatty():
        basic, grade = 10000, 'A'
        print(f"(demo) basic={basic}, grade={grade!r} -> {total_salary(basic, grade)}")
        return

    tokens = sys.stdin.read().split()
    basic = int(tokens[0])
    grade = tokens[1][0]
    print(total_salary(basic, grade))


if __name__ == "__main__":
    main()


# NOTES:
# - Python's `round()` uses BANKER'S rounding by default; Java's `Math.round`
#   rounds half UP. Be deliberate.
# - For exact decimal currency math, prefer `decimal.Decimal`.
# - Match-case (Python 3.10+) is the idiomatic switch replacement.
