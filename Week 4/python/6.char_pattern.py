"""
WEEK 4 - PYTHON PATTERN PROBLEMS
Topic: Consecutive Character Pattern
File: 6.char_pattern.py

PATTERN (N=4):
A
BC
CDE
DEFG

CONCEPT:
Row i starts at the i-th letter and prints i consecutive letters. The
character depends on BOTH the row (start) and the column (offset).

KEY POINTS:
 - Start of row i: chr(ord('A') + i - 1).
 - Position j in the row: chr(start + j - 1).
 - Pythonic: ''.join(chr(ord('A') + i - 1 + j) for j in range(i)).

DRY RUN (N=3):
 row 1: A
 row 2: BC
 row 3: CDE

COMPLEXITY: O(N^2).
"""

import sys


def main() -> None:
    n = 4 if sys.stdin.isatty() else int(sys.stdin.read().split()[0])

    for i in range(1, n + 1):
        start = ord('A') + i - 1
        for j in range(i):
            print(chr(start + j), end='')
        print()
    print("--- pythonic ---")
    for i in range(1, n + 1):
        start = ord('A') + i - 1
        print(''.join(chr(start + j) for j in range(i)))


if __name__ == "__main__":
    main()


# NOTES:
# - Letters are derived from ASCII offsets -- mind the wrap-around for N > 26.
# - The pattern depends on row AND column, unlike the simpler alpha_pattern.
