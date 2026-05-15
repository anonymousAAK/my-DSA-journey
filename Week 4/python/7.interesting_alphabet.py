"""
WEEK 4 - PYTHON PATTERN PROBLEMS
Topic: Interesting Alphabet Pattern
File: 7.interesting_alphabet.py

PATTERN (N=4):
D
CD
BCD
ABCD

PATTERN (N=5):
E
DE
CDE
BCDE
ABCDE

CONCEPT:
Each row ends at the N-th letter, and the starting letter shifts EARLIER
in the alphabet as rows grow. The bottom row always starts at 'A' and
spans 1..N.

KEY POINTS:
 - Start of row i: chr(ord('A') + N - i).
 - Print i consecutive letters from start.

DRY RUN (N=3):
 row 1: start='C' -> "C"
 row 2: start='B' -> "BC"
 row 3: start='A' -> "ABC"

COMPLEXITY: O(N^2).
"""

import sys


def main() -> None:
    n = 4 if sys.stdin.isatty() else int(sys.stdin.read().split()[0])

    for i in range(1, n + 1):
        start = ord('A') + n - i
        for j in range(i):
            print(chr(start + j), end='')
        print()
    print("--- pythonic ---")
    for i in range(1, n + 1):
        start = ord('A') + n - i
        print(''.join(chr(start + j) for j in range(i)))


if __name__ == "__main__":
    main()


# NOTES:
# - The 'interesting' twist: rows grow toward the LEFT instead of the RIGHT.
# - For larger N you'd run off the alphabet on the start side; clamp or wrap.
