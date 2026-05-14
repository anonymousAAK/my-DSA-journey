"""
WEEK 2 - PYTHON CONTROL FLOW
Topic: Multiplication Table via While Loop
File: 8.multiplication_table.py

PROBLEM:
Print the first 10 multiples of an integer n, each on its own line.

CONCEPT:
A classic counter-controlled while loop. We compare with the for-loop idiom
to highlight the difference in style — Python's `for i in range(1, 11)` is
much more concise than the equivalent Java while.

KEY POINTS:
 - Counter starts at 1 and is incremented manually.
 - `for i in range(1, 11)` is the idiomatic Python alternative.
 - O(1) iterations regardless of n (always exactly 10).

SYNTAX:
 i = 1
 while i <= 10:
     print(i * n)
     i += 1

 for i in range(1, 11):
     print(i * n)

DRY RUN:
 n=4 ->  4, 8, 12, 16, 20, 24, 28, 32, 36, 40
"""

import sys


def while_version(n: int) -> None:
    print("--- while loop (Java translation) ---")
    i = 1
    while i <= 10:
        print(i * n)
        i += 1


def for_version(n: int) -> None:
    print("\n--- idiomatic Python (for + range) ---")
    for i in range(1, 11):
        print(i * n)


def main() -> None:
    if sys.stdin.isatty():
        n = 4
    else:
        n = int(sys.stdin.read().split()[0])
    while_version(n)
    for_version(n)


if __name__ == "__main__":
    main()


# NOTES:
# - Java often uses explicit counters; Python prefers `for` over indexed `while`.
# - `range(a, b)` is half-open: includes a, EXCLUDES b. Use `range(1, n+1)` for 1..n.
# - For step != 1, `range(start, stop, step)` is the canonical form.
