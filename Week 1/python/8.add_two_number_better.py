"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Adding Two Numbers from User Input
File: 8.add_two_number_better.py

CONCEPT:
Improved version of "add two numbers" — instead of hard-coding the operands
we read them from stdin. Demonstrates the read -> process -> output pattern
that underlies almost every program.

KEY POINTS:
- `input()` returns a str; convert to int with `int(...)`
- `map(int, input().split())` reads multiple ints on the same line
- The expression `a + b` can be passed directly to print() — no temp variable needed
- f-strings (`f"..."`) interpolate variables cleanly: `print(f"sum = {a+b}")`

SYNTAX:
a, b = map(int, input().split())   # one line, two integers
print(a + b)                        # expression evaluated then printed

DRY RUN:
1. Stdin: "10 25"
   a = 10, b = 25
   print(a + b) -> "35"
2. Stdin: "-7 100"
   print(a + b) -> "93"

COMPLEXITY: O(1)
"""

import sys


def main() -> None:
    if sys.stdin.isatty():
        # No piped input — fall back to a demo
        a, b = 10, 25
        print(f"(demo) {a} + {b} = {a + b}")
        return

    # Two integers separated by whitespace, on the same line OR different lines
    tokens = sys.stdin.read().split()
    a, b = int(tokens[0]), int(tokens[1])
    print(a + b)


if __name__ == "__main__":
    main()


# NOTES:
# - Java needs `Scanner s = new Scanner(System.in);` then two `s.nextInt()` calls.
#   Python: `int(input())` twice OR `map(int, input().split())` once.
# - Both languages support inline expression evaluation in the print call.
# - Python doesn't differentiate `print` vs `println`: print() always newlines
#   unless `end=""` is passed.
