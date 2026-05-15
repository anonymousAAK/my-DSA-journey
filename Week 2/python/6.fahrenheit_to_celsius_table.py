"""
WEEK 2 - PYTHON CONTROL FLOW
Topic: Fahrenheit -> Celsius Table
File: 6.fahrenheit_to_celsius_table.py

PROBLEM:
Given START fahrenheit (S), END fahrenheit (E), and STEP W, print every
(F, C) pair where C = (F - 32) * 5 / 9, F runs from S to E in steps of W.

CONCEPT:
A while loop walks F from S to E, increments by W each iteration. The Java
example uses integer arithmetic (so C is truncated). Python's `/` is float
division by default; we use `//` to mimic the Java truncation exactly.

KEY POINTS:
 - `(F - 32) * 5 // 9` -> integer (Java-style) Celsius.
 - `(F - 32) * 5 / 9`  -> precise float Celsius.
 - Loop pattern: initialise, test, body, update.

SYNTAX:
 while s <= e:
     c = (s - 32) * 5 // 9
     print(s, c)
     s += w

DRY RUN:
 S=32, E=212, W=20
   F=32  -> C = 0
   F=52  -> C = 11   (Java int trunc; precise is 11.111...)
   F=72  -> C = 22
   ...
   F=212 -> C = 100

COMPLEXITY: O((E - S) / W) iterations.
"""

import sys


def print_table(s: int, e: int, w: int) -> None:
    if w <= 0:
        raise ValueError("step W must be positive")
    while s <= e:
        c_int = (s - 32) * 5 // 9            # matches Java
        c_flt = (s - 32) * 5 / 9              # precise
        print(f"{s} {c_int}   (precise: {c_flt:.4f})")
        s += w


def main() -> None:
    if sys.stdin.isatty():
        # Demo defaults
        print("(demo) S=32, E=212, W=20")
        print_table(32, 212, 20)
        return

    tokens = sys.stdin.read().split()
    s, e, w = int(tokens[0]), int(tokens[1]), int(tokens[2])
    print_table(s, e, w)


if __name__ == "__main__":
    main()


# NOTES:
# - Java's `int` arithmetic truncates the conversion result. Use `//` in Python
#   to match exactly.
# - `range(s, e + 1, w)` is the idiomatic Python alternative to a manual while loop:
#       for f in range(s, e + 1, w): ...
# - For floating-point loops, prefer fixed integer counters then multiply by a step,
#   to avoid accumulated float errors.
