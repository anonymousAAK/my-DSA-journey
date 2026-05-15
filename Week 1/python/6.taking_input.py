"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Taking User Input with input()
File: 6.taking_input.py

CONCEPT:
Python uses the built-in `input()` function for console input. It always
returns a STRING — even if the user typed digits — so you must explicitly
convert with `int()`, `float()`, etc. There is no `Scanner` class to import.

KEY POINTS:
- `input(prompt)` reads ONE LINE from stdin (newline stripped) as a str
- `int("42")` -> 42; `float("3.14")` -> 3.14
- For multiple values on one line: `a, b = map(int, input().split())`
- `input().split()` splits on whitespace by default (just like Java's Scanner tokens)
- A single character is just a length-1 string: `s[0]`
- For very large input volumes, prefer `sys.stdin.readline()` (faster)

SYNTAX:
line = input()                              # whole line as str
n    = int(input())                          # convert to int
a, b = map(int, input().split())             # two ints on one line
ch   = input()[0]                           # first character of the line

DRY RUN:
1. Stdin: "10 25\\nhello"
   a, b = 10, 25
   c    = 35
   line = "hello"; ch = 'h'
2. Stdin: "3.14"
   x = float(input()) -> 3.14
"""

import sys


def demo_basic_input() -> None:
    """Read two ints, sum them, then read a line and print its first char."""
    print("Enter two integers separated by whitespace:")
    a, b = map(int, input().split())   # tokenised input
    c = a + b
    print(f"a + b = {c}")

    print("Enter any line of text:")
    line = input()
    if line:
        ch = line[0]                   # first character (length-1 str)
        print(f"First character: {ch}")
    else:
        print("(empty line)")

    # Reading additional types — input() always returns a str, so cast manually
    print("Enter a decimal value:")
    d = float(input())
    print(f"As float: {d}")

    print("Enter a large integer (Python supports arbitrary precision):")
    big = int(input())
    print(f"As int: {big}")


def has_stdin() -> bool:
    """Return True if stdin appears to have data piped in."""
    try:
        return not sys.stdin.isatty()
    except Exception:
        return False


def main() -> None:
    if has_stdin():
        demo_basic_input()
    else:
        # No interactive terminal -> demonstrate the API on hard-coded values
        print("(no stdin) Demonstrating with mock data: '10 25' and 'hello'")
        a, b = map(int, "10 25".split())
        print(f"a + b = {a + b}")
        line = "hello"
        print(f"First character of '{line}' = '{line[0]}'")


if __name__ == "__main__":
    main()


# NOTES:
# - Java's Scanner needs `import java.util.Scanner;` and `new Scanner(System.in)`.
#   Python's `input()` is built in.
# - Java's nextInt() vs nextLine() pitfall (leftover newline) does NOT exist
#   in Python because each `input()` call consumes exactly one line.
# - `int(input())` will raise `ValueError` on invalid input — wrap with try/except.
# - To read MANY whitespace-separated tokens at once, prefer
#   `tokens = sys.stdin.read().split()` and index into the list.
