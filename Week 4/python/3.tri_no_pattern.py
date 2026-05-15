"""
WEEK 4 - PYTHON PATTERN PROBLEMS
Topic: Triangle Number Pattern
File: 3.tri_no_pattern.py

PATTERN (N=4):
1
22
333
4444

CONCEPT:
Right-angled triangle where row i contains the digit i, repeated i times.
Combines the triangular shape with row-dependent content.

KEY POINTS:
 - Outer: i in 1..N. Inner: j in 1..i. Print i (NOT j).
 - Pythonic: `print(str(i) * i)`.

DRY RUN (N=3):
 row 1 -> "1"
 row 2 -> "22"
 row 3 -> "333"

COMPLEXITY: O(N^2).
"""

import sys


def main() -> None:
    n = 4 if sys.stdin.isatty() else int(sys.stdin.read().split()[0])
    for i in range(1, n + 1):
        for _ in range(i):
            print(i, end='')
        print()
    print("--- one-liner ---")
    for i in range(1, n + 1):
        print(str(i) * i)


if __name__ == "__main__":
    main()


# NOTES:
# - The printed value comes from the OUTER loop variable.
# - Multi-digit row numbers (e.g. N=10) widen each row -- pad if alignment matters.
