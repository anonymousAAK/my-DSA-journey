"""
WEEK 4 - PYTHON PATTERN PROBLEMS
Topic: Alpha Pattern (single character per row)
File: 5.alpha_pattern.py

PATTERN (N=4):
A
BB
CCC
DDDD

CONCEPT:
Row i prints the i-th letter of the alphabet, repeated i times. Map row
number to character via `chr(ord('A') + i - 1)`.

KEY POINTS:
 - `chr(n)` -> character with code n.
 - `ord(ch)` -> integer code of character ch.
 - Pythonic: `print(chr(64 + i) * i)`.

DRY RUN (N=3):
 row 1 -> 'A' -> "A"
 row 2 -> 'B' -> "BB"
 row 3 -> 'C' -> "CCC"

COMPLEXITY: O(N^2).
"""

import sys


def main() -> None:
    n = 4 if sys.stdin.isatty() else int(sys.stdin.read().split()[0])

    for i in range(1, n + 1):
        ch = chr(ord('A') + i - 1)
        for _ in range(i):
            print(ch, end='')
        print()
    print("--- pythonic ---")
    for i in range(1, n + 1):
        print(chr(ord('A') + i - 1) * i)


if __name__ == "__main__":
    main()


# NOTES:
# - For row > 26 you'd run off the alphabet -- add `% 26` if you want to wrap.
# - In Python `'A' + 1` is a TypeError; you MUST use ord/chr explicitly.
