"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Mixing Integer and String Input + String Concatenation
File: 11.integer_and_string.py

CONCEPT:
Python — like Java — uses `+` to concatenate strings. Unlike Java, Python
does NOT auto-convert numbers to strings during concatenation; you must
explicitly call `str(n)` (or use an f-string). This is a common source of
TypeError for newcomers.

KEY POINTS:
- "abc" + "def"  -> "abcdef"
- "abc" + 1       -> TypeError (Java would give "abc1")
- str(1) + "x"    -> "1x"
- f"{name} {n}"  -> idiomatic — handles types automatically
- `" ".join([...])` is the fastest way to join many strings with a separator

SYNTAX:
print(name + " " + str(n))
print(f"{name} {n}")
print(" ".join([name, str(n)]))

DRY RUN:
Stdin: "Alice 30"
  name = "Alice"; n = 30
  print(name + " " + str(n)) -> "Alice 30"
  print(f"{name} {n}")        -> "Alice 30"
"""

import sys


def main() -> None:
    if sys.stdin.isatty():
        name, n = "Alice", 30
    else:
        tokens = sys.stdin.read().split()
        name = tokens[0]
        n = int(tokens[1])

    # Concatenation requires explicit str() conversion (NOT automatic like Java)
    print(name + " " + str(n))

    # f-string — preferred Python style
    print(f"{name} {n}")

    # join is great for many pieces and avoids quadratic copies
    print(" ".join([name, str(n)]))

    # Demonstrating the TypeError pitfall (commented to avoid raising)
    # print(name + n)  # TypeError: can only concatenate str (not "int") to str


if __name__ == "__main__":
    main()


# NOTES:
# - Java auto-coerces with `+`: `"x=" + 1` works. Python raises TypeError.
# - Python's `*` on strings repeats them: `"ab" * 3 == "ababab"`.
# - For performance with many concatenations, use `"".join([...])`, not `+=`.
# - f-strings (PEP 498) are the modern, fast, readable formatting choice.
