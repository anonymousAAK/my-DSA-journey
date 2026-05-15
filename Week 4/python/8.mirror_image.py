"""
WEEK 4 - PYTHON PATTERN PROBLEMS
Topic: Mirror Image Number Pattern (right-aligned)
File: 8.mirror_image.py

PATTERN (N=4):
   1
  12
 123
1234

(leading spaces fill (N - i) positions per row)

CONCEPT:
Right-aligned triangle. Row i has (N - i) leading spaces followed by the
digits 1..i. Total width per row stays N.

KEY POINTS:
 - Two inner loops (or two string parts): spaces + digits.
 - Pythonic: f"{''.join(...):>N}" or use rjust(N).

DRY RUN (N=3):
 row 1: "  1"
 row 2: " 12"
 row 3: "123"

COMPLEXITY: O(N^2).
"""

import sys


def main() -> None:
    n = 4 if sys.stdin.isatty() else int(sys.stdin.read().split()[0])

    for i in range(1, n + 1):
        # leading spaces
        for _ in range(n - i):
            print(' ', end='')
        # ascending digits
        for j in range(1, i + 1):
            print(j, end='')
        print()

    print("--- pythonic via rjust ---")
    for i in range(1, n + 1):
        print(''.join(str(j) for j in range(1, i + 1)).rjust(n))


if __name__ == "__main__":
    main()


# NOTES:
# - For N >= 10 the digit length per row varies; the rjust width should match
#   the maximum row width (sum of digit lengths from 1..N).
# - `str.rjust(width, fill)` and `str.ljust(width, fill)` make alignment trivial.
