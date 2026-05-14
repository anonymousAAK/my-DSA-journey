"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Reading All Common Input Types
File: 7.taking_input_all.py

CONCEPT:
Java's Scanner offers `nextInt`, `nextLong`, `nextDouble`, `next`, `nextLine`.
Python uses `input()` plus type conversions. Below we demonstrate the
equivalent helpers for every common Java Scanner method.

KEY POINTS:
- `int(input())`         -> Java's nextInt()
- `int(input())`         -> Java's nextLong()  (Python int has no fixed size)
- `float(input())`       -> Java's nextFloat() / nextDouble()
- `input().split()[0]`   -> Java's next() (first whitespace-separated token)
- `input()`              -> Java's nextLine()
- `input()[0]`           -> Java has no nextChar(); idiom: `s.next().charAt(0)`
- For many tokens at once, use `sys.stdin.read().split()`

SYNTAX:
i  = int(input())
lo = int(input())                # arbitrary precision — replaces nextLong
f  = float(input())              # replaces nextFloat / nextDouble
tok = input().split()[0]         # first token
line = input()                   # whole line
ch  = input()[0]                 # first character of the line
"""

import sys
from typing import Iterator


def token_stream() -> Iterator[str]:
    """Yield whitespace-separated tokens from stdin lazily."""
    for line in sys.stdin:
        for tok in line.split():
            yield tok


def demo_with_tokens() -> None:
    """Use a token stream similar to how Java's Scanner returns tokens."""
    tokens = token_stream()

    a = int(next(tokens))         # nextInt
    b = int(next(tokens))         # nextInt
    c = a + b
    print(f"a + b = {c}")

    word = next(tokens)            # next() -> single token
    ch = word[0]                   # first character
    print(f"First char of '{word}': '{ch}'")

    d = float(next(tokens))        # nextDouble
    print(f"Double = {d}")

    big = int(next(tokens))        # nextLong / arbitrary-precision int
    print(f"Long  = {big}")


def demo_mock() -> None:
    """Same logic but on hard-coded data when no stdin is present."""
    raw = "10 5 hello 3.14 12345678901234567890"
    parts = raw.split()
    print(f"(mock input) {raw}")
    a, b = int(parts[0]), int(parts[1])
    print(f"a + b = {a + b}")
    word = parts[2]
    print(f"First char of '{word}': '{word[0]}'")
    print(f"Double = {float(parts[3])}")
    print(f"Long  = {int(parts[4])}")


def main() -> None:
    if sys.stdin.isatty():
        demo_mock()
    else:
        demo_with_tokens()


if __name__ == "__main__":
    main()


# NOTES:
# - Java distinguishes int vs long; Python has ONE int type with arbitrary precision.
# - Java distinguishes float vs double; Python has ONE float type (64-bit IEEE 754).
# - Python has NO Scanner pitfall around `nextLine()` after `nextInt()` because
#   conversions are done explicitly.
# - For competitive-programming-grade input, replace `input()` with
#   `sys.stdin.readline()` and read all tokens up-front.
