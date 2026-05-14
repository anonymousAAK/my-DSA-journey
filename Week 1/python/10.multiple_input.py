"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Reading Mixed-Type Input
File: 10.multiple_input.py

CONCEPT:
Real-world programs need to read several values of DIFFERENT types in
sequence (e.g. an integer count followed by a name). Python handles this
with multiple `input()` calls or by parsing tokens from a single line.

KEY POINTS:
- `input()` ALWAYS returns a string; convert with `int`, `float`, etc.
- Whitespace separates "tokens" — match Java's Scanner via `.split()`.
- `print(a, b)` joins with a space (default `sep=" "`); use `end=""` to keep
  output on the same line, like Java's `System.out.print`.
- f-strings format mixed-type output cleanly.

SYNTAX:
a   = int(input())
str_ = input()                        # entire line as str
print(a, str_, sep="", end="")        # same line, no separator
print(f"{a}{str_}")                    # equivalent using f-string

DRY RUN:
Stdin: "42\\nhello"
  a   = 42
  str = "hello"
  print(a, end="");  print(str)  -> "42hello"
"""

import sys


def main() -> None:
    if sys.stdin.isatty():
        a, s = 42, "hello"
        print(f"(demo) a={a}, s={s!r}")
    else:
        # Read first integer (could be on its own line or with the rest)
        tokens = sys.stdin.read().split()
        a = int(tokens[0])
        s = tokens[1] if len(tokens) > 1 else ""

    # Print integer without newline, then string WITH newline -- same line
    print(a, end="")     # like Java's System.out.print(a)
    print(s)             # like Java's System.out.println(s)

    # f-string version (more idiomatic in Python)
    print(f"{a}{s}")


if __name__ == "__main__":
    main()


# NOTES:
# - Java's Scanner offers nextByte/nextShort/nextInt/nextLong/nextFloat/nextDouble.
#   Python uses one int() / float() function — int has arbitrary precision.
# - Python's `print(a, s)` would insert a SPACE between them by default; pass
#   `sep=""` to remove that space.
# - For very high-throughput input parsing, prefer:
#     data = sys.stdin.buffer.read().split()
