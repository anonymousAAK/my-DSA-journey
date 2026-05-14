"""
WEEK 4 - PYTHON PATTERN PROBLEMS
Topic: Triangular Star Pattern
File: 2.tri_star_pattern.py

PATTERN (N=4):
*
**
***
****

CONCEPT:
Right-angled triangle of '*'. Row i has i stars. Inner loop bound depends
on the OUTER variable.

KEY POINTS:
 - Outer: i in 1..N. Inner: j in 1..i. Print '*' each time.
 - Pythonic: `print('*' * i)` per row.

SYNTAX:
 for i in range(1, n+1):
     print('*' * i)

DRY RUN (N=3):
 row 1 -> "*"
 row 2 -> "**"
 row 3 -> "***"

COMPLEXITY: O(N^2) characters total (1+2+...+N = N(N+1)/2).
"""

import sys


def main() -> None:
    if sys.stdin.isatty():
        n = 4
    else:
        n = int(sys.stdin.read().split()[0])

    for i in range(1, n + 1):
        for _ in range(i):
            print('*', end='')
        print()
    print("--- one-liner ---")
    for i in range(1, n + 1):
        print('*' * i)


if __name__ == "__main__":
    main()


# NOTES:
# - String multiplication is 10x faster than character-by-character print.
# - For super-large patterns, build a list of lines and use '\n'.join(...).
